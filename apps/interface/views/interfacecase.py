import json

from flask import Blueprint, request, jsonify

from apps.interface.business.interfacecase import InterfaceCaseBusiness
from apps.interface.business.interfacecasedata import InterfaceCaseDataBusiness
from apps.interface.models.interfaceconfig import InterfaceConfig

interfacecase = Blueprint('interfacecase', __name__)


@interfacecase.route('/add', methods=['POST'])
def add_case():
    """
    @api {post} /v1/interfacecase/add InterfaceCase_用例添加、编辑
    @apiName interfaceCaseAddandEdit
    @apiGroup Interface
    @apiDescription 用例添加、编辑
    @apiParam {string} name 用例的名字
    @apiParam {string} desc 用例的描述
    @apiParam {int} ids 用例的id
    @apiParam {int} times 用例执行的次数
    @apiParam {int} caseSetId 用例集id
    @apiParam {list} funcAddress 用例需要引用的函数
    @apiParam {string} project 项目名称
    @apiParam {string} variable 用例公共参数
    @apiParam {list} apiCases 函数文件
    @apiParam {string} number 排序
    @apiParamExample {json} Request-Example:
    {
        "apiCases": [{"apiMsgId": 20,
                      "case_name": "12313123",
                      "desc": null,
                      "down_func": null,
                      "extract":[{"key":null,"remark":null,"value":null}],
                      "gather_id":14,
                      "json_variable":"",
                      "name":"12313123",
                      "num":1,
                      "param":[{"key":"","value":""}],
                      "status":true,
                      "statusCase":{"extract": [true, true], "param": [true, true],
                                    "validate": [true, true], "variable": [true, true]},
                      "time":1,
                      "up_func":null,
                      "url":"1121scvsfa",
                      "validate":[{"key":null,"value":null}],
                      "variable":[{"key":null,"param_type":"string","remark":null,"value":null}],
                      "variableType":"data"
                      }],
        "caseSetId": 1,
        "desc": "",
        "funcAddress": [],
        "ids": "",
        "name": "test",
        "num": "",
        "project": "mengtui",
        "times": 1,
        "variable": "[{"key":"","value":"","remark":""}]"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "case_id": 87,
        "status": 1,
        "msg":"新建成功"
    }
    """

    data = request.json
    name = data.get('name')
    desc = data.get('desc')
    ids = data.get('ids')
    times = data.get('times')
    case_set_id = data.get('caseSetId')
    func_address = json.dumps(data.get('funcAddress'))
    project = data.get('project')
    variable = data.get('variable')
    api_cases = data.get('apiCases')
    number = data.get('num')

    jsondata = InterfaceCaseBusiness.add_case(name, desc, ids, times, case_set_id, func_address, project,
                                              variable, api_cases, number)

    return jsondata


@interfacecase.route('/find', methods=['POST'])
def find_case():
    """
    @api {post} /v1/interfacecase/find InterfaceCase_查找用例
    @apiName interfacecaseFind
    @apiGroup Interface
    @apiDescription 查找用例
    @apiParam {string} projectName 项目名字
    @apiParam {string} caseName 用例名称
    @apiParam {int} setId 用例集id
    @apiParam {int} page 页数
    @apiParam {int} sizePage 页面数量
    @apiParamExample {json} Request-Example:
    {
        "projectName": "mengtui",
        "page": 1,
        "caseName":"",
        "setId": 1,
        "sizePage": 20
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": [
            {
                "desc": "111",
                "label": "test1",
                "leaf": true,
                "name": "test1",
                "num": 1,
                "sceneId": 84
            },
            {
                "desc": "",
                "label": "test",
                "leaf": true,
                "name": "test",
                "num": 2,
                "sceneId": 87
            }
        ],
        "status": 1,
        "total": 2
    }
    """
    data = request.json
    project_name = data.get('projectName')
    case_name = data.get('caseName')
    set_id = data.get('setId')
    page = data.get('page') if data.get('page') else 1
    per_page = data.get('sizePage') if data.get('sizePage') else 10

    jsondata = InterfaceCaseBusiness.find_case(project_name, case_name, set_id, page, per_page)

    return jsondata


