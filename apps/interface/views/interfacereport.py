import json

from flask import Blueprint, request, jsonify, current_app

from apps.interface.business.interfacereport import InterfaceReportBusiness
from apps.interface.models.interfaceproject import InterfaceProject
from apps.interface.util.http_run import RunCase

interfacereport = Blueprint('interfacereport', __name__)


@interfacereport.route('/run', methods=['POST'])
def run_cases():
    """
    @api {post} /v1/interfacereport/run InterfaceReport_跑接口
    @apiName interfaceReportRun
    @apiGroup Interface
    @apiDescription 跑接口
    @apiParam {list} sceneIds  场景id
    @apiParam {string} projectName  项目名称
    @apiParam {bool} reportStatus  报告状态
    @apiParamExample {json} Request-Example:
    {
        "sceneIds": [38],
        "projectName": "mengtui",
        "reportStatus": true
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": {
            "data": {
                "details": [
                    {
                        "base_url": "",
                        "in_out": {
                            "in": {},
                            "out": {}
                        },
                        "name": "www",
                        "records": [
                            {
                                "attachment": "Traceback (most recent call last):\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/parser.py\", line 343, in get_mapping_variable\n    return variables_mapping[variable_name]\nKeyError: 'token'\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/api.py\", line 195, in test\n    test_runner.run_test(teststep_dict)\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/runner.py\", line 168, in run_test\n    parsed_request = self.init_config(teststep_dict, level=\"teststep\")\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/runner.py\", line 85, in init_config\n    parsed_request = self.context.get_parsed_request(request_config, level)\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/context.py\", line 121, in get_parsed_request\n    request_dict\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/context.py\", line 81, in eval_content\n    self.TESTCASE_SHARED_FUNCTIONS_MAPPING\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/parser.py\", line 506, in parse_data\n    parsed_value = parse_data(value, variables_mapping, functions_mapping)\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/parser.py\", line 506, in parse_data\n    parsed_value = parse_data(value, variables_mapping, functions_mapping)\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/parser.py\", line 522, in parse_data\n    content = parse_string_variables(content, variables_mapping)\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/parser.py\", line 445, in parse_string_variables\n    variable_value = get_mapping_variable(variable_name, variables_mapping)\n  File \"/home/super/.local/share/virtualenvs/tcloudservers-IY81mg_K/lib/python3.7/site-packages/httprunner/parser.py\", line 345, in get_mapping_variable\n    raise exceptions.VariableNotFound(\"{} is not found.\".format(variable_name))\nhttprunner.exceptions.VariableNotFound: token is not found.\n",
                                "meta_data": {
                                    "request": {
                                        "headers": {},
                                        "method": "N/A",
                                        "start_timestamp": null,
                                        "url": "N/A"
                                    },
                                    "response": {
                                        "content": null,
                                        "content_size": "N/A",
                                        "content_type": "",
                                        "elapsed_ms": "N/A",
                                        "encoding": null,
                                        "headers": {},
                                        "response_time_ms": "N/A",
                                        "status_code": "N/A"
                                    },
                                    "validators": []
                                },
                                "name": "登录1",
                                "status": "error"
                            }
                        ],
                        "stat": {
                            "errors": 1,
                            "expectedFailures": 0,
                            "failures": 0,
                            "skipped": 0,
                            "successes": 0,
                            "testsRun": 1,
                            "unexpectedSuccesses": 0
                        },
                        "success": false,
                        "time": {
                            "duration": 0.0036885738372802734,
                            "start_at": 1564556076.868078
                        }
                    }
                ],
                "platform": {
                    "httprunner_version": "1.5.13",
                    "platform": "Linux-3.10.0-862.14.4.el7.x86_64-x86_64-with-centos-7.5.1804-Core",
                    "python_version": "CPython 3.7.3"
                },
                "stat": {
                    "all_scene": 1,
                    "errors": "1 (100%)",
                    "errors_1": 1,
                    "expectedFailures": 0,
                    "failures": "0 (0%)",
                    "failures_1": 0,
                    "failures_scene": 1,
                    "failures_scene1": "1 (100%)",
                    "skipped": 0,
                    "successes": "0 (0%)",
                    "successes_1": 0,
                    "successes_scene": 0,
                    "successes_scene1": "0 (0%)",
                    "testsRun": 1,
                    "unexpectedSuccesses": 0
                },
                "success": false,
                "time": {
                    "duration": "0.00",
                    "start_at": "2019/07/31 14:54:36"
                }
            },
            "report_id": 64
        },
        "msg": "测试完成",
        "status": 1
    }
    """
    data = request.json
    case_ids = data.get('sceneIds')
    project_name = data.get('projectName')
    report_status = data.get('reportStatus')
    # jsondata = InterfaceReportBusiness.run_cases(case_ids,project_name,report_status)

    if not project_name:
        return jsonify({'msg': '请选择项目', 'status': 0})
    if not case_ids:
        return jsonify({'msg': '请选择用例', 'status': 0})

    project_id = InterfaceProject.query.filter_by(name=project_name,
                                                  status=InterfaceProject.ACTIVE).first().id
    try:
        d = RunCase(project_id)
        jump_res = d.run_case(d.get_case_test(case_ids))
    except Exception as e:
        current_app.logger.info("批量运行生成报告运行的错误信息:" + str(e))
        return jsonify({'msg': '函数文件或者参数配置错误，请重新检查完再运行', 'status': 0})

    if report_status:
        d.build_report(jump_res, case_ids)
    res = json.loads(jump_res)

    return jsonify({'msg': '测试完成', 'status': 1, 'data': {'report_id': d.new_report_id, 'data': res}})
    # return jsondata


