import json

from flask import Blueprint, request

from apps.interface.business.interfaceproject import InterfaceProjectBusiness

interfaceproject = Blueprint("interfaceproject", __name__)


@interfaceproject.route('/proGather/list', methods=['POST'])
def get_pro_gather():
    """
    @api {post} /v1/interfaceproject/proGather/list InterfaceProject_获取项目的基本信息
    @apiName interfaceProGatherList
    @apiGroup Interface
    @apiDescription 获取项目的基本信息
    @apiParam  {int} all_project_id 总项目id
    @apiParamExample {json} Request-Example:
    {
        "all_project_id":4
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "config_name_list": {
            "实惠喵": [],
            "测试": [],
            "测试平台": [],
            "萌推接口测试": [
                {
                    "configId": 7,
                    "name": "萌推mpark"
                },
                {
                    "configId": 8,
                    "name": "登录账号"
                }
            ]
        },
        "data": {
            "123": [
                {
                    "moduleId": 24,
                    "name": "123"
                }
            ],
            "ceshi ": [],
            "mengtui": [
                {
                    "moduleId": 14,
                    "name": "haha"
                },
                {
                    "moduleId": 1,
                    "name": "login"
                },
                {
                    "moduleId": 15,
                    "name": "88888"
                },
                {
                    "moduleId": 16,
                    "name": "999"
                },
                {
                    "moduleId": 21,
                    "name": "频道"
                },
                {
                    "moduleId": 22,
                    "name": "342423"
                }
            ],
            "mengtuiApi": [
                {
                    "moduleId": 6,
                    "name": "buyer_public_api"
                },
                {
                    "moduleId": 7,
                    "name": "萌熊活动"
                }
            ]
            ]
        },
        "pro_and_id": [
            {
                "id": 1,
                "name": "mengtui"
            },
            {
                "id": 3,
                "name": "shmiao"
            }
        ],
        "scene_list": {
            "1": [
                {
                    "id": 84,
                    "label": "test1"
                }
            ],
            "23": [
                {
                    "id": 86,
                    "label": "登录"
                }
            ]
        },
        "set_list": {
            "123": [],
            "ceshi ": [],
            "mengtui": [
                {
                    "id": 21,
                    "label": "1231231"
                }
            ],
            "mengtuiApi": [
                {
                    "id": 13,
                    "label": "商品详情"
                }
            ],
            "shm": [
                {
                    "id": 23,
                    "label": "登录"
                }
            ],
            "shmiao": [
                {
                    "id": 2,
                    "label": "登录集"
                },
                {
                    "id": 22,
                    "label": "登录"
                }
            ],
            "test": [],
            "哈哈哈": [
                {
                    "id": 17,
                    "label": "呃呃呃"
                }
            ],
            "实惠喵": [
                {
                    "id": 10,
                    "label": "enen"
                }
            ],
            "测试": [],
            "测试平台": [],
            "萌推接口测试": [
                {
                    "id": 14,
                    "label": "萌推乐园"
                },
                {
                    "id": 15,
                    "label": "萌推乐园碎片blablabla"
                }
            ]
        },
        "status": 1,
        "urlData": {
            "测试平台": [],
            "萌推接口测试": [
                "http://sx.api.mengtuiapp.com"
            ]
        },
        "user_pro": {
            "model_list": [
                {
                    "moduleId": 14,
                    "name": "haha"
                }
            ],
            "pro_name": "mengtui"
        }
    }
    """
    data = request.json
    all_project_id = data.get('all_project_id')
    jsondata = InterfaceProjectBusiness.get_pro_gather(all_project_id)
    return jsondata


