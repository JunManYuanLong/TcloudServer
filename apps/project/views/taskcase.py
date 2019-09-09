from apps.auth.auth_require import required
from apps.project.business.issue import IssueBusiness
from apps.project.business.tasks import TaskCaseRecordBusiness, TaskDashBoardBusiness, TaskCaseBusiness
from apps.project.extentions import parse_json_form, validation
from library.api.render import json_detail_render
from library.api.tBlueprint import tblueprint

bpname = 'taskcase'
bpname_relate = 'case'
excute_permission = f'{bpname_relate}_excute'
taskcase = tblueprint(bpname, __name__, bpname=bpname_relate, has_delete=False)


# 根据taskcaseid进行修改，删除操作
@taskcase.route('/<int:task_case_id>', methods=['POST'])
@required(excute_permission)
@validation('POST:task_case_modify')
def task_case_modify_handler(task_case_id):
    """
    @api {post} /v1/taskcase/{taskcaseid} 修改 单个任务用例
    @apiName ModifyTaskCase
    @apiGroup 项目
    @apiDescription 修改单个任务用例
    @apiParam {int} executor 用例执行者保存的为用户id
    @apiParam {int} exe_way 执行方式，0:批量执行1:单个执行
    @apiParam {string} case_number 编号
    @apiParam {int} module_id 用例模块
    @apiParam {string} case_type 用例类型
    @apiParam {string} title 标题
    @apiParam {string} case_describe 用例描述
    @apiParam {string} precondition 前置条件
    @apiParam {string} step_result 用例步骤及预期结果json->string格式存入
    @apiParam {int} is_auto 是否可转自动化
    @apiParam {int} status 用例任务状态
    @apiParam {string} comment 备注
    @apiParam {int} version 版本
    @apiParamExample {json} Request-Example:
    {
        "version": 1,
        "module_id": 1,
        "executor": 1,
        "exe_way": 1,
        "case_type": "str112",
        "title": "title",
        "case_describe": "str",
        "precondition": "str",
        "step_result": "str",
        "is_auto": 1,
        "status": 1,
        "comment": "str"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    (module_id, project_id, version, executor, exe_way, ctype, title, description, precondition, step_result,
     is_auto, status, comment, priority) = parse_json_form('task_case_modify')
    ret = TaskCaseBusiness.modify(task_case_id, module_id, project_id, version, executor, exe_way, ctype, title,
                                  description, precondition, step_result, is_auto, status, comment, priority)
    return json_detail_render(ret)


# 根据taskcaseid进行删除操作
@taskcase.route('/<int:task_case_id>', methods=['DELETE'])
@required(excute_permission)
def task_case_delete_handler(task_case_id):
    """
    @api {delete} /v1/taskcase/{taskcaseid} 删除 任务用例
    @apiName DeleteTaskCase
    @apiGroup 项目
    @apiDescription 删除任务用例
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    ret = TaskCaseBusiness.delete(task_case_id)
    return json_detail_render(ret)


