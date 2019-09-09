from apps.auth.auth_require import required
from apps.project.business.version import VersionBusiness
from apps.project.extentions import parse_json_form, validation
from library.api.render import json_detail_render
from library.api.tBlueprint import tblueprint

bpname = 'version'
view_permission = f'{bpname}_view'
modify_permission = f'{bpname}_modify'
version = tblueprint(bpname, __name__, has_view=False)


# 版本新增
@version.route('/', methods=['POST'])
@required(modify_permission)
@validation('POST:versioncreate')
def version_add_handler():
    """
    @api {post} /v1/version/ 新增版本
    @apiName CreateVersion
    @apiGroup 项目
    @apiDescription 新增版本
    @apiParam {string} title 标题
    @apiParam {int} project_id 项目ID
    @apiParam {string} start_time 版本开始时间
    @apiParam {string} end_time 版本结束时间
    @apiParam {int} creator 创建人
    @apiParam {int} publish_status 发布状态0：未发布1：已发布
    @apiParam {string} description 描述
    @apiParam {string} comment 备注
    @apiParamExample {json} Request-Example:
    {
        "title": "str",
        "project_id": 1,
        "start_time": "2018-11-11",
        "end_time": "2018-11-11",
        "creator": 1,
        "publish_status": 1,
        "description": "str",
        "comment": "str"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[],
    "message":"ok"
    }
    """
    title, project_id, start_time, end_time, description = parse_json_form('versioncreate')
    ret = VersionBusiness.version_create(title, project_id, start_time, end_time, description)

    return json_detail_render(ret)


# 版本单个修改
@version.route('/<int:version_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:versionmodify')
def version_modify_handler(version_id):
    """
    @api {post} /v1/version/{version_id} 修改版本
    @apiName ModifyVersion
    @apiGroup 项目
    @apiDescription 修改版本
    @apiParam {string} title 标题
    @apiParam {int} project_id 项目ID
    @apiParam {string} start_time 版本开始时间
    @apiParam {string} end_time 版本结束时间
    @apiParam {int} publish_status 发布状态0：未发布1：已发布
    @apiParam {string} description 描述
    @apiParam {string} comment 备注
    @apiParamExample {json} Request-Example:
    {
        "title": "str",
        "project_id": 1,
        "start_time": "2018-11-11",
        "end_time": "2018-11-11",
        "publish_status": 1,
        "description": "str",
        "comment": "str"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[],
    "message":"ok"
    }
    """
    title, start_time, end_time, description = parse_json_form('versionmodify')
    ret = VersionBusiness.version_modify(version_id, title, start_time, end_time, description)
    return json_detail_render(ret)


# 版本单个删除
@version.route('/<int:version_id>', methods=['DELETE'])
def version_delete_handler(version_id):
    """
    @api {dalete} /v1/version/{id} 删除版本
    @apiName DeleteProject
    @apiGroup 项目
    @apiDescription 删除版本
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
    ret = VersionBusiness.version_delete(version_id)
    return json_detail_render(ret)


# 版本发布
@version.route('/publish/<int:version_id>', methods=['POST'])
@required(modify_permission)
def version_publish_detail_handler(version_id):
    """
    @api {post} /v1/version/publish/{version_id} 发布版本
    @apiName PublishVersion
    @apiGroup 项目
    @apiDescription 发布版本
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
    ret = VersionBusiness.version_publish(version_id)

    return json_detail_render(ret)


# 版本查询-projectid,versionid,publishstatus
@version.route('/', methods=['GET'])
def version_query_all_handler():
    """
    @api {post} /v1/version/ 查询版本
    @apiName ModifyVersion
    @apiGroup 项目
    @apiDescription 查询版本
    @apiParam {int} versionid 标题
    @apiParam {int} project_id 项目ID
    @apiParam {int} publishstatus 版本开始时间
    @apiParamExample {json} Request-Example:
    ?projectid=4
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "comment":"",
                "creation_time":"2019-07-24",
                "creator":[
                    {
                        "id":5,
                        "name":"周培丽hello"
                    }
                ],
                "description":"str",
                "end_time":"2019-07-24",
                "id":168,
                "project_id":4,
                "publish_status":0,
                "publish_time":"",
                "start_time":"2019-07-24",
                "status":0,
                "taskinfo":[
                    {
                        "attach":"",
                        "case_list":[
                            3891
                        ],
                        "creator":[
                            {
                                "id":26,
                                "name":"张素浈"
                            }
                        ],
                        "description":"",
                        "end_time":"2019-07-31",
                        "executor":[
                            {
                                "id":26,
                                "name":"张素浈"
                            }
                        ],
                        "id":154,
                        "name":"sztest 字段修改",
                        "priority":1,
                        "project_id":4,
                        "start_time":"2019-07-29",
                        "status":3,
                        "tag":"",
                        "testreport":"",
                        "tmethod":"自动化测试",
                        "ttype":"功能测试",
                        "version_id":168
                    }
                ]
            }
        ],
        "message":"ok"
    }
    """
    data = VersionBusiness.query_all_json()

    return json_detail_render(0, data)


# 版本单个查询
@version.route('/<int:version_id>', methods=['GET'])
def version_query_handler(version_id):
    """
    @api {post} /v1/version/{version_id} 查询单个版本
    @apiName GetOneVersion
    @apiGroup 项目
    @apiDescription 查询单个版本
    @apiParamExample {json} Request-Example:
    无
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "comment":"",
                "creation_time":"2019-07-22",
                "creator":[
                    {
                        "id":5,
                        "name":"周培丽hello"
                    }
                ],
                "description":"撒发达发达是啊记得发货大家看法和安科技记得发货卡空军的发挥",
                "end_time":"2019-07-23",
                "id":167,
                "project_id":4,
                "publish_status":0,
                "publish_time":"",
                "start_time":"2019-07-22",
                "status":0,
                "title":"1.2.4"
            }
        ],
        "message":"ok"
    }
    """
    data = VersionBusiness.query_by_id(version_id)

    return json_detail_render(0, data)
