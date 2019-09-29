from flask import request

from apps.auth.auth_require import required
from apps.project.business.cases import CaseBusiness
from apps.project.extentions import parse_list_args2, parse_json_form, validation
from library.api.render import json_detail_render, json_list_render2
from library.api.tBlueprint import tblueprint

bpname = 'case'
view_permission = f'{bpname}_view'
modify_permission = f'{bpname}_modify'
case = tblueprint(bpname, __name__)


@case.route('/', methods=['POST'])
@required(modify_permission)
@validation('POST:casecreate')
def case_create_handler():
    """
    @api {post} /v1/case/ 新增 用例
    @apiName CreateCase
    @apiGroup 项目
    @apiDescription 新增用例
    @apiParam {int} module_id 模块id
    @apiParam {string} ctype 用例类型
    @apiParam {string} title 标题
    @apiParam {string} precondition 前置条件
    @apiParam {string} step_result 用例步骤及预期结果 json->string格式存入
    @apiParam {int} creator 创建人
    @apiParam {int} priority 优先级 0:紧急 1:高 2:中 3:低
    @apiParam {list} requirement_ids 需求 ID 列表
    @apiParamExample {json} Request-Example:
    {
        "module_id": 1,
        "ctype": "功能回归",
        "title": "test",
        "precondition": "",
        "step_result": "",
        "creator": 1,
        "priority": 1,
        "requirement_ids": [1,2,3]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    module_id, ctype, title, precondition, step_result, creator, priority, requirement_ids = parse_json_form(
        'casecreate')
    if CaseBusiness.project_permission(mid=module_id):
        return json_detail_render(109)
    ret, msg = CaseBusiness.create(module_id, ctype, title, precondition, step_result, creator, priority,
                                   requirement_ids)
    return json_detail_render(ret, [], msg)


@case.route('/<int:case_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:caseupdate')
def case_single_modify_handler(case_id):
    """
    @api {post} /v1/case/{case_id} 修改 用例
    @apiName ModifyCase
    @apiGroup 项目
    @apiDescription 修改用例
    @apiParam {int} module_id 模块id
    @apiParam {string} ctype 用例类型
    @apiParam {string} title 标题
    @apiParam {string} precondition 前置条件
    @apiParam {string} step_result 用例步骤及预期结果 json->string格式存入
    @apiParam {int} is_auto 是否可转自动化
    @apiParam {int} priority 优先级 0:紧急 1:高 2:中 3:低
    @apiParam {list} requirement_ids 需求 ID 列表
    @apiParamExample {json} Request-Example:
    {
        "module_id": 1,
        "ctype": "功能回归",
        "title": "test",
        "precondition": "",
        "step_result": "",
        "is_auto": 1,
        "priority": 1,
        "requirement_ids": [1,2,3]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    if CaseBusiness.project_permission(id=case_id):
        return json_detail_render(109)
    module_id, ctype, title, precondition, step_result, is_auto, priority, requirement_ids = parse_json_form(
        'caseupdate')

    ret = CaseBusiness.update(case_id, module_id, ctype, title, precondition, step_result, is_auto, priority,
                              requirement_ids)

    return json_detail_render(ret)


@case.route('/duplication/<int:case_id>', methods=['POST'])
@required(modify_permission)
def copy_case(case_id):
    """
    @api {post} /v1/case/duplication/{case_id} 复制 用例
    @apiName CopyCase
    @apiGroup 项目
    @apiDescription 复制用例
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    code = CaseBusiness.copy_case_by_id(case_id)
    return {'code': code}


@case.route('/<int:case_id>', methods=['DELETE'])
def case_single_delete_handler(case_id):
    """
    @api {delete} /v1/case/{case_id} 删除 用例
    @apiName DeleteCase
    @apiGroup 项目
    @apiDescription 删除用例
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    if CaseBusiness.project_permission(id=case_id):
        return json_detail_render(109)
    ret = CaseBusiness.delete(case_id)
    return json_detail_render(ret)


@case.route('/', methods=['GET'])
def case_query_handler():
    """
    @api {get} /v1/case/ 查询 用例
    @apiName GetCase
    @apiGroup 项目
    @apiDescription 查询用例，可根据需求id查询
    @apiParam {int} [page_size] 分页-单页数目
    @apiParam {int} [page_index] 分页-页数
    @apiParam {int} [requirement_id] 需求id
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "cnumber": "TC3891",
                "creation_time": "2019-07-26 16:14:07",
                "ctype": "1",
                "id": 3891,
                "is_auto": 1,
                "modified_time": "2019-07-26 16:14:07",
                "module": "看板管理",
                "moduleid": 342,
                "precondition": "1",
                "priority": 0,
                "requirement":[
                    {
                        "requirement_id": 1,
                        "requirement_title": "123123",
                    }
                ],
                "status": 0,
                "step_result": "{\"step_result\":[{\"step\":\"1\",\"expect\":\"1\"}]}",
                "title": "1",
                "userid": 104,
                "username": "刘德华153"
            }
        ],
        "message": "ok",
        "page_index": 1,
        "page_size": 2,
        "total": 2915
    }
    """
    page_size, page_index = parse_list_args2()
    requirement_id = request.args.get('requirement_id')
    if requirement_id:
        data, count = CaseBusiness.query_by_requirement_id(requirement_id, page_size, page_index)
    else:
        data, count = CaseBusiness.paginate_data(page_size, page_index)
    return json_list_render2(0, data, page_size, page_index, count)


@case.route('/<int:case_id>', methods=['GET'])
def case_single_query_handler(case_id):
    """
    @api {get} /v1/case/{case_id} 查询 单个用例
    @apiName GetCaseByCaseId
    @apiGroup 项目
    @apiDescription 查询单个用例
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "cnumber": "TC3891",
                "creation_time": "2019-07-26 16:14:07",
                "ctype": "1",
                "id": 3891,
                "is_auto": 1,
                "modified_time": "2019-07-26 16:14:07",
                "module": "看板管理",
                "moduleid": 342,
                "precondition": "1",
                "priority": 0,
                "requirement":[
                    {
                        "requirement_id": 1,
                        "requirement_title": "123123",
                    }
                ],
                "status": 0,
                "step_result": "{\"step_result\":[{\"step\":\"1\",\"expect\":\"1\"}]}",
                "title": "1",
                "userid": 104,
                "username": "刘德华153"
            }
        ],
        "message": "ok"
    }
    """
    data = CaseBusiness.query_by_id(case_id)

    return json_detail_render(0, data)


@case.route('/querybymodule/<int:mid>', methods=['GET'])
def case_query_by_module_id_handler(mid):
    """
    @api {get} /v1/case/querybymodule/mid 查询 单个模块下的用例
    @apiName GetCaseByModuleId
    @apiGroup 项目
    @apiDescription 查询单个模块下的用例
    @apiParam {int} [page_size] 分页-单页数目
    @apiParam {int} [page_index] 分页-页数
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "cnumber": "TC8",
                "creation_time": "2018-12-19 11:04:57",
                "ctype": "1",
                "id": 8,
                "is_auto": 1,
                "modified_time": "2018-12-19 11:04:57",
                "module": "音频",
                "moduleid": 1,
                "precondition": "1231321321",
                "priority": "",
                "status": 0,
                "step_result": "{\"step_result\":[{\"step\":\"132\",\"expect\":\"321321321\"}]}",
                "title": "",
                "userid": 3,
                "username": "周冬彬"
            }
        ],
        "message": "ok",
        "page_index": 1,
        "page_size": 10,
        "total": 1
    }
    """
    page_size = request.args.get('page_size')
    page_index = request.args.get('page_index')
    data, count = CaseBusiness.paginate_data(mid=mid, page_size=page_size, page_index=page_index)

    return json_list_render2(0, data, page_size, page_index, count)


@case.route('/export', methods=['GET'])
def case_export():
    """
    @api {post} /v1/case/export 导出 所有用例
    @apiName ExportCases
    @apiGroup 项目
    @apiDescription 导出所有用例
    @apiParam {int} project_id 项目id
    @apiParam {list} module_data 模块信息
    @apiParam {int} user_id 用户id
    @apiParamExample {json} Request-Example:
    {
        "project_id":4,
        "user_id":96,
        "module_data":[{"module_id":342,"case_id":[]}]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":{"url":"http://tcloud-static.oss-cn-beijing.aliyuncs.com/v1/case_export/96/1564575657.xls"},
        "message":""
    }
    """
    code, data, message = CaseBusiness.case_export()
    return json_detail_render(code=code, data=data, message=message)


@case.route('/import', methods=['POST'])
@required(modify_permission)
@validation('POST:fileimport')
def case_import():
    """
    @api {post} /v1/case/import 导入 用例
    @apiName ImportCases
    @apiGroup 项目
    @apiDescription 导入用例
    @apiParam {string} url_path oss url
    @apiParam {int} creator 创建人
    @apiParam {int} project_id 项目id
    @apiParam {int} module_id 模块id
    @apiParamExample {json} Request-Example:
    {
        "url_path": "http://tcloud-static.oss-cn-beijing.aliyuncs.com/v1/case_export/96/1564575657.xls",
        "project_id":4,
        "creator":96,
        "module_id":342
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":"",
        "message":"ok"
    }
    """
    url_path, creator, project_id, module_id = parse_json_form('fileimport')
    code, message = CaseBusiness.case_import(url_path, creator, project_id, module_id)
    return json_detail_render(code, [], message)


@case.route('/list', methods=['POST'])
@required(view_permission)
def case_list():
    case_ids = parse_json_form('case_info_by_ids')
    data = CaseBusiness.case_info_by_ids(case_ids)
    return {'code': 0, 'data': data}
