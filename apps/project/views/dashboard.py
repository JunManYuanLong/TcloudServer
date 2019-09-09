from flask import Blueprint

from apps.project.business.dashboard import DashboardBusiness
from apps.project.extentions import parse_json_form, validation
from library.api.render import json_detail_render

bpname = 'dashboard'
dashboard = Blueprint(bpname, __name__)


@dashboard.route('/tester/work', methods=['POST'])
@validation('POST:tester_work_dashboard')
def dashboard_tester_work_handler():
    """
    @api {post} /v1/tester/work 项目用户工作面板
    @apiName TesterWorkDashboard
    @apiGroup 项目
    @apiDescription 项目用户工作面板
    @apiParam {string} start_time 开始时间
    @apiParam {string} end_time 结束时间
    @apiParamExample {json} Request-Example:
    {
        "start_time": "2018-11-11",
        "end_time": "2018-11-11"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "create_cases":[

                ],
                "exc_cases":[

                ],
                "nickname":"周冬彬",
                "submit_issues":[

                ],
                "userid":3
            }
        ],
        "message":"ok"
    }
    """
    begin_date, end_date = parse_json_form('tester_work_dashboard')
    data = DashboardBusiness.team_work_dashboard(begin_date, end_date)

    return json_detail_render(0, data)
