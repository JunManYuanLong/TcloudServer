from flask import Blueprint, current_app, request
from apps.autotest.business.performance import PerformanceTestLogBusiness, PerformanceTestBusiness
from apps.autotest.extentions import validation, parse_json_form
from library.api.exceptions import FieldMissingException
from library.api.render import json_detail_render
from library.trpc import Trpc

performance = Blueprint('performance', __name__)

tool_trpc = Trpc('extention')

#
# # 更新 device_status
# @performance.route('/devicestatus/<int:id>', methods=['POST'])
# @validation('POST:performance_device_status_update')
# def performance_device_status_update_handler(id):
#     current_app.logger.info(id)
#     if id is None:
#         return json_detail_render(101, [], "无效的id")
#     (process, activity_count, activity_tested_count,
#      activity_all, activity_tested, anr_count, crash_count, crash_rate, exception_count, exception_run_time,
#      setup_install_app_status, setup_uninstall_app_status, start_app_status, begin_time, login_app_status,
#      running_status, teardown_uninstall_app_status, end_time, run_time, device_connect_status, screen_lock_status,
#      current_stage, running_error_reason, mobile_resolution) = parse_json_form('performance_device_status_update')
#     ret, msg = PerformanceDeviceStatusBusiness.update(id=id, process=process,
#                                                  setup_install_app_status=setup_install_app_status,
#                                                  begin_time=begin_time, start_app_status=start_app_status,
#                                                  setup_uninstall_app_status=setup_uninstall_app_status,
#                                                  login_app_status=login_app_status, end_time=end_time,
#                                                  running_status=running_status, run_time=run_time,
#                                                  teardown_uninstall_app_status=teardown_uninstall_app_status,
#                                                  device_connect_status=device_connect_status,
#                                                  screen_lock_status=screen_lock_status, current_stage=current_stage,
#                                                  running_error_reason=running_error_reason,
#                                                  mobile_resolution=mobile_resolution)
#     response = {
#         "code": ret,
#         "data": [],
#         "message": msg
#     }
#     return response


# 上传实时 log
@performance.route('/realtime/<int:id>', methods=['POST'])
@validation('POST:performance_log_create')
def performance_log_create_handler(id):
    # current_app.logger.error(id)
    if id is None:
        return json_detail_render(101, [], "无效的id")
    cpu, rss, heap_size, heap_alloc = parse_json_form('performance_log_create')

    ret, msg = PerformanceTestLogBusiness.create(id, cpu, rss, heap_size, heap_alloc)
    response = {
        "code": ret,
        "message": msg,
        "data": []
    }
    return response


# 获取实时 log
@performance.route('/realtime/<int:id>', methods=['GET'])
def performance_log_get_handler(id):
    """
    @api {get} /v1/performance/realtime/{int:id} 获取设备实时信息
    @apiName GetRealtimeLog
    @apiGroup 自动化测试
    @apiDescription 获取设备实时实时信息
    @apiParam {int} [id] 性能测试具体场景的 id
    @apiParamExample {json} Request-Example:
    ?id=199
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
      "code": 0,
      "data": [
        {
          "cpu": 1.0,
          "creation_time": "2019-09-18 14:52:04",
          "heap_alloc": 1.0,
          "heap_size": 1.0,
          "id": 1,
          "performance_test_id": 1,
          "rss": 1.0
        }
      ],
      "message": "ok"
    }
    """
    current_app.logger.info(id)
    if id is None:
        return json_detail_render(101, [], "无效的id")
    ret= PerformanceTestLogBusiness.query_json_by_performance_test_id(id)
    response = {
        "code": 0,
        "data": ret
    }
    return response


# 创建场景测试
@performance.route('/test', methods=['POST'])
@validation('POST:performance_test_create')
def performance_test_create_handler():
    performance_id, run_type, run_time = parse_json_form('performance_test_create')
    performance_test_id = PerformanceTestBusiness.create(performance_id, run_type, run_time)
    response = {
        "code": 0,
        "data": [
            {
                "id": performance_test_id
            }
        ]
    }
    return response


# 更新测试场景测试信息
@performance.route('/test/calculate/<int:id>', methods=['GET'])
def performance_test_calculate_handler(id):
    if not id:
        raise FieldMissingException('id missing!')

    response = {
        "code": PerformanceTestBusiness.calculate_average(id),
        "data": []
    }
    return response

# 根据 设备 id 获取场景信息
@performance.route('/device', methods=['GET'])
def performance_name_by_device_get_handler():
    """
    @api {get} /v1/performance/device 根据 performance_id 获取场景列表
    @apiName GetPerformanceTestNameList
    @apiGroup 自动化测试
    @apiDescription 根据 performance_id 获取场景列表
    @apiParam {int} [performance_id] 性能测试 id
    @apiParamExample {json} Request-Example:
    ?performance_id=260
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
      "code": 0,
      "data": [
        {
          "id": 8,
          "name": "Wechat-01"
        },
        {
          "id": 9,
          "name": "Wechat-02"
        },
        {
          "id": 10,
          "name": "QQ-01"
        },
        {
          "id": 11,
          "name": "QQ-02"
        },
        {
          "id": 12,
          "name": "qjp"
        },
        {
          "id": 13,
          "name": "WPS"
        }
      ],
      "message": "ok"
    }
    """
    performance_id = request.args.get('performance_id')
    if not performance_id:
        raise FieldMissingException('performance_id is required')
    response = {
        "code": 0,
        "data": PerformanceTestBusiness.get_all_name(performance_id)
    }
    return response


# 根据 测试 id 获取场景信息
@performance.route('/name', methods=['GET'])
def performance_name_by_monkey_get_handler():
    """
    @api {get} /v1/performance/name 根据 测试ID 获取场景列表
    @apiName GetPerformanceTestNameListByMonkeyId
    @apiGroup 自动化测试
    @apiDescription 根据 测试ID 获取场景列表
    @apiParam {int} [performance_id] 性能测试 id
    @apiParamExample {json} Request-Example:
    ?performance_id=260
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
      "code": 0,
      "data": ["Wechat-01", "Wechat-02"],
      "message": "ok"
    }
    """
    performance_id = request.args.get('performance_id')
    if not performance_id:
        raise FieldMissingException('performance_id is required')
    response = {
        "code": 0,
        "data": PerformanceTestBusiness.get_all_name_by_monkey_id(performance_id)
    }
    return response

