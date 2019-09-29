from flask import Blueprint

from apps.tcdevices.business.tcDevices import TcDevicesBusiness
from apps.tcdevices.extentions import validation, parse_json_form
# from apps.tcdevices.settings.config import TCDEVICE_TIMEOUT
# from library.api.db import cache
from library.api.render import json_detail_render

tcdevices = Blueprint("tcdevices", __name__)


@tcdevices.route('/report', methods=['POST'])
@validation('POST:tc_devices')
def tcdevices_index_handler():
    """
    @api {post} /v1/tcdevices/report 云真机使用上报
    @apiName ReportDevices
    @apiGroup 云真机
    @apiDescription 云真机具体使用上报
    @apiParam {int} use_type 发送者
    @apiParam {string} manufacturer manufacturer
    @apiParam {string} model model
    @apiParam {string} platform 平台
    @apiParam {string} version 版本
    @apiParam {string} serial 序列号
    @apiParam {string} resolution 来源
    @apiParamExample {json} Request-Example:
    {
        "use_type": 2,
        "manufacturer": "manufacturer",
        "model": "model",
        "platform": "Android",
        "version": "8.0.0",
        "serial": "388ccc30",
        "resolution": "1920x720"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    use_type, manufacturer, model, platform, version, serial, resolution, uuid = parse_json_form('tc_devices')
    code, data = TcDevicesBusiness.devices_info(use_type, manufacturer, model, platform, version, serial, resolution,
                                                uuid)
    return json_detail_render(code, data)


@tcdevices.route('/getdevices', methods=['GET'])
# @cache.cached(timeout=TCDEVICE_TIMEOUT)
def get_tcdevices_handler():
    """
    @api {get} /v1/tcdevices/getdevices 云真机列表
    @apiName GetDevices
    @apiGroup 云真机
    @apiDescription 云真机列表
    @apiParamExample {json} Request-Example:
    无
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "abi":"arm64-v8a",
                "airplaneMode":false,
                "battery":{
                    "health":"good",
                    "level":100,
                    "scale":100,
                    "source":"ac",
                    "status":"full",
                    "temp":32,
                    "voltage":4.405
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
                    "url":"ws://stf.ywopt.com:7420",
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
                    "subtype":"",
                    "type":"WIFI"
                },
                "nickname":"",
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
                "pic":"http://ctsssource.oss-cn-shanghai.aliyuncs.com/devices_pic/VIVO-X9.png",
                "platform":"Android",
                "presenceChangedAt":"2019-07-08T07:07:58.290Z",
                "present":false,
                "product":"rolex",
                "provider":{
                    "channel":"UMnuDV5CSVWEd+YnIg/EDw==",
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
                "statusChangedAt":"2019-07-02T04:47:58.895Z",
                "times":0,
                "usage":null,
                "usageChangedAt":"2019-07-05T06:54:52.613Z",
                "use_time":"0",
                "using":false,
                "version":"6.0.1"
            }
        ],
        "message":"ok"
    }    """
    data = TcDevicesBusiness.get_devices()
    return json_detail_render(0, data)


@tcdevices.route('/gettoken', methods=['GET'])
def get_token_handler():
    """
    @api {get} /v1/tcdevices/gettoken 获取token
    @apiName GetToken
    @apiGroup 云真机
    @apiDescription 获取token
    @apiParam {string} name 名字
    @apiParamExample {json} Request-Example:
    ?name=wangjie
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":{
        "success":true,
        "token":"eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IndhbmdqaWVAMTI2LmNvbSIsIm5hbWUiOiJ3YW5namllIn0.m4Wz4WRhuYXs3DJbeLuXsuDjnQ4I8Q6R-pfCPl1ycHU"
    },
    "message":"ok"
    }
    """
    data = TcDevicesBusiness.stf_token()
    return json_detail_render(0, data)


@tcdevices.route('/disconnect', methods=['POST'])
@validation('POST:disconnect_devices')
def disconnect_devices_handler():
    """
    @api {post} /v1/tcdevices/disconnect 断开设备
    @apiName DisconnectDevices
    @apiGroup 云真机
    @apiDescription 断开设备
    @apiParam {int} userid 发送者
    @apiParam {string} serial Android设备序列号
    @apiParamExample {json} Request-Example:
    {
        "userid": 2,
        "serial": "Y2J5T17410004213"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    userid, serial = parse_json_form('disconnect_devices')
    data = TcDevicesBusiness.disconnect_devices(serial)
    return json_detail_render(0, data)


@tcdevices.route('/usedetail', methods=['GET'])
def get_usedetail_handler():
    """
    @api {get} /v1/tcdevices/usedetail 云真机设备使用详情
    @apiName DevicesDetail
    @apiGroup 云真机
    @apiDescription 云真机设备使用详情
    @apiParamExample {json} Request-Example:
    无
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "comment":"HUAWEI Che1-CL10",
                "id":1,
                "serial":"b43052ac3437",
                "times":169,
                "use_time":"863"
            }
        ],
        "message":"ok"
    }
    """
    data = TcDevicesBusiness.query_all_json()
    return json_detail_render(0, data)


@tcdevices.route('/usedetail/user', methods=['GET'])
def get_user_usedetail_handler():
    """
    @api {get} /v1/tcdevices/usedetail/user 云真机个人使用详情
    @apiName UserDetail
    @apiGroup 云真机
    @apiDescription 云真机个人使用详情
    @apiParam {string} userid 用户ID
    @apiParamExample {json} Request-Example:
    ?userid=1
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[
        {
            "creation_time":"2019-07-26 11:15:57",
            "id":1148,
            "manufacturer":"HUAWEI",
            "model":"VKY-AL00",
            "platform":"Android",
            "resolution":"2560x1440",
            "serial":"Y2J5T17410004213",
            "use_time":"140",
            "user_id":17,
            "user_name":"秦捷",
            "version":"7.0"
        }
    ],
    "message":"ok"
    }
    """
    data = TcDevicesBusiness.query_user_all_json()
    return json_detail_render(0, data)


@tcdevices.route('/dashboard', methods=['GET'])
def get_dashboard_usedetail_handler():
    """
    @api {get} /v1/tcdevices/dashboard 云真机使用报表
    @apiName Dashboard
    @apiGroup 云真机
    @apiDescription 云真机使用报表
    @apiParam {string} start_time 开始时间
    @apiParam {string} end_time 结束时间
    @apiParamExample {json} Request-Example:
    ?start_time=2019-07-26&end_time=2019-07-26
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[
        {
            "devices_times":[
                {
                    "date":"2019-07-26",
                    "times":1
                }
            ],
            "devices_use_time":[
                {
                    "date":"2019-07-26",
                    "use_time":140
                }
            ]
        }
    ],
    "message":"ok"
    }
    """
    data = TcDevicesBusiness.query_dashboard()
    return json_detail_render(0, data)
