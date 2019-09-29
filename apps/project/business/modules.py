from flask import g, current_app, request
from sqlalchemy import desc, func

from apps.auth.models.users import User
from apps.project.business.cases import CaseBusiness
from apps.project.models.cases import Case
from apps.project.models.modules import Module
from apps.project.models.tasks import TaskCase
from library.api.db import db
from library.api.exceptions import SaveObjectException
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
        ret = Module.query.filter_by(name=name, project_id=project_id, status=Case.ACTIVE).first()
        if ret:
            raise SaveObjectException('存在相同名称的模块')

        m = Module(
            name=name,
            project_id=project_id,
            description=description,
            parent_id=parent_id,
        )
        db.session.add(m)
        db.session.commit()
        return 0, None

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
    @transfer2json('?id|!projectid|!status|!total')
    def query_by_project_id_total(cls, pid):
        ret = CaseBusiness.case_total_groupby_module().filter(Module.status == Module.ACTIVE,
                                                              Module.project_id == pid).order_by(
            desc(Module.id)).group_by(Case.module_id).all()
        return ret

    @classmethod
    @transfer2json('?id|!name|!projectid|!description|!weight|!status|!parentid')
    def query_by_project_ids(cls, pid):
        ret = cls._query().filter(Module.status == Module.ACTIVE,
                                  Module.project_id == pid).order_by(desc(Module.id)).all()
        return ret

    @classmethod
    def filter_query(cls, pid=None, parent_ids=None, only_first=False, is_second=False):
        query = cls._query().filter(Module.status == Module.ACTIVE)
        if pid:
            query = query.filter(Module.project_id == pid)
        if is_second:
            query = query.filter(Module.parent_id.in_(parent_ids))
        else:
            module_name = request.args.get('modulename')
            if module_name:
                if '\\' in module_name:
                    module_name = module_name.replace('\\', '\\\\')
                query = query.filter(Module.name.like(f'%{module_name}%'))
            else:
                # 转义\, mysql需要一个\\\\才能识别
                if only_first:
                    query = query.filter(Module.parent_id.is_(None))
        query = query.order_by(desc(Module.id))
        return query

    @classmethod
    @transfer2json('?id|!name|!projectid|!description|!weight|!status|!parentid', ispagination=True)
    def pageinate_data(cls, pid):
        query = cls.filter_query(pid=pid, only_first=True)
        count = query.count()
        page_size = request.args.get('page_size')
        page_index = request.args.get('page_index')
        if page_size and page_index:
            size, index = int(page_size), int(page_index)
            query = query.limit(size).offset((index - 1) * size)
        # 一级模块总数，用来分页
        first_ret = query.all()
        first_ret_ids = []
        for fr in first_ret:
            first_ret_ids.append(fr.id)
        if first_ret_ids:
            second_query = cls.filter_query(parent_ids=first_ret_ids, is_second=True)
            second_ret = second_query.all()
            if second_ret:
                first_ret.extend(second_ret)
        return first_ret, count

    @classmethod
    def query_by_project_id(cls, pid):
        """
        这个版本在用例模块数量少的时候比上个版本慢，因为分页查询导致总数、二级用例模块需要多次查询数据库，但是数量多时应该会慢不少，因为不用一次
        返回所有数据，以及随着数量增加导致循环数增加
        """
        tlist = []
        # 查总数的时候，是0就查不到
        total_ret = cls.query_by_project_id_total(pid)
        total_ret_dict = {}
        for a in total_ret:
            tlist.append(a['id'])
            total_ret_dict[a['id']] = a
        case_total = 0
        for total_ret_obj in total_ret:
            case_total += total_ret_obj['total']

        first_ret, count = cls.pageinate_data(pid)

        for i in range(len(first_ret)):
            if first_ret[i]['id'] not in tlist:
                first_ret[i]['total'] = 0
            else:
                first_ret[i]['total'] = total_ret_dict[first_ret[i]['id']]['total']

        first_ret = cls.converter(first_ret)

        page_index = request.args.get('page_index')
        page_size = request.args.get('page_size')
        return first_ret, case_total, page_index, page_size, count

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
