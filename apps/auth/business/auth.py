import datetime
import hashlib
import json
import time

import jwt
import requests
from flask import current_app

from apps.auth.business.track import TrackUserBusiness
from apps.auth.business.users import UserBusiness
from apps.auth.extentions import parse_pwd
from apps.auth.models.ability import Ability
from apps.auth.models.roles import Role, RoleBindAbility
from apps.auth.models.users import User, UserBindRole
from apps.auth.settings.config import SESSION_TIME, SECRET, ALGORITHM, SIGN_KEY, RAND, CID, LOG_REPORT_URL
from library.api.exceptions import AuthErrorException


class AuthBusiness(object):
    @classmethod
    def _query(cls):
        return User.query.outerjoin(
            UserBindRole, User.id == UserBindRole.user_id).outerjoin(
            Role, UserBindRole.role_id == Role.id).add_columns(
            Role.name.label('rolename')
        )

    @classmethod
    def _query_ability(cls):
        return Role.query.outerjoin(
            RoleBindAbility, Role.id == RoleBindAbility.role_id).outerjoin(
            Ability, Ability.id == RoleBindAbility.ability_id).add_columns(
            Ability.name.label('abilityname'),
            Ability.handler.label('abilityhandler')
        )

    @classmethod
    def login(cls, username, password):
        ret = User.query.filter_by(
            name=username, password=parse_pwd(password),
            status=User.ACTIVE).all()
        if len(ret) == 0:
            return 303, []
        userid = ret[0].id
        userdetail = UserBusiness.query_json_by_id(userid)
        projectid = UserBusiness.query_project_by_userid(userid)
        if userdetail:
            userdetail[0]['projectid'] = projectid
            token = cls.jwt_b_encode(userdetail[0]).decode('utf-8')
            data = dict(token=token)
            try:
                res = User.query.filter(User.id == userid, User.status == User.ACTIVE).first()
                TrackUserBusiness.user_track(res)
            except Exception as e:
                current_app.logger.info(e)
            return 0, data
        else:
            return 413, []

    # 免密登录
    @classmethod
    def no_password_login(cls, username):
        ret = User.query.filter_by(name=username, status=User.ACTIVE).all()
        if len(ret) == 0:
            return 303, []
        userid = ret[0].id
        userdetail = UserBusiness.query_json_by_id(userid)
        projectid = UserBusiness.query_project_by_userid(userid)
        if userdetail:
            userdetail[0]['projectid'] = projectid
            token = cls.jwt_b_encode(userdetail[0]).decode('utf-8')
            data = dict(token=token)
            return 0, data
        else:
            return 413, []

    @classmethod
    def jwt_encode(cls, username, roles):
        return jwt.encode(
            dict(
                username=username,
                roles=roles,
                exp=datetime.datetime.now() + datetime.timedelta(seconds=SESSION_TIME)
            ),
            SECRET,
            algorithm=ALGORITHM)

    @classmethod
    def jwt_b_encode(cls, info, exp=SESSION_TIME):
        info.update(
            dict(
                exp=datetime.datetime.now() + datetime.timedelta(seconds=exp)))
        try:
            token_b = jwt.encode(info, SECRET, algorithm=ALGORITHM)
        except Exception:
            raise AuthErrorException()
        return token_b

    @classmethod
    def jwt_decode(cls, st):
        try:
            detail = jwt.decode(st, SECRET, algorithm=ALGORITHM)
        except Exception:
            current_app.logger.warn(st)
            raise AuthErrorException()
        return detail

    @classmethod
    def query_ability_by_role_name(cls, rolenames):
        return [
            item.abilityhandler for item in cls._query_ability().filter(
                Role.name.in_(rolenames)).all()
        ]

    @classmethod
    def upload_log(cls, request, function_name, event_arg):
        name = ''
        if request and request.headers and 'Authorization' in request.headers:
            name = cls.jwt_decode(request.headers['Authorization'])['nickname']
        datas = {
            "common": {"system_model": "Tcloud_WEB", "_user_id": name},
            "events": [{"_type": function_name, "_ts": str(int(time.time())), "event_arg1": event_arg}]
        }
        timestamp = int(time.time())
        hash_object = hashlib.md5()
        hash_object.update(json.dumps(datas) + SIGN_KEY + RAND + str(timestamp))
        m = hash_object.hexdigest()
        sign_string = "cid=%s&r=%s&t=%d&v=%s" % (CID, RAND, timestamp, m)
        header = {
            "X-Sign": sign_string
        }
        data = json.dumps(datas)
        requests.post(url=LOG_REPORT_URL, data=data, headers=header)

        # dic_data = json.loads(responseData.text,strict=False)
