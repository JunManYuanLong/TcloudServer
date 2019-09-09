import io

from flask import Blueprint, jsonify, request

from apps.interface.business.interfacefunc import InterfaceFuncBusiness
from apps.interface.util.global_variable import *
from apps.interface.util.utils import *

interfacefunc = Blueprint('interfacefunc', __name__)


@interfacefunc.route('/find', methods=['POST'])
def get_func():
    """
    @api {post} /v1/interfacefunc/find InterfaceFunc_获取函数文件信息
    @apiName interfaceFuncFind
    @apiGroup Interface
    @apiDescription 获取函数文件信息
    @apiParam {string} funcName 函数名称
    @apiParamExample {json} Request-Example:
    {
        "funcName": "aa.py",
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "func_data": "",
        "msg": "获取成功",
        "status": 1
    }
    """
    data = request.json
    func_name = data.get('funcName')
    datajson = InterfaceFuncBusiness.get_func(func_name)
    return datajson


@interfacefunc.route('/getAddress', methods=['POST'])
def get_funcs():
    """
    @api {post} /v1/interfacefunc/getAddress InterfaceFunc_查找所以函数文件
    @apiName interfaceFuncGetAddress
    @apiGroup Interface
    @apiDescription 查找所以函数文件
    @apiParamExample {json} Request-Example:
    {
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data":
        [
            {
                "value":"aa.py"
            }
        ],
        "msg": "获取成功",
        "status": 1
    }
    """
    files = ''
    for root, dirs, files in os.walk(os.path.abspath('.') + r'/func_list'):
        if '__init__.py' in files:
            files.remove('__init__.py')
        for f in files:
            if '.pyc' in f:
                files.remove(f)

        files = [{'value': f} for f in files]
        break
    return jsonify({'data': files, 'status': 1})


@interfacefunc.route('/save', methods=['POST'])
def save_func():
    """
    @api {post} /v1/interfacefunc/save InterfaceFunc_保存函数文件
    @apiName interfaceFuncSave
    @apiGroup Interface
    @apiDescription 保存函数文件
    @apiParam {string} funcData 函数data
    @apiParam {string} funcName 函数名称
    @apiParamExample {json} Request-Example:
    {
        "funcData":" def test():  return '1357' ",
        "funcName":""
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "保存成功",
        "status": 1
    }
    """
    data = request.json
    func_data = data.get('funcData')
    func_name = data.get('funcName')
    if not os.path.exists('{}/{}'.format(FUNC_ADDRESS, func_name)):
        return jsonify({'msg': '文件名不存在', 'status': 0})
    with io.open('{}/{}'.format(FUNC_ADDRESS, func_name), 'w') as f:
        f.write(func_data)
    return jsonify({'msg': '保存成功', 'status': 1})


def is_function(tup):
    """ Takes (name, object) tuple, returns True if it is a function.
    """
    name, item = tup
    return isinstance(item, types.FunctionType)


@interfacefunc.route('/check', methods=['POST'])
def check_func():
    """
    @api {post} /v1/interfacefunc/check InterfaceFunc_函数调试
    @apiName interfaceFuncCheck
    @apiGroup Interface
    @apiDescription 函数调试
    @apiParam {string} funcFileName 函数文件名
    @apiParam {string} funcName 函数名称
    @apiParamExample {json} Request-Example:
    {
        "funcData":"",
        "funcName":""
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "文件名不存在",
        "status": 0
    }
    """
    data = request.json
    func_file_name = data.get('funcFileName')
    func_name = data.get('funcName')
    jsondata = InterfaceFuncBusiness.check_func(func_file_name, func_name)
    return jsondata


@interfacefunc.route('/create', methods=['POST'])
def create_func():
    """
    @api {post} /v1/interfacefunc/create InterfaceFunc_创建函数文件
    @apiName interfaceFuncCreate
    @apiGroup Interface
    @apiDescription 创建函数文件
    @apiParam {string} funcName 函数名称
    @apiParamExample {json} Request-Example:
    {
        "funcName":"aa.py"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "文件名已存在",
        "status": 0
    }
    """
    data = request.json
    func_name = data.get('funcName')
    jsondata = InterfaceFuncBusiness.create_func(func_name)

    return jsondata


@interfacefunc.route('/remove', methods=['POST'])
def remove_func():
    """
    @api {post} /v1/interfacefunc/remove InterfaceFunc_删除函数文件
    @apiName interfaceFuncRemove
    @apiGroup Interface
    @apiDescription 删除函数文件
    @apiParam {string} funcName 函数名称
    @apiParamExample {json} Request-Example:
    {
        "funcName":"aa.py"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "文件名不存在",
        "status": 0
    }
    """
    data = request.json
    func_name = data.get('funcName')

    jsondata = InterfaceFuncBusiness.remove_func(func_name)
    return jsondata
