from flask import Blueprint, request, jsonify

from apps.interface.business.interfaceapimsg import InterfaceApiMsgBusiness
from apps.interface.util.global_variable import *

interfaceapimsg = Blueprint('interfaceapimsg', __name__)


@interfaceapimsg.route('/add', methods=['POST'])
def add_api_msg():
    """
    @api {post} /v1/interfaceapimsg/add InterfaceApiImsg_接口信息增加、编辑
    @apiName interfaceApiImsg
    @apiGroup Interface
    @apiDescription 接口信息增加、编辑
    @apiParam {string} projectName 项目名称
    @apiParam {string} apiMsgName 接口信息名称
    @apiParam {string} variableType 参数类型选择
    @apiParam {string} desc 接口信息描述
    @apiParam {string} header 头部信息
    @apiParam {string} extract 提取信息
    @apiParam {string} validate 断言信息
    @apiParam {int} apiMsgId 接口信息id
    @apiParam {string} upFunc 接口执行前的函数
    @apiParam {string} downFunc 接口执行后的函数
    @apiParam {string} method 请求方式
    @apiParam {int} moduleId 所属的接口模块id
    @apiParam {string} url 接口地址
    @apiParam {string} choiceUrl 基础url,序号对应项目的环境
    @apiParam {string} variable form-data形式的参数
    @apiParam {string} jsonVariable json形式的参数
    @apiParam {string} param url上面所带的参数
    @apiParam {int} all_project_id 总项目id
    @apiParamExample {json} Request-Example:
    {
        "id": 1,
        "all_project_id": 4
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": {
            "environment_choice": "first",
            "headers": [],
            "host": [
                "http://sx.api.mengtuiapp.com"
            ],
            "host_four": [],
            "host_three": [],
            "host_two": [],
            "principal": null,
            "pro_name": "mengtui",
            "user_id": 3,
            "variables": []
        },
        "status": 1
    }
    """
    data = request.json
    project_name = data.get('projectName')
    api_msg_name = data.get('apiMsgName')
    variable_type = data.get('variableType')
    desc_string = data.get('desc')
    header = data.get('header')
    extract = data.get('extract')
    validate = data.get('validate')
    api_msg_id = data.get('apiMsgId')
    up_func = data.get('upFunc')
    down_func = data.get('downFunc')
    method = data.get('method')
    module_id = data.get('moduleId')
    url = data.get('url').split('?')[0]
    status_url = data.get('choiceUrl')
    variable = data.get('variable')
    json_variable = data.get('jsonVariable')
    param = data.get('param')
    all_project_id = data.get('all_project_id')
    number = data.get('num')

    jsondata = InterfaceApiMsgBusiness.add_api_msg(project_name, api_msg_name, variable_type, desc_string, header,
                                                   extract, validate, api_msg_id, up_func, down_func, method, module_id,
                                                   url, status_url, variable, json_variable, param, all_project_id,
                                                   number)

    return jsondata


@interfaceapimsg.route('/editAndCopy', methods=['POST'])
def edit_api_msg():
    """
    @api {post} /v1/interfaceapimsg/editAndCopy InterfaceApiImsg_返回待编辑或复制的接口信息
    @apiName interfaceApiImsgEditAndCopy
    @apiGroup Interface
    @apiDescription 返回待编辑或复制的接口信息
    @apiParam {int} apiMsgId 接口信息id
    @apiParamExample {json} Request-Example:
    {
        "apiMsgId": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": {
            "desc": null,
            "down_func": null,
            "extract": [
                {
                    "key": null,
                    "remark": null,
                    "value": null
                }
            ],
            "header": [
                {
                    "key": null,
                    "value": null
                }
            ],
            "json_variable": "",
            "method": "POST",
            "name": "12313123",
            "num": 1,
            "param": [
                {
                    "key": "",
                    "value": ""
                }
            ],
            "status_url": 0,
            "up_func": null,
            "url": "1121scvsfa",
            "validate": [
                {
                    "key": null,
                    "value": null
                }
            ],
            "variable": [
                {
                    "key": null,
                    "param_type": "string",
                    "remark": null,
                    "value": null
                }
            ],
            "variableType": "data"
        },
        "status": 1
    }
    """
    data = request.json
    case_id = data.get('apiMsgId')
    jsondata = InterfaceApiMsgBusiness.edit_api_msg(case_id)
    return jsondata