@interfaceproject.route('/add', methods=['POST'])  # 项目新增和修改
def project_index_handler():
    """
    @api {post} /v1/interfaceproject/add InterfaceProject_项目新增和修改
    @apiName interfaceProAddAndUpdate
    @apiGroup Interface
    @apiDescription 项目新增和修改
    @apiParam {string} projectName  项目名称
    @apiParam {string} host 测试环境ip
    @apiParam {string} hostTwo 开发环境ip
    @apiParam {string} hostThree 线上环境ip
    @apiParam {string} hostFour 备用环境ip
    @apiParam {string} environmentChoice环境选择
    @apiParam {int} id 子项目id
    @apiParam {string} header 项目的公共头部信息
    @apiParam {string} description 项目的描述
    @apiParam {int} all_project_id总项目id
    @apiParam {int} userId 用户id
    @apiParamExample {json} Request-Example:
    {
        "all_project_id": 1,
        "environmentChoice":"first",
        "header":"[]",
        "host":["http://sx.api.com"],
        "hostTwo":[],
        "hostThree":[],
        "hostFour":[],
        "id":null,
        "principal": null,
        "projectName":"test1",
        "userId":117,
        "variable":"[]"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "新建成功",
        "status": 1
    }
    """
    data = request.json
    project_name = data.get('projectName')
    host = json.dumps(data.get('host'))
    host_two = json.dumps(data.get('hostTwo'))
    host_three = json.dumps(data.get('hostThree'))
    host_four = json.dumps(data.get('hostFour'))
    environment_choice = data.get("environmentChoice")
    ids = data.get('id')
    headers = data.get('header')
    variables = data.get('variable')
    description = ''
    all_project_id = data.get('all_project_id')
    user_id = data.get('userId')

    jsondata = InterfaceProjectBusiness.project_index_handler(project_name, host, host_two, host_three, host_four,
                                                              environment_choice, ids, headers, variables, description,
                                                              all_project_id, user_id
                                                              )
    return jsondata


@interfaceproject.route('/find', methods=['POST'])
def find_project():
    """
    @api {post} /v1/interfaceproject/find InterfaceProject_查找项目
    @apiName interfaceProFind
    @apiGroup Interface
    @apiDescription 查找项目
    @apiParam {string} projectName项目名称
    @apiParam {int} page 页数
    @apiParam {int} sizePage 当前页数的数量
    @apiParam {int}  all_project_id 总项目id

    @apiParamExample {json} Request-Example:
    {
        "projectName": null,
        "page":1,
        "sizePage":10,
        "all_project_id":4
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "status": 1,
        "total":13
        "userData": [
            {
                "user_id": 120,
                "user_name": "shiyao@innotechx.com",
            }
        ],
        "data": [
            {
                "choice": "first",
                "host": "["http://sx.api.mengtuiapp.com"]",
                "host_four": "[]",
                "host_three": "[]",
                "host_two": "[]",
                "id":1,
                "name": "mengtui",
                "pricipal": ""
            }
        ]
    }
    """
    data = request.json
    project_name = None
    if data and 'projectName' in data:
        project_name = data.get('projectName')
    page = 1
    if data and 'page' in data:
        page = data.get('page')
    per_page = 10
    if data and 'sizePage' in data:
        per_page = data.get('sizePage')
    all_project_id = data.get('all_project_id')
    jsondata = InterfaceProjectBusiness.find_project(project_name, page, per_page, all_project_id)
    return jsondata


@interfaceproject.route('/edit', methods=['POST'])
def edit_project():
    """
    @api {post} /v1/interfaceproject/edit InterfaceProject_返回待编辑项目信息
    @apiName interfaceProEdit
    @apiGroup Interface
    @apiDescription 返回待编辑项目信息
    @apiParam {int} id 子项目id
    @apiParam {int} all_project_id 总项目id
    @apiParamExample {json} Request-Example:
    {
        "id": 1,
        "all_project_id": 4
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": {
            "environment_choice": "first",
            "headers": [],
            "host": [
                "http://sx.api.mengtuiapp.com"
            ],
            "host_four": [],
            "host_three": [],
            "host_two": [],
            "principal": null,
            "pro_name": "mengtui",
            "user_id": 3,
            "variables": []
        },
        "status": 1
    }
    """
    data = request.json
    pro_id = data.get('id')
    all_project_id = data.get('all_project_id')
    jsondata = InterfaceProjectBusiness.edit_project(pro_id, all_project_id)
    return jsondata


@interfaceproject.route('/del', methods=['POST'])
def del_project():
    """
    @api {post} /v1/interfaceproject/del InterfaceProject_删除项目
    @apiName interfaceProDel
    @apiGroup Interface
    @apiDescription 删除项目
    @apiParam {int} id 子项目id
    @apiParam {int} all_project_id 总项目id
    @apiParamExample {json} Request-Example:
    {
        "id": 1,
        "all_project_id": 4
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": {
            "environment_choice": "first",
            "headers": [],
            "host": [
                "http://sx.api.mengtuiapp.com"
            ],
            "host_four": [],
            "host_three": [],
            "host_two": [],
            "principal": null,
            "pro_name": "mengtui",
            "user_id": 3,
            "variables": []
        },
        "status": 1
    }
    """
    data = request.json
    ids = data.get('id')
    all_project_id = data.get('all_project_id')
    jsondata = InterfaceProjectBusiness.del_project(ids, all_project_id)
    return jsondata
