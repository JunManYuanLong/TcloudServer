import json

import requests
from flask import request, g, current_app
from sqlalchemy import desc

from apps.auth.models.trackuser import TrackUpload, TrackUser
from library.api.db import db
from library.api.transfer import transfer2json
from library.trpc import Trpc


class TrackBusiness(object):
    public_trpc = Trpc('public')

    @classmethod
    def get_token(cls, user_id, name, nickname):

        url = str(cls.get_url()) + '/v1/user/innerAuth'
        data = {
            "userName": name, "userId": user_id, "userRealName": nickname, "mobile": "", "email": "tcloud",
            "type": 1
        }

        data = json.dumps(data)
        header = {"Content-Type": "application/json"}

        ret = requests.post(url=url, data=data, headers=header)
        ret = json.loads(ret.content)

        if ret and 'code' in ret and ret['code'] == 0:
            return ret['token']

        return None

    @classmethod
    def get_sdk_list(cls):

        project_id = request.args.get('project_id')
        page = request.args.get('page_index')
        size = request.args.get('page_size')
        url = str(TrackBusiness.get_url()) + '/v1/data'

        track_project_id = cls.get_project_id(project_id)

        if track_project_id is None:
            return 0, [], 0, 'ok'

        tarck_token = cls.get_token(g.userid, g.username, g.nickname)

        header = {"Authorization": tarck_token}

        params = {"project_id": track_project_id, "page": page, "size": size}

        ret = requests.get(url=url, params=params, headers=header)
        ret = json.loads(ret.content)

        if ret and 'code' in ret and ret['code'] == 0:
            return ret['code'], ret['data'], ret['total'], 'ok'

        return 101, [], 0, '获取列表失败'

    # 获取获取设备号类型列表
    @classmethod
    def get_device_type_list(cls):

        url = str(TrackBusiness.get_url()) + '/v1/device/id'

        tarck_token = cls.get_token(g.userid, g.username, g.nickname)
        header = {"Authorization": tarck_token}
        ret = requests.get(url=url, headers=header)
        ret = json.loads(ret.content)

        if ret and 'code' in ret and ret['code'] == 0:
            return ret['code'], ret['data'], 'ok'

        return 101, [], '获取设备类型失败'

    # 获取项目id
    @classmethod
    def get_project_id(cls, project_id):

        # project_config = Config.query.add_columns(Config.content.label('content')).filter(
        #     Config.module == 'track',
        #     Config.module_type == 1).first().content
        project_config = cls.public_trpc.requests('get', '/public/config', {'module': 'track', 'module_type': 1})
        if project_config:
            run_dict = json.loads(project_config)
        else:
            return None
        track_project_id = None
        operation_dict = run_dict['operation_dict']
        for i in range(0, len(operation_dict)):
            track_dict = operation_dict[i]
            for k, v in track_dict.items():
                if int(k) == int(project_id):
                    track_project_id = int(v)

        return track_project_id

    # 获取url
    @classmethod
    def get_url(cls):
        project_config = cls.public_trpc.requests('get', '/public/config', {'module': 'track', 'module_type': 2})
        if project_config:
            run_dict = json.loads(project_config)
        else:
            return None
        track_url = run_dict['URL']

        return track_url

    # 获取websocket_url
    @classmethod
    def get_websocket(cls):
        project_config = cls.public_trpc.requests('get', '/public/config', {'module': 'track', 'module_type': 3})
        if project_config:
            run_dict = json.loads(project_config)
        else:
            return None
        track_url = run_dict['URL']

        return track_url

    # 获取事件列表
    @classmethod
    def get_event_list(cls):

        project_id = request.args.get('project_id')
        page_index = request.args.get('page_index')
        page_size = request.args.get('page_size')
        name = request.args.get('name')
        platform = request.args.get('platform')
        updator = request.args.get('updator')
        creator = request.args.get('creator')

        track_project_id = cls.get_project_id(project_id)

        if track_project_id is None:
            return 0, [], 0, 'ok'

        url = str(TrackBusiness.get_url()) + '/v1/event'

        tarck_token = cls.get_token(g.userid, g.username, g.nickname)
        header = {"Authorization": tarck_token}

        params = {
            "project_id": track_project_id, "page": page_index, "size": page_size, "name": name,
            "platform": platform, "updator": updator, "creator": creator
        }

        ret = requests.get(url=url, headers=header, params=params)
        ret = json.loads(ret.content)

        if ret and 'code' in ret and ret['code'] == 0 and 'data' in ret:
            return ret['code'], ret['data'], ret['total'], 'ok'

        return 101, [], 0, '获取事件列表失败'

    # 获取事件列表
    @classmethod
    def create_event(cls, project_id, version, update_comment, platform_list, param_list, name, description):

        track_project_id = cls.get_project_id(project_id)
        if track_project_id is None:
            return 0, [], 'ok'

        url = str(TrackBusiness.get_url()) + '/v1/event'

        tarck_token = cls.get_token(g.userid, g.username, g.nickname)
        header = {"Authorization": tarck_token, "Content-Type": "application/json"}

        data = {
            "projectId": track_project_id, "version": version, "updateComment": update_comment,
            "platformList": platform_list, "paramList": param_list, "name": name, "description": description
        }
        data = json.dumps(data)

        ret = requests.post(url=url, data=data, headers=header)
        ret = json.loads(ret.content)

        if ret and 'code' in ret and ret['code'] == 0 and 'data' in ret:
            return ret['code'], ret['data'], 'ok'

        return 101, [], '创建事件失败'

    # 删除事件
    @classmethod
    def track_delete(cls, event_id, delete_comment):

        url = str(TrackBusiness.get_url()) + '/v1/event/' + str(event_id)

        tarck_token = cls.get_token(g.userid, g.username, g.nickname)
        header = {"Authorization": tarck_token, "Content-Type": "application/json"}

        data = {"deleteComment": delete_comment}
        data = json.dumps(data)

        ret = requests.delete(url=url, data=data, headers=header)
        ret = json.loads(ret.content)

        if ret and 'code' in ret and ret['code'] == 0 and 'data' in ret:
            return ret['code'], ret['data'], 'ok'

        return 101, [], '删除事件失败'

    # 获取事件列表
    @classmethod
    def track_modify(cls, event_id, create_at, creator, delete_comment, description, id, name, param_list, platform,
                     platform_list, projectId, project_id, status, updateComment, update_at,
                     update_comment, updator, version):

        url = str(TrackBusiness.get_url()) + '/v1/event/' + str(event_id)

        tarck_token = cls.get_token(g.userid, g.username, g.nickname)

        header = {"Authorization": tarck_token, "Content-Type": "application/json"}

        data = {
            "create_at": create_at, "creator": creator, "delete_comment": delete_comment,
            "description": description, "id": id, "name": name, "paramList": param_list,
            "platform": platform, "platformList": platform_list, "projectId": projectId, "project_id": project_id,
            "status": status, "updateComment": updateComment, "update_at": update_at,
            "update_comment": update_comment, "updator": updator, "version": version
        }
        data = json.dumps(data)

        ret = requests.patch(url=url, data=data, headers=header)
        ret = json.loads(ret.content)

        if ret and 'code' in ret and ret['code'] == 0 and 'data' in ret:
            return ret['code'], ret['data'], 'ok'

        return 101, [], '修改事件失败'

    # 创建属性
    @classmethod
    def track_add_param(cls):

        url = str(TrackBusiness.get_url()) + '/v1/event/createparam'

        tarck_token = cls.get_token(g.userid, g.username, g.nickname)
        header = {"Authorization": tarck_token, "Content-Type": "application/json"}

        data = request.json

        if data:
            data = json.dumps(data)

            ret = requests.post(url=url, data=data, headers=header)
            ret = json.loads(ret.content)

            if ret and 'code' in ret and ret['code'] == 0 and 'data' in ret:
                return ret['code'], ret['data'], 'ok'

        return 101, [], '创建属性失败'

    # 删除属性
    @classmethod
    def track_delete_param(cls):

        url = str(TrackBusiness.get_url()) + '/v1/event/deleteparam'

        tarck_token = cls.get_token(g.userid, g.username, g.nickname)
        header = {"Authorization": tarck_token, "Content-Type": "application/json"}

        data = request.json
        if data:
            data = json.dumps(data)
            ret = requests.delete(url=url, data=data, headers=header)
            ret = json.loads(ret.content)

            if ret and 'code' in ret and ret['code'] == 0 and 'data' in ret:
                return ret['code'], ret['data'], 'ok'

        return 101, [], '删除属性失败'