@interfacereport.route('/list', methods=['POST'])
def get_report():
    """
    @api {post} /v1/interfacereport/list InterfaceReport_查看报告
    @apiName interfaceProList
    @apiGroup Interface
    @apiDescription 查看报告
    @apiParam {int} reportId  报告id
    @apiParam {string} state  报告状态
    @apiParamExample {json} Request-Example:
    {
        "reportId": 1,
        "state": "error"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "报告还未生成、或生成失败",
        "status": 0
    }
    """

    data = request.json
    report_id = data.get('reportId')
    state = data.get('state')
    jsondata = InterfaceReportBusiness.get_report(report_id, state)
    return jsondata


@interfacereport.route('/download', methods=['POST'])
def download_report():
    """
    @api {post} /v1/interfacereport/download InterfaceReport_报告下载
    @apiName interfaceReportDownload
    @apiGroup Interface
    @apiDescription 报告下载
    @apiParam {int} reportId 报告id
    @apiParam  {bool} dataOrReport 报告
    @apiParamExample {json} Request-Example:
    {
        "reportId": 1,
        "dataOrReport": true
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "报告还未生成、或生成失败",
        "status": 0
    }
    """

    data = request.json
    report_id = data.get('reportId')
    data_or_report = data.get('dataOrReport')

    jsondata = InterfaceReportBusiness.download_report(report_id, data_or_report)

    return jsondata


@interfacereport.route('/del', methods=['POST'])
def del_report():
    """
    @api {post} /v1/interfacereport/del InterfaceReport_删除报告
    @apiName interfaceReportDel
    @apiGroup Interface
    @apiDescription 删除报告
    @apiParam  {int} report_id报告id
    @apiParamExample {json} Request-Example:
    {
        "report_id": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "删除成功",
        "status": 1
    }
    """
    data = request.json
    report_id = data.get('report_id')
    jsondata = InterfaceReportBusiness.del_report(report_id)
    return jsondata


@interfacereport.route('/find', methods=['POST'])
def find_report():
    """
    @api {post} /v1/interfacereport/find InterfaceReport_查找报告
    @apiName interfaceReportFind
    @apiGroup Interface
    @apiDescription 查找报告
    @apiParam {string} projectName  项目名称
    @apiParam {int} page 页数
    @apiParam {int} sizePage 页面数量
    @apiParamExample {json} Request-Example:
    {
        "projectName": "mengtui_api",
        "page": 1,
        "sizePage": 10
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": [
            {
                "address": "2019-06-25 17:06:55",
                "id": 95,
                "name": "coins_mall_check_what_coins_testcase,coins_mall_exchange_goods_cancel_delete_order_testcase",
                "project_name": "mengtui_api",
                "read_status": "已读"
            },
            {
                "address": "2019-06-25 16:06:09",
                "id": 94,
                "name": "address_delete_testcase,address_set_default_testcase",
                "project_name": "mengtui_api",
                "read_status": "已读"
            },
            {
                "address": "2019-06-25 16:06:29",
                "id": 93,
                "name": "address_set_default_testcase,address_delete_testcase",
                "project_name": "mengtui_api",
                "read_status": "已读"
            },
            {
                "address": "2019-06-25 16:06:18",
                "id": 92,
                "name": "address_delete_testcase,address_set_default_testcase",
                "project_name": "mengtui_api",
                "read_status": "已读"
            },
            {
                "address": "2019-06-19 10:06:40",
                "id": 84,
                "name": "coupon_description_testcase,coupon_no_use_testcase,delete_delivery_address_testcase",
                "project_name": "mengtui_api",
                "read_status": "已读"
            },
            {
                "address": "2019-05-22 10:05:19",
                "id": 83,
                "name": "kepler_add_cart_buy_then_refund_testcase",
                "project_name": "mengtui_api",
                "read_status": "已读"
            },
            {
                "address": "2019-05-22 10:05:57",
                "id": 82,
                "name": "kepler_add_cart_buy_then_refund_testcase",
                "project_name": "mengtui_api",
                "read_status": "已读"
            },
            {
                "address": "2019-05-22 10:05:32",
                "id": 81,
                "name": "add_goods_to_shop_cart_quantity_is_negiative_testcase",
                "project_name": "mengtui_api",
                "read_status": "已读"
            },
            {
                "address": "2019-05-20 11:05:51",
                "id": 80,
                "name": "search",
                "project_name": "mengtui_api",
                "read_status": "已读"
            },
            {
                "address": "2019-05-20 11:05:33",
                "id": 79,
                "name": "search",
                "project_name": "mengtui_api",
                "read_status": "已读"
            }
        ],
        "status": 1,
        "total": 11
    }
    """
    data = request.json
    project_name = data.get('projectName')
    page = data.get('page') if data.get('page') else 1
    per_page = data.get('sizePage') if data.get('sizePage') else 10

    jsondata = InterfaceReportBusiness.find_report(project_name, page, per_page)
    return jsondata
