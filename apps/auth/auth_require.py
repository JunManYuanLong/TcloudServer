from functools import wraps

from flask import g, request

from apps.auth.business.auth import AuthBusiness
from apps.auth.business.users import UserBusiness
from library.api.exceptions import PermissionDeniedException, OperationPermissionDeniedException

"""
admin和trpc 直接执行函数
"""


def is_admin():
    # return 'admin' in [r.get('name') for r in g.role]
    return g.is_admin


def is_owner():
    return 'owner' in [r.get('name') for r in g.role]


def required(ability=None):
    def _has_ability(_ability, have_abilities):
        return _ability in have_abilities

    def _is_owneristrator(roles):
        return 'owner' in roles

    def dec(func):
        @wraps(func)
        def _(*args, **kwargs):
            if g.istrpc == 1:
                return func(*args, **kwargs)
            if g.is_admin == 1:
                return func(*args, **kwargs)

            # 项目外需要owner权限的在premission中@owner_required
            roles = []

            if not g.projectid:
                raise OperationPermissionDeniedException
            roles_row = UserBusiness.query_json_by_id_and_project(g.userid, g.projectid)
            roles_list = roles_row[0]['role'] if roles_row else []
            for i in roles_list:
                roles.append(i['name'])

            if _is_owneristrator(roles):
                return func(*args, **kwargs)

            abilities = AuthBusiness.query_ability_by_role_name(roles)

            if _has_ability(ability, abilities):
                return func(*args, **kwargs)
            raise OperationPermissionDeniedException

        return _

    return dec


# 用于项目外无projectid的权限控制  暂时使用原来逻辑
def required_without_projectid(ability=None):
    def _has_ability(_ability, have_abilities):
        return _ability in have_abilities

    def _is_owneristrator(roles):
        return 'owner' in roles

    def _is_have_project(project, project_list):
        return project in project_list

    def dec(func):
        @wraps(func)
        def _(*args, **kwargs):
            if g.istrpc == 1:
                return func(*args, **kwargs)
            if g.is_admin == 1:
                return func(*args, **kwargs)

            roles = [i['name'] for i in UserBusiness.query_json_by_id(g.userid)[0]['role']]

            project = None
            if request.args and 'project_id' in request.args:
                project = request.args.get('project_id')
            if request.json and 'project_id' in request.json:
                project = request.json.get('project_id')

            project_list = UserBusiness.own_in_project()
            if project and _is_owneristrator(roles) and project_list and _is_have_project(int(project), project_list):
                return func(*args, **kwargs)

            abilities = AuthBusiness.query_ability_by_role_name(roles)

            if _has_ability(ability, abilities):
                return func(*args, **kwargs)
            raise OperationPermissionDeniedException

        return _

    return dec


def has_ability(_ability, have_abilities):
    return _ability in have_abilities


def is_owneristrator(roles):
    return 'owner' in roles


def is_have_project(project, project_list):
    return project in project_list


def required_no_pid_no_dec(ability=None):
    if g.istrpc == 1:
        return 1
    if g.is_admin == 1:
        return 1

    roles = [i['name'] for i in UserBusiness.query_json_by_id(g.userid)[0]['role']]

    project = None
    if request.args and 'project_id' in request.args:
        project = request.args.get('project_id')
    if request.json and 'project_id' in request.json:
        project = request.json.get('project_id')

    project_list = UserBusiness.own_in_project()
    if project and is_owneristrator(roles) and project_list and is_have_project(int(project), project_list):
        return 1

    abilities = AuthBusiness.query_ability_by_role_name(roles)

    if has_ability(ability, abilities):
        return 1
    return 0


def required_no_dec(ability=None):
    if g.istrpc == 1:
        return 1
    if g.is_admin == 1:
        return 1

    roles = []

    if not g.projectid:
        raise PermissionDeniedException
    roles_row = UserBusiness.query_json_by_id_and_project(g.userid, g.projectid)
    roles_list = roles_row[0]['role'] if roles_row else []
    for i in roles_list:
        roles.append(i['name'])

    if is_owneristrator(roles):
        return 1

    abilities = AuthBusiness.query_ability_by_role_name(roles)

    if has_ability(ability, abilities):
        return 1
    return 0


def rpc_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if g.istrpc == 1:
            return func(*args, **kw)
        raise OperationPermissionDeniedException

    return wrapper

#
# def owner_required(func):
#     @wraps(func)
#     def wrapper(*args, **kw):
#         if g.is_admin:
#             return func(*args, **kw)
#         if g.userid:
#             owner_query = Role.query.filter_by(name='owner').first()
#             owner_id = owner_query.id
#             user_bind_role = UserBindRole.query.filter_by(user_id=g.userid).all()
#             if user_bind_role:
#                 roles = [i.role_id for i in user_bind_role]
#                 if owner_id in roles:
#                     return func(*args, **kw)
#         raise AuthErrorException()
#
#     return wrapper
#
#
# def admin_required(func):
#     @wraps(func)
#     def wrapper(*args, **kw):
#         if g.is_admin:
#             return func(*args, **kw)
#         raise AuthErrorException()
#
#     return wrapper
