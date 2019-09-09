from flask import request, current_app, g

from apps.auth.auth_require import required
from apps.auth.business.auth import AuthBusiness
from apps.auth.business.users import UserBusiness
from apps.auth.extentions import parse_list_args, validation, parse_json_form
from library.api.render import json_list_render, json_detail_render
from library.api.tBlueprint import tblueprint

bpname = 'user'
bpname_relate = 'projectconfig'
view_permission = f'{bpname_relate}_view'
modify_permission = f'{bpname_relate}_modify'
user = tblueprint(bpname, __name__, bpname=bpname_relate, has_view=False)


@user.route('/', methods=['GET'])
def user_list_handler():
    """
    @api {get} /v1/user/ 获取 用户信息
    @apiName GetUserInfo
    @apiGroup 用户
    @apiDescription 分页查询用户信息，可选参数角色
    @apiParam {int} [role] roleid
    @apiSuccess {list} role 用户权限列表
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "nickname": "朱林林",
                "picture": "",
                "role": [
                    {
                        "comment": "测试",
                        "id": 3,
                        "name": "test"
                    }
                ],
                "userid": 106,
                "username": "zhulinlin@innotechx.com",
                "userweight": 1
            }
        ],
        "limit": 1,
        "message": "ok",
        "offset": 0
    }
    """
    base_info = request.args.get('base_info')
    if base_info:
        data = UserBusiness.query_all_base_info()
    else:
        data = UserBusiness.query_all_json()
    return json_detail_render(0, data)


@user.route('/search', methods=['GET'])
def user_search_handler():
    data = UserBusiness.search_by_nickname()
    return json_detail_render(0, data)


