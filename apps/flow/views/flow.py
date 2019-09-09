from flask import request

from apps.auth.auth_require import required
from apps.flow.business.deploy import DeployLogBusiness
from apps.flow.business.flow import FlowBusiness
from apps.flow.extentions import validation, parse_json_form, parse_list_args2
from library.api.render import json_detail_render, json_list_render2
from library.api.tBlueprint import tblueprint

bpname = 'flow'
view_permission = f'{bpname}_view'
modify_permission = f'{bpname}_modify'
flow = tblueprint(bpname, __name__)


# 流程新增
@flow.route('/', methods=['POST'])
@validation('POST:flow_create')
@required(modify_permission)
def flow_add_handler():
    """
    @api {post} /v1/flow/ 新增 流程
    @apiName CreateFlow
    @apiGroup 流程
    @apiDescription 新增流程
    @apiParam {int} flow_type 流程类型
    @apiParam {int} flow_assemble_id 流程集合
    @apiParam {int} [priority] 优先级
    @apiParam {int} project_id 项目ID
    @apiParam {int} version_id 版本ID
    @apiParam {int} creator 创建用户ID
    @apiParam {int} weight 权重
    @apiParam {str} name 流程名称
    @apiParam {str} requirement_list 需求列表
    @apiParam {str} action 步骤
    @apiParam {str} dependence 上线依赖
    @apiParam {str} comment 备注
    @apiParam {list} platform 涉及端
    @apiParam {list} user_owner 流程负责人
    @apiParam {list} user_test 流程测试
    @apiParam {list} user_prod 流程产品
    @apiParam {list} user_dev 流程开发
    @apiParamExample {json} Request-Example:
    {
        "name": "str",
        "flow_type": 1,
        "requirement_list": "str",
        "flow_assemble_id": 1,
        "priority": 1,
        "project_id": 1,
        "version_id": 1,
        "creator": 1,
        "user_dev": [1],
        "user_prod": [1,3],
        "user_test": [1],
        "user_owner": [1,3],
        "action": "str",
        "platform": [1,3],
        "dependence": "dependence",
        "weight": 1,
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
    (name, flow_type, requirement_list, flow_assemble_id, priority, project_id, version_id, creator, user_dev,
     user_prod, user_test, user_owner, action, weight, comment, platform, dependence) = parse_json_form('flow_create')

    ret, data = FlowBusiness.flow_create(name, flow_type, requirement_list, flow_assemble_id, priority, project_id,
                                         version_id, creator, user_dev, user_prod, user_test, user_owner, action,
                                         weight, comment, platform, dependence)
    return json_detail_render(ret, data)


# 流程单个修改
@flow.route('/<int:flow_id>', methods=['POST'])
@validation('POST:flow_modify')
@required(modify_permission)
def flow_modify_handler(flow_id):
    """
    @api {post} /v1/flow/{flow_id} 修改流程
    @apiName ModifyFlow
    @apiGroup 流程
    @apiDescription 修改流程
    @apiParam {int} [priority] 优先级
    @apiParam {int} weight 权重
    @apiParam {str} name 流程名称
    @apiParam {str} dependence 上线依赖
    @apiParam {str} comment 备注
    @apiParam {list} platform 涉及端
    @apiParam {list} user_owner 流程负责人
    @apiParam {list} user_test 流程测试
    @apiParam {list} user_prod 流程产品
    @apiParam {list} user_dev 流程开发
    @apiParamExample {json} Request-Example:
    {
        "name": "str",
        "priority": 1,
        "user_dev": [1],
        "user_prod": [1,3],
        "user_test": [1],
        "user_owner": [1,3],
        "action": "str",
        "platform": [1,3],
        "dependence": "dependence",
        "weight": 1,
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
    name, priority, user_dev, user_prod, user_test, user_owner, weight, comment, dependence = parse_json_form(
        'flow_modify')
    ret, msg = FlowBusiness.flow_modify(flow_id, name, priority, user_dev, user_prod, user_test, user_owner, weight,
                                        comment, dependence)
    return json_detail_render(ret, [], msg)


# 流程单个删除
@flow.route('/<int:flow_id>', methods=['DELETE'])
def flow_delete_handler(flow_id):
    """
    @api {delete} /v1/flow/{flow_id} 删除流程
    @apiName DeleteFlow
    @apiGroup 流程
    @apiDescription 删除流程
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
    ret, msg = FlowBusiness.flow_delete(flow_id)
    return json_detail_render(ret, message=msg)


# 流程终止
@flow.route('/stop/<int:flow_id>', methods=['POST'])
def flow_stop_handler(flow_id):
    """
    @api {post} /v1/flow/stop/{flow_id} 终止流程
    @apiName StopFlow
    @apiGroup 流程
    @apiDescription 终止流程
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
    ret, msg = FlowBusiness.flow_stop(flow_id)
    return json_detail_render(ret, message=msg)


# 执行流程
@flow.route('/next/<int:flow_id>', methods=['POST'])
@validation('POST:flow_next')
def flow_priority_switch_handler(flow_id):
    """
    @api {post} /v1/flow/next/{flow_id} 执行流程
    @apiName NextFlow
    @apiGroup 流程
    @apiDescription 执行流程
    @apiParam {int} id 步骤ID
    @apiParam {str} name 名称
    @apiParam {str} result 结果
    @apiParam {str} comment 备注
    @apiParamExample {json} Request-Example:
    {
        "id":2,
        "name":"测试新版流程（+涉及端和上线依赖)2",
        "result":"6",
        "comment":"<p>pass</p>"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    _id, name, result, comment = parse_json_form('flow_next')
    ret, msg = FlowBusiness.flow_next(flow_id, _id, name, result, comment)
    return json_detail_render(ret, [], msg)


# 流程查询-projectid,version_idid
@flow.route('/', methods=['GET'])
def flow_query_all_handler():
    """
    @api {get} /v1/flow/ 查询流程
    @apiName GetFlow
    @apiGroup 流程
    @apiDescription 查询流程
    @apiParam {int} projectid 项目ID
    @apiParam {int} versionid 版本ID
    @apiParam {str} status 状态
    @apiParam {str} name 名称
    @apiParam {int} userid 用户ID
    @apiParam {str} start_time 开始时间
    @apiParam {str} end_time 结束时间
    @apiParam {int} flow_assemble_id 流程集合ID
    @apiParam {str} flow_type 备注
    @apiParam {int} flow_id 流程ID
    @apiParam {list} platform 涉及端
    @apiParam {int} page_size 每页条数
    @apiParam {int} page_index 第几页
    @apiParamExample {json} Request-Example:
    ?projectid=4&name=&page_size=10&page_index=1&status=0&flow_assemble_id=&flow_type=&flow_id=261
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[
        {
            "action":{
                "current_step":"2",
                "current_step_name":"开发自测",
                "process":0,
                "step_tab":[
                    {
                        "step_tab_id":"6",
                        "step_tab_name":"备注",
                        "step_tab_result":"会停留在当前步骤",
                        "step_tab_user":"刘德华,张宇"
                    },
                    {
                        "step_tab_id":"1",
                        "step_tab_name":"通过",
                        "step_tab_result":"会跳转到下一步",
                        "step_tab_user":"刘德华,张宇"
                    }
                ],
                "steps":[

                ]
            },
            "all_user_list":[
                96,
                20
            ],
            "comment":"<p>asdsad</p>",
            "creator_id":96,
            "creator_name":"张宇",
            "dependence":"",
            "end_time":"",
            "flow_assemble_id":4,
            "flow_assemble_name":"HotFix",
            "flow_assemble_type":1,
            "flow_base_list":"2,7,11,12,16",
            "flow_type":2,
            "id":261,
            "name":"asdsada",
            "picture":"https://p.qlogo.cn/bizmail/WRZVs2uMphoxc2918UvZzL31u6A9ibTNuqnIibzJ4GxjWIVVDxHvUGuA/0",
            "platform":"",
            "priority":"",
            "project_id":4,
            "requirement_list":"",
            "start_time":"2019-07-22 21:40:54",
            "status":0,
            "user_dev":[
                {
                    "user_id":96,
                    "user_name":"张宇"
                }
            ],
            "user_dev_id":[
                96
            ],
            "user_owner":[
                {
                    "user_id":20,
                    "user_name":"刘德华"
                }
            ],
            "user_owner_id":[
                20
            ],
            "user_prod":[
                {
                    "user_id":96,
                    "user_name":"张宇"
                }
            ],
            "user_prod_id":[
                96
            ],
            "user_test":[
                {
                    "user_id":96,
                    "user_name":"张宇"
                }
            ],
            "user_test_id":[
                96
            ],
            "version_id":"",
            "weight":1
        }
    ],
    "message":"ok",
    "page_index":1,
    "page_size":10,
    "total":1
    }
    """
    page_size, page_index = parse_list_args2()
    data, count, code = FlowBusiness.query_all_json(page_size, page_index)
    return json_list_render2(code, data, page_size, page_index, count)


@flow.route('/row/export', methods=['GET'])
def flow_info_export():
    """
    @api {post} /row/export 导出流程列表
    @apiName ExportFlow
    @apiGroup 流程
    @apiDescription 导出流程列表
    @apiParam {int} projectid 项目ID
    @apiParam {int} versionid 版本ID
    @apiParam {str} status 状态
    @apiParam {str} name 名称
    @apiParam {int} userid 用户ID
    @apiParam {str} start_time 开始时间
    @apiParam {str} end_time 结束时间
    @apiParam {int} flow_assemble_id 流程集合ID
    @apiParam {str} flow_type 备注
    @apiParam {int} flow_id 流程ID
    @apiParam {list} platform 涉及端
    @apiParamExample {json} Request-Example:
    ?projectid=4&name=&status=0&flow_assemble_id=&flow_type=&flow_id=261
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    data = FlowBusiness.flow_export()
    return json_detail_render(0, data)


