from flask import request

from apps.auth.auth_require import required
from apps.project.business.modules import ModuleBusiness
from apps.project.extentions import parse_json_form, validation
from library.api.render import json_detail_render
from library.api.tBlueprint import tblueprint

bpname = 'module'
view_permission = f'{bpname}_view'
modify_permission = f'{bpname}_modify'
module = tblueprint(bpname, __name__)


@module.route('/', methods=['POST'])
@required(modify_permission)
@validation('POST:modulecreate')
def module_indexs_handler():
    """
    @api {post} /v1/module/ 新增 模块
    @apiName CreateModule
    @apiGroup 项目
    @apiDescription 新增模块,分为父模块还是子模块
    @apiParam {string} name 名称
    @apiParam {int} project_id 项目od
    @apiParam {string} description 描述
    @apiParam {int} parent_id 父模块id
    @apiParamExample {json} Request-Example:
    {
        "name":"用力模块",
        "project_id":4,
        "description":"",
        "parent_id":110
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": "",
        "message": "ok"
    }
    """
    name, project_id, description, parent_id = parse_json_form('modulecreate')
    ret, msg = ModuleBusiness.module_create(name, project_id, description, parent_id)

    return json_detail_render(ret, [], msg)


@module.route('/<int:mid>', methods=['POST'])
@required(modify_permission)
@validation('POST:modulemodify')
def module_details_handler(mid):
    """
    @api {post} /v1/module/{id} 修改 模块
    @apiName ModifyModule
    @apiGroup 项目
    @apiDescription 修改模块，应该只是修改名称描述，感觉后续可能要修改parent_id
    @apiParam {string} name 名称
    @apiParam {int} project_id 项目od
    @apiParam {string} description 描述
    @apiParam {int} weight weight
    @apiParamExample {json} Request-Example:
    {
        "name":"用力模块",
        "project_id":"4",
        "description":"",
        "weight":1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": "",
        "message": "ok"
    }
    """
    name, project_id, description, weight = parse_json_form('modulemodify')
    ret, msg = ModuleBusiness.module_modify(mid, name, project_id, description, weight)

    return json_detail_render(ret, [], msg)


@module.route('/<int:mid>', methods=['DELETE'])
def module_delete_handler(mid):
    """
    @api {delete} /v1/module/{id} 删除 模块
    @apiName DeleteModule
    @apiGroup 项目
    @apiDescription 删除模块
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": "",
        "message": "ok"
    }
    """
    ret = ModuleBusiness.module_delete(mid)
    return json_detail_render(ret)


@module.route('/querybyproject/<int:pid>', methods=['GET'])
def module_query_by_project_id_handler(pid):
    """
    @api {get} /v1/module/querybyproject/{pid} 获取 项目的用例模块
    @apiName GetMoudleByProject
    @apiGroup 项目
    @apiDescription 获取当前项目的用例模块
    @apiSuccess {string} module_name 模块名称
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
         "code":0,
         "data":[
            {"description":"","id":340,"modules":
                [
                    {
                        "description":"","id":342,"name":"\u770b\u677f\u7ba1\u7406","parentid":340,"projectid":4,
                        "status":0,"total":1,"weight":1
                    }
                ],
        ],
        "message":"ok",
        "total":85
     }
    """
    data, case_total, page_index, page_size, module_total = ModuleBusiness.query_by_project_id(pid)
    return {
        'code': 0, 'data': data, 'total': case_total, 'page_index': page_index, 'page_size': page_size,
        'module_total': module_total
    }


@module.route('/queryprojectcase/<int:pid>', methods=['GET'])
def module_query_by_project_case_handler(pid):
    """
    @api {get} /v1/module/queryprojectcase/{pid} 获取 项目的用例模块的用例
    @apiName GetCaseByProject
    @apiGroup 项目
    @apiDescription 获取项目的用例模块的用例
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
         "code":0,
         "data":[
            过长省略
        ],
        "message":"ok",
        "total":85
     }
    """
    data = ModuleBusiness.query_by_project_case(pid)
    return json_detail_render(0, data)


@module.route('/<int:mid>', methods=['GET'])
def module_detail_handler(mid):
    """
    @api {get} /v1/module/{id} 获取 项目的某个用例模块
    @apiName GetModuleByModuleid
    @apiGroup 项目
    @apiDescription 获取项目的某个用例模块(需要token)
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
         "code":0,
         "data":[
            {
                "description": "",
                "id": 342,
                "name": "看板管理",
                "projectid": 4,
                "status": 0,
                "weight": 1
            }
        ],
        "message":"ok",
     }
    """
    data = ModuleBusiness.query_json_by_id(mid)

    return json_detail_render(0, data)