@interfaceapimsg.route('/run', methods=['POST'])
def run_api_msg():
    """
    @api {post} /v1/interfaceapimsg/run InterfaceApiImsg_跑接口信息
    @apiName interfaceApiImsgRun
    @apiGroup Interface
    @apiDescription 跑接口信息
    @apiParam {dict} api_msg_data 接口信息
    @apiParam {string} projectName 项目名称
    @apiParam {int} configId 配置id

    @apiParamExample {json} Request-Example:
    {
        "id": 1,
        "all_project_id": 4
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "测试完成",
        "data": {},
        "status": 1
    }
    """
    data = request.json
    api_msg_data = data.get('apiMsgData')
    project_name = data.get('projectName')
    config_id = data.get('configId')

    jsondata = InterfaceApiMsgBusiness.run_api_msg(api_msg_data, project_name, config_id)
    return jsondata


@interfaceapimsg.route('/find', methods=['POST'])
def find_api_msg():
    """
    @api {post} /v1/interfaceapimsg/find InterfaceApiImsg_查接口信息
    @apiName interfaceApiImsgFind
    @apiGroup Interface
    @apiDescription 查接口信息
    @apiParam {int} moduleId 模块id
    @apiParam {string} projectName 项目名称
    @apiParam {string} apiName 接口名称
    @apiParam {int} page 当前页码
    @apiParam {int} sizePage 当前页码数量
    @apiParamExample {json} Request-Example:
    {
        "id": 1,
        "all_project_id": 4
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": [
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
                "gather_id": 14,
                "json_variable": "",
                "name": "12313123",
                "num": 1,
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
                "url": "1121scvsfa",
                "validate": [
                    {
                        "key": null,
                        "value": null
                    }
                ],
                "variable": [
                    {
                        "key": null,
                        "param_type": "string",
                        "remark": null,
                        "value": null
                    }
                ],
                "variableType": "data"
            }
        ],
        "status": 1,
        "total": 1
    }
    """
    data = request.json

    module_id = data.get('moduleId')
    project_name = data.get('projectName')
    api_name = data.get('apiName')
    page = data.get('page') if data.get('page') else 1
    per_page = data.get('sizePage') if data.get('sizePage') else 20

    jsondata = InterfaceApiMsgBusiness.find_api_msg(project_name, module_id, api_name, page, per_page)
    return jsondata


@interfaceapimsg.route('/del', methods=['POST'])
def del_api_msg():
    """
    @api {post} /v1/interfaceapimsg/del InterfaceApiImsg_删除接口信息
    @apiName interfaceApiImsgDel
    @apiGroup Interface
    @apiDescription 删除接口信息
    @apiParam {int} apiMsgId 接口信息id
    @apiParamExample {json} Request-Example:
    {
        "apiMsgId": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "删除成功",
        "status": 1
    }
    """
    data = request.json
    api_msg_id = data.get('apiMsgId')
    jsondata = InterfaceApiMsgBusiness.del_api_msg(api_msg_id)
    return jsondata


# 上传文件
@interfaceapimsg.route('/upload', methods=['POST'])
def api_upload():
    """
    @api {post} /v1/interfaceapimsg/upload InterfaceApiImsg_文件上传
    @apiName interfaceApiImsgUpload
    @apiGroup Interface
    @apiDescription 文件上传
    @apiParam {string} file 文件路径
    @apiParam {int} skip 是否跳过
    @apiParamExample {json} Request-Example:
    {
        "file": "/use/test.py",
        "skip": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "文件已存在，请修改文件名字后再上传",
        "status": 0
    }
    """
    data = request.files
    file = data['file']
    skip = request.form.get('skip')

    jsondata = InterfaceApiMsgBusiness.api_upload(file, skip)
    return jsondata


@interfaceapimsg.route('/checkFile', methods=['POST'])
def check_file():
    """
    @api {post} /v1/interfaceapimsg/checkFile InterfaceApiImsg_检查文件是否存在
    @apiName interfaceApiImsgCheck
    @apiGroup Interface
    @apiDescription 检查文件是否存在
    @apiParam {string} address 文件路径
    @apiParamExample {json} Request-Example:
    {
        "address": "/use/test.py",
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "文件已存在",
        "status": 0
    }
    """
    data = request.json
    address = data.get('address')
    if os.path.exists(address):
        return jsonify({"msg": "文件已存在", "status": 0})
    else:
        return jsonify({"msg": "文件不存在", "status": 1})
