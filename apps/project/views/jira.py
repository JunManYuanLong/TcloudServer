from flask import Blueprint, request, current_app

from apps.project.business.jira import JiraBusiness
from library.api.render import json_detail_render

jira = Blueprint("jira", __name__)


# 接收 jira 传来的 request ：requirement
# 不能加权限，处理jira的webhook
@jira.route('/requirement', methods=['POST'])
def jira_receive_requirement_handler():
    """
    @api {POST} /v1/jira/requirement jira 同步 requirement
    @apiName JiraRequirementCreate
    @apiGroup 项目
    @apiDescription Jira 使用，同步 requirement
    @apiParam {string} key Jira ISSUE key
    @apiParam {string} user_id Jira 用户 id
    @apiParam {string} user_key Jira 用户 key
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [],
      "message": "ok"
    }
    """
    key = request.args.get('key')
    JiraBusiness.requirement_handler(key)
    return json_detail_render(0, [], "success")


# 接收 jira 传来的 request ：flow
# 不能加权限，处理jira的webhook
@jira.route('/flow', methods=['POST'])
def jira_receive_flow_handler():
    """
    @api {POST} /v1/jira/flow jira 同步 flow
    @apiName JiraFlowCreate
    @apiGroup 项目
    @apiDescription Jira 使用，同步 flow
    @apiParam {string} user_id Jira 用户 id
    @apiParam {string} user_key Jira 用户 key
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
    current_app.logger.info(f'body: {request.json}')
    key = request.args.get('key')
    JiraBusiness.flow_handler(key)
    return json_detail_render(0, [], "success")
