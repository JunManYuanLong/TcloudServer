from flask import current_app, jsonify
from sqlalchemy import desc

from apps.interface.models.interfacecaseset import InterfaceCaseSet
from apps.interface.models.interfaceproject import InterfaceProject
from apps.interface.util.utils import *
from library.api.db import db
from library.api.transfer import transfer2json


class InterfaceCaseSetBusiness(object):

    @classmethod
    def _query(cls):
        return InterfaceCaseSet.query.add_columns(
            InterfaceCaseSet.id.label('id'),
            InterfaceCaseSet.num.label('num'),
            InterfaceCaseSet.name.label('name'),
            InterfaceCaseSet.project_id.label('project_id'),
            InterfaceCaseSet.status.label('status'),
        )

    @classmethod
    @transfer2json('?id|!num|!name|!project_id|!status')
    def query_all_json(cls, limit, offset):
        ret = cls._query().filter(InterfaceCaseSet.status == InterfaceCaseSet.ACTIVE) \
            .order_by(desc(InterfaceCaseSet.id)) \
            .limit(limit).offset(offset).all()
        return ret

    @classmethod
    def caseset_create(cls, num, name, project_id):
        try:
            m = InterfaceCaseSet(
                num=num,
                name=name,
                project_id=project_id,
            )
            db.session.add(m)
            db.session.commit()
            return m.id, m.num
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def caseset_delete(cls, id):
        try:
            m = InterfaceCaseSet.query.get(id)
            m.status = InterfaceCaseSet.DISABLE
            db.session.add(m)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def caseset_modify(cls, id, name, project_id):
        try:
            m = InterfaceCaseSet.query.get(id)
            m.name = name,
            m.project_id = project_id,
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def add_set(cls, project_name, name, ids, number):

        if not name:
            return jsonify({'msg': '用例集名称不能为空', 'status': 0})
        project_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id
        num = auto_num(number, InterfaceCaseSet, project_id=project_id, status=InterfaceCaseSet.ACTIVE)
        if ids:
            old_data = InterfaceCaseSet.query.filter_by(id=ids, status=InterfaceCaseSet.ACTIVE).first()
            if InterfaceCaseSet.query.filter_by(name=name, project_id=project_id,
                                                status=InterfaceCaseSet.ACTIVE).first() and name != old_data.name:
                return jsonify({'msg': '用例集名字重复', 'status': 0})
            InterfaceCaseSetBusiness.caseset_modify(ids, name, project_id)
            return jsonify({'msg': '修改成功', 'status': 1})
        else:
            if InterfaceCaseSet.query.filter_by(name=name, project_id=project_id,
                                                status=InterfaceCaseSet.ACTIVE).first():
                return jsonify({'msg': '用例集名字重复', 'status': 0})
            else:
                InterfaceCaseSetBusiness.caseset_create(num, name, project_id)
                return jsonify({'msg': '新建成功', 'status': 1})

    @classmethod
    def stick_set(cls, set_id, project_name):

        old_data = InterfaceCaseSet.query.filter_by(id=set_id, status=InterfaceCaseSet.ACTIVE).first()
        old_num = old_data.num
        list_data_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id
        list_data = InterfaceCaseSet.query.filter_by(project_id=list_data_id, status=InterfaceCaseSet.ACTIVE).order_by(
            InterfaceCaseSet.num.asc()).all()
        num_sort(1, old_num, list_data, old_data)
        db.session.commit()
        return jsonify({'msg': '置顶完成', 'status': 1})

    @classmethod
    def find_set(cls, page, per_page, project_name):

        if not project_name:
            return jsonify({'msg': '请先创建属于自己的项目', 'status': 0})

        pro_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id
        all_sets = InterfaceCaseSet.query.filter_by(project_id=pro_id, status=InterfaceCaseSet.ACTIVE).order_by(
            InterfaceCaseSet.num.asc())
        pagination = all_sets.paginate(page, per_page=per_page, error_out=False)
        _items = pagination.items
        total = pagination.total
        current_set = [{'label': s.name, 'id': s.id} for s in _items]
        all_set = [{'label': s.name, 'id': s.id} for s in all_sets.all()]
        return jsonify({'status': 1, 'total': total, 'data': current_set, 'all_set': all_set})
