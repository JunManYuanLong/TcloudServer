from flask import g, current_app, jsonify
from sqlalchemy import asc, desc, func

from apps.interface.models.interfaceapimsg import InterfaceApiMsg
from apps.interface.models.interfacecase import InterfaceCase
from apps.interface.models.interfacemodule import InterfaceModule
from apps.interface.models.interfaceproject import InterfaceProject
from apps.interface.util.utils import *
from library.api.db import db
from library.api.transfer import transfer2json


class InterfaceModuleBusiness(object):
    @classmethod
    def project_permission(cls, pid=None, id=None):
        if g.is_admin:
            return 0
        if pid:
            return 0 if pid in g.projectid else 1
        else:
            ret = InterfaceModule.query.add_columns(InterfaceModule.project_id.label('projectid')).filter(
                InterfaceModule.id == id).first()
            return 0 if ret.projectid in g.projectid else 1

    @classmethod
    def _query(cls):
        return InterfaceModule.query.add_columns(
            InterfaceModule.id.label('id'),
            InterfaceModule.name.label('name'),
            InterfaceModule.project_id.label('projectid'),
            InterfaceModule.num.label('num'),
            InterfaceModule.weight.label('weight'),
            InterfaceModule.status.label('status'),
        )

    @classmethod
    @transfer2json('?id|!name|!projectid|!num|!weight|!status')
    def query_all_json(cls, limit, offset):
        ret = cls._query().filter(InterfaceModule.status == InterfaceModule.ACTIVE) \
            .order_by(desc(InterfaceModule.id)) \
            .limit(limit).offset(offset).all()
        return ret

    @classmethod
    def module_create(cls, name, project_id, num):
        try:
            m = InterfaceModule(
                name=name,
                project_id=project_id,
                num=num,
            )
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def module_delete(cls, id):
        try:
            m = InterfaceModule.query.get(id)
            m.status = InterfaceModule.DISABLE
            db.session.add(m)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def module_modify(cls, id, name, project_id):
        try:
            m = InterfaceModule.query.get(id)
            m.name = name
            m.project_id = project_id
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    @transfer2json('?id|!name|!projectid|!num|!weight|!status')
    def query_json_by_id(cls, id):
        ret = cls._query().filter(InterfaceModule.status == InterfaceModule.ACTIVE,
                                  InterfaceModule.id == id).all()
        return ret

    @classmethod
    def _query_total(cls):
        return InterfaceModule.query.outerjoin(
            InterfaceCase, InterfaceCase.module_id == InterfaceModule.id).add_columns(
            InterfaceModule.id.label('id'),
            InterfaceModule.name.label('name'),
            InterfaceModule.project_id.label('projectid'),
            InterfaceModule.num.label('num'),
            InterfaceModule.weight.label('weight'),
            InterfaceModule.status.label('status'),
            func.count('*').label('total'),
        )

    @classmethod
    @transfer2json('?id|!name|!projectid|!num|!weight|!status|!total')
    def query_by_project_id_total(cls, pid):
        # TODO : here need case import
        # ret = cls._query_total().filter(InterfaceModule.status == InterfaceModule.ACTIVE,
        #                                 InterfaceModule.project_id == pid, Case.status != Case.DISABLE).order_by(
        #     desc(InterfaceModule.id)).group_by(Case.module_id).all()
        ret = []
        return ret

    @classmethod
    @transfer2json('?id|!name|!projectid|!num|!weight|!status')
    def query_by_project_ids(cls, pid):
        ret = cls._query().filter(InterfaceModule.status == InterfaceModule.ACTIVE,
                                  InterfaceModule.project_id == pid).order_by(desc(InterfaceModule.id)).all()
        return ret

    @classmethod
    def query_by_project_id(cls, pid):
        tlist = []
        total_ret = cls.query_by_project_id_total(pid)
        for a in total_ret:
            tlist.append(a['id'])
        ret = cls.query_by_project_ids(pid)
        for i in range(len(ret)):
            if ret[i]['id'] not in tlist:
                ret[i]['total'] = 0
                total_ret.append(ret[i])
        total_ret = sorted(total_ret, key=lambda x: x['id'], reverse=True)
        return total_ret

    @classmethod
    def find_model(cls, page, per_page, project_name):

        if not project_name:
            return jsonify({'msg': '请先选择项目', 'status': 0})

        peoject_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id
        all_module = InterfaceModule.query.filter_by(status=InterfaceModule.ACTIVE, project_id=peoject_id).order_by(
            InterfaceModule.num.asc())

        pagination = all_module.paginate(page, per_page=per_page, error_out=False)

        my_module = pagination.items
        total = pagination.total
        my_module = [{'name': c.name, 'moduleId': c.id, 'num': c.num} for c in my_module]

        # 查询出所有的接口模块是为了接口录入的时候可以选所有的模块
        _all_module = [{'name': s.name, 'moduleId': s.id, 'num': s.num} for s in all_module.all()]
        return jsonify({'data': my_module, 'total': total, 'status': 1, 'all_module': _all_module})

    @classmethod
    def add_model(cls, project_name, name, ids, number):

        if not project_name:
            return jsonify({'msg': '请先创建项目', 'status': 0})
        if not name:
            return jsonify({'msg': '模块名称不能为空', 'status': 0})

        project_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id
        num = auto_num(number, InterfaceModule, project_id=project_id, status=InterfaceModule.ACTIVE)
        if ids:
            old_data = InterfaceModule.query.filter_by(id=ids, status=InterfaceModule.ACTIVE).first()
            old_num = old_data.num
            list_data = InterfaceModule.query.filter(InterfaceModule.status == InterfaceModule.ACTIVE,
                                                     InterfaceModule.project_id == project_id).order_by(
                InterfaceModule.num.asc()).all()
            if InterfaceModule.query.filter_by(name=name, project_id=project_id,
                                               status=InterfaceModule.ACTIVE).first() and name != old_data.name:
                return jsonify({'msg': '模块名字重复', 'status': 0})

            num_sort(num, old_num, list_data, old_data)
            InterfaceModuleBusiness.module_modify(ids, name, project_id)
            return jsonify({'msg': '修改成功', 'status': 1})
        else:
            if InterfaceModule.query.filter_by(name=name, project_id=project_id, status=InterfaceModule.ACTIVE).first():
                return jsonify({'msg': '模块名字重复', 'status': 0})
            else:
                InterfaceModuleBusiness.module_create(name, project_id, num)
                return jsonify({'msg': '新建成功', 'status': 1})

    @classmethod
    def del_model(cls, ids):

        # _edit = InterfaceModule.query.filter_by(id=ids).first()
        # if current_user.id != Project.query.filter_by(id=_edit.project_id).first().user_id:
        #     return jsonify({'msg': '不能删除别人项目下的模块', 'status': 0})

        if InterfaceApiMsg.query.filter(
                InterfaceApiMsg.module_id == ids,
                InterfaceApiMsg.status == InterfaceApiMsg.ACTIVE
        ).order_by(asc(InterfaceApiMsg.num)).all():
            return jsonify({'msg': '请先删除模块下的接口用例', 'status': 0})

        InterfaceModuleBusiness.module_delete(ids)

        return jsonify({'msg': '删除成功', 'status': 1})

    @classmethod
    def stick_module(cls, module_id, project_name):

        old_data = InterfaceModule.query.filter_by(id=module_id, status=InterfaceModule.ACTIVE).first()
        old_num = old_data.num

        list_data_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id
        list_data = InterfaceModule.query.filter_by(project_id=list_data_id, status=InterfaceModule.ACTIVE).order_by(
            InterfaceModule.num.asc()).all()

        num_sort(1, old_num, list_data, old_data)
        db.session.commit()
        return jsonify({'msg': '置顶完成', 'status': 1})