@user.route('/add', methods=['POST'])
@required(modify_permission)
@validation('POST:adduser')
def user_index_handler():
    """
    @api {post} /v1/user/add 新增 用户
    @apiName CreateUser
    @apiGroup 用户
    @apiDescription 新增用户
    @apiParam {string} username 用户名：字母[+数字]
    @apiParam {string} nickname 昵称
    @apiParam {string} password 密码
    @apiParam {int[]} roleids 角色，可传入空数组
    @apiParam {string} email 邮箱
    @apiParam {string} telephone 手机号
    @apiParamExample {json} Request-Example:
    {
        "username":"zhangsan",
        "nickname":"zhangdashan",
        "password":"Aa123456",
        "roleids":[],
        "email":"zhangsan@innotechx.com",
        "telephone":"13131313131"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    username, nickname, password, email, telephone = parse_json_form('adduser')
    ret, msg = UserBusiness.create_new_user_and_bind_roles(
        username, nickname, password, email, telephone)

    return json_detail_render(ret, [], msg)


@user.route('/<int:user_id>', methods=['GET'])
def user_detail_handler(user_id):
    """
    @api {get} /v1/user/{user_id} 查询 用户信息根据用户id
    @apiName GetUserInfoById
    @apiGroup 用户
    @apiDescription 查询 用户信息根据用户id
    @apiSuccess {list} role 用户权限列表
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "nickname": "张宇",
                "picture": "https://p.qlogo.cn/bizmail/WRZVs2uMphoxc2918UvZzL31u6A9ibTNuqnIibzJ4GxjWIVVDxHvUGuA/0",
                "role": [
                    {
                        "comment": "超级管理员",
                        "id": 1,
                        "name": "admin"
                    }
                ],
                "userid": 96,
                "username": "zhangyu02@innotechx.com",
                "userweight": 1
            }
        ],
        "message": "ok"
    }
    """
    project_id = request.args.get('project_id')
    if not project_id:
        project_id = request.headers.get('projectid')
    if not project_id:
        data = UserBusiness.query_json_by_id(user_id)
    else:
        data = UserBusiness.query_json_by_id_and_project(user_id, project_id)
    if len(data) == 0:
        return json_detail_render(101, data)
    return json_detail_render(0, data)


@user.route('/<int:user_id>', methods=['POST'])
# @required(modify_permission)
@validation('POST:modifypassword')
def user_detail_modify_handler(user_id):
    """
    @api {post} /v1/user/{user_id} 修改 用户密码
    @apiName ModifyPassword
    @apiGroup 用户
    @apiDescription 修改用户密码
    @apiParam {string} oldpassword 旧密码
    @apiParam {string} newpassword 新密码
    @apiParamExample {json} Request-Example:
    {
        "oldpassword":"1q2w3e4r",
        "newpassword":"1q2w3e4r"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    @apiErrorExample {json} Error-Response:
     HTTP/1.1 200 OK
     {
        "code": 301,
        "data": [],
        "message": "password wrong"
    }
    """
    project_id = request.args.get('project_id')
    oldpassword, newpassword = parse_json_form('modifypassword')
    ret = UserBusiness.modify_password(user_id, oldpassword, newpassword, project_id)
    return json_detail_render(ret)


@user.route('/<int:user_id>', methods=['DELETE'])
def user_delete_handler(user_id):
    """
    @api {delete} /v1/user/{user_id} 删除 用户
    @apiName DeleteUser
    @apiGroup 用户
    @apiDescription 删除 用户
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    ret = UserBusiness.delete_user(user_id)
    return json_detail_render(ret)


@user.route('/resetpassword', methods=['POST'])
@required(modify_permission)
@validation('POST:resetpassword')
def user_reset_handler():
    """
    @api {post} /v1/user/resetpassword 重置 用户密码
    @apiName ResetPassword
    @apiGroup 用户
    @apiDescription 重置用户密码
    @apiParam {int} userid 用户ID
    @apiParam {string} newpassword 新密码
    @apiParamExample {json} Request-Example:
    {
        "userid":1,
        "newpassword":"1q2w3e4r"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    project_id = request.args.get('project_id')
    userid, newpassword = parse_json_form('resetpassword')
    ret, msg = UserBusiness.reset_password(userid, newpassword, project_id)

    return json_detail_render(ret, message=msg)


@user.route('/userbindroles', methods=['POST'])
@required(modify_permission)
@validation('POST:userbindroles')
def user_bind_role_handler():
    """
    @api {post} /v1/user/userbindroles 绑定 用户角色
    @apiName BindUserRole
    @apiGroup 用户
    @apiDescription 绑定用户角色
    @apiParam {int} userid 用户ID
    @apiParam {int[]} roleids role list可以为空，表示清空绑定关系
    @apiParamExample {json} Request-Example:
    {
        "userid":6,
        "roleids":[4]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
       "code": 0,
       "data": [],
       "message": ""
     }
    """
    userid, roleids, project_id = parse_json_form('userbindroles')

    ret, msg = UserBusiness.user_bind_roles(userid, roleids, project_id)
    return json_detail_render(ret, [], msg)


@user.route('/login', methods=['POST'])
@validation('POST:login')
def login_handler():
    """
    @api {post} /v1/user/login 登录
    @apiName Login
    @apiGroup 用户
    @apiDescription 登录
    @apiParam {string} username 用户
    @apiParam {string} password 密码
    @apiParamExample {json} Request-Example:
    {
        "username":"wiggens",
        "password":"1q2w3e4r"
    }
    @apiSuccess {string} token 用户token
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IndpZ2dlbnMiLCJ1c2VyaWQiOj"
        },
        "message": "ok"
    }
    """
    username, passwd = parse_json_form('login')
    if passwd is '':
        return json_detail_render(301)
    code, data = AuthBusiness.login(username, passwd)

    return json_detail_render(code, data)


@user.route('/renewtoken', methods=['GET'])
def renew_token_handler():
    """
    @api {get} /v1/user/renewtoken 刷新 token
    @apiName RenewToken
    @apiGroup 用户
    @apiDescription 刷新 token
    @apiSuccess {string} token 用户token
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IndpZ2dlbnMiLCJ1"
        },
        "message": "ok"
    }
    """
    token = request.headers.get('Authorization')
    userdetail = AuthBusiness.jwt_decode(token)
    new_token = AuthBusiness.jwt_b_encode(userdetail).decode('utf-8')
    data = dict(token=new_token)

    return json_detail_render(0, data)


@user.route('/byproject/<int:pid>', methods=['GET'])
def query_user_by_project_handler(pid):
    """
    @api {get} /v1/user/byproject/{pid} 查询 用户信息通过项目id
    @apiName GetUserinfoByProjectId
    @apiGroup 用户
    @apiDescription 通过项目id查询用户信息
    @apiSuccess {list} role 用户权限列表
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "nickname": "周培丽hello",
                "picture": "http://p.qlogo.cn/bizmail/DLjOz7icMnHySKca5HDofMyDUHdjCM28iauyRdCl1DKx9uaJibfqpViang/0",
                "role": [
                    {
                        "comment": "超级管理员",
                        "id": 1,
                        "name": "admin"
                    }
                ],
                "userid": 5,
                "username": "zhoupeili1987",
                "userweight": 1
            }
        ],
        "limit": 99999,
        "message": "ok",
        "offset": 0
    }
    """

    # 第一个接口查询后会只返回有角色的用户
    role_id = request.args.get('role')
    if role_id:
        data = UserBusiness.query_by_project(pid, role_id)
    else:
        data = UserBusiness.query_by_project_v2(pid)

    return json_detail_render(0, data)


@user.route('/bindproject', methods=['POST'])
@required(modify_permission)
@validation('POST:userbindprojects')
def user_bind_project_handler():
    """
    @api {post} /v1/user/bindproject 绑定 项目到用户
    @apiName BindProject
    @apiGroup 用户
    @apiDescription 给用户绑定项目，赋予访问权限等
    @apiParam {int} user_id 用户ID
    @apiParam {int[]} project_ids 项目
    @apiParamExample {json} Request-Example:
    {
        "user_id":1,
        "project_ids":[1]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
       "code": 0,
       "data": [],
       "message": ""
     }
    """
    user_id, pids = parse_json_form('userbindprojects')
    ret, msg = UserBusiness.bind_projects(user_id, pids)

    return json_detail_render(ret, [], msg)


@user.route('/name', methods=['POST'])
@required(modify_permission)
@validation('POST:modifyname')
def user_name_handler():
    """
    @api {post} /v1/user/name 修改 用户名
    @apiName ModifyName
    @apiGroup 用户
    @apiDescription 修改用户名
    @apiParam {int} userid 用户ID
    @apiParam {string} username 新的用户名
    @apiParamExample {json} Request-Example:
    {
        "userid":1,
        "username":"李四"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
       "code": 0,
       "data": [],
       "message": ""
     }
    """
    userid, username = parse_json_form('modifyname')
    ret = UserBusiness.modify_name(userid, username)
    return json_detail_render(ret)


@user.route('/nickname', methods=['POST'])
@required(modify_permission)
@validation('POST:modifynickname')
def user_modify_name_handler():
    """
    @api {post} /v1/user/nickname 修改 昵称
    @apiName ModifyNickName
    @apiGroup 用户
    @apiDescription 修改昵称
    @apiParam {int} userid 用户ID
    @apiParam {string} nickname 新的昵称
    @apiParamExample {json} Request-Example:
    {
        "userid":1,
        "nickname":"嘻嘻哈哈"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
       "code": 0,
       "data": [],
       "message": ""
     }
    """
    userid, nickname = parse_json_form('modifynickname')
    ret = UserBusiness.modify_nickname(userid, nickname)
    return json_detail_render(ret)


@user.route('/wxbinduser', methods=['POST'])
@required(modify_permission)
@validation('POST:wxbinduser')
def wx_user_bind_handler():
    """
    @api {post} /v1/user/wxbinduser 关联 企业微信到老账号
    @apiName WxBindUser
    @apiGroup 用户
    @apiDescription 企业微信关联老账号
    @apiParam {int} userid 老账号的ID
    @apiParam {int} wxuserid 企业微信用户的ID
    @apiParamExample {json} Request-Example:
    {
        "wxuserid": 58,
        "userid": 20
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
       "code": 0,
       "data": [],
       "message": ""
     }
    """
    userid, wxuserid = parse_json_form('wxbinduser')
    ret, msg = UserBusiness.wx_bind_user(userid, wxuserid)

    return json_detail_render(ret, msg)


@user.route('/isresetpassword/<int:user_id>', methods=['GET'])
def user_is_reset_handler(user_id):
    """
    @api {get} /v1/user/isresetpassword/{user_id} 判断 是否重置过密码
    @apiName IsResetPassword
    @apiGroup 用户
    @apiDescription 判断是否重置过密码
    @apiSuccess {int} is_reset_password 为0代表未重置过，1代表重置过
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
        {
          "is_reset_password": 0
        }
        ],
        "message": "ok"
    }
    """
    ret, data = UserBusiness.is_reset_passwd(user_id)

    return json_detail_render(ret, data)


@user.route('/parsetoken', methods=['GET'])
def user_parse_tokent_handler():
    ret, data, msg = UserBusiness.parsetoken()
    return json_detail_render(ret, data, msg)


@user.route('/currentuser/project_list', methods=['GET'])
def user_project_list():
    """
    @api {get} /v1/user/currentuser/project_list 获取 当前用户的项目列表
    @apiName GetProjectListsByUser
    @apiGroup 用户
    @apiDescription 获取当前用户的项目列表
    @apiParam {int} user_id 用户id
    @apiSuccess {string} project_id 拥有的项目
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "project_id": 4
            }
        ],
        "message": "ok"
    }
    """
    user_id = request.args.get('user_id')
    data = UserBusiness.query_user_in_project(user_id)
    return json_detail_render(0, data)


# 获取项目的所有用户列表和角色
@user.route('/project_role_list', methods=['GET'])
def project_role_list_user():
    """
    @api {get} /v1/user/project_role_list 获取 项目的所有用户列表和角色
    @apiName GetProjectAndRoleListsByUser
    @apiGroup 用户
    @apiDescription 获取项目的所有用户列表和角色
    @apiParam {int} [limit] limit
    @apiParam {int} [offset] offset
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "nickname": "吴茂澍",
                "project": [
                    {
                        "id": 4,
                        "name": "云测平台66"
                    }
                ],
                "role": [
                    {
                        "comment": "测试",
                        "id": 3,
                        "name": "test"
                    }
                ],
                "userid": 110,
                "username": "wumaoshu@innotechx.com",
                "userweight": 1
            }
        ],
        "limit": 1,
        "message": "ok",
        "offset": 2
    }
    """
    limit, offset = parse_list_args()
    data = UserBusiness.query_user_project_role(limit, offset)

    return json_list_render(0, data, limit, offset)


# 获取单个用户的项目和角色
@user.route('/project_role_list/<int:user_id>', methods=['GET'])
def project_single_role_list_user(user_id):
    """
    @api {get} /v1/user/project_role_list/{user_id} 获取 项目的单个用户列表和角色
    @apiName GetSingleProjectAndRoleListsByUser
    @apiGroup 用户
    @apiDescription 项目的单个用户列表和角色
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "email":"wangjinlong@innotechx.com",
                "nickname":"王金龙",
                "project":[
                    {
                        "id":11,
                        "name":"z_test"
                    }
                ],
                "role":[
                    {
                        "comment":"超级管理员",
                        "id":1,
                        "name":"admin"
                    }
                ],
                "userid":1,
                "username":"wiggens",
                "userweight":1
            }
        ],
        "message":"ok"
    }
    """
    data = UserBusiness.query_user_single_project_role(user_id)

    return json_detail_render(0, data)


# 获取不是当前项目的用户列表
@user.route('/unless/user_list', methods=['GET'])
def project_unless_user():
    """
    @api {get} /v1/user/unless/user_list 获取 不是当前项目的用户列表
    @apiName GetUserListsByUnlessPorject
    @apiGroup 用户
    @apiDescription 获取不是当前项目的用户列表
    @apiParam {int} project_id 项目id
    @apiParam {int} [limit] limit
    @apiParam {int} [offset] offset
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "project_id": 4
            }
        ],
        "message": "ok"
    }
    """
    user_list = []
    user_data = UserBusiness.query_user_list()
    # 项目列表的用户
    for i in range(0, len(user_data)):
        user_list.append(int(user_data[i]['user_id']))
    # 过滤admin用户
    # admin_list = UserBusiness.query_admin_list()

    user_list = list(set(user_list))

    data = UserBusiness.query_unless_user_list(user_list)

    return json_detail_render(0, data)


# 获取所有用户列表和昵称
@user.route('/all', methods=['GET'])
def user_all_list():
    """
    @api {get} /v1/user/all 获取 所有用户列表和昵称
    @apiName GetAllUser
    @apiGroup 用户
    @apiDescription 获取所有用户列表和昵称
    @apiParam {int} [limit] limit
    @apiParam {int} [offset] offset
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "id": 117,
                "nickname": "李晓龙"
            },
        ],
        "message": "ok"
    }
    """
    data = UserBusiness.query_all_user_list()
    return json_detail_render(0, data)


# 获取项目的admin的id
@user.route('/manage/isappear', methods=['GET'])
def isappera_admin():
    user_id = request.args.get('user_id')
    project_id = request.args.get('project_id')

    owner_list = UserBusiness.owner_project_list()
    isappear = 1

    if user_id:
        roles_row = UserBusiness.query_json_by_id_and_project(user_id, project_id)
        roles_list = roles_row[0]['role'] if roles_row else []
        roles = [i['name'] for i in roles_list]

        if g.is_admin or (roles and 'owner' in roles and owner_list and int(project_id) in owner_list):
            isappear = 0
    data = [{'isappear': isappear}]

    return json_detail_render(0, data)


# 获取用户的权限和项目列表e
@user.route('/gain/roles_projects', methods=['GET'])
def gain_role_project():
    user_id = request.args.get('user_id')
    roles = []
    project_list = UserBusiness.owner_project_list()

    roles_list = UserBusiness.query_json_by_id(user_id)
    current_app.logger.info(roles_list)

    if len(roles_list) > 0:
        roles = roles_list[0]['role']

    data = {'role': roles, 'project': project_list}

    return json_detail_render(0, data)


@user.route('/userbindproject', methods=['GET'])
def get_bind_project_by_user():
    user_id = request.args.get('userid')
    project_id = UserBusiness.query_project_by_userid(user_id)
    return json_detail_render(0, project_id)


@user.route('/allflow', methods=['GET'])
def get_all_flow():
    data = UserBusiness.query_flow_all_json()
    return json_detail_render(0, data)


@user.route('/projectlist', methods=['GET'])
def get_project_list():
    project_list = UserBusiness.own_in_project()
    return json_detail_render(0, project_list)


@user.route('/userinfo', methods=['GET'])
def get_json_by_id():
    user_id = request.args.get('userid')
    project_id = request.args.get('project_id')
    if not project_id:
        project_id = request.headers.get('projectid')
    data = UserBusiness.query_json_by_id_and_project(user_id, project_id)
    return json_detail_render(0, data)


@user.route('/wxemail', methods=['GET'])
def get_wxemails():
    userids = request.args.get('userids')
    email_list = UserBusiness.get_wxemails(userids)
    return json_detail_render(0, email_list)


# 获取roleID为X的用户
@user.route('/role/<int:role_id>', methods=['GET'])
def get_user_by_role_id(role_id):
    ret = UserBusiness.query_by_roleid(role_id)
    return json_detail_render(0, ret)


@user.route('/projectandrole', methods=['GET'])
def get_user_by_project_and_role_id():
    project_id = request.args.get('project_id')
    role_id = request.args.get('role_id')
    ret = UserBusiness.get_user_by_project_and_role_id(project_id, role_id)
    return json_detail_render(0, ret)


# 获取admin的用户
@user.route('/admin', methods=['GET'])
def get_user_by_admin():
    ret = UserBusiness.query_admin_list()
    return json_detail_render(0, ret)


# 解除用户和项目的绑定的关系
@user.route('/detachuser', methods=['POST'])
@required(modify_permission)
@validation('POST:projectdetachusers')
def detach_user():
    """
    @api {post} /v1/user/detachuser 项目解绑用户
    @apiName DetachUserForProject
    @apiGroup 用户
    @apiDescription 项目解绑用户
    @apiParam {int} user_id 用户ID
    @apiParam {int} project_id 项目ID
    @apiParamExample {json} Request-Example:
    {
        "project_id": 75,
        "user_id":1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[],
    "message":"ok"
    }
    """
    project_id, user_id = parse_json_form('projectdetachusers')
    ret, msg = UserBusiness.project_detach_user(project_id, user_id)

    return json_detail_render(ret, [], msg)


# 批量增加用户到当前的项目中
@user.route('/adduser', methods=['POST'])
@required(modify_permission)
@validation('POST:projectadduser')
def add_users():
    """
    @api {post} /v1/user/adduser 项目绑定用户
    @apiName AddUserForProject
    @apiGroup 用户
    @apiDescription 项目绑定用户
    @apiParam {list} user_list 用户ID
    @apiParam {int} project_id 项目ID
    @apiParamExample {json} Request-Example:
    {
        "project_id": 75,
        "user_list":[1,2]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[],
    "message":"ok"
    }
    """
    project_id, user_list = parse_json_form('projectadduser')
    ret, msg = UserBusiness.project_add_users(project_id, user_list)
    return json_detail_render(ret, [], msg)


# 根据 wx-email 获取 userinfo
@user.route('/userinfo/wxemail', methods=['GET'])
def get_user_by_wxemail():
    wxemail = request.args.get('email')
    ret = UserBusiness.query_json_by_wxemail(wxemail)
    return json_detail_render(0, ret)
