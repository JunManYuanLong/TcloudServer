from flask import Blueprint, request, current_app

from apps.autotest.business.monkey import (
    MonkeyBusiness, MonkeyDeviceStatusBusiness, MonkeyErrorLogBusiness,
    MonkeyPackageBusiness, MonkeyReportBusiness, MonkeyDeviceUsingBusiness,
)
from apps.autotest.extentions import parse_list_args2, parse_list_args, validation, parse_json_form
from library.api.exceptions import FieldMissingException
from library.api.render import json_list_render, json_detail_render
from library.trpc import Trpc

monkey = Blueprint('monkey', __name__)

tool_trpc = Trpc('extention')


@monkey.route('/', methods=['GET'])
def monkey_index_handler():
    limit, offset = parse_list_args()

    monkey_id = request.args.get('monkey_id')
    test_type = request.args.get('test_type', 1)

    if monkey_id:
        data = MonkeyBusiness.query_all_json()
        return json_list_render(0, data, limit, offset)

    data = MonkeyBusiness.query_all_json(limit, offset, test_type=test_type)
    return {
        "code": 0,
        "data": data
    }


# 包含了所有数据（monkey和device）
@monkey.route('/all', methods=['GET'])
def monkey_all_handler():
    """
    @api {get} /v1/monkey/all 查询 Monkey 测试列表
    @apiName GetMonkeyAll
    @apiGroup 自动化测试
    @apiDescription 查询 所有的 monkey 测试信息
    @apiParam {int} [page_size] 分页-单页数目
    @apiParam {int} [page_index] 分页-页数
    @apiParam {int} [user_id] 用户 ID，获取当前用户 ID 的 monkey 测试信息
    @apiParam {int} [id] Monkey ID，根据 ID 获取 monkey 信息
    @apiParam {int} [test_type] 测试类型 1：monkey ，2：performance
    @apiParamExample {json} Request-Example:
    {
       "page_index": 1,
       "page_size": 10,
       "user_id": 1,
       "test_type": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "actual_run_time": "",
                "app_default_activity": "com.mengtuiapp.mall.SplashActivity",
                "app_id": 86,
                "app_install_required": 1,
                "app_name": "萌推",
                "app_oss_url": "http://tcloud-static.ywopt.com/static/00c43b89-f68d-4348-940d-f4dc36979f47.apk",
                "app_package_name": "com.mengtuiapp.mall",
                "app_picture": "iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAABCFBMVEX/AEj/6YT/9fj/7PH/9/n/8/b/6O",
                "app_size": "14.43",
                "app_version": "2.4.7",
                "begin_time": "2019-07-24 11:40:42",
                "cancel_status": 1,
                "creation_time": "2019-07-24 11:40:42",
                "download_app_status": 1,
                "end_time": "Wed, 24 Jul 2019 13:44:15 GMT",
                "id": 111,
                "jenkins_url": "http://ci.automancloud.com/job/monkey_autotest/325/",
                "login_password": "",
                "login_required": 0,
                "login_username": "",
                "mobile_ids": "Y2J5T17410004213",
                "monkey_device_status": [
                    {
                        "activity_all": "[]",
                        "activity_count": 0,
                        "activity_tested": "[]",
                        "activity_tested_count": 0,
                        "anr_count": 3,
                        "begin_time": "2019-07-24 11:40:54",
                        "cancel_status": 1,
                        "crash_count": 0,
                        "current_stage": "通过",
                        "device_connect_status": 1,
                        "end_time": "2019-07-24 13:41:51",
                        "exception_count": 0,
                        "exception_run_time": 0,
                        "id": 178,
                        "login_app_status": 1,
                        "mobile_id": 43,
                        "mobile_model": "HUAWEI VKY-AL00",
                        "mobile_resolution": "2560 x 1440",
                        "mobile_serial": "Y2J5T17410004213",
                        "mobile_use_times": 16,
                        "mobile_version": "7.0",
                        "monkey_id": 111,
                        "process": 100,
                        "run_time": 120,
                        "running_error_reason": "",
                        "running_status": 1,
                        "screen_lock_status": 1,
                        "setup_install_app_status": 1,
                        "setup_uninstall_app_status": 1,
                        "start_app_status": 1,
                        "teardown_uninstall_app_status": 1
                    }
                ],
                "package_name": "com.mengtuiapp.mall",
                "parameters": "{'system_device': 0, 'app': {'user_id': 93, 'app_id': 86}, 'login': {
                                'required': 0, 'username': '', 'password': ''}}",
                "process": 100,
                "report_url": "",
                "run_time": 0,
                "status": 0,
                "system_device": 0,
                "type_id": 1,
                "user_id": 93,
                "user_nickname": "孟伟"
            }
        ],
        "message": "ok",
        "page_index": 1,
        "page_size": 10,
        "total": 66
    }
    """
    page_size, page_index = parse_list_args2()
    page_size = page_size or 10
    page_index = page_index or 1

    user_id = request.args.get('user_id')
    id = request.args.get('id')
    test_type = request.args.get('test_type', 1)

    monkeys, count = MonkeyBusiness.get_all_monkeys(id, user_id, page_size, page_index, test_type=test_type)

    return {
        "code": 0,
        "data": monkeys,
        "page_size": page_size,
        "page_index": page_index,
        "total": count
    }


