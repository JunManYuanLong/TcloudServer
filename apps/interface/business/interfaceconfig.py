from flask import current_app, jsonify
from sqlalchemy import desc

from apps.interface.models.interfaceconfig import InterfaceConfig
from apps.interface.models.interfaceproject import InterfaceProject
from apps.interface.util.utils import *
from library.api.db import db
from library.api.transfer import transfer2json


class InterfaceConfigBusiness(object):
    @classmethod
    def _query(cls):
        return InterfaceConfig.query.add_columns(
            InterfaceConfig.id.label('id'),
            InterfaceConfig.name.label('name'),
            InterfaceConfig.project_id.label('projectid'),
            InterfaceConfig.num.label('num'),
            InterfaceConfig.status.label('status'),
            InterfaceConfig.variables.label('variables'),
            InterfaceConfig.func_address.label('func_address'),
        )

    @classmethod
    @transfer2json('?id|!name|!projectid|!num|!status|!variables|!func_address')
    def query_all_json(cls, limit, offset):
        ret = cls._query().filter(InterfaceConfig.status == InterfaceConfig.ACTIVE) \
            .order_by(desc(InterfaceConfig.id)) \
            .limit(limit).offset(offset).all()
        return ret

    @classmethod
    def config_create(cls, name, project_id, num, variables, func_address):
        try:
            m = InterfaceConfig(
                name=name,
                project_id=project_id,
                num=num,
                variables=variables,
                func_address=func_address,
            )
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def config_delete(cls, id):
        try:
            m = InterfaceConfig.query.get(id)
            m.status = InterfaceConfig.DISABLE
            db.session.add(m)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def config_modify(cls, id, name, project_id, variables, func_address):
        try:
            m = InterfaceConfig.query.get(id)
            m.name = name
            m.project_id = project_id
            m.variables = variables
            m.func_address = func_address
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    @transfer2json('?id|!name|!projectid|!num|!status|!variables|!func_address')
    def query_json_by_id(cls, id):
        ret = cls._query().filter(InterfaceConfig.status == InterfaceConfig.ACTIVE,
                                  InterfaceConfig.id == id).all()
        return ret

    @classmethod
    def add_scene_config(cls, all_project_id, project_name, name, ids, func_address, variable, number):

        project_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE,
                                                      all_project_id=all_project_id).first().id
        if not project_name:
            return jsonify({'msg': '请选择项目', 'status': 0})
        if re.search('\\${(.*?)}', variable, flags=0) and not func_address:
            return jsonify({'msg': '参数引用函数后，必须引用函数文件', 'status': 0})

        num = auto_num(number, InterfaceConfig, project_id=project_id, status=InterfaceConfig.ACTIVE)

        if ids:
            old_data = InterfaceConfig.query.filter_by(id=ids, status=InterfaceConfig.ACTIVE).first()
            old_num = old_data.num

            project_id_temporary = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE,
                                                                    all_project_id=all_project_id).first().id
            list_data = InterfaceConfig.query.filter(InterfaceConfig.status == InterfaceConfig.ACTIVE,
                                                     InterfaceConfig.project_id == project_id_temporary).order_by(
                InterfaceConfig.num.asc()).all()

            if InterfaceConfig.query.filter_by(name=name, project_id=project_id,
                                               status=InterfaceConfig.ACTIVE).first() and name != old_data.name:
                return jsonify({'msg': '配置名字重复', 'status': 0})
            num_sort(num, old_num, list_data, old_data)

            InterfaceConfigBusiness.config_modify(ids, name, project_id, variable, func_address)
            return jsonify({'msg': '修改成功', 'status': 1})
        else:
            if InterfaceConfig.query.filter_by(name=name, project_id=project_id, status=InterfaceConfig.ACTIVE).first():
                return jsonify({'msg': '配置名字重复', 'status': 0})
            else:
                InterfaceConfigBusiness.config_create(name, project_id, num, variable, func_address)
                return jsonify({'msg': '新建成功', 'status': 1})

    @classmethod
    def find_config(cls, all_project_id, project_name, config_name, page, per_page):

        if not project_name:
            return jsonify({'msg': '请先选择项目', 'status': 0})

        pro_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceConfig.ACTIVE,
                                                  all_project_id=all_project_id).first().id
        if config_name:
            _config = InterfaceConfig.query.filter_by(project_id=pro_id, status=InterfaceConfig.ACTIVE).filter(
                InterfaceConfig.name.like('%{}%'.format(config_name))).all()
            total = len(_config)
            if not _config:
                return jsonify({'msg': '没有该配置', 'status': 0})
        else:
            _config = InterfaceConfig.query.filter_by(project_id=pro_id, status=InterfaceConfig.ACTIVE)
            pagination = _config.order_by(InterfaceConfig.num.asc()).paginate(page, per_page=per_page, error_out=False)
            _config = pagination.items
            total = pagination.total
        _config = [{'name': c.name, 'id': c.id, 'num': c.num, 'func_address': c.func_address} for c in _config]
        return jsonify({'data': _config, 'total': total, 'status': 1})