@flow.route('/resource', methods=['GET'])
def resource():
    """
    @api {post} /resource 查询流程资源
    @apiName GetResource
    @apiGroup 流程
    @apiDescription 查询流程资源
    @apiParam {int} projectid 项目ID
    @apiParam {str} users 用户ID，逗号分隔
    @apiParamExample {json} Request-Example:
    ?projectid=4&users=9,12
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "flows":{
                    "active":[
                        {
                            "id":158,
                            "name":"6/18流程1",
                            "step":"功能测试"
                        },
                        {
                            "id":139,
                            "name":"流程3",
                            "step":"开发自测"
                        },
                        {
                            "id":107,
                            "name":"流程111",
                            "step":"提测"
                        }
                    ],
                    "finished":[

                    ]
                },
                "total_active":3,
                "total_finished":0,
                "user_id":"9",
                "user_name":"黄立平"
            },
            {
                "flows":{
                    "active":[
                        {
                            "id":106,
                            "name":"dsfa ",
                            "step":"开发自测"
                        },
                        {
                            "id":96,
                            "name":"test",
                            "step":"提测"
                        }
                    ],
                    "finished":[

                    ]
                },
                "total_active":2,
                "total_finished":0,
                "user_id":"12",
                "user_name":"刘焕焕"
            }
        ],
    "message":"ok"
    }
    """
    users = request.args.get('users')
    project_id = request.args.get('projectid')
    data = FlowBusiness.flow_info_by_users(users, project_id)
    return json_detail_render(0, data)


