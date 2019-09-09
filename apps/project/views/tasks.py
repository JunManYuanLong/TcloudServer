from apps.auth.auth_require import required
from apps.project.business.tasks import TaskBusiness, TaskDashBoardBusiness
from apps.project.extentions import parse_list_args2, parse_json_form, validation
from library.api.render import json_detail_render, json_list_render2
from library.api.tBlueprint import tblueprint

bpname = 'task'
view_permission = f'{bpname}_view'
modify_permission = f'{bpname}_modify'
task = tblueprint(bpname, __name__)


# 新增task
@task.route('/', methods=['POST'])
@required(modify_permission)
@validation('POST:task_create')
def task_add_handler():
    """
    @api {post} /v1/task/ 新增 任务
    @apiName CreateTask
    @apiGroup 项目
    @apiDescription 新增任务
    @apiParam {string} description 任务描述
    @apiParam {string} tmethod 任务方法：自动化or人工测试
    @apiParam {string} ttype 任务类型：功能测试，兼容性测试…
    @apiParam {int} creator 创建任务的人
    @apiParam {int} executor 执行任务的人
    @apiParam {int} priority 优先级0:紧急1:高2:中3:低
    @apiParam {list} case_list 关联的case列表
    @apiParam {string} name 名称
    @apiParam {int} project_id 项目ID
    @apiParam {string} start_date 开始时间
    @apiParam {string} end_date 结束时间
    @apiParam {int} version 版本ID
    @apiParam {string} testreport 测试总结
    @apiParam {string} attach 附件：测试报告附件
    @apiParam {string} attachment 附件：新建修改任务的时候上传的 附件文件
    @apiParamExample {json} Request-Example:
    {
        "case_list": [1,2,3],
        "description": "str",
        "tmethod": "str",
        "ttype": "str",
        "creator": 1,
        "executor": 1,
        "start_date": "2018-11-11",
        "end_date": "2018-11-22",
        "project_id": 1,
        "version": 1,
        "name": "str12",
        "testreport": "str123",
        "attach": "str1234",
        "priority": 1,
        "attachmenet": "",
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    (name, description, tmethod, ttype, creator, executor, start_time, end_time, priority, project_id, version,
     case_list, testreport, attach, tag, attachment) = parse_json_form('task_create')
    ret = TaskBusiness.create(name, description, tmethod, ttype, creator, executor, start_time, end_time, priority,
                              project_id, version, case_list, testreport, attach, tag, attachment)

    return json_detail_render(ret)


# 根据taskid进行修改，删除操作
@task.route('/<int:task_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:task_modify')
def task_modify_handler(task_id):
    """
    @api {post} /v1/task/{taskid} 修改 任务
    @apiName ModifyTask
    @apiGroup 项目
    @apiDescription 修改任务
    @apiParam {string} description 任务描述
    @apiParam {string} tmethod 任务方法：自动化or人工测试
    @apiParam {string} ttype 任务类型：功能测试，兼容性测试…
    @apiParam {int} creator 创建任务的人
    @apiParam {int} executor 执行任务的人
    @apiParam {int} priority 优先级0:紧急1:高2:中3:低
    @apiParam {list} case_list 关联的case列表
    @apiParam {string} name 名称
    @apiParam {int} project_id 项目ID
    @apiParam {string} start_date 开始时间
    @apiParam {string} end_date 结束时间
    @apiParam {int} version 版本ID
    @apiParam {string} testreport 测试总结
    @apiParam {string} attach 附件：测试报告附件
    @apiParam {string} attachment 附件：新建修改任务的时候上传的 附件文件
    @apiParamExample {json} Request-Example:
    {
        "case_list": [1,2,3],
        "description": "str",
        "tmethod": "str",
        "ttype": "str",
        "creator": 1,
        "executor": 1,
        "start_date": "2018-11-11",
        "end_date": "2018-11-22",
        "project_id": 1,
        "version": 1,
        "name": "str12",
        "testreport": "str123",
        "attach": "str1234",
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
    (name, description, tmethod, ttype, executor, start_time, end_time, priority, case_list, testreport,
     attach, tag, attachment) = parse_json_form(modify_permission)
    ret = TaskBusiness.modify(task_id, name, description, tmethod, ttype, executor, start_time, end_time, priority,
                              case_list, testreport, attach, tag, attachment)

    return json_detail_render(ret)


# 根据taskid进行删除操作
@task.route('/<int:task_id>', methods=['DELETE'])
def task_delete_handler(task_id):
    """
    @api {delete} /v1/task/{taskid} 删除 任务
    @apiName DeleteTask
    @apiGroup 项目
    @apiDescription 删除任务
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    ret, msg = TaskBusiness.delete(task_id)
    return json_detail_render(ret, message=msg)


# 修改task状态
@task.route('/status/<int:task_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:task_status')
def task_finish_handler(task_id):
    """
    @api {post} /v1/task/status/{taskid} 修改 任务状态
    @apiName ModifyTaskStatus
    @apiGroup 项目
    @apiDescription 修改任务状态
    @apiParam {int} status 任务状态 0:任务创建 1:任务已删除 2:任务已完成 3: 已拒绝
    @apiParamExample {json} Request-Example:
    {
        "status": 3
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    status = parse_json_form('task_status')
    ret, msg = TaskBusiness.status_switch(task_id, status[0])

    return json_detail_render(ret, message=msg)


# 修改测试总结，附件
@task.route('/testreport/<int:task_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:task_testreport')
def task_testreport_handler(task_id):
    """
    @api {post} /v1/task/testreport/{taskid} 修改 测试总结和附件
    @apiName ModifyTaskReport
    @apiGroup 项目
    @apiDescription 修改测试总结和附件
    @apiParam {string} testreport 测试总结
    @apiParam {string} attach 附件
    @apiParamExample {json} Request-Example:
    {
        "testreport": "str123",
        "attach": "str1234",
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    testreport, attach = parse_json_form('task_testreport')
    ret, msg = TaskBusiness.testreport_switch(task_id, testreport, attach)
    return json_detail_render(ret, message=msg)


# 查询task列表-projectid,versionid
@task.route('/', methods=['GET'])
def task_query_all_handler():
    """
    @api {get} /v1/task/ 获取 task列表
    @apiName GetTaskList
    @apiGroup 项目
    @apiDescription 获取task列表
    @apiParam {int} [page_size] 分页-单页大小
    @apiParam {int} [page_index] 分页-页数
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
              "id": 1,
              "name": "wiggens"
            }
          ],
          "id": 4,
          "name": "str12",
          "priority": 1,
          "start_time": "",
          "status": 0,
          "tmethod": "",
          "ttype": "str"
        },
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
              "id": 1,
              "name": "wiggens"
            }
          ],
          "id": 1,
          "name": "str12",
          "priority": 1,
          "start_time": "",
          "status": 0,
          "tmethod": "",
          "ttype": "str"
        }
      ],
      "limit": 99999,
      "message": "ok",
      "offset": 0
    }
    """
    page_size, page_index = parse_list_args2()
    data, count = TaskBusiness.query_task_case_json(page_size, page_index)
    return json_list_render2(0, data, page_size, page_index, count)


# 根据taskid进行查询
@task.route('/<int:task_id>', methods=['GET'])
def task_query_handler(task_id):
    """
    @api {get} /v1/task/{taskid} 获取 单个task
    @apiName GetTask
    @apiGroup 项目
    @apiDescription 获取单个task
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
              "id": 1,
              "name": "wiggens"
            }
          ],
          "id": 1,
          "name": "str12",
          "priority": 1,
          "start_time": "",
          "status": 0,
          "tmethod": "",
          "ttype": "str"
        }
      ],
      "message": "ok",
    }
    """
    data = TaskBusiness.query_task_case_json_by_id(task_id)

    return json_detail_render(0, data)


# 看板根据条件查询task,条件为空则默认ALL
@task.route('/board', methods=['POST'])
@required(view_permission)
@validation('POST:task_board')
def task_board_query_handler():
    """
    @api {post} /v1/task/board 查询 task看板
    @apiName GetTaskBoard
    @apiGroup 项目
    @apiDescription 查询task看板
    @apiParam {int} user 用户ID，根据task表的executor字段筛选
    @apiParam {string} start_time 开始日期
    @apiParam {string} end_time 结束日期
    @apiParam {int} project_id 项目ID
    @apiParam {int} version 版本ID
    @apiParamExample {json} Request-Example:
    {
        "user": 1,
        "start_time": "2018-11-22",
        "end_time": "2018-11-22",
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
          "description": "description",
          "end_time": "2018-11-22",
          "executor": [
            {
              "id": 1,
              "name": "wiggens"
            }
          ],
          "id": 1,
          "name": "name",
          "priority": 1,
          "project_id": 1,
          "start_time": "2018-11-22",
          "status": 0,
          "tmethod": "1",
          "ttype": "1",
          "version": "1.1.1"
        }
      ],
      "limit": 999999,
      "message": "ok",
      "offset": 0
    }
    """
    user, start_time, end_time, project_id, version = parse_json_form('task_board')
    ret = TaskBusiness.query_borad(user, start_time, end_time, project_id, version)

    return json_detail_render(0, ret)


# 查询测试人员每天执行的case个数
@task.route('/dashboard/tester', methods=['POST'])
@required(view_permission)
@validation('POST:issuedashboard')
def tester_task_case_work_handler():
    """
    @api {post} /v1/task/dashboard/tester 查询 测试人员每天执行的case个数
    @apiName GetTaskTester
    @apiGroup 项目
    @apiDescription 查询测试人员每天执行的case个数
    @apiParam {string} start_time 开始日期
    @apiParam {string} end_time 结束日期
    @apiParamExample {json} Request-Example:
    {
        "start_time": "2018-11-22",
        "end_time": "2018-11-22",
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
          "description": "description",
          "end_time": "2018-11-22",
          "executor": [
            {
              "id": 1,
              "name": "wiggens"
            }
          ],
          "id": 1,
          "name": "name",
          "priority": 1,
          "project_id": 1,
          "start_time": "2018-11-22",
          "status": 0,
          "tmethod": "1",
          "ttype": "1",
          "version": "1.1.1"
        }
      ],
      "limit": 999999,
      "message": "ok",
      "offset": 0
    }
    """
    start_date, end_date = parse_json_form('issuedashboard')
    data = TaskDashBoardBusiness.task_case_all_tester_dashboard(start_date, end_date)

    return json_detail_render(0, data)


@task.route('/dashboard/project', methods=['POST'])
@required(view_permission)
@validation('POST:issuedashboard')
def task_summary_handler():
    """
    @api {post} /v1/task/dashboard/project 查询 各个项目的task汇总
    @apiName GetTaskProject
    @apiGroup 项目
    @apiDescription 查询各个项目的task汇总
    @apiParam {string} start_time 开始日期
    @apiParam {string} end_time 结束日期
    @apiParamExample {json} Request-Example:
    {
        "start_time": "2018-11-22",
        "end_time": "2018-11-22",
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
          "description": "description",
          "end_time": "2018-11-22",
          "executor": [
            {
              "id": 1,
              "name": "wiggens"
            }
          ],
          "id": 1,
          "name": "name",
          "priority": 1,
          "project_id": 1,
          "start_time": "2018-11-22",
          "status": 0,
          "tmethod": "1",
          "ttype": "1",
          "version": "1.1.1"
        }
      ],
      "limit": 999999,
      "message": "ok",
      "offset": 0
    }
    """
    start_date, end_date = parse_json_form('issuedashboard')
    data = TaskDashBoardBusiness.task_project_dashboard(start_date, end_date)

    return json_detail_render(0, data)


# 修改task优先级
@task.route('/priority/<int:task_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:task_priority')
def task_modify_priority_handler(task_id):
    """
    @api {post} /v1/task/priority/{taskid} 修改 task优先级
    @apiName ModifyTaskPriority
    @apiGroup 项目
    @apiDescription 修改task优先级
    @apiParam {int} priority 优先级 0:紧急1:高2:中3:低
    @apiParamExample {json} Request-Example:
    {
        "priority": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [],
      "message": "ok",
    }
    """
    priority = parse_json_form('task_priority')
    ret, msg = TaskBusiness.priority_switch(task_id, priority[0])

    return json_detail_render(ret, message=msg)
