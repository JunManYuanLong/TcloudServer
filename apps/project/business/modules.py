import time

from flask import g, current_app
from sqlalchemy import desc, func

from apps.auth.models.users import User
from apps.project.models.cases import Case
from apps.project.models.modules import Module
from apps.project.models.tasks import TaskCase
from library.api.db import db
from library.api.transfer import transfer2json
from library.trpc import Trpc


class ModuleBusiness(object):
    user_trpc = Trpc('auth')

    @classmethod
    def project_permission(cls, pid=None, id=None):
        project_id = cls.user_trpc.requests('get', '/user/userbindproject', {'userid': g.userid})
        if g.is_admin:
            return 0
        if pid:
            return 0 if pid in project_id else 1
        else:
            ret = Module.query.add_columns(Module.project_id.label('projectid')).filter(Module.id == id).first()
            return 0 if ret.projectid in project_id else 1

    @classmethod
    def _query(cls):
        return Module.query.add_columns(
            Module.id.label('id'),
            Module.name.label('name'),
            Module.project_id.label('projectid'),
            Module.description.label('description'),
            Module.weight.label('weight'),
            Module.status.label('status'),
            Module.parent_id.label('parentid')
        )

    @classmethod
    @transfer2json('?id|!name|!projectid|!description|!weight|!status')
    def query_all_json(cls, limit, offset):
        ret = cls._query().filter(Module.status == Module.ACTIVE) \
            .order_by(desc(Module.id)) \
            .limit(limit).offset(offset).all()
        return ret

    @classmethod
    def module_create(cls, name, project_id, description, parent_id=None):
        try:
            ret = Module.query.filter(Module.name == name, Module.status != Module.DISABLE,
                                      Module.project_id == project_id).first()
            if ret:
                return 103, None
            m = Module(
                name=name,
                project_id=project_id,
                description=description,
                parent_id=parent_id,
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
            m = Module.query.get(id)
            m.status = Module.DISABLE
            db.session.add(m)
            for case in Case.query.filter_by(module_id=id):
                case.status = Case.DISABLE
                db.session.add(case)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def module_modify(cls, id, name, project_id, description, weight):
        try:
            ret = Module.query.filter(Module.name == name, Module.status != Module.DISABLE, Module.id != id).first()
            if ret:
                return 103, None
            m = Module.query.get(id)
            m.name = name
            m.project_id = project_id
            m.description = description
            m.weight = weight
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    @transfer2json('?id|!name|!projectid|!description|!weight|!status')
    def query_json_by_id(cls, id):
        ret = cls._query().filter(Module.status == Module.ACTIVE,
                                  Module.id == id).all()
        return ret

    @classmethod
    def _query_total(cls):
        return Module.query.outerjoin(
            Case, Case.module_id == Module.id).add_columns(
            Module.id.label('id'),
            Module.name.label('name'),
            Module.project_id.label('projectid'),
            Module.description.label('description'),
            Module.weight.label('weight'),
            Module.status.label('status'),
            func.count('*').label('total'),
            Module.parent_id.label('parentid')
        )

    @classmethod
    def _query_total_taskcase(cls):
        return Module.query.outerjoin(
            TaskCase, TaskCase.module_id == Module.id).add_columns(
            Module.id.label('id'),
            Module.name.label('name'),
            Module.project_id.label('projectid'),
            Module.description.label('description'),
            Module.weight.label('weight'),
            Module.status.label('status'),
            func.count('*').label('total'),
            Module.parent_id.label('parentid')
        )

    @classmethod
    @transfer2json('?id|!name|!projectid|!description|!weight|!status|!total|!parentid')
    def query_by_project_id_total(cls, pid):
        ret = cls._query_total().filter(Module.status == Module.ACTIVE,
                                        Module.project_id == pid, Case.status != Case.DISABLE).order_by(
            desc(Module.id)).group_by(Case.module_id).all()
        return ret

    @classmethod
    @transfer2json('?id|!name|!projectid|!description|!weight|!status|!parentid')
    def query_by_project_ids(cls, pid):
        ret = cls._query().filter(Module.status == Module.ACTIVE,
                                  Module.project_id == pid).order_by(desc(Module.id)).all()
        return ret

    @classmethod
    def query_by_project_id(cls, pid, module_name=None):
        tlist = []
        # 查总数的时候，是0就查不到
        total_ret = cls.query_by_project_id_total(pid)
        for a in total_ret:
            tlist.append(a['id'])
        ret = cls.query_by_project_ids(pid)
        for i in range(len(ret)):
            if ret[i]['id'] not in tlist:
                ret[i]['total'] = 0
                total_ret.append(ret[i])
        case_total = 0
        for total_ret_obj in total_ret:
            case_total += total_ret_obj['total']

        total_ret = cls.converter(total_ret)

        # 查询模块名,new一个新的列表存储符合条件的父模块（带子模块）
        if module_name:
            filter_total_ret = []
            for i in total_ret:
                if module_name in i['name']:
                    filter_total_ret.append(i)
                elif 'modules' in i and i['modules']:
                    for j in i['modules']:
                        if module_name in j['name']:
                            filter_total_ret.append(i)
                            break
            total_ret = filter_total_ret

        # case_total = 0
        # for total_ret_obj in total_ret:
        #     case_total += total_ret_obj['total']
        #     if 'modules' in total_ret_obj and total_ret_obj['modules']:
        #         for j in total_ret_obj['modules']:
        #             case_total += j['total']

        total_ret = sorted(total_ret, key=lambda x: x['id'], reverse=True)
        return total_ret, case_total

    @classmethod
    def query_by_project_case(cls, pid):
        # 查总数的时候，是0就查不到
        # 获取当前项目所有模块
        # total_ret = cls.query_by_project_id_total(pid)
        # if total_ret:
        total_ret = cls.query_by_project_ids(pid)
        tlist = [module['id'] for module in total_ret]

        module_case = cls._case_query(tlist)
        for t in range(len(total_ret)):
            i = 0
            total_ret[t]['case_list'] = []
            total_ret[t]['total'] = i
            for mc in module_case:
                if total_ret[t]['id'] == mc['moduleid']:
                    total_ret[t]['case_list'].append(mc)
                    i += 1
                    total_ret[t]['total'] = i

        total_ret = cls.converter(total_ret)
        total_ret = sorted(total_ret, key=lambda x: x['id'], reverse=True)
        return total_ret

    @staticmethod
    def converter(total_ret):
        # TODO 二级目录，待修改  双层循环
        num = 0
        tmp_total_ret = total_ret[:]
        for index, module in enumerate(tmp_total_ret):
            if module['parentid']:
                for j in tmp_total_ret:
                    if j['id'] == module['parentid']:
                        if 'parentid' not in j or not j['parentid']:
                            if 'modules' not in j:
                                j['modules'] = []
                            j['modules'].append(module)
                            del total_ret[index - num]
                            num += 1
                            break
            else:
                del module['parentid']

        return total_ret

    @classmethod
    @transfer2json(
        '?id|!cnumber|!ctype|!title|!precondition|!step_result|!creation_time|!modified_time'
        '|!is_auto|!status|!moduleid|!module|!userid|!username|!priority')
    def _case_query(cls, tlist):
        return Case.query.outerjoin(
            Module, Case.module_id == Module.id).outerjoin(
            User, User.id == Case.creator).add_columns(
            Case.id.label('id'),
            Case.cnumber.label('cnumber'),
            Case.ctype.label('ctype'),
            Case.title.label('title'),
            Case.precondition.label('precondition'),
            Case.step_result.label('step_result'),
            Case.is_auto.label('is_auto'),
            Case.priority.label('priority'),
            Case.status.label('status'),
            func.date_format(Case.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(Case.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
            Module.id.label('moduleid'),
            Module.name.label('module'),
            User.id.label('userid'),
            User.nickname.label('username')
        ).filter(Case.status != Case.DISABLE).filter(Case.module_id.in_(tlist)).order_by(desc(Case.id)).all()
