from flask import request

from apps.auth.auth_require import required
from apps.project.business.requirement import RequirementBusiness, RequirementRecordBusiness, RequirementReviewBusiness
from apps.project.extentions import parse_list_args2, parse_json_form, validation
from library.api.render import json_detail_render, json_list_render2
from library.api.tBlueprint import tblueprint

bpname = 'requirement'
view_permission = f'{bpname}_view'
modify_permission = f'{bpname}_modify'
requirement = tblueprint(bpname, __name__)


# 需求新增
@requirement.route('/', methods=['POST'])
@required(modify_permission)
@validation('POST:requirementcreate')
def requirement_add_handler():
    """
    @api {post} /requirement/ 新增需求
    @apiName CreateRequirement
    @apiGroup 项目
    @apiDescription 新增需求
    @apiParam {string} title 标题
    @apiParam {int} project_id 项目ID
    @apiParam {string} version 所属版本
    @apiParam {int} requirement_type 类型
    @apiParam {int} creator 创建人
    @apiParam {int} handler 处理人
    @apiParam {int} board_status 需求看板状态
    @apiParam {string} description 描述
    @apiParam {int} priority 优先级0:紧急1:高2:中3:低
    @apiParam {string} attach 附件
    @apiParam {string} comment 备注
    @apiParam {int} weight 权重，仅作用于排序
    @apiParam {int} parent_id 父类项目ID
    @apiParam {int} review_status 评审的状态1-未评审，2-评审成功3-评审失败
    @apiParam {string} jira_id jira号
    @apiParam {int} worth 需求价值1:高价值2:非高价值
    @apiParam {string} report_time 上线评估结果时间(天)
    @apiParam {string} report_expect 高价值预期结果
    @apiParam {string} report_real 高价值实际结果
    @apiParam {int} worth_sure 确认需求价值1:高价值2:非高价值
    @apiParam {list} [case_ids] 关联的 用例 ID
    @apiParam {string} expect_time 预期时间
    @apiParam {string} [tag] 标签
    @apiParamExample {json} Request-Example:
    {
        "title": "str",
        "project_id": 1,
        "version": "str",
        "requirement_type": 1,
        "creator": 1,
        "handler": 1,
        "board_status": 1,
        "description": "str",
        "priority": 1,
        "attach": "str",
        "comment": "str",
        "weight": 1,
        "parent_id": 1,
        "review_status": 1,
        "jira_id": "str",
        "worth": 1,
        "report_time": "str",
        "report_expect": "str",
        "report_real": "str",
        "worth_sure": 1,
        "case_ids": [1,2,3],
        "expect_time": "2018-1-30",
        "tag": "1,2,3"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    (title, project_id, version, handler, priority, requirement_type, attach, board_status, description, comment,
     jira_id, worth, report_time, report_expect, report_real, worth_sure,
     case_ids, expect_time, tag) = parse_json_form('requirementcreate')
    ret = RequirementBusiness.requirement_create(title, project_id, version, handler, priority, requirement_type,
                                                 attach, board_status, description, comment, jira_id, worth,
                                                 report_time, report_expect, report_real, worth_sure, case_ids, tag,
                                                 expect_time=expect_time)
    return json_detail_render(ret)


# 需求单个修改
@requirement.route('/<int:requirement_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:requirementmodify')
def requirement_modify_handler(requirement_id):
    """
    @api {post} /requirement/{requirement_id} 修改需求
    @apiName ModifyRequirement
    @apiGroup 项目
    @apiDescription 修改需求
    @apiParam {string} title 标题
    @apiParam {int} project_id 项目ID
    @apiParam {string} version 所属版本
    @apiParam {int} requirement_type 类型
    @apiParam {int} creator 创建人
    @apiParam {int} handler 处理人
    @apiParam {int} board_status 需求看板状态
    @apiParam {string} description 描述
    @apiParam {int} priority 优先级0:紧急1:高2:中3:低
    @apiParam {string} attach 附件
    @apiParam {string} comment 备注
    @apiParam {int} weight 权重，仅作用于排序
    @apiParam {int} review_status 评审的状态1-未评审，2-评审成功3-评审失败
    @apiParam {string} jira_id jira号
    @apiParam {int} worth 需求价值1:高价值2:非高价值
    @apiParam {string} report_time 上线评估结果时间(天)
    @apiParam {string} report_expect 高价值预期结果
    @apiParam {string} report_real 高价值实际结果
    @apiParam {int} worth_sure 确认需求价值1:高价值2:非高价值
    @apiParam {list} [case_ids] 关联的 用例 ID
    @apiParam {string} expect_time 预期时间
    @apiParam {string} [tag] 标签
    @apiParamExample {json} Request-Example:
    {
        "title": "str",
        "project_id": 1,
        "version": "str",
        "requirement_type": 1,
        "creator": 1,
        "handler": 1,
        "board_status": 1,
        "description": "str",
        "priority": 1,
        "attach": "str",
        "comment": "str",
        "weight": 1,
        "review_status": 1,
        "jira_id": "str",
        "worth": 1,
        "report_time": "str",
        "report_expect": "str",
        "report_real": "str",
        "worth_sure": 1,
        "case_ids": [1,2],
        "expect_time": "2018-1-30",
        "tag": "1,2,3"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[],
    "message":"ok"
    }
    """
    (title, project_id, version, priority, requirement_type, attach, handler, board_status, description,
     comment, parent_id, jira_id, worth, report_time, report_expect, report_real, worth_sure,
     case_ids, expect_time, tag) = parse_json_form('requirementmodify')
    ret = RequirementBusiness.requirement_modify(requirement_id, title, project_id, version, board_status, handler,
                                                 description, comment, priority, requirement_type, attach, parent_id,
                                                 jira_id, worth, report_time, report_expect, report_real, worth_sure,
                                                 case_ids, tag, expect_time=expect_time)
    return json_detail_render(ret)


# 需求单个删除
@requirement.route('/<int:requirement_id>', methods=['DELETE'])
def requirement_delete_handler(requirement_id):
    """
    @api {dalete} /requirement_id/{id} 删除需求
    @apiName DeleteRequirement
    @apiGroup 项目
    @apiDescription 删除需求
    @apiParamExample {json} Request-Example:
    无
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    ret = RequirementBusiness.requirement_delete(requirement_id)
    return json_detail_render(ret)