# 修改taskcase的comment
@taskcase.route('/comment/<int:task_case_id>', methods=['POST'])
@validation('POST:add_comment')
@required(excute_permission)
def task_case_add_comment_handler(task_case_id):
    """
    @api {post} /v1/taskcase/comment/{taskcaseid} 修改 taskcase的comment
    @apiName ModifyTaskCaseComment
    @apiGroup 项目
    @apiDescription 修改taskcase的comment
    @apiParam {string} comment 备注
    @apiParamExample {json} Request-Example:
    {
        "comment": "add_comment"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    comment = parse_json_form('add_comment')
    ret = TaskCaseBusiness.add_comment(task_case_id, comment)
    return json_detail_render(ret)


# 切换taskcase状态
@taskcase.route('/status/<int:task_case_id>', methods=['POST'])
@required(excute_permission)
@validation('POST:task_status')
def task_case_status_handler(task_case_id):
    """
    @api {post} /v1/taskcase/status/{taskcaseid} 修改 taskcase状态
    @apiName ModifytaskCaseStatus
    @apiGroup 项目
    @apiDescription 修改taskcase状态
    @apiParam {int} status 任务状态 0:任务创建 1:任务已删除 2:任务已完成 3: 已拒绝
    @apiParamExample {json} Request-Example:
    {
        "status": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    handle_status = parse_json_form('task_status')
    ret = TaskCaseBusiness.status_switch(task_case_id, handle_status)
    return json_detail_render(ret)


# taskcase关联issue
@taskcase.route('/relation', methods=['POST'])
@required(excute_permission)
@validation('POST:case_relation_issue')
def task_case_relation_handler():
    """
    @api {post} /v1/taskcase/relation/ 关联 taskcase和issue
    @apiName RelationTaskCaseAndIssue
    @apiGroup 项目
    @apiDescription 关联taskcase和issue
    @apiParam {int} task_case_id taskcase的id
    @apiParam {int} issue_id issue的id
    @apiParamExample {json} Request-Example:
    {
        "task_case_id": 1,
        "issue_id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    task_case_id, issue_id = parse_json_form('case_relation_issue')
    ret = IssueBusiness.relation_issue(task_case_id, issue_id)
    return json_detail_render(ret)


# 切换taskcase优先级
@taskcase.route('/priority/<int:task_case_id>', methods=['POST'])
@required(excute_permission)
@validation('POST:priority_switch')
def issue_priority_switch_handler(task_case_id):
    """
    @api {post} /v1/taskcase/priority/{taskcaseid} 修改 taskcase的优先级
    @apiName ChangeTaskCasePriority
    @apiGroup 项目
    @apiDescription 修改taskcase的优先级
    @apiParam {int} priority 优先级 0:紧急 1:高 2:中 3:低
    @apiParamExample {json} Request-Example:
    {
        "priority": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    priority = parse_json_form('priority_switch')
    ret = TaskCaseBusiness.priority_switch(task_case_id, priority)
    return json_detail_render(ret)


# 批量切换taskcase优先级
@taskcase.route('/priority', methods=['POST'])
@required(excute_permission)
@validation('POST:priority_batch_switch')
def issue_priority_batch_switch_handler():
    """
    @api {post} /v1/taskcase/priority/ 修改 多个taskcase的优先级
    @apiName ChangeTaskCasesPriority
    @apiGroup 项目
    @apiDescription 修改多个taskcase的优先级
    @apiParam {int} priority 优先级 0:紧急 1:高 2:中 3:低
    @apiParam {int} project_id 项目id
    @apiParam {list} case_list taskcase的列表
    @apiParamExample {json} Request-Example:
    {
        "case_list": [1,2,3],
        "priority": 1,
        "project_id": 4
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    project_id, case_list, priority = parse_json_form('priority_batch_switch')
    ret = TaskCaseBusiness.priority_batch_switch(project_id, case_list, priority)
    return json_detail_render(ret)


# 分配taskcase
@taskcase.route('/assign', methods=['POST'])
@required(excute_permission)
@validation('POST:assign_task_case')
def task_case_assign_handler():
    """
    @api {post} /v1/taskcase/assign/ 分配 taskcase指定人员执行
    @apiName AssignTaskCase
    @apiGroup 项目
    @apiDescription 分配taskcase指定人员执行
    @apiParam {list} case_list taskcase的列表
    @apiParam {int} handler 被分配执行taskcase的人的ID
    @apiParamExample {json} Request-Example:
    {
        "case_list": [1,2,3],
        "handler": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    project_id, case_list, handler = parse_json_form('assign_task_case')
    ret = TaskCaseBusiness.assign_task_case(project_id, case_list, handler)
    return json_detail_render(ret)


# 查询所有taskcase，projectid,versionid,taskid非必传
@taskcase.route('/', methods=['GET'])
def task_cases_query_all_handler():
    """
    @api {get} /v1/taskcase/ 获取 taskcase列表
    @apiName GetTaskCaseList
    @apiGroup 项目
    @apiDescription 获取taskcase列表
    @apiSuccess {int} task_id 关联的taskID
    @apiSuccess {int} task_case_id 关联的task_caseID
    @apiSuccess {int} executor 用例执行者保存的为用户id
    @apiSuccess {int} exe_way 执行方式，0:批量执行1:单个执行
    @apiSuccess {int} case_number 编号
    @apiSuccess {int} module_id 用例模块ID
    @apiSuccess {string} module_name 用例模块
    @apiSuccess {int} feature_id 子模块
    @apiSuccess {string} ctype 用例类型
    @apiSuccess {string} description 用例描述
    @apiSuccess {string} precondition 前置条件
    @apiSuccess {string} step_result 用例步骤及预期结果json->string格式存入
    @apiSuccess {int} is_auto 是否可转自动化
    @apiSuccess {int} status 任务用例状态 0:新增 1:已删除 2:跳过 3:执行通过 4:执行不通过

    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [
        {
          "info": [
            {
              "cnumber": "case001",
              "comment": "aaaaa",
              "ctype": "1",
              "description": "str",
              "exe_way": 1,
              "executor_id": 3,
              "executor_name": "jimmy",
              "handler_id": 1,
              "handler_name": "wiggens",
              "is_auto": 1,
              "module_id": 1,
              "module_name": "音频",
              "precondition": "777",
              "status": 0,
              "step_result": "111",
              "task_id": 1,
              "taskcaseid": 1,
              "title": ""
            },
            {
              "cnumber": "case001",
              "comment": "",
              "ctype": "1,2",
              "description": "888",
              "exe_way": "",
              "executor_id": 1,
              "executor_name": "wiggens",
              "handler_id": 1,
              "handler_name": "wiggens",
              "is_auto": 1,
              "module_id": 1,
              "module_name": "音频",
              "precondition": "999",
              "status": 0,
              "step_result": "222",
              "task_id": 2,
              "taskcaseid": 2,
              "title": ""
            }
          ],
          "module_id": 1,
          "module_name": "音频"
        }
      ],
      "message": "ok"
    }
    """
    data = TaskCaseBusiness.query_all_json()
    return json_detail_render(0, data)


# 查询单个taskcase
@taskcase.route('/<int:task_case_id>', methods=['GET'])
def task_case_query_handler(task_case_id):
    """
    @api {get} /v1/taskcase/{taskcaseid} 获取 单个taskcase
    @apiName GetTaskCase
    @apiGroup 项目
    @apiDescription 获取单个taskcase列表
    @apiSuccess {int} task_id 关联的taskID
    @apiSuccess {int} task_case_id 关联的task_caseID
    @apiSuccess {int} executor 用例执行者保存的为用户id
    @apiSuccess {int} exe_way 执行方式，0:批量执行1:单个执行
    @apiSuccess {int} case_number 编号
    @apiSuccess {int} module_id 用例模块ID
    @apiSuccess {string} module_name 用例模块
    @apiSuccess {int} feature_id 子模块
    @apiSuccess {string} ctype 用例类型
    @apiSuccess {string} description 用例描述
    @apiSuccess {string} precondition 前置条件
    @apiSuccess {string} step_result 用例步骤及预期结果json->string格式存入
    @apiSuccess {int} is_auto 是否可转自动化
    @apiSuccess {int} status 任务用例状态 0:新增 1:已删除 2:跳过 3:执行通过 4:执行不通过

    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [
        {
            "cnumber": "case001",
            "comment": "aaaaa",
            "ctype": "1",
            "description": "str",
            "exe_way": 1,
            "executor_id": 3,
            "executor_name": "jimmy",
            "handler_id": 1,
            "handler_name": "wiggens",
            "is_auto": 1,
            "module_id": 1,
            "module_name": "音频",
            "precondition": "777",
            "status": 0,
            "step_result": "111",
            "task_id": 1,
            "taskcaseid": 1,
            "title": ""
        }
      ],
      "message": "ok"
    }
    """
    data = TaskCaseBusiness.query_by_id(task_case_id)
    return json_detail_render(0, data)


# 根据task_case_id查询taskcaserecord
@taskcase.route('/record/<int:task_case_id>', methods=['GET'])
def task_case_record_handler(task_case_id):
    """
    @api {get} /v1/taskcase/record/{taskcaseid} 查询 taskcase历史记录
    @apiName GetTaskCaseRecord
    @apiGroup 项目
    @apiDescription 查询taskcase历史记录
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
        {
            "case_describe": "每次新打开App，检测三项设置是否开启",
            "case_number": "",
            "case_type": "2",
            "comment": "",
            "exe_way": "",
            "executor_id": "",
            "feature": "播放音频",
            "featureid": 1,
            "is_auto": 1,
            "module": "视频",
            "moduleid": 2,
            "precondition": "未开启表情键盘或完全访问权限，未切换到表情键盘",
            "status": 0,
            "step_result": "",
            "task_id": 1,
            "task_case_id": 3,
            "taskcaserecordid":1,
            "weight": 1
        }
        ],
        "message": "ok"
    }
    """
    data = TaskCaseRecordBusiness.query_by_task_case_id(task_case_id)
    return json_detail_render(0, data)


# 看板根据user,project,version,task查询tack_case,条件为空则默认ALL
@taskcase.route('/board', methods=['POST'])
@validation('POST:task_case_board')
def task_case_board_query_handler():
    """
    @api {post} /v1/taskcase/board/ taskcase看板
    @apiName TaskCaseBoard
    @apiGroup 项目
    @apiDescription 根据user,project,version,task查询tack_case
    @apiParam {int} task_id 任务ID
    @apiParam {int} user 用户ID，根据taskcase表的executor字段筛选
    @apiParam {int} project_id 项目ID
    @apiParam {int} version 版本ID
    @apiParamExample {json} Request-Example:
    {
        "user": 1,
        "task_id": 1,
        "project_id": 1,
        "version": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [
        {
          "creator": [
            {
              "id": 1,
              "name": "wiggens"
            }
          ],
          "description": "str",
          "end_time": "",
          "executor": [
            {
              "id": 2,
              "name": "max"
            }
          ],
          "id": 2,
          "name": "str",
          "priority": 6,
          "start_time": "",
          "status": 0,
          "tmethod": "str3",
          "ttype": "str"
        }
      ],
      "message": "ok"
    }
    """
    user, project_id, version, task_id = parse_json_form('task_case_board')
    ret = TaskCaseBusiness.query_borad(user, project_id, version, task_id)
    return json_detail_render(0, ret)


# 查询测试人员每天执行的case个数
@taskcase.route('/dashboard/tester', methods=['POST'])
@required(excute_permission)
@validation('POST:issuedashboard')
def task_case_dashboard_tester_handler():
    """
    @api {post} /v1/taskcase/dashboard/tester 查询 测试人员每天执行的case个数
    @apiName TaskCaseDashboardTester
    @apiGroup 项目
    @apiDescription 查询测试人员每天执行的case个数
    @apiParam {string} start_date 开始日期
    @apiParam {string} end_date 结束日期
    @apiParamExample {json} Request-Example:
    {
        "start_date": "2018-11-11",
        "end_date": "2018-11-22"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [
        {
              "info": [
                {
                  "count": 2,
                  "date": "2018-12-17"
                }
              ],
              "userid": 1,
              "username": "wiggens"
            }
      "message": "ok"
    }
    """
    start_date, end_date = parse_json_form('issuedashboard')
    data = TaskDashBoardBusiness.task_case_all_tester_dashboard(start_date, end_date)
    return json_detail_render(0, data)


# 各个项目的case汇总
@taskcase.route('/dashboard/project', methods=['POST'])
@required(excute_permission)
@validation('POST:issuedashboard')
def task_case_dashboard_project_handler():
    """
    @api {post} /v1/taskcase/dashboard/project 查询 各个项目的case汇总
    @apiName TaskCaseDashboardProject
    @apiGroup 项目
    @apiDescription 查询各个项目的case汇总
    @apiParam {string} start_date 开始日期
    @apiParam {string} end_date 结束日期
    @apiParamExample {json} Request-Example:
    {
        "start_date": "2018-11-11",
        "end_date": "2018-11-22"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [
        {
              "info": [
                {
                  "count": 2,
                  "date": "2018-12-17"
                }
              ],
              "userid": 1,
              "username": "wiggens"
            }
      "message": "ok"
    }
    """
    start_date, end_date = parse_json_form('issuedashboard')
    data = TaskDashBoardBusiness.task_case_project_dashboard(start_date, end_date)
    return json_detail_render(0, data)


@taskcase.route('/export', methods=['POST'])
# @required(excute_permission)
@validation('POST:taskcase_export')
def case_export():
    """
    @api {post} /v1/taskcase/export 导出任务下的用例
    @apiName ExportTaskcase
    @apiGroup 项目
    @apiDescription 导出任务下的用例
    @apiParam {int} project_id 项目id
    @apiParam {int} task_id 任务id
    @apiParamExample {json} Request-Example:
    {
        "project_id":4,
        "task_id":96
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":{"url":"http://tcloud-static.oss-cn-beijing.aliyuncs.com/v1/case_export/96/1564575657.xls"},
        "message":""
    }
    """
    project_id, task_id = parse_json_form('taskcase_export')
    code, data, message = TaskCaseBusiness.export(project_id, task_id)
    return json_detail_render(code=code, data=data, message=message)
