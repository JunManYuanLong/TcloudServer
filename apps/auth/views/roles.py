from flask import request

from apps.auth.auth_require import required
from apps.auth.business.role import RoleBusiness
from apps.auth.extentions import validation, parse_json_form, parse_list_args
from library.api.render import json_detail_render, json_list_render
from library.api.tBlueprint import tblueprint

# 数据库中不添加该权限，只有admin能修改和查看
bpname = 'role'
modify_permission = f'{bpname}_modify'
role = tblueprint(bpname, __name__)


@role.route('/', methods=['POST'])
@required(modify_permission)
@validation('POST:addrole')
def role_indexs_handler():
    """
    @api {post} /v1/role 新增 Role
    @apiName CreateRole
    @apiGroup 用户
    @apiDescription 新增Role
    @apiParam {string} name rolename
    @apiParam {string} comment 备注
    @apiParam {string} ability_ids 权限ID
    @apiParamExample {json} Request-Example:
    {
        "name":"dev",
        "comment":"开发",
        "ability_ids": [1,2,3]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    name, comment, ability_ids = parse_json_form('addrole')
    ret, msg = RoleBusiness.create(name, comment, ability_ids)

    return json_detail_render(ret, [], msg)


@role.route('/<int:roleid>', methods=['POST', 'DELETE'])
@required(modify_permission)
@validation('POST:modifyrole')
def role_details_handler(roleid):
    """
    @api {post} /v1/role/{role_id} 修改 role
    @apiName ModifyRole
    @apiGroup 用户
    @apiDescription 修改role
    @apiParam {string} name rolename
    @apiParam {string} comment 备注
    @apiParamExample {json} Request-Example:
    {
        "name":"dev",
        "comment":"开发",
        "ability_ids": [1,2,3]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
       "code": 0,
       "data": [],
       "message": ""
     }

    @api {delete} /v1/role/{role_id} 删除 role
    @apiName DeleteRole
    @apiGroup 用户
    @apiDescription 删除role
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
       "code": 0,
       "data": [],
       "message": ""
     }
    """
    if request.method == 'DELETE':
        if roleid in range(1, 7):
            return json_detail_render(101, [], '初始角色不允许删除')
        ret = RoleBusiness.delete(roleid)
        return json_detail_render(ret)
    name, comment, ability_ids = parse_json_form('modifyrole')
    ret, msg = RoleBusiness.modify(roleid, name, comment, ability_ids)
    return json_detail_render(ret, [], msg)


@role.route('/bindability', methods=['POST'])
@required(modify_permission)
@validation('POST:rolebindability')
def role_bind_ability_handler():
    """
    @api {post} /v1/role/bindability 绑定 Ability到Role
    @apiName RoleBindAbility
    @apiGroup 用户
    @apiDescription Role绑定Ability
    @apiParam {int} role_id Role ID
    @apiParam {int[]} ability_ids ability id 列表，为空表述清除绑定关系
    @apiParamExample {json} Request-Example:
    {
        "role_id":3,
        "ability_ids":[1]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "content": "[Tcloud - 测试站内信3]",
                "create_time": "2019-07-10 18:58:04",
                "id": 10,
                "status": 0
            },
            {
                "content": "[Tcloud - 测试站内信2]",
                "create_time": "2019-07-10 17:44:51",
                "id": 3,
                "status": 0
            }
        ],
        "message": "ok"
    }
    """
    roleid, ability_ids = parse_json_form('rolebindability')

    ret, msg = RoleBusiness.bind_abilities(roleid, ability_ids)
    return json_detail_render(ret, [], msg)


@role.route('/', methods=['GET'])
def role_index_handler():
    """
    @api {get} /v1/role 获取 role列表
    @apiName GetRoleList
    @apiGroup 用户
    @apiDescription 查询role列表
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "id": 4,
                "name": "opt1",
                "status": 0,
                "weight": 2
            },
            {
                "id": 1,
                "name": "admin",
                "status": 0,
                "weight": 1
            }
        ],
        "limit": 99999,
        "message": "ok",
        "offset": 0
    }
    """
    limit, offset = parse_list_args()
    data = RoleBusiness.query_all_json(limit, offset)

    return json_list_render(0, data, limit, offset)


@role.route('/<int:roleid>', methods=['GET'])
def role_detail_handler(roleid):
    """
    @api {get} /v1/role/{role_id} 查询 Role根据ID
    @apiName GetRoleById
    @apiGroup 用户
    @apiDescription 根据ID查询Role
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "id": 5,
                "name": "newRole",
                "status": 0,
                "weight": 1
            }
        ],
        "message": "ok"
    }
    """
    data = RoleBusiness.query_by_id(roleid)

    return json_detail_render(0, data)


@role.route('/projectrole', methods=['GET'])
def project_role_handler():
    """
    @api {get} /v1/role/projectrole 获取 所有角色的权限
    @apiName GetAllRole
    @apiGroup 用户
    @apiDescription 获取所有角色的权限
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
    "code": 0,
    "data": [
        {
            "ability": [
                {
                    "id": 6,
                    "name": "执行用例"
                },
                {
                    "id": 4,
                    "name": "编辑模块"
                },
                {
                    "id": 3,
                    "name": "编辑任务"
                },
                {
                    "id": 1,
                    "name": "编辑版本"
                }
            ],
            "comment": "开发",
            "id": 2,
            "name": "dev",
            "status": 0,
            "weight": 1
        },
        {
            "ability": [],
            "comment": "超级管理员",
            "id": 1,
            "name": "admin",
            "status": 0,
            "weight": 1
        }
    ],
    "limit": 99999,
    "message": "ok",
    "offset": 0
    }
    """
    limit, offset = parse_list_args()
    data = RoleBusiness.query_all_json(limit, offset)

    return json_list_render(0, data, limit, offset)