# 切换需求看板状态
@requirement.route('/boardstatus/<int:requirement_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:board_status')
def requirement_board_status_handler(requirement_id):
    board_status = parse_json_form('board_status')
    ret = RequirementBusiness.boardstatus_switch(requirement_id, board_status)
    return json_detail_render(ret)


# 切换需求处理人
@requirement.route('/handler/<int:requirement_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:requirement_handler_switch')
def requirement_handler(requirement_id):
    """
    @api {post} /v1/requirement/handler/{requirement_id} 切换需求处理人
    @apiName SwitchHandler
    @apiGroup 项目
    @apiDescription 切换需求处理人
    @apiParam {int} handler 处理人
    @apiParamExample {json} Request-Example:
    {
        "handler":1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    handler = parse_json_form('requirement_handler_switch')
    ret = RequirementBusiness.handler_switch(requirement_id, handler)

    return json_detail_render(ret)


# 切换需求状态
@requirement.route('/status/<int:requirement_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:requirement_status')
def requirement_status_handler(requirement_id):
    """
    @api {post} /v1/requirement/handler/{requirement_id} 切换需求状态
    @apiName SwitchStatus
    @apiGroup 项目
    @apiDescription 切换需求状态
    @apiParam {int} status 处理人
    @apiParamExample {json} Request-Example:
    {
        "status":1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    rstatus = parse_json_form('requirement_status')
    ret = RequirementBusiness.status_switch(requirement_id, rstatus)

    return json_detail_render(ret)


# 切换需求优先级
@requirement.route('/priority/<int:requirement_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:requirement_priority_switch')
def requirement_priority_switch_handler(requirement_id):
    """
    @api {post} /v1/requirement/handler/{requirement_id} 切换需求优先级
    @apiName SwitchPriority
    @apiGroup 项目
    @apiDescription 切换需求优先级
    @apiParam {int} priority 优先级
    @apiParamExample {json} Request-Example:
    {
        "priority":1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    priority = parse_json_form('requirement_priority_switch')
    ret = RequirementBusiness.priority_switch(requirement_id, priority)

    return json_detail_render(ret)


# 修改需求的comment
@requirement.route('/comment/<int:requirement_id>', methods=['POST'])
@validation('POST:requirement_add_comment')
@required(modify_permission)
def issue_add_comment_handler(requirement_id):
    """
    @api {post} /v1/requirement/handler/{requirement_id} 切换需求优先级
    @apiName SwitchPriority
    @apiGroup 项目
    @apiDescription 切换需求优先级
    @apiParam {int} comment 备注
    @apiParamExample {json} Request-Example:
    {
        "comment":1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    comment = parse_json_form('requirement_add_comment')
    ret = RequirementBusiness.add_comment(requirement_id, comment)

    return json_detail_render(ret)


# 根据审核状态需求查询-projectid,versionid  
@requirement.route('/', methods=['GET'])
def requirement_query_pass_handler():
    id_or_title = request.args.get('id_or_title')
    if id_or_title:
        data = RequirementBusiness.get_requirement_by_id_or_title(id_or_title)
        return json_detail_render(0, data)
    else:
        code, data = RequirementBusiness.get_requirement()
        return json_detail_render(code, data)


# 获取需求列表
@requirement.route('/list', methods=['GET'])
def requirement_query_list():
    page_size, page_index = parse_list_args2()
    father_data, count = RequirementBusiness.paginate_data(page_size, page_index)

    return json_list_render2(0, father_data, page_size, page_index, count)


# 需求title 和attach 修改 则审核状态
@requirement.route('/update/review_status', methods=['POST'])
@required(modify_permission)
@validation('POST:update_review_status')
def requirement_query_update_review_status():
    requirement_id = parse_json_form('update_review_status')
    ret = RequirementBusiness.review_status_modify(requirement_id)

    return json_detail_render(ret)


# 需求单个查询
@requirement.route('/<int:requirement_id>', methods=['GET'])
def requirement_query_handler(requirement_id):
    data = RequirementBusiness.query_requirement_by_id(requirement_id)
    return json_detail_render(0, data)


# 查询requirement历史记录详情
@requirement.route('/record/detail/<int:requirement_id>', methods=['GET'])
def issue_record_detail_handler(requirement_id):
    data = RequirementRecordBusiness.query_record_detail(requirement_id)

    return json_detail_render(0, data)


# 获取某个需求的所有的子需求
@requirement.route('/gain/childrequirement', methods=['POST'])
@required(view_permission)
@validation('POST:gain_children_requirement')
def gain_childrequirement():
    requirement_id, project_id, version = parse_json_form('gain_children_requirement')
    data = RequirementBusiness.look_up_chidren_requirement(requirement_id, project_id, version)
    return json_detail_render(0, data)


# 创建子需求
@requirement.route('/create/childrequirement', methods=['POST'])
@required(modify_permission)
@validation('POST:childrenrequirementcreate')
def create_childrequirement():
    """
    @api {post} /requirement/ 新增子需求
    @apiName CreateVersion
    @apiGroup 项目
    @apiDescription 新增子需求
    @apiParam {string} title 标题
    @apiParam {int} project_id 项目ID
    @apiParam {string} version 所属版本
    @apiParam {int} requirement_type 类型
    @apiParam {int} creator 创建人
    @apiParam {int} handler 处理人
    @apiParam {int} board_status 需求看板状态
    @apiParam {string} description 描述
    @apiParam {int} priority 优先级0:紧急1:高2:中3:低
    @apiParam {string} attach 附件
    @apiParam {string} comment 备注
    @apiParam {int} weight 权重，仅作用于排序
    @apiParam {int} parent_id 父类项目ID
    @apiParam {int} review_status 评审的状态1-未评审，2-评审成功3-评审失败
    @apiParam {string} jira_id jira号
    @apiParam {int} worth 需求价值1:高价值2:非高价值
    @apiParam {string} report_time 上线评估结果时间(天)
    @apiParam {string} report_expect 高价值预期结果
    @apiParam {string} report_real 高价值实际结果
    @apiParam {int} worth_sure 确认需求价值1:高价值2:非高价值
    @apiParam {list} [case_ids] 关联的 用例 ID
    @apiParamExample {json} Request-Example:
    {
        "title": "str",
        "project_id": 1,
        "version": "str",
        "requirement_type": 1,
        "creator": 1,
        "handler": 1,
        "board_status": 1,
        "description": "str",
        "priority": 1,
        "attach": "str",
        "comment": "str",
        "weight": 1,
        "parent_id": 1,
        "review_status": 1,
        "jira_id": "str",
        "worth": 1,
        "report_time": "str",
        "report_expect": "str",
        "report_real": "str",
        "worth_sure": 1,
        "case_ids": [1,3]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    (title, project_id, version, handler, priority, requirement_type, attach, board_status, description,
     comment, parent_id, jira_id, worth, report_time, report_expect, report_real, worth_sure,
     case_ids, expect_time, tag) = parse_json_form('childrenrequirementcreate')
    ret = RequirementBusiness.requirement_children_create(title, project_id, version, board_status, handler,
                                                          description,
                                                          comment, priority, requirement_type, attach, parent_id,
                                                          jira_id, worth, report_time, report_expect, report_real,
                                                          worth_sure, case_ids, tag, expect_time=expect_time)
    return json_detail_render(ret)


# 发起评审
@requirement.route('/review', methods=['POST'])
@required(modify_permission)
@validation('POST:review_create')
def review_requirement():
    (title, requirement_list, project_id, version_id, creator, modifier, reviewer, status, attach,
     comment, weight, review_status) = parse_json_form('review_create')
    ret = RequirementReviewBusiness.review_create(title, requirement_list, project_id, version_id, creator, modifier,
                                                  reviewer, status, attach, comment, weight, review_status)
    return json_detail_render(ret)


# 评审评论
@requirement.route('/review/comment/<int:review_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:review_comment')
def review_comment_requirement(review_id):
    comment, result = parse_json_form('review_comment')
    RequirementReviewBusiness.review_modify(review_id, comment, result)

    # 数据同步到需求列表中
    ret = RequirementBusiness.review_modify(result)
    return json_detail_render(ret)


# 评审查询
@requirement.route('/review', methods=['GET'])
def review_query_all_handler():
    page_size = request.args.get('page_size')
    page_index = request.args.get('page_index')

    data, count = RequirementReviewBusiness.paginate_data(page_size, page_index)
    return {'code': 0, 'data': data, 'page_size': page_size, 'page_index': page_index, 'count': count}


# 评审单个查询
@requirement.route('/review/<int:review_id>', methods=['GET'])
def review_id_query_handler(review_id):
    code, data = RequirementReviewBusiness.query_review_by_id(review_id)
    return json_detail_render(code, data)


# 删除评审
@requirement.route('/review/<int:review_id>', methods=['DELETE'])
def review_id_delete_handler(review_id):
    """
    @api {dalete} /v1/requirement/review/{review_id} 删除评审
    @apiName DeleteReview
    @apiGroup 项目
    @apiDescription 删除评审
    @apiParamExample {json} Request-Example:
    无
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    ret = RequirementReviewBusiness.review_delete(review_id)
    return json_detail_render(ret)
