from flask import Blueprint, request, jsonify

from apps.interface.business.interfacemodule import InterfaceModuleBusiness
from apps.interface.models.interfacemodule import InterfaceModule

interfacemodule = Blueprint('interfacemodule', __name__)


@interfacemodule.route('/find', methods=['POST'])
def find_model():
    """
    @api {post} /v1/interfacemodule/find InterfaceModule_查找接口模块
    @apiName interfaceModuleFind
    @apiGroup Interface
    @apiDescription 查找接口模块
    @apiParam {string} projectName项目/模块名称
    @apiParam {int} page当前的页数
    @apiParam {int} sizePage 当前页数的数量
    @apiParamExample {json} Request-Example:
    {
        "projectName": "",
        "page": 1,
        "sizepage": 10
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "all_module": [
            {
                "moduleId": 2,
                "name": "单接口",
                "num": 1
            },
            {
                "moduleId": 11,
                "name": "用户签到",
                "num": 3
            },
            {
                "moduleId": 25,
                "name": "登录",
                "num": 4
            },
            {
                "moduleId": 27,
                "name": "test",
                "num": 5
            }
        ],
        "data": [
            {
                "moduleId": 2,
                "name": "单接口",
                "num": 1
            },
            {
                "moduleId": 11,
                "name": "用户签到",
                "num": 3
            },
            {
                "moduleId": 25,
                "name": "登录",
                "num": 4
            },
            {
                "moduleId": 27,
                "name": "test",
                "num": 5
            }
        ],
        "status": 1,
        "total": 4
    }
    """
    data = request.json
    page = data.get('page') if data.get('page') else 1
    per_page = data.get('sizePage') if data.get('sizePage') else 10
    project_name = data.get('projectName')
    jsondata = InterfaceModuleBusiness.find_model(page, per_page, project_name)

    return jsondata


@interfacemodule.route('/add', methods=['POST'])
def add_model():
    """
    @api {post} /v1/interfacemodule/add InterfaceModule_接口模块增加、编辑
    @apiName interfaceModuleAdd
    @apiGroup Interface
    @apiDescription 接口模块增加、编辑
    @apiParam {string} projectName  项目名称
    @apiParam {string} name  模块名字
    @apiParam {int} id  模块id
    @apiParam {int} num  排序
    @apiParamExample {json} Request-Example:
    {
        "projectName": "shmiao",
        "name": "test",
        "id": ""
        "num": ""
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
    name = data.get('name')
    ids = data.get('id')
    number = data.get('num')
    jsondata = InterfaceModuleBusiness.add_model(project_name, name, ids, number)
    return jsondata


@interfacemodule.route('/edit', methods=['POST'])
def edit_model():
    """
    @api {post} /v1/interfacemodule/edit InterfaceModule_返回待编辑模块信息
    @apiName interfaceModuleEdit
    @apiGroup Interface
    @apiDescription 返回待编辑模块信息
    @apiParam {int} id模块id
    @apiParamExample {json} Request-Example:
    {
        "id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": {},
        "status": 1
    }
    """
    data = request.json
    model_id = data.get('id')
    _edit = InterfaceModule.query.filter(InterfaceModule.id == model_id,
                                         InterfaceModule.status == InterfaceModule.ACTIVE).first()
    _data = {'gatherName': _edit.name, 'num': _edit.num}

    return jsonify({'data': _data, 'status': 1})


@interfacemodule.route('/del', methods=['POST'])
def del_model():
    """
    @api {post} /v1/interfacemodule/del InterfaceModule_删除模块
    @apiName interfaceModuleDel
    @apiGroup Interface
    @apiDescription 删除模块
    @apiParam {int} id 模块id
    @apiParamExample {json} Request-Example:
    {
        "id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "删除成功",
        "status": 1
    }
    """
    data = request.json
    ids = data.get('id')
    jsondata = InterfaceModuleBusiness.del_model(ids)
    return jsondata


@interfacemodule.route('/stick', methods=['POST'])
def stick_module():
    """
    @api {post} /v1/interfacemodule/stick InterfaceModule_置顶模块
    @apiName interfaceModuleStick
    @apiGroup Interface
    @apiDescription 置顶模块
    @apiParam {int} id 模块id
    @apiParam {string} projectName 项目名称
    @apiParamExample {json} Request-Example:
    {
        "id": 27,
        "projectName": "shmiao"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "置顶完成",
        "status": 1
    }
    """
    data = request.json
    module_id = data.get('id')
    project_name = data.get('projectName')
    jsondata = InterfaceModuleBusiness.stick_module(module_id, project_name)
    return jsondata
