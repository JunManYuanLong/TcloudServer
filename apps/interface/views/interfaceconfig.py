from flask import Blueprint, request, jsonify

from apps.interface.business.interfaceconfig import InterfaceConfigBusiness
from apps.interface.models.interfaceconfig import InterfaceConfig
from apps.interface.util.utils import *

interfaceconfig = Blueprint('interfaceconfig', __name__)


@interfaceconfig.route('/add', methods=['POST'])
def add_scene_config():
    """
    @api {post} /v1/interfaceconfig/add InterfaceConfig_添加配置
    @apiName interfaceConfigAdd
    @apiGroup Interface
    @apiDescription 添加配置
    @apiParam {int} all_project_id 总项目id
    @apiParam {string} projectName 项目名称
    @apiParam {string} sceneConfigName 配置名称
    @apiParam {int} id 配置id
    @apiParam {dict} funcAddress 配置函数
    @apiParam {list} variable 配置参数
    @apiParam {int} num 排序
    @apiParamExample {json} Request-Example:
    {
        "all_project_id": 4,
        "projectName": "mengtui",
        "sceneConfigName": "test",
        "id": null,
        "funcAddress": [],
        "variable": "[{"key":null,"value":null,"remark":null}]",
        "num": null,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "新建成功",
        "status": 1
    }
    """
    data = request.json
    all_project_id = data.get('all_project_id')
    project_name = data.get('projectName')
    name = data.get('sceneConfigName')
    ids = data.get('id')
    func_address = json.dumps(data.get('funcAddress'))
    variable = data.get('variable')
    number = data.get('num')
    jsondata = InterfaceConfigBusiness.add_scene_config(all_project_id, project_name, name, ids, func_address, variable,
                                                        number)

    return jsondata


@interfaceconfig.route('/find', methods=['POST'])
def find_config():
    """
    @api {post} /v1/interfaceconfig/find InterfaceConfig_查找配置
    @apiName interfaceConfigFind
    @apiGroup Interface
    @apiDescription 查找配置
    @apiParam {int} all_project_id 总项目id
    @apiParam {string} projectName 项目名称
    @apiParam {string} configName 配置名称
    @apiParam {int} page 页数
    @apiParam {int} sizePage 页面数量
    @apiParamExample {json} Request-Example:
    {
        "all_project_id": 4,
        "projectName": "mengtui",
        "configName": null,
        "page": 1,
        "sizePage": 10
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": [
            {
                "func_address": "[\"shm.py\"]",
                "id": 11,
                "name": "手机号",
                "num": 1
            },
            {
                "func_address": "[]",
                "id": 13,
                "name": "test",
                "num": 2
            }
        ],
        "status": 1,
        "total": 2
    }
    """
    data = request.json
    all_project_id = data.get('all_project_id')
    project_name = data.get('projectName')
    config_name = data.get('configName')
    page = data.get('page') if data.get('page') else 1
    per_page = data.get('sizePage') if data.get('sizePage') else 10
    jsondata = InterfaceConfigBusiness.find_config(all_project_id, project_name, config_name, page, per_page)

    return jsondata


@interfaceconfig.route('/del', methods=['POST'])
def del_config():
    """
    @api {post} /v1/interfaceconfig/del InterfaceConfig_删除配置
    @apiName interfaceConfigDel
    @apiGroup Interface
    @apiDescription 删除配置
    @apiParam {int} id 配置id
    @apiParamExample {json} Request-Example:
    {
        "id": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "删除成功",
        "status": 1,
    }
    """
    data = request.json
    ids = data.get('id')
    # _edit = InterfaceConfig.query.filter_by(id=ids).first()
    # if current_user.id != Project.query.filter_by(id=_edit.project_id).first().user_id:
    #     return jsonify({'msg': '不能删除别人项目下的配置', 'status': 0})
    # db.session.delete(_edit)
    InterfaceConfigBusiness.config_delete(ids)
    return jsonify({'msg': '删除成功', 'status': 1})


@interfaceconfig.route('/edit', methods=['POST'])
# @login_required
def edit_config():
    """
    @api {post} /v1/interfaceconfig/edit InterfaceConfig_返回待编辑配置信息
    @apiName interfaceConfigEdit
    @apiGroup Interface
    @apiDescription 返回待编辑配置信息
    @apiParam {int} id 配置id
    @apiParamExample {json} Request-Example:
    {
        "id": 11,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": {
            "func_address": [
                "shm.py"
            ],
            "name": "手机号",
            "num": 1,
            "variables": [
                {
                    "key": "phone",
                    "remark": null,
                    "value": "10055660001"
                }
            ]
        },
        "status": 1
    }
    """
    data = request.json
    ids = data.get('id')
    _edit = InterfaceConfig.query.filter_by(id=ids, status=InterfaceConfig.ACTIVE).first()
    _data = {
        'name': _edit.name,
        'num': _edit.num,
        'variables': json.loads(_edit.variables),
        'func_address': json.loads(_edit.func_address)
    }
    return jsonify({'data': _data, 'status': 1})
