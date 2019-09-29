from flask import request

from apps.auth.auth_require import required
from apps.project.business.issue import IssueBusiness, IssueRecordBusiness, IssueDashBoardBusiness
from apps.project.extentions import parse_json_form, validation, parse_list_args2
from library.api.render import json_detail_render, json_list_render2
from library.api.tBlueprint import tblueprint

bpname = 'issue'
view_permission = f'{bpname}_view'
modify_permission = f'{bpname}_modify'
issue = tblueprint(bpname, __name__)


# 新增issue
@issue.route('/', methods=['POST'])
@required(modify_permission)
@validation('POST:issue_create')
def issue_add_handler():
    """
    @api {post} /v1/issue 新增 缺陷
    @apiName CreateIssue
    @apiGroup 项目
    @apiDescription 新增 缺陷
    @apiParam {int} module_id 模块 ID
    @apiParam {int} handler 处理人 ID
    @apiParam {int} issue_type 类型
    @apiParam {int} chance 出现几率
    @apiParam {int} level 级别
    @apiParam {int} priority 优先级
    @apiParam {int} system 系统
    @apiParam {string} title 标题
    @apiParam {string} attach 福建
    @apiParam {string} description 描述
    @apiParam {int} detection_chance 用户识别度
    @apiParam {int} project_id 项目 ID
    @apiParam {int} version 版本
    @apiParam {int} creator 创建人 ID
    @apiParam {int} modifier 修改人 ID
    @apiParam {int} [requirement_id] 关联的 需求 ID
    @apiParam {string} [tag] 标签
    @apiParamExample {json} Request-Example:
    {
        "module_id": 340,
        "handler": 93,
        "issue_type": 0,
        "chance": 0,
        "level": 0,
        "priority": 0,
        "system": 4,
        "title": "123",
        "attach": "{\"images\":[],\"files\":[],\"videos\":[]}",
        "description": "<p>test</p>",
        "detection_chance": 0,
        "project_id": 4,
        "version": 168,
        "creator": 93,
        "modifier": 93,
        "requirement_id": 123,
        "tag": 13,14
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    (system, version, project_id, module_id, creator, modifier, handler,
     issue_type, chance, level, priority, stage,title, attach, handle_status,
     description, comment, detection_chance, requirement_id, case_covered, tag) = parse_json_form('issue_create')
    ret = IssueBusiness.create(system, version, project_id, module_id, creator, modifier, handler, issue_type,
                               chance, level, priority, stage, title, attach, handle_status, description, comment,
                               detection_chance, requirement_id, case_covered, tag)

    return json_detail_render(ret)


# 根据id修改，删除issue
@issue.route('/<int:issue_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:issue_modify')
def issue_modify_handler(issue_id):
    """
    @api {post} /v1/issue/{int:id} 修改 缺陷
    @apiName ModifyIssue
    @apiGroup 项目
    @apiDescription 修改 缺陷
    @apiParam {int} module_id 模块 ID
    @apiParam {int} handler 处理人 ID
    @apiParam {int} issue_type 类型
    @apiParam {int} chance 出现几率
    @apiParam {int} level 级别
    @apiParam {int} priority 优先级
    @apiParam {int} system 系统
    @apiParam {string} title 标题
    @apiParam {string} attach 福建
    @apiParam {string} description 描述
    @apiParam {int} detection_chance 用户识别度
    @apiParam {int} project_id 项目 ID
    @apiParam {int} version 版本
    @apiParam {int} creator 创建人 ID
    @apiParam {int} modifier 修改人 ID
    @apiParam {int} [requirement_id] 关联的 需求 ID
    @apiParam {string} [tag] 标签
    @apiParamExample {json} Request-Example:
    {
        "module_id": 340,
        "handler": 93,
        "issue_type": 0,
        "chance": 0,
        "level": 0,
        "priority": 0,
        "system": 4,
        "title": "123",
        "attach": "{\"images\":[],\"files\":[],\"videos\":[]}",
        "description": "<p>test</p>",
        "detection_chance": 0,
        "project_id": 4,
        "version": 168,
        "creator": 93,
        "modifier": 93,
        "requirement_id": 1,
        "tag": 13,14
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    (system, version, project_id, module_id, modifier, handler, issue_type,
     chance, level, priority, stage, title, attach, handle_status, description,
     comment, detection_chance, requirement_id, case_covered, tag) = parse_json_form('issue_modify')
    ret = IssueBusiness.modify(issue_id, system, version, project_id, module_id, modifier, handler, issue_type,
                               chance, level, priority, stage, title, attach, handle_status, description, comment,
                               detection_chance, requirement_id, case_covered, tag)
    return json_detail_render(ret)


# 根据id修改，删除issue
@issue.route('/<int:issue_id>', methods=['DELETE'])
def issue_delete_handler(issue_id):
    """
    @api {delete} /v1/issue/{int:id} 删除 缺陷
    @apiName DeleteIssue
    @apiGroup 项目
    @apiDescription 删除 缺陷
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    ret = IssueBusiness.delete(issue_id)
    return json_detail_render(ret)


# 切换issue状态
@issue.route('/handlestatus/<int:issue_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:handle_status')
def issue_board_status_handler(issue_id):
    """
    @api {post} /v1/issue/handlestatus/{int:id} 切换 缺陷状态
    @apiName ModifyIssueStatus
    @apiGroup 项目
    @apiDescription 切换 缺陷状态
    @apiParamExample {json} Request-Example:
    {
        "handle_status": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    handle_status = parse_json_form('handle_status')[0]
    ret = IssueBusiness.status_switch(issue_id, handle_status)

    return json_detail_render(ret)


# 切换issue处理人
@issue.route('/handler/<int:issue_id>', methods=['POST'])
@validation('POST:handler_switch')
@required(modify_permission)
def issue_handler_switch_handler(issue_id):
    """
    @api {post} /v1/issue/handler/{int:id} 切换 缺陷处理人
    @apiName ModifyIssueSwitch
    @apiGroup 项目
    @apiDescription 切换 缺陷处理人
    @apiParamExample {json} Request-Example:
    {
        "handler": 11
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    handler = parse_json_form('handler_switch')
    ret = IssueBusiness.handler_switch(issue_id, handler)

    return json_detail_render(ret)


# 切换issue等级
@issue.route('/level/<int:issue_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:level_switch')
def issue_level_switch_handler(issue_id):
    """
    @api {post} /v1/issue/level/{int:id} 切换 缺陷等级
    @apiName ModifyIssueLevel
    @apiGroup 项目
    @apiDescription 切换 缺陷等级
    @apiParamExample {json} Request-Example:
    {
        "level": 3
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    level = parse_json_form('level_switch')
    ret = IssueBusiness.level_switch(issue_id, level)

    return json_detail_render(ret)


# 切换issue优先级
@issue.route('/priority/<int:issue_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:priority_switch')
def issue_priority_switch_handler(issue_id):
    """
    @api {post} /v1/issue/priority/{int:id} 切换 缺陷优先级
    @apiName ModifyIssuePriority
    @apiGroup 项目
    @apiDescription 切换 缺陷优先级
    @apiParamExample {json} Request-Example:
    {
        "priority": 3
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
    ret = IssueBusiness.priority_switch(issue_id, priority)

    return json_detail_render(ret)


# 修改issue的comment
@issue.route('/comment/<int:issue_id>', methods=['POST'])
@validation('POST:add_comment')
@required(modify_permission)
def issue_add_comment_handler(issue_id):
    """
    @api {post} /v1/issue/comment/{int:id} 切换 缺陷备注
    @apiName ModifyIssueComment
    @apiGroup 项目
    @apiDescription 切换 缺陷备注
    @apiParamExample {json} Request-Example:
    {
        "comment": 3
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
    ret = IssueBusiness.add_comment(issue_id, comment)

    return json_detail_render(ret)


# 查询issue-projectid,versionid
@issue.route('/', methods=['GET'])
def issue_query_all_handler():
    """
    @api {get} /v1/issue/ 查询 issue 列表
    @apiName SearchIssue
    @apiGroup 项目
    @apiDescription 查询 issue 列表
    @apiParam {int} [projectid] 项目 ID
    @apiParam {int} [versionid] 版本 ID
    @apiParam {string} [creator_id] 创建人 ID，使用 ',' 分割
    @apiParam {string} [handler_id] 处理人 ID，使用 ',' 分割
    @apiParam {int} [title] 标题
    @apiParam {string} [handle_status] 处理状态 ID，使用 ',' 分割
    @apiParam {string} [module_id] 模块 ID，使用 ',' 分割
    @apiParam {string} [priority] 优先级 ID，使用 ',' 分割
    @apiParam {int} [page_size] 分页 页面大小
    @apiparam {int} [page_index] 分页 页数
    @apiParamExample {json} Request-Example:
    {
        "projectid": 4,
        "versionid": 173,
        "creator_id": "1,2,3,4",
        "page_size": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "attach": "{"images":[],"files":[],"videos":[]}",
                "chance": 2,
                "comment": "",
                "creation_time": "2019-08-08 20:58:49",
                "creator": [
                    {
                    "id": 96,
                    "name": "张宇"
                    }
                ],
                "description": "",
                "detection_chance": "",
                "handle_status": 2,
                "handler": [
                    {
                    "id": 96,
                    "name": "张宇"
                    }
                ],
                "issue_number": "T398",
                "issue_type": 1,
                "issueid": 398,
                "level": 1,
                "modified_time": "2019-08-08 20:58:49",
                "modifier": [],
                "module": [
                    {
                    "id": 329,
                    "name": "用例二级2222"
                    }
                ],
                "priority": 1,
                "project_id": 4,
                "rank": 12,
                "reopen": 0,
                "repair_time": "",
                "requirement_id": "",
                "requirement_title": "",
                "stage": "",
                "status": 0,
                "system": "",
                "test_time": "",
                "title": "1.2.7issuse55555",
                "version": [
                    {
                    "id": 173,
                    "name": "1.2.7"
                    }
                ],
                "weight": ""
            }
        ],
        "message": "ok",
        "page_index": 1,
        "page_size": 1,
        "total": 8
    }
    """
    requirement_id = request.args.get('requirement_id')
    if requirement_id:
        page_size, page_index = parse_list_args2()
        data, count = IssueBusiness.paginate_data_by_rid(page_size, page_index, requirement_id)
        return json_list_render2(0, data, page_size, page_index, count)
    else:
        page_size, page_index = parse_list_args2()
        data, count = IssueBusiness.paginate_data(page_size, page_index)
        return json_list_render2(0, data, page_size, page_index, count)


# 查询issue历史记录
@issue.route('/record', methods=['GET'])
def issue_record_query_all_handler():
    """
    @api {get} /v1/issue/record 查询 缺陷历史记录列表
    @apiName GetIssueRecordList
    @apiGroup 项目
    @apiDescription 查询 缺陷历史记录列表
    @apiParam {int} projectid 项目 ID
    @apiParam {int} versionid 版本 ID
    @apiParamExample {json} Request-Example:
    ?projectid=1
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
        {
            "attach": "{"images":[],"files":[],"videos":[]}",
            "chance": 0,
            "comment": "",
            "creation_time": "2019-05-10 16:23:28",
            "creator": [
                {
                    "id": 12,
                    "name": "刘焕焕"
                }
            ],
            "description": "<p>分享微信不成功.</p>",
            "detection_chance": 0,
            "handle_status": 1,
            "handler": [
                {
                    "id": 12,
                    "name": "刘焕焕"
                }
            ],
            "issue_number": "T309",
            "issue_type": 0,
            "issueid": 309,
            "level": 1,
            "modified_time": "2019-05-13 13:02:45",
            "modifier": [],
            "module": [
                {
                    "id": 291,
                    "name": "V2.4.9版本用例飞科"
                }
            ],
            "priority": 1,
            "project_id": 1,
            "rank": 20,
            "reopen": 0,
            "repair_time": "",
            "requirement_id": "",
            "requirement_title": "",
            "stage": "",
            "status": 0,
            "system": 1,
            "test_time": "",
            "title": "分享微信不成功",
            "version": [
                {
                    "id": 128,
                    "name": "V2.4.9"
                }
            ],
            "weight": ""
            }
        ],
        "message": "ok"
    }
    """
    data = IssueRecordBusiness.query_all_json()
    return json_detail_render(0, data)


# 查询issue历史记录详情
@issue.route('/record/detail/<int:issue_id>', methods=['GET'])
def issue_record_detail_handler(issue_id):
    """
    @api {get} /v1/issue/record/detail/{int:issue_id} 查询 缺陷历史记录详情
    @apiName GetIssueRecordDetailById
    @apiGroup 项目
    @apiDescription 查询 缺陷历史记录详情
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "modified_time": "2018-12-19 14:59:34",
                "modifier_id": 1,
                "modifier_name": "王金龙",
                "operation": "修改了处理状态 待办 为 处理中"
            },
            {
                "modified_time": "2018-12-18 20:28:39",
                "modifier_id": 1,
                "modifier_name": "王金龙",
                "operation": "创建了BUG title"
            }
        ],
        "message": "ok"
    }
    """
    data = IssueRecordBusiness.query_record_detail(issue_id)

    return json_detail_render(0, data)


# 根据id查询issue
@issue.route('/<int:issue_id>', methods=['GET'])
def issue_query_handler(issue_id):
    """
   @api {get} /v1/issue/{int:issue_id} 查询 缺陷详情 (id)
   @apiName GetIssueById
   @apiGroup 项目
   @apiDescription 查询 缺陷详情 通过 ID
   @apiParamExample {json} Request-Example:
   -
   @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "attach":"attach",
                "chance":1,
                "comment":"",
                "creation_time":"2018-12-18 20:28:39",
                "creator":[
                    {
                        "id":1,
                        "name":"王金龙"
                    }
                ],
                "description":"description",
                "handle_status":3,
                "handler":[
                    {
                        "id":1,
                        "name":"王金龙"
                    }
                ],
                "issue_number":"T1",
                "issue_type":1,
                "issueid":1,
                "level":1,
                "modified_time":"2019-03-01 16:46:10",
                "modifier":[
                    {
                        "id":1,
                        "name":"王金龙"
                    }
                ],
                "module":[
                    {
                        "id":1,
                        "name":"音频"
                    }
                ],
                "priority":1,
                "project_id":1,
                "reopen":0,
                "repair_time":"0:00:05",
                "requirement_id":"",
                "requirement_title":"",
                "stage":1,
                "status":0,
                "system":0,
                "test_time":"2 days, 20:21:05",
                "title":"title",
                "version":[
                    {
                        "id":1,
                        "name":"str"
                    }
                ],
                "weight":""
            }
        ],
        "message":"ok"
    }
   """
    data = IssueBusiness.query_by_id(issue_id)

    return json_detail_render(0, data)


# issue关闭和打开的dashboard
@issue.route('/dashboard', methods=['POST'])
@required(view_permission)
@validation('POST:issue_dashboard')
def issue_dashboard_work_handler():
    start_date, end_date = parse_json_form('issue_dashboard')
    data = IssueDashBoardBusiness.issue_dashboard(start_date, end_date)

    return json_detail_render(0, data)


# 查询测试人员每天创建的issue个数
@issue.route('/dashboard/tester', methods=['POST'])
@required(view_permission)
@validation('POST:issue_dashboard')
def tester_issue_work_handler():
    start_date, end_date = parse_json_form('issue_dashboard')
    data = IssueDashBoardBusiness.issue_all_tester_dashboard(start_date, end_date)

    return json_detail_render(0, data)


# issue的状态分布和优先级分布
@issue.route('/dashboard/project', methods=['POST'])
@required(view_permission)
@validation('POST:issue_dashboard')
def issue_project_dashboard_handler():
    """
    @api {POST} /v1/issue/dashboard/project 查询 缺陷状态分布和优先级分布
    @apiName GetIssueByStatusAndPriority
    @apiGroup 项目
    @apiDescription 查询 缺陷状态分布和优先级分布
    @apiParamExample {json} Request-Example:
    {
        "start_date": "2019-01-02 10:10:11",
        "end_date": "2019-01-03 10:10:12",
    }
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "modified_time": "2018-12-19 14:59:34",
                "modifier_id": 1,
                "modifier_name": "王金龙",
                "operation": "修改了处理状态 待办 为 处理中"
            },
            {
                "modified_time": "2018-12-18 20:28:39",
                "modifier_id": 1,
                "modifier_name": "王金龙",
                "operation": "创建了BUG title"
            }
        ],
        "message": "ok"
    }
    """
    start_date, end_date = parse_json_form('issue_dashboard')
    data = IssueDashBoardBusiness.issue_project_dashboard(start_date, end_date)

    return json_detail_render(0, data)


# 看板根据pro_id查询issue各个状态的数量
@issue.route('/dashboard/project/<int:pro_id>', methods=['GET'])
def issue_query_pro_handler(pro_id):
    """
    @api {post} /v1/issue/dashboard/project/{int:project_id} 查询 看板缺陷 根据 project ID
    @apiName GetBoardIssueByProjectId
    @apiGroup 项目
    @apiDescription 根据 project ID 查询 看板缺陷
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "info":[
                    {
                        "detail":[
                            {
                                "count":1,
                                "handle_status":1
                            },
                            {
                                "count":1,
                                "handle_status":2
                            },
                            {
                                "count":1,
                                "handle_status":3
                            }
                        ],
                        "total":3,
                        "version":1
                    },
                    {
                        "detail":[
                            {
                                "count":1,
                                "handle_status":4
                            }
                        ],
                        "total":1,
                        "version":2
                    },
                    {
                        "detail":[
                            {
                                "count":1,
                                "handle_status":1
                            }
                        ],
                        "total":1,
                        "version":3
                    },
                    {
                        "detail":[
                            {
                                "count":3,
                                "handle_status":4
                            }
                        ],
                        "total":3,
                        "version":4
                    },
                    {
                        "detail":[
                            {
                                "count":1,
                                "handle_status":1
                            },
                            {
                                "count":1,
                                "handle_status":4
                            }
                        ],
                        "total":2,
                        "version":128
                    }
                ],
                "project_id":1
            }
        ],
        "message":"ok"
    }
    """
    data = IssueDashBoardBusiness.issue_project_id_dashboard(pro_id)

    return json_detail_render(0, data)


# 绑定 issue 到 requirement
@issue.route('/bind/requirement', methods=['POST'])
@required(modify_permission)
@validation('POST:issue_bind_requirement')
def issue_bind_requirement():
    """
    @api {post} /v1/issue/bind/requirement 绑定 缺陷 issue 到 需求 requirement
    @apiName IssueBindRequirement
    @apiGroup 项目
    @apiDescription 绑定 缺陷到需求
    @apiParam {int} issue_id 缺陷 ID
    @apiParam {int} requirement_id 需求 ID
    @apiParamExample {json} Request-Example:
    {
        "issue": 11,
        "requirement_id": 22
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    requirement_id, issue_id = parse_json_form('issue_bind_requirement')
    ret, msg = IssueBusiness.issue_bind_requirement(issue_id, requirement_id)
    return json_detail_render(ret, [], msg)


# 导出 issue 列表
@issue.route('/export', methods=['GET'])
def issue_export():
    """
    @api {get} /v1/issue/ 导出 issue 到 xls
    @apiName IssueExportToXls
    @apiGroup 项目
    @apiDescription 导出 issue 到 xls
    @apiParam {int} [projectid] 项目 ID
    @apiParam {int} [versionid] 版本 ID
    @apiParam {int} [creator_id] 创建人 ID
    @apiParam {int} [title] 标题
    @apiParam {int} [handle_status] 处理状态 ID
    @apiParam {int} [module_id] 模块 ID
    @apiParam {int} [priority] 优先级 ID
    @apiParam {int} [page_size] 分页 页面大小
    @apiparam {int} [page_index] 分页 页数
    @apiParamExample {json} Request-Example:
    {
        "projectid": 4,
        "versionid": 173,
        "page_size": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": "http://tcloud-static.oss-cn-beijing.aliyuncs.com/issue_export/0/Issues-20190809.164431.xls",
        "message": "ok"
    }
    """
    issue_url = IssueBusiness.export()
    return json_detail_render(code=0, data=issue_url)
