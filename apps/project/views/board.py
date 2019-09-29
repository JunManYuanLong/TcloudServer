from flask import Blueprint, request

from apps.project.business.board import BoardBusiness
from apps.project.extentions import parse_list_args2
from library.api.render import json_detail_render

bpname = 'board'
board = Blueprint(bpname, __name__)


# 我创建的
@board.route('/create', methods=['GET'])
def create_work_handler():
    """
    @api {GET} /v1/board/create 查询 我的创建
    @apiName GetCreateByMe
    @apiGroup 项目
    @apiDescription 查询 我的创建
    @apiParam {int} projectid 项目编号
    @apiParam {string} type 类型 ： task，issue
    @apiParam {string} title 标题：根据标题搜索
    @apiParamExample {json} Request-Example:
    ?projectid=1
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "data": {
            "issue_info": [
                {
                    "chance": 3,
                    "creator_id": 26,
                    "creator_name": "张素浈",
                    "description": "",
                    "handle_status": 1,
                    "handler_id": "",
                    "handler_name": "",
                    "id": 363,
                    "issue_number": "T363",
                    "level": 4,
                    "priority": 3,
                    "project_id": 4,
                    "stage": "",
                    "title": "testsz111111",
                    "version_id": 168,
                    "version_name": "1.2.5啊啊"
                }
            ],
            "task_case_info": [
                {
                    "cnumber": "TC3835",
                    "comment": "",
                    "ctype": "1,5",
                    "description": "",
                    "exe_way": "",
                    "executor_id": "",
                    "executor_name": "",
                    "handler_id": "",
                    "handler_name": "",
                    "is_auto": 1,
                    "module_id": 321,
                    "module_name": "二级目录11111111111111111111111",
                    "precondition": "多条必须换行，由数字加、开头，可为空",
                    "project_id": 4,
                    "status": 0,
                    "step_result": "{"step_result": [{"step": "点击新建流程按钮", "expect": "啊啊啊啊啊"}, {"step": "点击添加需求的按钮，选择需要的需求，点击确定", "expect": "求选择成功"}]}",
                    "task_id": 152,
                    "taskcaseid": 682,
                    "title": "11111这是用例描述"
                }
            ]
        },
     "message": "ok",
     "page_size": 1,
     "page_index": 1,
     "total": 1
    }
    """
    page_size, page_index = parse_list_args2()
    r_type = request.args.get("type")
    title = request.args.get("title")
    data, count = BoardBusiness.user_create(page_size, page_index, r_type, title)
    return {
        "code": 0,
        "data": data,
        "total": count,
        "page_size": page_size,
        "page_index": page_index
    }


# 我的代办
@board.route('/unfinish', methods=['GET'])
def unfinish_work_handler():
    """
    @api {GET} /v1/board/unfinish 查询 我的待办
    @apiName GetTodoByMe
    @apiGroup 项目
    @apiDescription 查询 我的待办
    @apiParam {int} projectid 项目编号
    @apiParam {string} type 类型 ： task，issue, task_case
    @apiParam {string} title 标题：根据标题搜索
    @apiParamExample {json} Request-Example:
    ?projectid=1
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "data": {
            "issue_info": [
                {
                    "chance": 3,
                    "creator_id": 26,
                    "creator_name": "张素浈",
                    "description": "",
                    "handle_status": 1,
                    "handler_id": "",
                    "handler_name": "",
                    "id": 363,
                    "issue_number": "T363",
                    "level": 4,
                    "priority": 3,
                    "project_id": 4,
                    "stage": "",
                    "title": "testsz111111",
                    "version_id": 168,
                    "version_name": "1.2.5啊啊"
                }
            ],
            "task_case_info": [
                {
                    "cnumber": "TC3835",
                    "comment": "",
                    "ctype": "1,5",
                    "description": "",
                    "exe_way": "",
                    "executor_id": "",
                    "executor_name": "",
                    "handler_id": "",
                    "handler_name": "",
                    "is_auto": 1,
                    "module_id": 321,
                    "module_name": "二级目录11111111111111111111111",
                    "precondition": "多条必须换行，由数字加、开头，可为空",
                    "project_id": 4,
                    "status": 0,
                    "step_result": "{"step_result": [{"step": "点击新建流程按钮", "expect": "啊啊啊啊啊"}, {"step": "点击添加需求的按钮，选择需要的需求，点击确定", "expect": "求选择成功"}]}",
                    "task_id": 152,
                    "taskcaseid": 682,
                    "title": "11111这是用例描述"
                }
            ]
        },
     "message": "ok",
     "page_size": 1,
     "page_index": 1,
     "total": 1
    }
    """
    page_size, page_index = parse_list_args2()
    r_type = request.args.get("type")
    title = request.args.get("title")
    data, count = BoardBusiness.user_unfinish(page_size, page_index, r_type, title)
    return {
        "code": 0,
        "data": data,
        "total": count,
        "page_size": page_size,
        "page_index": page_index
    }