# 包含了 device status 数据
@monkey.route('/devicestatus', methods=['GET'])
def monkey_device_status_all_handler():
    limit, offset = parse_list_args()

    monkey_id = request.args.get('monkey_id')

    if monkey_id:
        data = MonkeyDeviceStatusBusiness.query_json_by_monkey_id(monkey_id)
        return json_list_render(0, data, limit, offset)

    monkeys = MonkeyDeviceStatusBusiness.query_all_json(limit, offset)
    return {
        "code": 0,
        "data": monkeys
    }


# 更新 monkey 状态
@monkey.route('/<int:id>', methods=['POST'])
@validation('POST:monkey_update')
def monkey_update_handler(id):
    """
    @api {post} /v1/monkey/:id 更新 Monkey 状态
    @apiName UpdateMonkey
    @apiGroup 自动化测试
    @apiDescription 更新 Monkey 运行状态
    @apiParam {string} [end_time] Monkey 结束时间
    @apiParam {int} [process Monkey] 运行的进度 1-100
    @apiParam {int} [jenkins_url] 当前测试的 Jenkins url
    @apiParam {int} [status] 测试的状态
    @apiParam {int} [app_version] 测试的实际的 app 版本号
    @apiParam {int} [begin_time] 测试开始时间
    @apiParam {int} [report_url] 测试报告地址
    @apiParam {int} [run_time] 测试运行时间
    @apiParam {int} [actual_run_time] 测试实际运行时间
    @apiParam {int} [download_app_status] 下载 app 的结果，0：未开始，1：成功，2：失败
    @apiParamExample {json} Request-Example:
    {
        "download_app_status": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    (end_time, process, jenkins_url, status, app_version, begin_time, report_url, run_time, actual_run_time,
     download_app_status) = parse_json_form('monkey_update')
    ret, msg = MonkeyBusiness.update(id=id, end_time=end_time, process=process, jenkins_url=jenkins_url, status=status,
                                     app_version=app_version, begin_time=begin_time, report_url=report_url,
                                     run_time=run_time, actual_run_time=actual_run_time,
                                     download_app_status=download_app_status)
    return {
        "code": ret,
        "message": msg
    }


# 触发 monkey
@monkey.route('/start', methods=['POST'])
@validation('POST:monkey_start')
def monkey_start_handler():
    """
    @api {post} /v1/monkey/start 启动 Monkey 测试
    @apiName GetMonkeyDeviceAll
    @apiGroup 自动化测试
    @apiDescription 启动 Monkey 测试
    @apiParam {int} user_id required 用户 ID，启动用户的 ID
    @apiParam {list} mobile_infos 测试使用的设备相关的信息
    @apiParam {int} type_id Monkey 测试类型，1：mix，2：dfs，3：可配置模式
    @apiParam {int} run_time 运行时间，单位 min
    @apiParam {int} system_device 是否是系统设备，1：是，2：否
    @apiParam {int} login_required 是否需要登录，1：是，2：否
    @apiParam {string} login_username 登录用户名信息
    @apiParam {string} login_password 登录用户名密码
    @apiParam {int} app_id 要测试的app id
    @apiParam {int} app_install_required 是否需要安装 app，1：是，2：否
    @apiParam {int} test_type 测试类型，默认 1：monkey，性能测试需要传 2
    @apiParam {int} test_config 测试配置文件 默认 qjp_ui/config.json
    @apiParamExample {json} Request-Example:
    ?test_type=2
    {
        "user_id": 1,
        "mobile_infos": [
            {
                "mobile_id": "ZTEC880U",
                "mobile_version": "android 7.0",
                "mobile_model": "os105",
                "mobile_resolution": "1080*1080"
            }
        ],
        "system_device": 0,
        "login_required": 0,
        "login_username": "",
        "login_password": "",
        "type_id": 1,
        "run_time": 1,
        "app_id": 1,
        "app_install_required": 1,
        "test_config": "qjp_ui/config.json"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    (user_id, mobile_infos, type_id, run_time, system_device, login_required, login_username, login_password, app_id,
     app_install_required, test_config) = parse_json_form('monkey_start')
    test_type = request.args.get('test_type', 1)
    # test_config = request.args.get('test_config', '')
    parameters = {
        "system_device": system_device,
        "app": {
            "user_id": user_id,
            "app_id": app_id
        },
        "login": {
            "required": login_required,
            "username": login_username,
            "password": login_password,
        }
    }
    ret, msg = MonkeyBusiness.start_test(user_id, mobile_infos, type_id, run_time, system_device, login_required,
                                           login_username, login_password, app_id, parameters, app_install_required,
                                           test_type=test_type, test_config=test_config)
    return {
        "code": ret,
        "message": msg
    }


# 上传 error_log
@monkey.route('/errorlog', methods=['POST'])
@validation('POST:monkey_error_log_create')
def monkey_error_log_create_handler():
    """
    @api {post} /v1/monkey/errorlog 上传 错误日志
    @apiName UpdateErrorLog
    @apiGroup 自动化测试
    @apiDescription 上传 错误日志
    @apiParam {int} monkey_id Monkey ID
    @apiParam {string} error_type 错误类型
    @apiParam {string} error_message 错误信息
    @apiParam {int} task_id 单个设备的测试 ID
    @apiParam {int} error_count 错误数量
    @apiParamExample {json} Request-Example:
    {
        "monkey_id":1,
        "error_type": "Exception",
        "error_message": "Java.Lang.Iellagle",
        "task_id": 1,
        "error_count": 10
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    monkey_id, task_id, error_type, error_message, error_count = parse_json_form('monkey_error_log_create')
    ret, msg = MonkeyErrorLogBusiness.create(monkey_id=monkey_id, task_id=task_id, error_type=error_type,
                                             error_message=error_message, error_count=error_count)
    return {
        "code": ret,
        "message": msg
    }


# 获取 error_log
@monkey.route('/errorlog', methods=['GET'])
def monkey_error_log_index_handler():
    """
    @api {get} /v1/monkey/errorlog 查询 Monkey error log 列表
    @apiName GetMonkeyErrorLog
    @apiGroup 自动化测试
    @apiDescription 查询 Monkey 测试的错误日志
    @apiParam {int} [page_size] 分页-单页大小
    @apiParam {int} [page_index] 分页-页数
    @apiParam {int} [monkey_id] Monkey 的 ID
    @apiParam {int} [task_id] 单个设备的测试 ID
    @apiParamExample {json} Request-Example:
    {
        "page_size": 10,
        "page_index": 1,
        "monkey_id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "error_count": 1,
                "error_message": "['oom:\\n', '//OOM: com.mengtuiapp.mall (pid 28586)(dump time: 2019-07-03 12:13:56']",
                "error_type": "OOM",
                "id": 5,
                "monkey_id": 29
            }
        ],
        "message": "ok"
    }
    """
    page_size, page_index = parse_list_args2()
    page_size = page_size or 10
    page_index = page_index or 1

    monkey_id = request.args.get('monkey_id')
    task_id = request.args.get('task_id')

    if monkey_id:
        current_app.logger.info('get error log <monkey_id> : {}'.format(monkey_id))
        error_logs = MonkeyErrorLogBusiness.query_json_by_monkey_id(monkey_id, page_size, page_index)
        count = MonkeyErrorLogBusiness.query_count_by_monkey_id(monkey_id)
    elif task_id:
        current_app.logger.info('get error log <task_id> : {}'.format(task_id))
        error_logs = MonkeyErrorLogBusiness.query_json_by_task_id(task_id, page_size, page_index)
        count = MonkeyErrorLogBusiness.query_count_by_task_id(task_id)
    else:
        raise FieldMissingException('no monkey id or task id found!')
    response = {
        "data": error_logs,
        "page_size": page_size,
        "page_index": page_index,
        "total": count
    }
    return response


# 更新 device_status
@monkey.route('/devicestatus/<int:id>', methods=['POST'])
@validation('POST:monkey_device_status_update')
def monkey_device_status_update_handler(id):
    current_app.logger.info(id)
    if id is None:
        return json_detail_render(101, [], "无效的id")
    (process, activity_count, activity_tested_count,
     activity_all, activity_tested, anr_count, crash_count, crash_rate, exception_count, exception_run_time,
     setup_install_app_status, setup_uninstall_app_status, start_app_status, begin_time, login_app_status,
     running_status, teardown_uninstall_app_status, end_time, run_time, device_connect_status, screen_lock_status,
     current_stage, running_error_reason, mobile_resolution) = parse_json_form('monkey_device_status_update')
    ret, msg = MonkeyDeviceStatusBusiness.update(id=id, process=process, activity_count=activity_count,
                                                 activity_tested_count=activity_tested_count, activity_all=activity_all,
                                                 activity_tested=activity_tested, anr_count=anr_count,
                                                 crash_count=crash_count, exception_count=exception_count,
                                                 exception_run_time=exception_run_time,
                                                 setup_install_app_status=setup_install_app_status,
                                                 begin_time=begin_time, start_app_status=start_app_status,
                                                 setup_uninstall_app_status=setup_uninstall_app_status,
                                                 login_app_status=login_app_status, end_time=end_time,
                                                 running_status=running_status, run_time=run_time,
                                                 teardown_uninstall_app_status=teardown_uninstall_app_status,
                                                 device_connect_status=device_connect_status,
                                                 screen_lock_status=screen_lock_status, current_stage=current_stage,
                                                 running_error_reason=running_error_reason,
                                                 mobile_resolution=mobile_resolution)
    response = {
        "code": ret,
        "data": [],
        "message": msg
    }
    return response


# 获取上传的 apk 可以根据 id，user_id 分别获取
@monkey.route('/package', methods=['GET'])
def monkey_package_index_handler():
    """
    @api {get} /v1/monkey/package 查询 Monkey package 列表
    @apiName GetMonkeyPackage
    @apiGroup 自动化测试
    @apiDescription 查询 Monkey 测试的上传的包列表
    @apiParam {int} [page_size] 分页-单页大小
    @apiParam {int} [page_index] 分页-页数
    @apiParam {int} [id] Monkey 的 ID
    @apiParam {int} [user_id] 单个设备的测试 ID
    @apiParam {int} test_type 测试类型，默认为 1：monkey，性能测试需要传 2
    @apiParamExample {json} Request-Example:
    {
        "page_size": 10,
        "page_index": 1,
        "monkey_id": 1,
        "test_type": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "default_activity": "com.mengtuiapp.mall.SplashActivity",
                "id": 3,
                "name": "萌推",
                "oss_url": "http://js.xiazaicc.com/apk3/mengtuiv2.4.7_downcc.com.apk",
                "package_name": "com.mengtuiapp.mall",
                "picture": "iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAMAAAApWqozAAABCFBMVEX/AEj/6YT/9fj/7PH/9/n/8/b/6O",
                "size": "",
                "upload_time": "Tue, 09 Jul 2019 17:53:31 GMT",
                "user_id": 1,
                "user_nickname": "王金龙",
                "version": "2.4.7"
            }
        ],
        "message": "ok"
    }
    """
    page_size, page_index = parse_list_args2()
    page_size = page_size or 10
    page_index = page_index or 1

    id = request.args.get('id')
    user_id = request.args.get('user_id')
    test_type = request.args.get('test_type', 1)

    if id:
        data = MonkeyPackageBusiness.query_json_by_id(id)
        return json_detail_render(0, data)
    all, count = MonkeyPackageBusiness.get_monkey_packages_by_user_id(user_id, page_size, page_index, test_type)
    response = dict(
        code=0,
        data=all,
        page_size=page_size,
        page_index=page_index,
        total=count
    )
    return response


# 上传 apk
@monkey.route('/package', methods=['POST'])
@validation('POST:monkey_package_create')
def monkey_package_create_handler():
    """
    @api {post} /v1/monkey/package 上传 Monkey Package
    @apiName UploadMonkeyPackage
    @apiGroup 自动化测试
    @apiDescription 上传 Monkey 测试包
    @apiParam {int} user_id 上传用户 ID
    @apiParam {string} oss_url 存放 apk 的 oss 路径
    @apiParam {int} test_type 测试类型，1：monkey，2：performance
    @apiParamExample {json} Request-Example:
    {
        "user_id": 1,
        "oss_url": "http://js.xiazaicc.com/apk3/mengtuiv2.4.7_downcc.com.apk"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    (name, package_name, oss_url, picture, version, default_activity,
     user_id, test_type) = parse_json_form('monkey_package_create')
    apk_info = tool_trpc.requests('post', '/tool/apk/analysis', body={"apk_download_url": oss_url})

    package_name = apk_info.get('package_name')
    default_activity = apk_info.get('default_activity')
    version = apk_info.get('version_name')
    picture = apk_info.get('icon')
    name = apk_info.get('label')
    size = apk_info.get('size') or ''

    ret, msg = MonkeyPackageBusiness.create(name=name, package_name=package_name, oss_url=oss_url, picture=picture,
                                            version=version, default_activity=default_activity, user_id=user_id,
                                            size=size, test_type=test_type)
    response = dict(
        code=ret,
        message=msg
    )
    return response


# 删除 apk
@monkey.route('/package/<int:id>', methods=['DELETE'])
def monkey_package_delete_handler(id):
    """
    @api {delete} /v1/monkey/package/:id 删除 Monkey 测试包
    @apiName DeleteMonkeyPackage
    @apiGroup 自动化测试
    @apiDescription 删除 Monkey 测试包
    @apiParam {int} id 包的 ID.
    @apiParamExample {json} Request-Example:
    {

    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    ret, msg = MonkeyPackageBusiness.delete(id)
    return dict(
        code=ret,
        message=msg
    )


# 上传 report 信息
@monkey.route('/report', methods=['POST'])
@validation('POST:monkey_report_create')
def monkey_report_create_handler():
    """
    @api {post} /v1/monkey/report 上传 Monkey 测试报告
    @apiName UploadMonkeyReport
    @apiGroup 自动化测试
    @apiDescription 上传 Monkey 测试报告
    @apiParam {int} monkey_id 上传用户 ID
    @apiParam {int} report_type 存放 apk 的 oss 路径
    @apiParam {int} task_id 上传用户 ID
    @apiParam {string} report_url 存放 apk 的 oss 路径
    @apiParamExample {json} Request-Example:
    {
        "monkey_id": 1,
        "report_type": 1,
        "report_url": "http://ctsssource.oss-cn-shanghai.aliyuncs.com/monkey/2019-07-12//index.html",
        "task_id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    monkey_id, task_id, report_type, report_url = parse_json_form('monkey_report_create')
    ret, msg = MonkeyReportBusiness.create(monkey_id=monkey_id, task_id=task_id, report_type=report_type,
                                           report_url=report_url)
    return dict(
        code=ret,
        message=msg
    )


# 更新 report 信息
@monkey.route('/report/<int:id>', methods=['POST'])
@validation('POST:monkey_report_update')
def monkey_report_update_handler(id):
    """
    @api {post} /v1/monkey/report/:id 更新 Monkey 测试报告
    @apiName UpdateMonkeyReport
    @apiGroup 自动化测试
    @apiDescription 更新 Monkey 测试报告
    @apiParam {int} [monkey_id] 上传用户 ID
    @apiParam {int} [report_type] 存放 apk 的 oss 路径
    @apiParam {int} [task_id] 上传用户 ID
    @apiParam {string} [report_url] 存放 apk 的 oss 路径
    @apiParamExample {json} Request-Example:
    {
        "monkey_id": 1,
        "report_type": 1,
        "report_url": "http://ctsssource.oss-cn-shanghai.aliyuncs.com/monkey/2019-07-12/None/index.html",
        "task_id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    monkey_id, task_id, report_type, report_url = parse_json_form('monkey_report_update')
    ret, msg = MonkeyReportBusiness.update(id, monkey_id=monkey_id, task_id=task_id, report_type=report_type,
                                           report_url=report_url)
    return dict(
        code=ret,
        message=msg
    )


# 获取 report
@monkey.route('/report', methods=['GET'])
def monkey_report_index_handler():
    """
    @api {get} /v1/monkey/report 查询 Monkey 测试报告列表
    @apiName GetMonkeyReport
    @apiGroup 自动化测试
    @apiDescription 查询 Monkey 测试报告列表
    @apiParam {int} [page_size] 分页-单页大小
    @apiParam {int} [page_index] 分页-页数
    @apiParam {int} [monkey_id] Monkey 的 ID
    @apiParam {int} [task_id] 单个设备的测试 ID
    @apiParamExample {json} Request-Example:
    {
        "page_size": 10,
        "page_index": 1,
        "monkey_id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
             {
                "id": 14,
                "mobile_model": "os105",
                "monkey_id": 115,
                "report_type": 1,
                "report_url": "http://ctsssource.oss-cn-shanghai.aliyuncs.com/monkey/2019-07-15/182/index.html",
                "task_id": 143
            }
        ],
        "message": "ok"
    }
    """
    page_size, page_index = parse_list_args2()
    page_size = page_size or 10
    page_index = page_index or 1

    monkey_id = request.args.get('monkey_id')
    task_id = request.args.get('task_id')
    data, count = MonkeyReportBusiness.get_report(monkey_id, task_id, page_size, page_index)
    response = dict(
        code=0,
        data=data,
        page_size=page_size,
        page_index=page_index,
        total=count
    )
    return response


# cancel monkey
@monkey.route('/cancel', methods=['POST'])
def monkey_cancel_handler():
    """
    @api {post} /v1/monkey/cancel 中断 monkey 测试
    @apiName CancelMonkey
    @apiGroup 自动化测试
    @apiDescription 中断 monkey
    @apiParam {int} [monkey_id] Monkey ID
    @apiParam {int} [task_id] 具体设备测试项目的 ID
    @apiParamExample {json} Request-Example:
    {
        "monkey_id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    monkey_id, task_id = parse_json_form('monkey_cancel')

    ret, msg = MonkeyBusiness.cancel_monkey(monkey_id, task_id)
    return dict(
        code=ret,
        message=msg
    )


# get monkey cancel status
@monkey.route('/cancel', methods=['GET'])
def monkey_cancel_status_handler():
    """
    @api {get} /v1/monkey/cancel 查询 monkey 测试中断状态
    @apiName GetCancelMonkeyStatus
    @apiGroup 自动化测试
    @apiDescription 查询 monkey 测试中断状态
    @apiParam {int} [monkey_id] Monkey ID
    @apiParam {int} [task_id] 具体设备测试项目的 ID
    @apiParamExample {json} Request-Example:
    {
        "task_id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": {
            "cancel_status": 0,
            "id": 56
        },
        "message": "ok"
    }
    """
    task_id = request.args.get('task_id')
    if task_id:
        data = MonkeyDeviceStatusBusiness.query_cancel_status_by_id(task_id)
        return dict(
            data=data
        )
    else:
        raise FieldMissingException('task_id is required')


# using device with serial
@monkey.route('/device/using', methods=['POST'])
@validation('POST:monkey_device_using')
def monkey_device_using_handler():
    """
    @api {post} /v1/monkey/device/using 使用 设备
    @apiName UsingMonkeyDevice
    @apiGroup 自动化测试
    @apiDescription 更新正在使用设备使用状态为使用中
    @apiParam {string} [serial] 设备序列号
    @apiParamExample {json} Request-Example:
    {
        "serial": "7189ac55"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    serial = parse_json_form('monkey_device_using')
    current_app.logger.info(serial)
    if serial:
        ret, msg = MonkeyDeviceUsingBusiness.using_device(serial)
        return dict(
            code=ret,
            message=msg
        )
    else:
        raise FieldMissingException('serial is required')


# release device with serial
@monkey.route('/device/release', methods=['POST'])
@validation('POST:monkey_device_release')
def monkey_device_release():
    """
    @api {post} /v1/monkey/device/release 释放 设备
    @apiName ReleaseMonkeyDevice
    @apiGroup 自动化测试
    @apiDescription 更新正在使用设备使用状态为空闲
    @apiParam {string} [serial] 设备序列号
    @apiParamExample {json} Request-Example:
    {
     "serial": "7189ac55"
    }
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
     "code": 0,
     "data": [],
     "message": "ok"
    }
    """
    serial = parse_json_form('monkey_device_using')
    if serial:
        ret, msg = MonkeyDeviceUsingBusiness.release_device(serial)
        return dict(
            code=ret,
            message=msg
        )
    else:
        raise FieldMissingException('serial is required')


# 获取所有性能测试名称
@monkey.route('/name', methods=['GET'])
def monkey_test_name_get_handler():
    """
    @api {get} /v1/monkey/name 根据 测试类型 获取测试列表
    @apiName GetAutotestListByTestType
    @apiGroup 自动化测试
    @apiDescription 根据 测试类型 获取测试列表
    @apiParam {int} [test_type] 测试类型
    @apiParamExample {json} Request-Example:
    ?test_type=2
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [
        {
          "id": 163,
          "name": "163-2019-09-19 15:16:54-xxxx-1.5.5.1"
        },
      ],
      "message": "ok"
    }
    """
    test_type = request.args.get('test_type', 1)
    response = {
        "code": 0,
        "data": MonkeyBusiness.get_all_name(test_type)
    }
    return response


# 根据 id 获取信息
@monkey.route('/test', methods=['GET'])
def performance_test_get_by_performance_id_handler():
    """
    @api {get} /v1/monkey/test 根据 monkey id 和 测试场景 获取场景的设备测试信息列表
    @apiName GetAutotestListByMonkeyIdAndTestType
    @apiGroup 自动化测试
    @apiDescription 根据 monkey id 和 测试场景 获取场景的设备测试信息列表
    @apiParam {int} monkey_id 测试 id
    @apiParam {string} run_type 测试场景
    @apiParamExample {json} Request-Example:
    ?performance_id=260
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [
        {
          "ZTEC880U": [
            {
              "cpu_average": 0.0,
              "cpu_top": 0.0,
              "creation_time": "2019-09-19 15:41:46",
              "heap_alloc_average": 0.0,
              "heap_alloc_top": 0.0,
              "heap_size_average": 0.0,
              "heap_size_top": 0.0,
              "id": 12,
              "modified_time": "2019-09-19 15:41:45",
              "performance_id": 260,
              "rss_top": 0.0,
              "run_time": 1,
              "run_type": "qjp"
            }
          ]
        }
      ],
      "message": "ok"
    }
    """
    monkey_id = request.args.get('monkey_id')
    run_type = request.args.get('run_type')
    if not monkey_id:
        raise FieldMissingException('monkey_id is required')

    if not run_type:
        raise FieldMissingException('run_type is required')

    response = {
        "code": 0,
        "data": MonkeyBusiness.get_performance_by_monkey_id_and_type(monkey_id, run_type)
    }
    return response
