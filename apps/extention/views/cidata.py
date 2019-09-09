import json

from flask import Blueprint, request

from apps.extention.business.cidata import CiDataBusiness, CiJobBusiness
from apps.extention.extentions import parse_list_args2, parse_json_form, validation
from apps.public.models.public import Config
from library.api.render import json_detail_render, json_list_render2

cidata = Blueprint('cidata', __name__)


@cidata.route('/', methods=['GET'])
def ci_list():
    """
    @api {get} /v1/cidata/ 获取jenkins的job
    @apiName GetJenkinsJob
    @apiGroup CI
    @apiDescription 查询jenkins的job
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "accuracy": "0",
                "case_count": 0,
                "description": "自动化例会通知",
                "id": 15,
                "name": "automation_meeting",
                "nextBuildNumber": 63,
                "status": 0
            }
        ],
        "message": "ok"
    }
    """
    data = CiDataBusiness.query_all_json()
    return json_detail_render(0, data)


@cidata.route('/job/<int:ci_id>', methods=['get'])
def job_list(ci_id):
    """
    @api {get} /v1/cidata/job/:ci_id 获取某个job的数据
    @apiName GetJenkinsJobData
    @apiGroup CI
    @apiDescription 获取某个job的数据
    @apiParam {int} ci_id job id
    @apiParam {int} page_size 当前页面的数量
    @apiParam {int} page_index 当前页面的页数
    @apiParam {string} start_time 开始日期
    @apiParam {string} end_time 结束日期
    @apiParam {string} start_name 触发者
    @apiParamExample {json} Request-Example:
    {
        "ci_id": 1，
        "page_size":10,
        "page_index":1,
        "start_time":"2019-04-27",
        "end_time":"2019-07-26",
        "start_name":""
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "ci_id": 16,
                "id": 3547,
                "job_accuracy": "0.7814",
                "job_count": 883,
                "number": 135,
                "report": "http://ctsssource.oss-cn-shanghai.aliyuncs.com/api_report/2019-07-23/1563857285.html",
                "run_date": "Tue, 23 Jul 2019 12:48:00 GMT",
                "run_time": "3232.939",
                "start_name": "timer",
                "status": 0,
                "url": "http://ci.automancloud.com/job/mengtui_activity_api/135/"
            }
        ],
        "message": "ok",
        "page_index": 1,
        "page_size": 10,
        "total": 1
    }
    """
    page_size, page_index = parse_list_args2()
    data = CiJobBusiness.query_json_by_id(ci_id, page_size, page_index)
    count = CiJobBusiness.query_count(ci_id)

    return json_list_render2(0, data, page_size, page_index, count)


@cidata.route('/description/<int:ci_id>', methods=['get'])
def description_list(ci_id):
    """
    @api {get} /v1/description/:ci_id 获取job的描述
    @apiName GetJenkinsJobDescription
    @apiGroup CI
    @apiDescription 获取job的描述
    @apiParam {int} ci_id job id
    @apiParamExample {json} Request-Example:
    {
        "ci_id": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "error_count": 1,
                "error_message": "['oom:\\n', '// OOM: com.mengtuiapp.mall(pid 28586)(dump time: 2019-07-03 12:13:56)]",
                "error_type": "OOM",
                "id": 5,
                "monkey_id": 29
            }
        ],
        "message": "ok"
    }
    """
    data = CiDataBusiness.query_description_by_id(ci_id)
    return json_detail_render(0, data)


# @cidata.route('/updatedata', methods=['get'])
# def update_data():
#     #改为内部job每天触发一次即可
#     CiJobBusiness.update_jenkins_data()
#     return json_detail_render(0, [])


@cidata.route('/run', methods=['POST'])
@validation('POST:cidatarunandreport')
def run_project():
    """
    @api {post} /v1/cidata/run 触发job
    @apiName runJob
    @apiGroup CI
    @apiDescription 触发job
    @apiParam {list} run_list 触发的list
    @apiParam {int} project_id 项目id
    @apiParamExample {json} Request-Example:
    {
        "run_list": [1],
        "project_id":1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "id": 1,
                "isexcuting": false,
                "job": "test_email",
                "name": "test view"
            }
        ],
        "message": "ok"
    }
    """
    project_id, run_list = parse_json_form('cidatarunandreport')
    code, data, message = CiJobBusiness.run(project_id, run_list)
    return json_detail_render(code, data, message)


@cidata.route('/report', methods=['POST'])
@validation('POST:cidatarunandreport')
def gain_report():
    """
    @api {post} /v1/cidata/report 获取报告
    @apiName gainJobReport
    @apiGroup CI
    @apiDescription job的报告
    @apiParam {list} run_list 触发的list
    @apiParam {int} project_id 项目id
    @apiParamExample {json} Request-Example:
    {
        "run_list": [1],
        "project_id":1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "id": 1,
                "isexcuting": false,
                "job": "mengtui_regression_test",
                "name": "萌推回归测试",
                "url": "http://ctsssource.oss-cn-shanghai.aliyuncs.com/api_report/2019-07-26/1564128677.html"
            }
        ],
        "message": "ok"
    }
    """
    project_id, run_list = parse_json_form('cidatarunandreport')
    code, data, message = CiJobBusiness.gain_report(project_id, run_list)
    return json_detail_render(code, data, message)


@cidata.route('/config/info', methods=['POST'])
@validation('POST:configinfo')
def gain_config_info():
    """
    @api {post} /v1/cidata/config/info ci配置数据的获取
    @apiName GainCIConfigData
    @apiGroup CI
    @apiDescription ci配置数据的获取
    @apiParam {int} project_id 项目id
    @apiParamExample {json} Request-Example:
    {
        "project_id":1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "id": 1,
                "job": "mengtui_regression_test",
                "name": "萌推回归测试"
            }
        ],
        "message": "ok"
    }
    """
    data = []
    project_id = parse_json_form('configinfo')[0]

    jenkins_config = Config.query.add_columns(Config.content.label('content')).filter(
        Config.module == 'jenkins',
        Config.module_type == 1).first()
    run_dict = json.loads(jenkins_config.content)

    if str(project_id) in run_dict.keys():
        data = run_dict[str(project_id)]

    return json_detail_render(0, data)


@cidata.route('/rundict', methods=['GET'])
def get_run_dict():
    project_id = request.args.get('projectid')
    run_dict, run_name_dict = CiJobBusiness.gain_run_dict(project_id)
    data = {'run_dict': run_dict, 'run_name_dict': run_name_dict}
    return json_detail_render(0, data)