# 我的已办
@board.route('/finish', methods=['GET'])
def finish_work_handler():
    """
    @api {GET} /v1/board/finish 查询 我的已完成
    @apiName GetDoneByMe
    @apiGroup 项目
    @apiDescription 查询 我的已完成
    @apiParam {int} projectid 项目编号
    @apiParam {string} type 类型 ： task，issue, task_case
    @apiParam {string} title 标题：根据标题搜索
    @apiParamExample {json} Request-Example:
    ?projectid=1
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "data": {
            "issue_info": [
                {
                    "chance": 3,
                    "creator_id": 26,
                    "creator_name": "张素浈",
                    "description": "",
                    "handle_status": 1,
                    "handler_id": "",
                    "handler_name": "",
                    "id": 363,
                    "issue_number": "T363",
                    "level": 4,
                    "priority": 3,
                    "project_id": 4,
                    "stage": "",
                    "title": "testsz111111",
                    "version_id": 168,
                    "version_name": "1.2.5啊啊"
                }
            ],
            "task_case_info": [
                {
                    "cnumber": "TC3835",
                    "comment": "",
                    "ctype": "1,5",
                    "description": "",
                    "exe_way": "",
                    "executor_id": "",
                    "executor_name": "",
                    "handler_id": "",
                    "handler_name": "",
                    "is_auto": 1,
                    "module_id": 321,
                    "module_name": "二级目录11111111111111111111111",
                    "precondition": "多条必须换行，由数字加、开头，可为空",
                    "project_id": 4,
                    "status": 0,
                    "step_result": "{"step_result": [{"step": "点击新建流程按钮", "expect": "啊啊啊啊啊"}, {"step": "点击添加需求的按钮，选择需要的需求，点击确定", "expect": "求选择成功"}]}",
                    "task_id": 152,
                    "taskcaseid": 682,
                    "title": "11111这是用例描述"
                }
            ]
        },
     "message": "ok",
     "page_size": 1,
     "page_index": 1,
     "total": 1
    }
    """
    page_size, page_index = parse_list_args2()
    r_type = request.args.get("type")
    title = request.args.get("title")
    data, count = BoardBusiness.user_finish(page_size, page_index, r_type, title)
    return {
        "code": 0,
        "data": data,
        "total": count,
        "page_size": page_size,
        "page_index": page_index
    }


# STF接口
@board.route('/devices', methods=['GET'])
def stf_devices_handler():
    """
    @api {GET} /v1/board/devices 查询 STF 设备
    @apiName GetStfByMe
    @apiGroup 项目
    @apiDescription 查询 STF 设备
    @apiParam {int} projectid 项目编号
    @apiParamExample {json} Request-Example:
    ?projectid=1
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
    "code":0,
    "data":{
        "devices":[
            {
                "abi":"arm64-v8a",
                "airplaneMode":false,
                "battery":{
                    "health":"good",
                    "level":100,
                    "scale":100,
                    "source":"ac",
                    "status":"full",
                    "temp":33,
                    "voltage":4.408
                },
                "browser":{
                    "apps":[
                        {
                            "developer":"Google Inc.",
                            "id":"com.android.browser/.BrowserActivity",
                            "name":"Browser",
                            "selected":true,
                            "system":true,
                            "type":"android-browser"
                        }
                    ],
                    "selected":true
                },
                "channel":"TfzwXWVTHC9D/tlxwjRpxnig5a8=",
                "cpuPlatform":"msm8937",
                "createdAt":"2019-06-14T06:49:52.169Z",
                "display":{
                    "density":2,
                    "fps":60.000003814697266,
                    "height":1280,
                    "id":0,
                    "rotation":0,
                    "secure":true,
                    "size":4.971253395080566,
                    "url":"ws://stf.ywopt.com:7456",
                    "width":720,
                    "xdpi":294.9670104980469,
                    "ydpi":295.56298828125
                },
                "manufacturer":"XIAOMI",
                "model":"Redmi 4A",
                "network":{
                    "connected":false,
                    "failover":false,
                    "roaming":false,
                    "subtype":null,
                    "type":null
                },
                "openGLESVersion":"3.0",
                "operator":"中国移动",
                "owner":null,
                "phone":{
                    "iccid":"898602e3091531017955",
                    "imei":"866982035506783",
                    "imsi":"460070311106955",
                    "network":"UNKNOWN",
                    "phoneNumber":"+8617031117086"
                },
                "platform":"Android",
                "presenceChangedAt":"2019-07-30T08:22:16.153Z",
                "present":true,
                "product":"rolex",
                "provider":{
                    "channel":"tPuKucXkSMmwJM4D7it1yA==",
                    "name":"whmacdeMac-mini.local"
                },
                "ready":true,
                "remoteConnect":false,
                "remoteConnectUrl":null,
                "reverseForwards":[

                ],
                "sdk":"23",
                "serial":"2fba959b7d74",
                "status":3,
                "statusChangedAt":"2019-07-30T08:22:16.168Z",
                "usage":null,
                "usageChangedAt":"2019-07-05T06:54:52.613Z",
                "using":false,
                "version":"6.0.1"
            }
        ]
    ]
     "message": "ok"
    }
    """
    data = BoardBusiness.stf_devices()
    return json_detail_render(0, data)