from flask import jsonify, current_app
from sqlalchemy import asc

from apps.interface.business.interfacecasedata import InterfaceCaseDataBusiness
from apps.interface.models.interfaceapimsg import InterfaceApiMsg
from apps.interface.models.interfacecasedata import InterfaceCaseData
from apps.interface.models.interfacemodule import InterfaceModule
from apps.interface.models.interfaceproject import InterfaceProject
from apps.interface.util.global_variable import *
from apps.interface.util.global_variable import FILE_ADDRESS
from apps.interface.util.http_run import RunCase
from apps.interface.util.utils import *
from library.api.db import db


class InterfaceApiMsgBusiness(object):

    @classmethod
    def _query(cls):
        return InterfaceApiMsg.query.add_columns(
            InterfaceApiMsg.id.label('id'),
            InterfaceApiMsg.num.label('num'),
            InterfaceApiMsg.name.label('name'),
            InterfaceApiMsg.desc.label('desc'),
            InterfaceApiMsg.variable_type.label('variable_type'),
            InterfaceApiMsg.status_url.label('status_url'),
            InterfaceApiMsg.up_func.label('up_func'),
            InterfaceApiMsg.down_func.label('down_func'),
            InterfaceApiMsg.method.label('method'),
            InterfaceApiMsg.variable.label('variable'),
            InterfaceApiMsg.json_variable.label('json_variable'),
            InterfaceApiMsg.param.label('param'),
            InterfaceApiMsg.url.label('url'),
            InterfaceApiMsg.extract.label('extract'),
            InterfaceApiMsg.validate.label('validate'),
            InterfaceApiMsg.header.label('header'),
            InterfaceApiMsg.module_id.label('module_id'),
            InterfaceApiMsg.project_id.label('project_id'),
            InterfaceApiMsg.status.label('status'),
        )

    @classmethod
    def apimsg_create(cls, num, name, desc, variable_type, status_url, up_func, down_func, method, variable,
                      json_variable, param, url, extract, validate, header, module_id, project_id):
        try:
            m = InterfaceApiMsg(
                num=num,
                name=name,
                desc=desc,
                variable_type=variable_type,
                status_url=status_url,
                up_func=up_func,
                down_func=down_func,
                method=method,
                variable=variable,
                json_variable=json_variable,
                param=param,
                url=url,
                extract=extract,
                validate=validate,
                header=header,
                module_id=module_id,
                project_id=project_id,
            )
            db.session.add(m)
            db.session.commit()
            return m.id, m.num
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def apimsg_delete(cls, id):
        try:
            m = InterfaceApiMsg.query.get(id)
            m.status = InterfaceApiMsg.DISABLE
            db.session.add(m)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def apimsg_modify(cls, id, name, desc, variable_type, status_url, up_func, down_func, method, variable,
                      json_variable, param, url, extract, validate, header, module_id, project_id):
        try:
            m = InterfaceApiMsg.query.get(id)
            m.name = name,
            m.desc = desc,
            m.variable_type = variable_type,
            m.status_url = status_url,
            m.up_func = up_func,
            m.down_func = down_func,
            m.method = method,
            m.variable = variable,
            m.json_variable = json_variable,
            m.param = param,
            m.url = url,
            m.extract = extract,
            m.validate = validate,
            m.header = header,
            m.module_id = module_id,
            m.project_id = project_id,
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def add_api_msg(cls, project_name, api_msg_name, variable_type, desc_string, header, extract,
                    validate, api_msg_id, up_func, down_func, method, module_id, url, status_url,
                    variable, json_variable, param, all_project_id, number):

        if not project_name:
            return jsonify({'msg': '项目不能为空', 'status': 0})
        if not module_id:
            return jsonify({'msg': '接口模块不能为空', 'status': 0})
        if not api_msg_name:
            return jsonify({'msg': '接口名称不能为空', 'status': 0})
        if method == -1:
            return jsonify({'msg': '请求方式不能为空', 'status': 0})
        if not url:
            return jsonify({'msg': '接口url不能为空', 'status': 0})
        if status_url == -1:
            if 'http' not in url:
                return jsonify({'msg': '基础url为空时，请补全api地址', 'status': 0})

        project_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE,
                                                      all_project_id=all_project_id).first().id
        num = auto_num(number, InterfaceApiMsg, module_id=module_id, status=InterfaceApiMsg.ACTIVE)

        if api_msg_id:
            old_data = InterfaceApiMsg.query.filter_by(id=api_msg_id, status=InterfaceApiMsg.ACTIVE).first()
            old_num = old_data.num
            if InterfaceApiMsg.query.filter_by(name=api_msg_name, module_id=module_id,
                                               status=0).first() and api_msg_name != old_data.name:
                return jsonify({'msg': '接口名字重复', 'status': 0})

            # list_data = Module.query.filter_by(id=module_id).first().api_msg.all()
            list_data = InterfaceApiMsg.query.filter_by(module_id=module_id, status=0).order_by(
                asc(InterfaceApiMsg.num)).all()

            num_sort(num, old_num, list_data, old_data)
            InterfaceApiMsgBusiness.apimsg_modify(api_msg_id, api_msg_name, desc_string, variable_type, status_url,
                                                  up_func,
                                                  down_func, method, variable, json_variable, param, url, extract,
                                                  validate,
                                                  header, module_id, project_id)

            return jsonify({'msg': '修改成功', 'status': 1, 'api_msg_id': api_msg_id, 'num': num})
        else:
            if InterfaceApiMsg.query.filter_by(name=api_msg_name, module_id=module_id, status=0).first():
                return jsonify({'msg': '接口名字重复', 'status': 0})
            else:
                interface_id, interface_num = InterfaceApiMsgBusiness.apimsg_create(num, api_msg_name, desc_string,
                                                                                    variable_type, status_url, up_func,
                                                                                    down_func, method, variable,
                                                                                    json_variable, param, url, extract,
                                                                                    validate, header, module_id,
                                                                                    project_id)

                return jsonify({'msg': '新建成功', 'status': 1, 'api_msg_id': interface_id, 'num': interface_num})

    @classmethod
    def edit_api_msg(cls, case_id):

        _edit = InterfaceApiMsg.query.filter_by(id=case_id, status=InterfaceApiMsg.ACTIVE).first()
        _data = {
            'name': _edit.name, 'num': _edit.num, 'desc': _edit.desc, 'url': _edit.url,
            'method': _edit.method, 'status_url': int(_edit.status_url),
            'up_func': _edit.up_func, 'down_func': _edit.down_func,
            'variableType': _edit.variable_type,
            'param': json.loads(_edit.param),
            'header': json.loads(_edit.header),
            'variable': json.loads(_edit.variable),
            'json_variable': _edit.json_variable,
            'extract': json.loads(_edit.extract),
            'validate': json.loads(_edit.validate)
        }

        return jsonify({'data': _data, 'status': 1})

    @classmethod
    def run_api_msg(cls, api_msg_data, project_name, config_id):

        if not api_msg_data:
            return jsonify({'msg': '请勾选信息后，再进行测试', 'status': 0})

        # 前端传入的数据不是按照编号来的，所以这里重新排序
        api_ids = [(item['num'], item['apiMsgId']) for item in api_msg_data]
        api_ids.sort(key=lambda x: x[0])
        # api_data = [ApiMsg.query.filter_by(id=c[1]).first() for c in api_ids]
        api_ids = [c[1] for c in api_ids]

        project_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id

        try:
            d = RunCase(project_id)
            res = json.loads(d.run_case(d.get_api_test(api_ids, config_id)))
        except Exception as e:
            current_app.logger.info("单个接口运行的错误信息:" + str(e))
            return jsonify({'msg': '参数或者文件配置错误，请检查完再运行', 'status': 0})

        return jsonify({'msg': '测试完成', 'data': res, 'status': 1})

    @classmethod
    def find_api_msg(cls, project_name, module_id, api_name, page, per_page):
        if not project_name:
            return jsonify({'msg': '请选择项目', 'status': 0})
        if not module_id:
            return jsonify({'msg': '请先创建{}项目下的模块'.format(project_name), 'status': 0})

        if api_name:
            api_data = InterfaceApiMsg.query.filter_by(module_id=module_id, status=0).filter(
                InterfaceApiMsg.name.like('%{}%'.format(api_name))).all()
            total = len(api_data)
            if not api_data:
                return jsonify({'msg': '没有该接口信息', 'status': 0})
        else:
            api_data = InterfaceApiMsg.query.filter_by(module_id=module_id, status=0)
            pagination = api_data.order_by(InterfaceApiMsg.num.asc()).paginate(page, per_page=per_page, error_out=False)
            api_data = pagination.items
            total = pagination.total

        _api = [{
            'num': c.num,
            'name': c.name,
            'desc': c.desc,
            'url': c.url,
            'apiMsgId': c.id,
            'gather_id': c.module_id,
            'variableType': c.variable_type,
            'variable': json.loads(c.variable),
            'json_variable': c.json_variable,
            'extract': json.loads(c.extract),
            'validate': json.loads(c.validate),
            'param': json.loads(c.param),
            'statusCase': {
                'extract': [True, True], 'variable': [True, True],
                'validate': [True, True], 'param': [True, True]
            },
            'status': True, 'case_name': c.name, 'down_func': c.down_func, 'up_func': c.up_func, 'time': 1
        }
            for c in api_data]

        return jsonify({'data': _api, 'total': total, 'status': 1})

    @classmethod
    def del_api_msg(cls, api_msg_id):

        _data = InterfaceApiMsg.query.filter_by(id=api_msg_id, status=0).first()

        project_id = InterfaceModule.query.filter_by(id=_data.module_id, status=0).first().project_id
        # if current_user.id != InterfaceProject.query.filter_by(id=project_id).first().user_id:
        #     return jsonify({'msg': '不能删除别人项目下的接口', 'status': 0})

        InterfaceApiMsgBusiness.apimsg_delete(api_msg_id)

        # 同步删除接口信息下对应用例下的接口步骤信息
        for d in InterfaceCaseData.query.filter_by(api_msg_id=api_msg_id, execute_status=0).all():
            InterfaceCaseDataBusiness.casedata_delete(d.id)

        return jsonify({'msg': '删除成功', 'status': 1})

    @classmethod
    def api_upload(cls, file, skip):

        if os.path.exists(os.path.join(FILE_ADDRESS, file.filename)) and not skip:
            return jsonify({"msg": "文件已存在，请修改文件名字后再上传", "status": 0})
        else:
            file.save(os.path.join(FILE_ADDRESS, file.filename))
            return jsonify({'data': os.path.join(FILE_ADDRESS, file.filename), "msg": "上传成功", "status": 1})
