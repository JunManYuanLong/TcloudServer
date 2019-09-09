from apps.auth.auth_require import required
from apps.project.business.project import ProjectBusiness
from apps.project.extentions import parse_json_form, validation
from library.api.render import json_detail_render
from library.api.tBlueprint import tblueprint

bpname = 'project'
view_permission = f'{bpname}_view'
modify_permission = f'{bpname}_modify'
project = tblueprint(bpname, __name__, with_pid=False, has_view=False)


@project.route('/', methods=['POST'])
@required(modify_permission)
@validation('POST:addproject')
def project_indexs_handler():
    """
    @api {post} /v1/project/ 新增项目
    @apiName CreateProject
    @apiGroup 项目
    @apiDescription 新增项目
    @apiParam {string} name 项目名称
    @apiParam {string} description 描述
    @apiParam {string} logo logo图片
    @apiParamExample {json} Request-Example:
    {
        "name": "电梯贷款",
        "description": "description",
        "logo":"pic"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[],
    "message":"ok"
    }
    """
    name, description, logo = parse_json_form('addproject')
    ret, msg = ProjectBusiness.create_new_project(name, description, logo)

    return json_detail_render(ret, [], msg)


@project.route('/<int:pid>', methods=['POST'])
@required(modify_permission)
@validation('POST:modifyproject')
def project_details_handler(pid):
    """
    @api {post} /v1/project/{id} 修改项目
    @apiName ModifyProject
    @apiGroup 项目
    @apiDescription 修改项目
    @apiParam {string} name 项目名称
    @apiParam {string} description 描述
    @apiParam {string} logo logo图片
    @apiParam {int} weight 权重
    @apiParamExample {json} Request-Example:
    {
        "name": "电梯贷款",
        "description": "",
        "logo":"pic",
        "weight": 2
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[],
    "message":"ok"
    }
    """
    name, description, weight, logo = parse_json_form('modifyproject')
    ret, msg = ProjectBusiness.modify(pid, name, description, weight, logo)
    return json_detail_render(ret, [], msg)


@project.route('/<int:pid>', methods=['DELETE'])
def project_delete_handler(pid):
    """
    @api {dalete} /v1/project/{id} 删除项目
    @apiName DeleteProject
    @apiGroup 项目
    @apiDescription 删除项目
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
    ret = ProjectBusiness.close_project(pid)
    return json_detail_render(ret)


@project.route('/bindusers', methods=['POST'])
@required(modify_permission)
@validation('POST:projectbindusers')
def project_bind_users():
    """
    @api {post} /v1/project/bindusers 项目批量绑定用户
    @apiName BindUserForProject
    @apiGroup 项目
    @apiDescription 项目批量绑定用户
    @apiParam {list} user_ids 用户ID
    @apiParam {int} project_id 项目ID
    @apiParamExample {json} Request-Example:
    {
        "project_id": 75,
        "user_ids":[1]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[],
    "message":"ok"
    }
    """
    project_id, user_ids = parse_json_form('projectbindusers')
    ret, msg = ProjectBusiness.bind_users(project_id, user_ids)

    return json_detail_render(ret, [], msg)


@project.route('/', methods=['GET'])
def project_query_handler():
    """
    @api {post} /v1/project/ 查询项目
    @apiName GetProject
    @apiGroup 项目
    @apiDescription 查询项目
    @apiParam {list} userid 用户ID
    @apiParamExample {json} Request-Example:
    ?userid=1
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "description":"云测平台",
                "id":4,
                "logo":"http://tcloud-static.ywopt.com/static/44ee66b0-8d2f-4263-a7ea-ad7eb24c1f3f.png",
                "name":"云测平台66",
                "status":0,
                "user":[
                    {
                        "id":31,
                        "nickname":"开发"
                    }
                ],
                "weight":10
            }
        ],
        "message":"ok"
    }
    """
    data = ProjectBusiness.query_all_json()
    return json_detail_render(0, data)


@project.route('/<int:pid>', methods=['GET'])
def project_detail_handler(pid):
    """
    @api {get} /v1/project/{id} 查询单个项目
    @apiName GetOneProject
    @apiGroup 项目
    @apiDescription 查询单个项目
    @apiParamExample {json} Request-Example:
    无
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "description":"云测平台",
                "id":4,
                "logo":"http://tcloud-static.ywopt.com/static/44ee66b0-8d2f-4263-a7ea-ad7eb24c1f3f.png",
                "name":"云测平台66",
                "status":0,
                "user":[
                    {
                        "id":31,
                        "nickname":"开发"
                    }
                ],
                "weight":10
            }
        ],
        "limit":99999,
        "message":"ok",
        "offset":0
    }
    """
    data = ProjectBusiness.query_json_by_id(pid)
    return json_detail_render(0, data)


@project.route('/index/<int:pid>', methods=['GET'])
def project_index_handler(pid):
    """
    @api {get} /v1/project/index/{project_id} 项目面板
    @apiName DetachUserForProject
    @apiGroup 项目
    @apiDescription 项目面板
    @apiParam {int} start_time 用户ID
    @apiParam {int} end_time 项目ID
    @apiParamExample {json} Request-Example:
    ?start_time=2019-05-02&end_time=2019-07-31
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code":0,
        "data":[
            {
                "issue_info":[
                    {
                        "count":4,
                        "open":4,
                        "rank":72,
                        "version_id":168,
                        "version_title":"1.2.5啊啊"
                    }
                ],
                "issue_status":[
                    {
                        "count":9,
                        "handle_status":1
                    }
                ],
                "issue_sum":44,
                "requirement_info":[
                    {
                        "count":8,
                        "version_id":"130",
                        "version_title":"1.1.3"
                    }
                ],
                "requirement_sum":93,
                "task_info":[
                    {
                        "count":8,
                        "version_id":168,
                        "version_title":"1.2.5啊啊"
                    }
                ],
                "task_sum":45,
                "taskcase_sum":243
            }
        ],
        "message":"ok"
    }
    """
    data = ProjectBusiness.index(pid)
    return json_detail_render(0, data)


# 解除用户和项目的绑定的关系
@project.route('/detachusers', methods=['POST'])
@required(modify_permission)
@validation('POST:projectdetachusers')
def project_detach_users():
    """
    @api {post} /v1/project/bindusers 项目解绑用户
    @apiName DetachUserForProject
    @apiGroup 项目
    @apiDescription 项目解绑用户
    @apiParam {int} user_id 用户ID
    @apiParam {int} project_id 项目ID
    @apiParamExample {json} Request-Example:
    {
        "project_id": 75,
        "user_id":1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[],
    "message":"ok"
    }
    """
    project_id, user_id = parse_json_form('projectdetachusers')
    ret, msg = ProjectBusiness.detach_users(project_id, user_id)

    return json_detail_render(ret, [], msg)


# 批量增加用户到当前的项目中
@project.route('/adduser', methods=['POST'])
@required(modify_permission)
@validation('POST:projectadduser')
def project_add_users():
    """
    @api {post} /v1/project/adduser 项目绑定用户
    @apiName AddUserForProject
    @apiGroup 项目
    @apiDescription 项目绑定用户
    @apiParam {list} user_list 用户ID
    @apiParam {int} project_id 项目ID
    @apiParamExample {json} Request-Example:
    {
        "project_id": 75,
        "user_list":[1]
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
    "code":0,
    "data":[],
    "message":"ok"
    }
    """
    project_id, user_list = parse_json_form('projectadduser')
    ret, msg = ProjectBusiness.add_users(project_id, user_list)
    return json_detail_render(ret, [], msg)
