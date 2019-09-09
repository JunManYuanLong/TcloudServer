import datetime
import json

import requests
from flask import current_app

from apps.auth.business.auth import AuthBusiness
from apps.auth.business.track import TrackUserBusiness
from apps.auth.business.users import UserBusiness
from apps.auth.models.users import User
from library.api.db import db
from library.trpc import Trpc
from public_config import CORP_ID, QYWXHost


class WxLoginBusiness(object):
    public_trpc = Trpc('public')

    @classmethod
    def get_access_token(cls):
        # acc = Config.query.filter(Config.module == 'access_token', Config.module_type == 1).first()
        acc = cls.public_trpc.requests('get', '/public/config',
                                       {'module': 'access_token', 'module_type': 1, 'is_all': 1})
        if not acc:
            return 102, [], 'error'
        if '{' in acc['content']:
            content = json.loads(acc['content'])
            token = content['access_token']
        else:
            token = acc['content']
        modified_time = datetime.datetime.strptime(acc['modified_time'], '%Y-%m-%d %H:%M:%S')
        expires_time = datetime.datetime.now() + datetime.timedelta(hours=-2)
        if modified_time > expires_time:
            current_app.logger.info('access_token未过期')
            return token
        else:
            current_app.logger.info('access_token已过期，重新获取！')
            ret = cls.force_get_access_token()
            return ret

    @classmethod
    def force_get_access_token(cls):
        # 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET'
        # corpid 企业ID,corpsecret 应用的凭证密钥
        corp_id = CORP_ID
        # corp_secret = Config.query.filter(Config.module == 'corp_secret', Config.module_type == 1).first()
        corp_secret = cls.public_trpc.requests('get', '/public/config', {'module': 'corp_secret', 'module_type': 1})
        # corp_secret = corp_secret.content
        current_app.logger.info('corp_id:' + corp_id + ',corp_secret:' + corp_secret)
        url = QYWXHost + 'gettoken' + '?corpid={}&corpsecret={}'.format(corp_id, corp_secret)
        current_app.logger.info(url)
        ret = requests.get(url=url)
        current_app.logger.info(ret.text)
        r = json.loads(ret.text)
        if r['errcode'] is 0:
            # acc = Config.query.filter(Config.module == 'access_token', Config.module_type == 1).first()
            access_token_info = cls.public_trpc.requests('get', '/public/config',
                                                         {'module': 'access_token', 'module_type': 1, 'is_all': 1})

            data = cls.public_trpc.requests('post', f"/public/config/{access_token_info['id']}",
                                            body={
                                                'module': 'access_token', 'module_type': 1,
                                                'content': {"access_token": r['access_token']},
                                                'project_id': 0
                                            })
            if data == 'success':
                return r['access_token']
            else:
                return ''
        else:
            return ''

    @classmethod
    def get_user_info(cls, access_token, user_code):
        # 获取访问用户身份 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=ACCESS_TOKEN&code=CODE'
        # access_token 调用接口凭证,
        # code 通过成员授权获取到的code，最大为512字节。每次成员授权带上的code将不一样，code只能使用一次，5分钟未被使用自动过期。
        # "errcode":40029, "errmsg":"invalid code
        # "errcode":40014, "errmsg":"invalid access_token"
        code = user_code
        url = QYWXHost + 'user/getuserinfo' + '?access_token={}&code={}'.format(access_token, code)
        current_app.logger.info(url)
        ret = requests.get(url=url)
        current_app.logger.info(ret.text)
        r = json.loads(ret.text)
        if r['errcode'] is 0:
            if 'UserId' in r.keys():
                return r['errcode'], r['UserId']
            return 102, ''
        else:
            return r['errcode'], ''

    @classmethod
    def get_user(cls, user_code):
        # 读取成员 'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=ACCESS_TOKEN&userid=USERID'
        # access_token 调用接口凭证,
        # userid 成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节

        access_token = cls.get_access_token()
        errcode, user_id = cls.get_user_info(access_token, user_code)
        if errcode == 102:
            return 109, [], '非企业人员'
        if errcode == 40014:
            access_token = cls.force_get_access_token()

        url = QYWXHost + 'user/get' + '?access_token={}&userid={}'.format(access_token, user_id)
        current_app.logger.info(url)
        ret = requests.get(url=url)
        current_app.logger.info(ret.text)
        r = json.loads(ret.text)
        if r['errcode'] is 0:
            uid = r['userid']
            nickname = r['name']
            email = r['email']
            telephone = r['mobile']
            avatar = r['avatar']
            current_app.logger.info("avatar:" + str(avatar))
            res = User.query.filter(User.wx_userid == uid, User.status == User.ACTIVE).first()

            if res:
                code, data = AuthBusiness.no_password_login(res.name)
                pic = User.query.get(res.id)
                pic.picture = avatar
                db.session.add(pic)
                db.session.commit()
                try:
                    TrackUserBusiness.user_track(res)
                except Exception as e:
                    current_app.logger.info(e)
                return code, data, ''
            else:
                UserBusiness.create_new_wxuser(uid, nickname, '', email, telephone, avatar)
                code, data = AuthBusiness.no_password_login(uid)
                return code, data, ''
        else:
            return r['errcode'], [], r['errmsg']
