from flask import Blueprint, request, jsonify

from apps.interface.business.interfacecaseset import InterfaceCaseSetBusiness
from apps.interface.models.interfacecase import InterfaceCase
from apps.interface.models.interfacecaseset import InterfaceCaseSet

interfacecaseset = Blueprint('interfacecaseset', __name__)


@interfacecaseset.route('/add', methods=['POST'])
def add_set():
    """
    @api {post} /v1/interfacecaseset/add InterfaceCaseSet_添加用例集合
    @apiName interfacecasesetAdd
    @apiGroup Interface
    @apiDescription 添加用例集合
    @apiParam {string} projectName 项目名称
    @apiParam {string} name 用例集名称
    @apiParam {int} id 用例集id
    @apiParam {int} num 用例集排序
    @apiParamExample {json} Request-Example:
    {
        "projectName": "mengtui",
        "name": "2222",
        "id": 24,
        "num": ""
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "修改成功"
        "status": 1
    }
    """
    data = request.json
    project_name = data.get('projectName')
    name = data.get('name')
    ids = data.get('id')
    number = data.get('num')
    jsondata = InterfaceCaseSetBusiness.add_set(project_name, name, ids, number)

    return jsondata


@interfacecaseset.route('/stick', methods=['POST'])
def stick_set():
    """
    @api {post} /v1/interfacecaseset/stick InterfaceCaseSet_置顶用例集合
    @apiName interfacecasesetStick
    @apiGroup Interface
    @apiDescription 置顶用例集合
    @apiParam {string} projectName 项目名称
    @apiParam {int} id 用例集id
    @apiParamExample {json} Request-Example:
    {
        "projectName": "mengtui",
        "id": 24,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "置顶完成"
        "status": 1
    }
    """
    data = request.json
    set_id = data.get('id')
    project_name = data.get('projectName')
    jsondata = InterfaceCaseSetBusiness.stick_set(set_id, project_name)
    return jsondata


@interfacecaseset.route('/find', methods=['POST'])
def find_set():
    """
    @api {post} /v1/interfacecaseset/find InterfaceCaseSet_查找用例集合
    @apiName interfacecasesetFind
    @apiGroup Interface
    @apiDescription 查找用例集合
    @apiParam {string} projectName 项目名称
    @apiParam {int} page 页数
    @apiParam {int} sizePage 页面数量
    @apiParamExample {json} Request-Example:
    {
        "projectName": "mengtui",
        "page": 1,
        "sizePage": 30
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "all_set": [
            {
                "id": 1,
                "label": "登陆集"
            }

        ],
        "data": [
            {
                "id": 1,
                "label": "登陆集"
            }
        ],
        "status": 1,
        "total": 1
    }
    """
    data = request.json
    page = data.get('page') if data.get('page') else 1
    per_page = data.get('sizePage') if data.get('sizePage') else 10
    project_name = data.get('projectName')
    jsondata = InterfaceCaseSetBusiness.find_set(page, per_page, project_name)
    return jsondata


@interfacecaseset.route('/edit', methods=['POST'])
def edit_set():
    """
    @api {post} /v1/interfacecaseset/edit InterfaceCaseSet_返回待编辑用例集合
    @apiName interfacecasesetEdit
    @apiGroup Interface
    @apiDescription 返回待编辑用例集合
    @apiParam {int} id 用例集id
    @apiParamExample {json} Request-Example:
    {
        "id": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": [
            {
                "id": 1,
                "label": "登陆集"
            }
        ],
        "status": 1,
    }
    """
    data = request.json
    set_id = data.get('id')
    _edit = InterfaceCaseSet.query.filter_by(id=set_id, status=InterfaceCaseSet.ACTIVE).first()
    _data = {'name': _edit.name, 'num': _edit.num}
    return jsonify({'data': _data, 'status': 1})


@interfacecaseset.route('/del', methods=['POST'])
def del_set():
    """
    @api {post} /v1/interfacecaseset/del InterfaceCaseSet_删除用例集合
    @apiName interfacecasesetDel
    @apiGroup Interface
    @apiDescription 删除用例集合
    @apiParam {int} id 用例集id
    @apiParamExample {json} Request-Example:
    {
        "id": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "status": 1,
        "msg": "删除成功"
    }
    """
    data = request.json
    set_id = data.get('id')
    # _edit = InterfaceCaseSet.query.filter_by(id=set_id).first()
    case = InterfaceCase.query.filter_by(case_set_id=set_id, status=InterfaceCase.ACTIVE).first()
    # if current_user.id != Project.query.filter_by(id=_edit.project_id).first().user_id:
    #     return jsonify({'msg': '不能删除别人项目下的模块', 'status': 0})
    if case:
        return jsonify({'msg': '请先删除集合下的接口用例', 'status': 0})
    InterfaceCaseSetBusiness.caseset_delete(set_id)
    return jsonify({'msg': '删除成功', 'status': 1})