@interfacecase.route('/del', methods=['POST'])
def del_case():
    """
    @api {post} /v1/interfacecase/del InterfaceCase_删除用例
    @apiName interfacecaseDel
    @apiGroup Interface
    @apiDescription 删除用例
    @apiParam {int} caseId 用例id
    @apiParamExample {json} Request-Example:
    {
        "caseId": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "删除成功",
        "status": 1
    }
    """
    data = request.json
    case_id = data.get('caseId')
    jsondata = InterfaceCaseBusiness.del_case(case_id)
    return jsondata


@interfacecase.route('/apiCase/del', methods=['POST'])
def del_api_case():
    """
    @api {post} /v1/interfacecase/apiCase/del InterfaceCase_删除用例下的接口步骤信息
    @apiName interfacecaseApiCaseDel
    @apiGroup Interface
    @apiDescription 删除用例下的接口步骤信息
    @apiParam {int} id 用例id
    @apiParamExample {json} Request-Example:
    {
        "id": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "删除成功",
        "status": 1
    }
    """
    data = request.json
    case_id = data.get('id')
    #     _data = CaseData.query.filter_by(id=case_id).first()
    #     db.session.delete(_data)
    InterfaceCaseDataBusiness.casedata_delete(case_id)
    return jsonify({'msg': '删除成功', 'status': 1})


@interfacecase.route('/edit', methods=['POST'])
def edit_case():
    """
    @api {post} /v1/interfacecase/edit InterfaceCase_返回待编辑用例信息
    @apiName interfacecaseEdit
    @apiGroup Interface
    @apiDescription 返回待编辑用例信息
    @apiParam {int} caseId 用例id
    @apiParam {bool} copyEditStatus 编辑用例的状态
    @apiParamExample {json} Request-Example:
    {
        "caseId": 84,
        "copyEditStatus": false
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": {
            "cases": [
                {
                    "apiMsgId": 20,
                    "case_name": "12313123",
                    "desc": null,
                    "down_func": null,
                    "extract": [
                        {
                            "key": null,
                            "remark": null,
                            "value": null
                        }
                    ],
                    "id": 216,
                    "json_variable": "",
                    "name": "12313123",
                    "num": 0,
                    "param": [
                        {
                            "key": "",
                            "value": ""
                        }
                    ],
                    "status": true,
                    "statusCase": {
                        "extract": [
                            true,
                            true
                        ],
                        "param": [
                            true,
                            true
                        ],
                        "validate": [
                            true,
                            true
                        ],
                        "variable": [
                            true,
                            true
                        ]
                    },
                    "time": 1,
                    "up_func": null,
                    "validate": [
                        {
                            "key": null,
                            "value": null
                        }
                    ],
                    "variable": [
                        true,
                        true
                    ],
                    "variableType": "data"
                }
            ],
            "desc": "111",
            "func_address": [],
            "name": "test1",
            "num": 1,
            "setId": 1,
            "times": 1,
            "variable": [
                {
                    "key": "1",
                    "remark": "",
                    "value": "1"
                }
            ]
        },
        "status": 1
    }
    """
    data = request.json
    case_id = data.get('caseId')
    status = data.get('copyEditStatus')
    jsondata = InterfaceCaseBusiness.edit_case(case_id, status)
    return jsondata


@interfacecase.route('/config/data', methods=['POST'])
def data_config():
    """
    @api {post} /v1/interfacecase/config/data InterfaceCase_返回需要配置信息
    @apiName interfacecaseConfigData
    @apiGroup Interface
    @apiDescription 返回需要配置信息
    @apiParam {int} configId 配置id
    @apiParamExample {json} Request-Example:
    {
        "configId": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": {},
        "status": 1
    }
    """
    data = request.json
    config_id = data.get('configId')
    _data = InterfaceConfig.query.filter_by(id=config_id, status=InterfaceConfig.ACTIVE).first()

    return jsonify({
        'data': {
            'variables': json.loads(_data.variables),
            'func_address': json.loads(_data.func_address)
        },
        'status': 1
    })
