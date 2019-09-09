import io
import traceback

from flask import jsonify, current_app

from apps.interface.util.global_variable import *
from apps.interface.util.utils import *


class InterfaceFuncBusiness(object):

    @classmethod
    def get_func(cls, func_name):

        if not func_name:
            return jsonify({'msg': '请输入文件名', 'status': 0})
        if not os.path.exists('{}/{}'.format(FUNC_ADDRESS, func_name)):
            return jsonify({'msg': '文件名不存在', 'status': 0})
        with io.open('{}/{}'.format(FUNC_ADDRESS, func_name), 'r') as f:
            d = f.read()
        return jsonify({'msg': '获取成功', 'func_data': d, 'status': 1})

    @classmethod
    def check_func(cls, func_file_name, func_name):

        if not os.path.exists('{}/{}'.format(FUNC_ADDRESS, func_file_name)):
            return jsonify({'msg': '文件名不存在', 'status': 0})
        try:
            import_path = 'func_list.{}'.format(func_file_name.replace('.py', ''))
            # import_path = '{}'.format(func_file_name.replace('.py', ''))
            func_list = importlib.import_module(import_path)
            module_functions_dict = {name: item for name, item in vars(func_list).items() if
                                     isinstance(item, types.FunctionType)}

            ext_func = extract_functions(func_name)
            if len(ext_func) == 0:
                return jsonify({'msg': '函数解析失败，注意格式问题', 'status': 0})
            func = parse_function(ext_func[0])
            return jsonify(
                {'msg': '请查看', 'status': 1, 'result': module_functions_dict[func['func_name']](*func['args'])})

        except Exception as e:
            current_app.logger.info(str(e))
            error_data = '\n'.join('{}'.format(traceback.format_exc()).split('↵'))
            return jsonify({'msg': '语法错误，请自行检查', 'result': error_data, 'status': 0})

    @classmethod
    def create_func(cls, func_name):

        if func_name.find('.py') == -1:
            return jsonify({'msg': '请创建正确格式的py文件', 'status': 0})
        if not func_name:
            return jsonify({'msg': '文件名不能为空', 'status': 0})
        if os.path.exists('{}/{}'.format(FUNC_ADDRESS, func_name)):
            return jsonify({'msg': '文件名已存在', 'status': 0})
        with io.open('{}/{}'.format(FUNC_ADDRESS, func_name), 'w') as f:
            pass
        return jsonify({'msg': '创建成功', 'status': 1})

    @classmethod
    def remove_func(cls, func_name):

        if func_name == '':
            return jsonify({'msg': '文件名不存在', 'status': 0})
        if not os.path.exists('{}/{}'.format(FUNC_ADDRESS, func_name)):
            return jsonify({'msg': '文件名不存在', 'status': 0})
        else:
            os.remove('{}/{}'.format(FUNC_ADDRESS, func_name))
        return jsonify({'msg': '删除成功', 'status': 1})
