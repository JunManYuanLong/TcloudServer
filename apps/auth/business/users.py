import jwt
from flask import g, request, current_app
from sqlalchemy import desc, asc

import public_config
from apps.auth.business.track import TrackUserBusiness
from apps.auth.extentions import parse_pwd
from apps.auth.models.roles import Role
from apps.auth.models.users import User, UserBindRole, UserBindProject
from apps.project.models.project import Project
from library.api.db import db
from library.api.exceptions import CannotFindObjectException, OperationPermissionDeniedException
from library.api.render import row2list
from library.api.transfer import slice3json, transfer2json, slicejson


class UserBusiness(object):
    @classmethod
    def _query(cls):
        return User.query.outerjoin(
            UserBindRole, User.id == UserBindRole.user_id).outerjoin(
            Role, UserBindRole.role_id == Role.id).outerjoin(
            UserBindProject, UserBindProject.user_id == User.id).outerjoin(
            Project, Project.id == UserBindProject.project_id).add_columns(
            User.id.label('userid'),
            User.name.label('username'),
            User.nickname.label('nickname'),
            User.email.label('email'),
            User.telephone.label('telephone'),
            User.picture.label('picture'),
            User.weight.label('userweight'),
            Role.id.label('roleid'),
            Role.name.label('rolename'),
            Role.comment.label('rolecomment'),
            Project.id.label('project_id'),
            Project.name.label('project_name'),
        )

    @classmethod
    @slice3json(['role|id|name|comment|roleid|rolename|rolecomment'])
    @transfer2json('?userid|!username|!nickname|!picture|!userweight|@roleid|@rolename|@rolecomment')
    def query_all_json(cls):
        roleid = request.args.get('role')
        if roleid is not None:
            return cls._query().filter(Role.id == int(roleid),
                                       User.status == User.ACTIVE).all()
        ret = cls._query().filter(User.status == User.ACTIVE).order_by(
            desc(User.id)).all()
        return ret

    @classmethod
    @transfer2json('?userid|!username|!nickname|!email|!telephone')
    def query_all_base_info(cls):
        data = User.query.add_columns(
            User.id.label('userid'),
            User.name.label('username'),
            User.nickname.label('nickname'),
            User.email.label('email'),
            User.telephone.label('telephone'),
        ).filter(User.status == User.ACTIVE).all()
        return data

    @classmethod
    @transfer2json('?userid|!nickname')
    def search_by_nickname(cls):
        nickname = request.args.get('nickname')
        ret = cls._query().filter(User.status == User.ACTIVE,
                                  User.nickname.like(f'%{nickname}%')).all()
        return ret

    @classmethod
    @slice3json(['role|id|name|comment|roleid|rolename|rolecomment'])
    @transfer2json('?userid|!username|!nickname|!picture|!userweight|@roleid|@rolename|@rolecomment')
    def query_flow_all_json(cls):
        ret = cls._query().filter().order_by(
            desc(User.id)).all()
        return ret

    @classmethod
    def _query_all_json(cls, limit, offset):
        ret = cls._query_all_json(limit, offset)
        na = [[
            dict(i) for i in map(lambda x: zip(('id', 'name'), x),
                                 zip(r.get('roleid'), r.get('rolename')))
        ] for r in ret]
        for index, item in enumerate(ret):
            for k in ['roleid', 'rolename']:
                del item[k]
            item['role'] = na[index]
        return ret

    @classmethod
    @slice3json(['role|id|name|comment|roleid|rolename|rolecomment'])
    @transfer2json('?userid|!username|!nickname|!picture|!userweight|@roleid|@rolename|@rolecomment')
    def query_json_by_id(cls, _id):
        data = cls._query().filter(User.id == _id, User.status == User.ACTIVE).order_by(desc(User.weight)).all()
        return data

    @classmethod
    @slice3json(['role|id|name|comment|roleid|rolename|rolecomment'])
    @transfer2json('?userid|!username|!nickname|!picture|!userweight|@roleid|@rolename|@rolecomment')
    def query_json_by_id_and_project(cls, _id, pid):
        return cls._query().filter(User.id == _id, UserBindRole.project_id == pid, User.status == User.ACTIVE).order_by(
            desc(User.weight)).all()

    @classmethod
    def user_bind_roles(cls, userid, roleids, project_id):
        roles_list_without_pid = [i['name'] for i in UserBusiness.query_json_by_id(userid)[0]['role']]
        modify_roles_row = UserBusiness.query_json_by_id_and_project(g.userid, project_id)
        modify_roles = modify_roles_row[0]['role'] if modify_roles_row else []
        modify_roles_list = []
        if modify_roles:
            modify_roles_list = [modify_role['name'] for modify_role in modify_roles]
        admin_id = Role.query.filter(Role.status == Role.ACTIVE, Role.name == 'admin').first().id
        if not g.is_admin:
            # 如果你不是admin，那你必须是owner，且你不能修改Admin
            if not modify_roles_list or 'owner' not in modify_roles_list:
                raise OperationPermissionDeniedException()
            if admin_id in roleids:
                raise OperationPermissionDeniedException()
            if 'admin' in roles_list_without_pid:
                raise OperationPermissionDeniedException()
        with db.auto_commit():
            for item in UserBindRole.query.filter_by(user_id=userid, project_id=project_id).all():
                db.session.delete(item)
            for roleid in roleids:
                db.session.add(UserBindRole(user_id=userid, role_id=roleid, project_id=project_id))
        return 0, None

    @classmethod
    def create_new_user_and_bind_roles(cls, username, nickname, password,
                                       email, telephone):
        try:
            ret = User.query.filter(User.name == username, User.status == User.ACTIVE).first()
            if ret:
                return 103, None
            n = User(
                name=username,
                nickname=nickname,
                password=parse_pwd(password),
                email=email,
                telephone=telephone)
            db.session.add(n)
            # TrackUserBusiness.data_create_data(n.id,n.name,'',n.nickname,n.email,n.telephone)

            db.session.commit()
            # nuid = n.id
            # for rid in roleids:
            #     t = UserBindRole(user_id=nuid, role_id=rid)
            #     db.session.add(t)
            # db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def create_new_wxuser(cls, username, nickname, password, email, telephone, avatar):
        try:
            ret = User.query.filter(User.name == username, User.status == User.ACTIVE).first()
            if ret:
                return 103, None
            n = User(
                name=username,
                wx_userid=username,
                nickname=nickname,
                password=parse_pwd(password),
                email=email,
                telephone=telephone,
                ext=1,
                picture=avatar)
            db.session.add(n)

            try:
                TrackUserBusiness.user_track(n)
            except Exception as e:
                current_app.logger.info(e)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def modify_password(cls, userid, oldpassword, newpassword, project_id):
        roles_row = UserBusiness.query_json_by_id_and_project(g.userid, project_id)
        roles_list = roles_row[0]['role'] if roles_row else []
        roles = [i['name'] for i in roles_list]
        if userid == g.userid or g.is_admin or 'owner' in roles:
            user = User.query.get(userid)
            if user.password == parse_pwd(oldpassword):
                user.password = parse_pwd(newpassword)
                db.session.add(user)
                db.session.commit()
                return 0
            return 301
        return 108

    @classmethod
    def reset_password(cls, userid, newpassword, project_id):
        roles_row = UserBusiness.query_json_by_id_and_project(g.userid, project_id)
        roles_list = roles_row[0]['role'] if roles_row else []
        modi_roles_row = UserBusiness.query_json_by_id_and_project(userid, project_id)
        modi_roles_list = modi_roles_row[0]['role'] if modi_roles_row else []
        roles = [i['name'] for i in roles_list]
        modi_roles = [i['name'] for i in modi_roles_list]
        if 'admin' in modi_roles:
            if 'admin' not in roles:
                raise OperationPermissionDeniedException('权限不够，请联系管理员')

        if userid == g.userid or g.is_admin or 'owner' in roles:
            user = User.query.get(userid)
            user.password = parse_pwd(newpassword)
            db.session.add(user)
            db.session.commit()
            return 0, None
        raise OperationPermissionDeniedException('权限不够，请联系管理员')

    @classmethod
    def delete_user(cls, userid):
        user = User.query.get(userid)
        if user is None:
            return 0
        user.status = User.DISABLE
        [
            db.session.delete(item)
            for item in UserBindRole.query.filter_by(user_id=userid).all()
        ]
        [
            db.session.delete(item)
            for item in UserBindProject.query.filter_by(user_id=userid).all()
        ]
        db.session.add(user)
        db.session.commit()
        return 0

    @classmethod
    @transfer2json('?userid|!nickname|!picture')
    def query_by_roleid(cls, rid):
        return cls._query().filter(Role.id == rid,
                                   User.status == User.ACTIVE).all()

    @classmethod
    @transfer2json('?userid|!nickname')
    def get_user_by_project_and_role_id(cls, project_id, role_id):
        data = cls._query().filter(User.status == User.ACTIVE)
        if project_id:
            data = data.filter(UserBindRole.project_id == project_id)
        if role_id:
            data = data.filter(Role.id == role_id)
        return data.all()

    @classmethod
    def bind_projects(cls, userid, pids):
        try:
            [
                db.session.delete(item)
                for item in UserBindProject.query.filter_by(user_id=userid).all()
            ]
            [
                db.session.add(
                    UserBindProject(user_id=userid, project_id=pid))
                for pid in pids
            ]
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    @slice3json(['role|id|name|comment|roleid|rolename|rolecomment'])
    @transfer2json('?userid|!username|!nickname|!picture|!userweight|@roleid|@rolename|@rolecomment')
    def query_by_project(cls, pid, role_id):
        return cls._query().filter(User.status == User.ACTIVE,
                                   UserBindRole.project_id == pid,
                                   Role.id == role_id).order_by(asc(User.id)).all()

    @classmethod
    def query_project_by_userid(cls, userid):
        return [r.projectid for r in UserBindProject.query.add_columns(
            UserBindProject.project_id.label('projectid')).filter(
            UserBindProject.user_id == userid).all()]

    @classmethod
    def modify_name(cls, user_id, user_name):
        if user_id == g.userid or g.is_admin:
            user = User.query.get(user_id)
            user.name = user_name
            db.session.add(user)
            db.session.commit()
            return 0
        return 108

    @classmethod
    def modify_nickname(cls, user_id, nickname):
        user = User.query.get(user_id)
        user.nickname = nickname
        db.session.add(user)
        db.session.commit()
        return 0

    @classmethod
    def wx_bind_user(cls, user_id, wx_user_id):
        if wx_user_id == g.userid or g.is_admin:
            wxuser = User.query.get(wx_user_id)
            user = User.query.get(user_id)
            # 需确认wx_userid且关联的账号昵称名一致
            if not user.wx_userid and wxuser.nickname == user.nickname:
                user.wx_userid = wxuser.wx_userid
                wxuser.status = User.DISABLE
                db.session.add(user, wxuser)
                db.session.commit()
                return 0, ''
            return 106, '账号已被关联或关联账号名字不一致！'
        return 108, ''

    @classmethod
    def is_reset_passwd(cls, userid):
        user = User.query.get(userid)
        if user.password == parse_pwd(''):
            return 0, [{'is_reset_password': 0}]
        return 0, [{'is_reset_password': 1}]

    @classmethod
    def parsetoken(cls):
        token = request.args.get('token')
        data = []
        if token:
            try:
                data = jwt.decode(token, public_config.SECRET, algorithm=public_config.ALGORITHM)
            except jwt.exceptions:
                return 0, data, 'Error token'
        return 0, data, 'ok'

    @classmethod
    @transfer2json('?project_id')
    def query_user_in_project(cls, user_id):
        ret = UserBindProject.query.filter(UserBindProject.user_id == user_id)
        return ret.order_by(asc(UserBindProject.id)).all()

    @classmethod
    def own_in_project(cls):

        return [
            int(item.project_id) for item in
            UserBindProject.query.filter(UserBindProject.user_id == g.userid).order_by(asc(UserBindProject.id)).all()
        ]

    @classmethod
    @transfer2json('?user_id')
    def query_user_list(cls):
        project_id = request.args.get('project_id')
        ret = UserBindProject.query.filter(UserBindProject.project_id == project_id)
        return ret.order_by(asc(UserBindProject.id)).all()

    @classmethod
    @slicejson(['project|id|name|project_id|project_name'])
    @slice3json(['role|id|name|comment|roleid|rolename|rolecomment'])
    @transfer2json('?userid|!username|!nickname|!userweight|@project_id|@project_name|@roleid|@rolename|'
                   '@rolecomment|!email|!telephone|!picture')
    def query_user_project_role(cls, limit, offset):
        ret = cls._query().filter(User.status == User.ACTIVE).order_by(
            desc(User.id)).limit(limit).offset(offset).all()
        return ret

    @classmethod
    @slicejson(['project|id|name|project_id|project_name'])
    @slice3json(['role|id|name|comment|roleid|rolename|rolecomment'])
    @transfer2json(
        '?userid|!username|!nickname|!email|!userweight|@project_id|@project_name|@roleid|@rolename|@rolecomment')
    def query_user_single_project_role(cls, user_id):
        ret = cls._query().filter(User.status == User.ACTIVE, User.id == user_id).all()
        return ret

    @classmethod
    @slicejson(['project|id|name|project_id|project_name'])
    @transfer2json('?userid|@project_id|@project_name')
    def query_user_project_role_owner(cls, limit, offset):

        user_id = request.args.get('user_id')
        ret = cls._query().filter(User.status == User.ACTIVE, User.id == user_id).order_by(
            desc(User.id)).limit(limit).offset(offset).all()
        return ret

    @classmethod
    @transfer2json('?id|!name|!nickname')
    def query_unless_user_list(cls, user_list):
        ret = User.query.filter(User.status == User.ACTIVE)
        if user_list:
            ret = ret.filter(User.id.notin_(user_list))

        return ret.order_by(desc(User.id)).all()

    @classmethod
    def query_admin_list(cls):

        role_id = Role.query.filter(Role.name == 'admin').first().id
        return [
            int(item.user_id) for item in UserBindRole.query.filter(UserBindRole.role_id == role_id).all()
        ]

    @classmethod
    @transfer2json('?id|!nickname')
    def query_all_user_list(cls):
        ret = User.query.filter(User.status == User.ACTIVE)

        return ret.order_by(desc(User.id)).all()

    @classmethod
    def query_admin_id(cls):

        return [
            int(item.id) for item in Role.query.filter(Role.status == Role.ACTIVE, Role.name == 'admin').all()
        ]

    @classmethod
    def owner_project_list(cls):

        user_id = request.args.get('user_id')

        return [
            int(item.project_id) for item in
            UserBindProject.query.filter(UserBindProject.user_id == user_id).order_by(asc(UserBindProject.id)).all()
        ]

    @classmethod
    def get_wxemails(cls, userids):
        user_list = userids.split(',')
        emails = User.query.add_columns(
            User.email.label('email')).filter(User.id.in_(user_list)).all()
        return [email_obj.email for email_obj in emails]

    @classmethod
    def project_detach_user(cls, project_id, user_id):
        user_bind_project = UserBindProject.query.filter_by(project_id=project_id, user_id=user_id).first()
        if user_bind_project:
            with db.auto_commit():
                db.session.delete(user_bind_project)
                list_user_bind_role = UserBindRole.query.filter_by(project_id=project_id, user_id=user_id).all()
                [db.session.delete(user_bind_role) for user_bind_role in list_user_bind_role]
            return 0, None
        raise CannotFindObjectException()

    @classmethod
    def project_add_users(cls, project_id, user_list):
        with db.auto_commit():
            ret = UserBindProject.query.filter(
                UserBindProject.user_id.in_(user_list),
                UserBindProject.project_id == project_id).all()
            if ret:
                for r in ret:
                    db.session.delete(r)
            for uid in user_list:
                db.session.add(UserBindProject(user_id=uid, project_id=project_id))
        return 0, None

    @classmethod
    def query_by_project_v2(cls, pid):
        user_list = [item.user_id for item in UserBindProject.query.filter_by(project_id=pid).all()]
        user_info_row = User.query.add_columns(
            User.id.label('userid'),
            User.name.label('username'),
            User.nickname.label('nickname'),
            User.email.label('email'),
            User.telephone.label('telephone'),
            User.picture.label('picture'),
            User.weight.label('userweight')).filter(User.id.in_(user_list)).all()
        user_info_list = row2list(user_info_row)
        role_row = Role.query.filter(Role.status != Role.DISABLE).all()
        role_list = row2list(role_row)
        role_dict = {}
        for role in role_list:
            role_dict[role['id']] = role
        for user in user_info_list:
            user_role_info = []
            role_list = [item.role_id for item in
                         UserBindRole.query.filter_by(user_id=user['userid'], project_id=pid).all()]
            for role_id in role_list:
                if role_id:
                    if role_id in role_dict.keys() and role_dict.get(role_id):
                        role_info = role_dict.get(role_id)
                        role_info['project_id'] = pid
                        user_role_info.append(role_info)
            user['role'] = user_role_info
        return user_info_list

    @classmethod
    @slice3json(['role|id|name|comment|roleid|rolename|rolecomment'])
    @transfer2json('?userid|!username|!nickname|!picture|!userweight|@roleid|@rolename|@rolecomment')
    def query_json_by_wxemail(cls, wxemail):
        if '@' in wxemail:
            data = cls._query().filter(User.status == User.ACTIVE,
                                       User.email == wxemail).all()
        else:
            data = cls._query().filter(User.status == User.ACTIVE,
                                       User.email.startswith(f'{wxemail}@%')).all()
        return data