@flow.route('/resource/export', methods=['GET'])
def resource_export():
    """
    @api {post} /resource/export 导出流程资源
    @apiName ExportResource
    @apiGroup 流程
    @apiDescription 导出流程资源
    @apiParam {int} projectid 项目ID
    @apiParam {str} users 用户ID
    @apiParamExample {json} Request-Example:
    {
        "project_id":4,
        "user_ids":"[9,12]"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    users = request.args.get('users')
    project_id = request.args.get('projectid')
    code, data = FlowBusiness.export_resource(users, project_id)
    return json_detail_render(code, data)


# 流程单个查询
@flow.route('/<int:flow_id>', methods=['GET'])
def flow_query_handler(flow_id):
    """
    @api {get} /v1/flow/{flow_id} 查询单个流程
    @apiName GetSingleFlow
    @apiGroup 流程
    @apiDescription 查询单个流程
    @apiParamExample {json} Request-Example:
    无
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "action":{
                    "current_step":"2",
                    "current_step_name":"开发自测",
                    "process":0,
                    "step_tab":[
                        {
                            "step_tab_id":"6",
                            "step_tab_name":"备注",
                            "step_tab_result":"会停留在当前步骤",
                            "step_tab_user":"张宇"
                        },
                        {
                            "step_tab_id":"1",
                            "step_tab_name":"通过",
                            "step_tab_result":"会跳转到下一步",
                            "step_tab_user":"张宇"
                        }
                    ],
                    "steps":[
                        {
                            "comment":"<p>pass</p>",
                            "creation_time":"2019-07-29 20:06:51",
                            "id":2,
                            "name":"测试新版流程（+涉及端和上线依赖)2",
                            "result":"6",
                            "user_id":104,
                            "user_name":"刘德华153"
                        }
                    ]
                },
                "all_user_list":[
                    96,
                    104
                ],
                "comment":"<p>测试新版流程（+涉及端和上线依赖)</p>",
                "creator_id":96,
                "creator_name":"张宇",
                "dependence":"",
                "end_time":"",
                "flow_assemble_id":3,
                "flow_assemble_name":"SkipTest",
                "flow_assemble_type":1,
                "flow_base_list":"2,6,7,11,12,16",
                "flow_type":2,
                "id":270,
                "name":"测试新版流程（+涉及端和上线依赖)2",
                "picture":"https://p.qlogo.cn/bizmail/WRZVs2uMphoxc2918UvZzL31u6A9ibTNuqnIibzJ4GxjWIVVDxHvUGuA/0",
                "platform":"['APP', 'H5']",
                "priority":"",
                "project_id":4,
                "requirement_list":"",
                "start_time":"2019-07-29 19:39:30",
                "status":0,
                "user_dev":[
                    {
                        "user_id":96,
                        "user_name":"张宇"
                    }
                ],
                "user_dev_id":[
                    96
                ],
                "user_owner":[
                    {
                        "user_id":96,
                        "user_name":"张宇"
                    }
                ],
                "user_owner_id":[
                    96
                ],
                "user_prod":[
                    {
                        "user_id":96,
                        "user_name":"张宇"
                    }
                ],
                "user_prod_id":[
                    96
                ],
                "user_test":[
                    {
                        "user_id":104,
                        "user_name":"刘德华153"
                    }
                ],
                "user_test_id":[
                    104
                ],
                "version_id":"",
                "weight":""
            }
        ],
        "message":"ok"
    }
    """
    data = FlowBusiness.query_by_id(flow_id)

    deploy_log_data = DeployLogBusiness.query_all_json(flow_id)

    for i in range(0, len(deploy_log_data)):
        deploy_log_data[i]['id'] = deploy_log_data[i]['result_id']

    if len(deploy_log_data) > 0:
        data[0]['action']['steps'].extend(deploy_log_data)
        all_data = data[0]['action']['steps']

        # 排序
        data[0]['action']['steps'] = sorted(all_data, key=lambda e: e.__getitem__('creation_time'))

    return json_detail_render(0, data)


# 流程基表查询
@flow.route('/base', methods=['GET'])
def flow_base_query_all_handler():
    """
    @api {get} /v1/flow/base 获取流程基表
    @apiName GetBase
    @apiGroup 流程
    @apiDescription 获取流程基表
    @apiParamExample {json} Request-Example:
    无
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "id":1,
                "name":"分支开发",
                "step":[
                    {
                        "6":"备注"
                    },
                    {
                        "2":"不通过"
                    },
                    {
                        "1":"通过"
                    },
                    {
                        "3":"跳过"
                    }
                ]
            }
        ],
        "message":"ok"
    }
    """
    data = FlowBusiness.query_base_all_json()
    return json_detail_render(0, data)


# 流程集合查询
@flow.route('/assemble', methods=['GET'])
def flow_assemble_query_all_handler():
    """
    @api {get} /v1/flow/assemble 获取流程集合
    @apiName GetAssemble
    @apiGroup 流程
    @apiDescription 获取流程集合
    @apiParamExample {json} Request-Example:
    无
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "comment":"",
                "flow_base_list":"2,4,7,11,12,16",
                "id":5,
                "name":"HotFix（需QA验证）",
                "project_id":"",
                "weight":1
            },
            {
                "comment":"",
                "flow_base_list":"3,4,5,8,9,10,13,14,15,16",
                "id":1,
                "name":"客户端",
                "project_id":1,
                "weight":1
            }
        ],
        "message":"ok"
    }
    """
    data = FlowBusiness.query_assemble_all_json()
    return json_detail_render(0, data)


# 每日新增流程数查询,流程数的总耗时和平均耗时
@flow.route('/dashboard', methods=['POST'])
@required(view_permission)
@validation('POST:flowdashboard')
def flow_day_query_all_handler():
    """
    @api {post} /v1/flow/dashboard 获取流程统计
    @apiName GetFlowDashboard
    @apiGroup 流程
    @apiDescription 获取流程统计
    @apiParam {int} project_id 项目ID
    @apiParam {str} start_date 开始时间
    @apiParam {str} end_date 结束时间
    @apiParamExample {json} Request-Example:
    {
        "project_id":1,
        "start_date":"2019-07-26",
        "end_date":"2019-07-26"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    project_id, start_date, end_date = parse_json_form('flowdashboard')
    data = FlowBusiness.flow_add_dashboard(project_id, start_date, end_date)
    return json_detail_render(0, data)


# 新增用户的flow——user配置
@flow.route('/source', methods=['POST'])
@required(modify_permission)
@validation('POST:flowsource')
def flow_source_handler():
    """
    @api {post} /v1/flow/source 新增用户流程配置
    @apiName CreateSource
    @apiGroup 流程
    @apiDescription 新增用户流程配置
    @apiParam {int} project_id 项目ID
    @apiParam {str} user_ids 选择的用户list
    @apiParamExample {json} Request-Example:
    {
        "project_id":1,
        "user_ids":"[1,2,4,5,6]"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[],
        "message":"ok"
    }
    """
    project_id, user_ids, = parse_json_form('flowsource')
    code = FlowBusiness.flow_source_add(project_id, user_ids)
    return json_detail_render(code)


# 查询用户的flow——user配置
@flow.route('/getsource', methods=['POST'])
@required(view_permission)
@validation('POST:getflowsource')
def flow_source_query_handler():
    """
    @api {post} /v1/flow/getsource 获取用户流程配置
    @apiName GetSource
    @apiGroup 流程
    @apiDescription 获取用户流程配置
    @apiParam {int} project_id 项目ID
    @apiParam {int} user_id 用户ID
    @apiParamExample {json} Request-Example:
    {
        "project_id": 2,
        "user_id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "creator":17,
                "id":12,
                "project_id":1,
                "user_ids":"[1,2,4,5,6]"
            }
        ],
        "message":"ok"
    }
    """
    project_id, user_id = parse_json_form('getflowsource')
    data = FlowBusiness.flow_source_get(project_id, user_id)
    return json_detail_render(0, data=data)