class TrackUploadBusiness(object):

    @classmethod
    def _query(cls):
        return TrackUpload.query.add_columns(
            TrackUpload.id.label('id'),
            TrackUpload.project_id.label('project_id'),
            TrackUpload.user_id.label('user_id'),
            TrackUpload.device_type.label('device_type'),
            TrackUpload.device_typename.label('device_typename'),
            TrackUpload.device_number.label('device_number'),
            TrackUpload.status.label('status'),
        )

    @classmethod
    def create(cls, project_id, user_id, device_type, device_typename, device_number):

        try:
            c = TrackUpload(
                project_id=project_id,
                user_id=user_id,
                device_type=device_type,
                device_typename=device_typename,
                device_number=device_number,
            )
            db.session.add(c)
            db.session.commit()
            return 0, "ok"
        except Exception as e:
            current_app.logger.error(e)
            return 102, "error"

    @classmethod
    @transfer2json('?device_number')
    def gain_history_data(cls):
        project_id = request.args.get('project_id')
        user_id = request.args.get('user_id')
        device_typename = request.args.get('device_typename')

        ret = cls._query().filter(TrackUpload.status != TrackUpload.DISABLE)
        ret = ret.filter(TrackUpload.project_id == project_id, TrackUpload.user_id == user_id,
                         TrackUpload.device_typename == device_typename)

        ret = ret.order_by(desc(TrackUpload.id)).limit(10).all()
        return ret

    @classmethod
    @transfer2json('?id')
    def check_device_exist(cls, project_id, user_id, device_number):

        ret = cls._query().filter(TrackUpload.status != TrackUpload.DISABLE)
        ret = ret.filter(TrackUpload.project_id == project_id, TrackUpload.user_id == user_id,
                         TrackUpload.device_number == device_number)

        ret = ret.order_by(desc(TrackUpload.id)).all()
        return ret


class TrackUserBusiness(object):

    @classmethod
    def _query(cls):
        return TrackUser.query.add_columns(
            TrackUser.id.label('id'),
            TrackUser.nickname.label('nickname'),
            TrackUser.wx_userid.label('wx_userid'),
            TrackUser.status.label('status'),
            TrackUser.email.label('email'),
            TrackUser.telephone.label('telephone'),
            TrackUser.weight.label('weight'),
            TrackUser.track_token.label('track_token'),
            TrackUser.name.label('name'),
            TrackUser.user_id.label('user_id'),
        )

    @classmethod
    def create(cls, nickname, name, wx_userid, email, telephone, track_token, user_id):
        try:
            c = TrackUser(
                nickname=nickname,
                wx_userid=wx_userid,
                email=email,
                telephone=telephone,
                track_token=track_token,
                name=name,
                user_id=user_id
            )
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            return 102

    @classmethod
    def user_track(cls, res):

        try:
            if res:
                TrackUserBusiness.create(res.nickname, res.name, res.wx_userid, res.email, res.telephone, '', res.id)
        except Exception as e:
            current_app.logger.info(e)

        return 0
