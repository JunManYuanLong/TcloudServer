import json
import os
import re
import time

import xlrd
import xlwt
from flask import g, current_app, request
from sqlalchemy import desc, func, and_, or_

from apps.auth.models.users import User
from apps.project.business.requirement import RequirementBindCaseBusiness
from apps.project.models.cases import Case
from apps.project.models.modules import Module
from apps.project.models.project import Project
from apps.project.models.requirement import Requirement, RequirementBindCase
from library.api.db import db
from library.api.exceptions import CannotFindObjectException, OperationFailedException
from library.api.transfer import transfer2jsonwithoutset, slicejson, transfer2json
from library.oss import oss_upload, oss_download
from library.trpc import Trpc
from public_config import CTYPE, TCLOUD_FILE_TEMP_PATH


class CaseBusiness(object):
    user_trpc = Trpc('auth')

    @classmethod
    def project_permission(cls, pid=None, mid=None, id=None):
        project_id = cls.user_trpc.requests('get', '/user/userbindproject', {'userid': g.userid})
        if g.is_admin:
            return 0

        ret = Module.query.add_columns(Module.project_id.label('projectid')).filter(Module.id == mid).first()
        if ret:
            pid = ret.projectid
        if pid:
            return 0 if pid in project_id else 1
        else:
            ret = Case.query.outerjoin(
                Module, Case.module_id == Module.id).add_columns(
                Module.project_id.label('projectid')).filter(
                Case.id == id).first()
            return 0 if ret.projectid in project_id else 1

    @classmethod
    def _query(cls):
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
        )

    @classmethod
    def case_total_groupby_module(cls):
        return Case.query.outerjoin(
            Module, Module.id == Case.module_id).add_columns(
            Module.id.label('id'),
            Module.project_id.label('projectid'),
            Module.status.label('status'),
            func.count('*').label('total'),
        )

    @classmethod
    def _query_for_requirement(cls):
        return Case.query.outerjoin(
            Module, Case.module_id == Module.id).outerjoin(
            User, User.id == Case.creator).outerjoin(
            RequirementBindCase, and_(RequirementBindCase.case_id == Case.id,
                                      RequirementBindCase.status == RequirementBindCase.ACTIVE)).outerjoin(
            Requirement, and_(RequirementBindCase.requirement_id == Requirement.id,
                              Requirement.status == Requirement.ACTIVE)).add_columns(
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
            User.nickname.label('username'),
            Requirement.id.label('requirement_id'),
            Requirement.title.label('requirement_title')
        )

    @classmethod
    @transfer2json(
        '?id|!cnumber|!ctype|!title|!precondition|!step_result|!creation_time|!modified_time'
        '|!is_auto|!status|!moduleid|!module|!userid|!username|!priority')
    def query_all_json(cls, limit, offset):
        pid = request.args.get('projectid')
        if pid is not None:
            ret = []
            [
                ret.extend(case) for case in (
                cls._query().filter(Case.status == Case.ACTIVE, Case.
                                    module_id == moduleid[0]).order_by(desc(Case.id)).all()
                for moduleid in db.session.query(Module.id).filter(Module.project_id == pid).all())
            ]
            return ret
        data = cls._query().filter(Case.status == Case.ACTIVE).order_by(
            desc(Case.id)).limit(limit).offset(offset)
        return data.all()

    @classmethod
    @slicejson(['requirement|id|title|requirement_id|requirement_title'])
    @transfer2jsonwithoutset('?id|!cnumber|!ctype|!title|!precondition|!step_result|!creation_time|!modified_time|'
                             '!is_auto|!status|!moduleid|!module|!userid|!username|!priority|@requirement_id|'
                             '@requirement_title')
    def query_by_id(cls, caseid):
        ret = cls._query_for_requirement().filter(Case.status == Case.ACTIVE, Case.id == caseid).all()

        return ret

    @classmethod
    @slicejson(['requirement|id|title|requirement_id|requirement_title'], ispagination=True)
    @transfer2jsonwithoutset('?id|!cnumber|!ctype|!title|!precondition|!step_result|!creation_time|!modified_time|'
                             '!is_auto|!status|!moduleid|!module|!userid|!username|!priority|@requirement_id|'
                             '@requirement_title', ispagination=True)
    def _query_by_requirement_id(cls, requirement_id, page_size, page_index):
        query = cls._query_for_requirement().filter(Case.status == Case.ACTIVE,
                                                    RequirementBindCase.requirement_id == requirement_id)
        count = query.count()
        data = query.order_by(
            desc(Case.id)).limit(int(page_size)).offset(int(page_index - 1) * int(page_size)).all()
        return data, count

    @classmethod
    def query_by_requirement_id(cls, requirement_id, page_size, page_index):
        ret, count = cls._query_by_requirement_id(requirement_id, page_size, page_index)
        module_id_list = []
        module_ret = {}
        for i in range(len(ret)):
            module_id_list.append(ret[i]['moduleid'])
        module_id_list = list(set(module_id_list))
        for i in range(len(module_id_list)):
            module_ret[module_id_list[i]] = dict(module_id=module_id_list[i], info=[])
        for i in range(len(ret)):
            temp_ret = ret[i]
            module_id = temp_ret['moduleid']
            module_ret[module_id]['info'].append(temp_ret)
            module_ret[module_id]['module_name'] = temp_ret['module']

        return list(module_ret.values()), count

    @classmethod
    def delete(cls, caseid):
        case = Case.query.get(caseid)
        case.status = Case.DISABLE
        db.session.add(case)
        db.session.commit()
        return 0

    @classmethod
    def create(cls, moduleid, ctype, title, precondition, step_result, creator, priority, requirement_ids=None):
        c = Case(
            module_id=moduleid,
            ctype=ctype,
            title=title,
            precondition=precondition,
            step_result=step_result,
            creator=creator,
            priority=priority
        )
        db.session.add(c)
        db.session.flush()
        mid = c.id
        c.cnumber = 'TC' + str(mid)
        db.session.add(c)
        current_app.logger.info(requirement_ids)
        if requirement_ids is not None:
            current_app.logger.info('create case')
            RequirementBindCaseBusiness.case_bind_requirements(c.id, requirement_ids)
        db.session.commit()
        return 0, None

    @classmethod
    def update(cls, caseid, moduleid, ctype, title, precondition, step_result, is_auto, priority, requirement_ids):
        c = Case.query.get(caseid)
        if not c:
            raise CannotFindObjectException

        c.module_id = moduleid
        c.ctype = ctype
        c.title = title
        c.precondition = precondition
        c.step_result = step_result
        c.is_auto = is_auto
        c.priority = priority
        db.session.add(c)
        if requirement_ids is not None:
            RequirementBindCaseBusiness.case_bind_requirements(caseid, requirement_ids)
        db.session.commit()
        return 0

    @classmethod
    def case_all_tester_dashboard(cls, begin_date, end_date, testers=None):
        if not testers:
            testers = cls.user_trpc.requests('get', '/user/role/3')
        detaillist = []
        dashboard_ret = Case.query.add_columns(
            func.date_format(Case.creation_time, "%Y-%m-%d").label('creation_time'),
            Case.creator.label('creator'),
            func.count('*').label('count')). \
            filter(Case.creation_time.between(begin_date, end_date + " 23:59:59")). \
            group_by(func.date_format(Case.creation_time, "%Y-%m-%d"), Case.creator).order_by(
            desc(Case.creator)).all()

        for tester in testers:
            userid = tester.get('userid')
            nickname = tester.get('nickname')
            info = []
            for da in dashboard_ret:
                if userid == da.creator:
                    info.append({"date": da.creation_time, "count": da.count})
            detail = [
                dict(
                    userid=userid,
                    nickname=nickname,
                    info=info)
            ]
            detaillist.extend(detail)
        return detaillist

    @classmethod
    def case_all_tester_dashboard_for_project(cls, data_temp, project_id, begin_date, end_date):
        cases = Case.query.outerjoin(Module, Module.id == Case.module_id
                                     ).filter(Case.creation_time.between(begin_date, end_date + " 23:59:59"),
                                              Case.creator.in_(list(data_temp.keys())),
                                              Module.project_id == project_id,
                                              Case.status == 0
                                              ).all()
        for case in cases:
            data_temp[case.creator]["case_count"] += 1
        return data_temp

    @classmethod
    def case_export(cls):
        project_id = request.args.get('project_id')
        module_id = request.args.get('module_data')
        user_id = request.args.get('user_id')
        if module_id:
            module_id = module_id.split(',')
            module_all = Module.query.filter(Module.id.in_(module_id), Module.status == Module.ACTIVE).all()
        else:
            module_all = Module.query.filter(Module.project_id == project_id, Module.status == Module.ACTIVE).all()
        if not module_all:
            return 201, [], '前端传入接口格式错误'
        # for module_data in module_all:
        #     module_list.append(module_data.id)
        #     module_sheet_name.append(module_data.name)
        #     if module_data.parent_id:
        #         parent_module_data = Module.query.get(module_data.parent_id).name
        #         module_name.append(f'{parent_module_data}/{module_data.name}')
        #     else:
        #         module_name.append(module_data.name)

        workbook = xlwt.Workbook()
        alignment = xlwt.Alignment()
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        alignment.horz = xlwt.Alignment.HORZ_LEFT
        alignment.vert = xlwt.Alignment.VERT_TOP
        style = xlwt.XFStyle()
        style.alignment = alignment
        project_name = Project.query.get(project_id).name

        try:
            sheet_name = project_name
            sheet_name = sheet_name.replace('/', '').replace('\\', '').replace(':', '').replace('?', '').replace(
                '*', '').replace('[', '').replace(']', '')
            sheet = workbook.add_sheet(sheet_name[:30], cell_overwrite_ok=True)
        except Exception as e:
            return 102, {"url": ''}, '未找到相关用例'

        for i in (2, 4, 5):
            sheet.col(i).width = 256 * 30
        sheet.col(1).width = 256 * 13
        sheet.col(3).width = 256 * 13
        sheet.col(11).width = 256 * 12
        sheet.write_merge(0, 0, 0, 0, '项目名称')
        sheet.write_merge(0, 0, 1, 3, project_name)
        sheet.write_merge(0, 0, 4, 4, '版本号')
        sheet.write_merge(0, 0, 5, 7, '')
        sheet.write_merge(1, 1, 0, 0, '测试环境')
        sheet.write_merge(1, 1, 1, 7, '')
        sheet.write(2, 0, '用例编号')
        sheet.write(2, 1, '功能模块')
        sheet.write(2, 2, '用例描述')
        sheet.write(2, 3, '预置条件')
        sheet.write(2, 4, '操作步骤')
        sheet.write(2, 5, '预期结果')
        sheet.write(2, 6, '优先级')
        sheet.write(2, 7, 'case类型')
        sheet.write(2, 8, '测试结果(PASS/Fail)')
        sheet.write(2, 9, '备注')
        sheet.write(2, 10, '测试人员')
        sheet.write(2, 11, '创建时间')

        case_description_list = []
        precondition_list = []
        opearating_steps_list = []
        expect_result_list = []
        cnumber_list = []
        priority_list = []
        ctype_list = []
        creator_list = []
        module_name_list = []
        creation_time_list = []

        taskcase_data, _ = cls.paginate_data(only_data=True)
        taskcase_data = sorted(taskcase_data, key=lambda x: x['username'])
        for case_count in range(0, len(taskcase_data)):
            creation_time_list.append(taskcase_data[case_count]['creation_time'])
            creator_list.append(taskcase_data[case_count]['username'])
            module_name_list.append(taskcase_data[case_count]['module'])
            case_description_list.append(taskcase_data[case_count]['title'])
            precondition_list.append(taskcase_data[case_count]['precondition'])
            opearating_steps_data = json.loads(taskcase_data[case_count]['step_result'])['step_result']

            opearating_steps_string = ''
            expect_result_string = ''
            for step_count in range(0, len(opearating_steps_data)):
                if opearating_steps_string:
                    opearating_steps_string = (opearating_steps_string + ' \n' + '{}、'.format(step_count + 1)
                                               + opearating_steps_data[step_count]['step'])
                else:
                    opearating_steps_string = (str(step_count + 1) + '、' + opearating_steps_string
                                               + opearating_steps_data[step_count]['step'])
                if expect_result_string:
                    expect_result_string = (expect_result_string + ' \n' + '{}、'.format(step_count + 1)
                                            + opearating_steps_data[step_count]['expect'])
                else:
                    expect_result_string = (str(step_count + 1) + '、' + expect_result_string
                                            + opearating_steps_data[step_count]['expect'])
            opearating_steps_list.append(opearating_steps_string)
            expect_result_list.append(expect_result_string)
            cnumber_list.append(taskcase_data[case_count]['cnumber'])
            ctype = taskcase_data[case_count]['ctype'].split(',')

            ctype_list.append(','.join([CTYPE[i] for i in ctype]))
            if (str(taskcase_data[case_count]['priority'])).isdigit():
                if int(taskcase_data[case_count]['priority']) == 0:
                    priority_list.append('紧急')
                elif int(taskcase_data[case_count]['priority']) == 1:
                    priority_list.append('高')
                elif int(taskcase_data[case_count]['priority']) == 2:
                    priority_list.append('中')
                elif int(taskcase_data[case_count]['priority']) == 3:
                    priority_list.append('低')
                else:
                    priority_list.append('')
            else:
                priority_list.append('')

        for i in range(3, len(cnumber_list) + 3):
            sheet.write(i, 0, cnumber_list[i - 3], style)
            sheet.write(i, 1, module_name_list[i - 3], style)
            sheet.write(i, 2, case_description_list[i - 3], style)
            sheet.write(i, 3, precondition_list[i - 3], style)
            sheet.write(i, 4, opearating_steps_list[i - 3], style)
            sheet.write(i, 5, expect_result_list[i - 3], style)
            sheet.write(i, 6, priority_list[i - 3], style)
            sheet.write(i, 7, ctype_list[i - 3], style)
            sheet.write(i, 10, creator_list[i - 3], style)
            sheet.write(i, 11, creation_time_list[i - 3], style)

        dir_path = f'{TCLOUD_FILE_TEMP_PATH}/cases/'

        if not os.path.exists(TCLOUD_FILE_TEMP_PATH):
            os.mkdir(TCLOUD_FILE_TEMP_PATH)

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        if not user_id:
            user_id = 'nobody'

        file_path = f'{dir_path}/case-{user_id}.xls'
        workbook.save(file_path)
        url = oss_upload(path=file_path, project_name='case_export',
                         file_name=str(int(time.time())) + '.xls', user_id=user_id)

        return 0, {"url": url}, 'ok'

    @classmethod
    def case_import(cls, url_path, creator, project_id, module_id):
        file_path = oss_download(creator, url_path)
        code, message = cls.analysis_excel(file_path, creator, project_id, module_id)
        return code, message

    @classmethod
    def analysis_excel(cls, file_path, creator, project_id, module_id):
        workbook = xlrd.open_workbook(file_path)
        # 获取sheet
        sheet_names = workbook.sheet_names()
        if len(sheet_names) != 1:
            return 102, '未按规定填写sheet'

        table = workbook.sheet_by_index(0)

        if table.row_len(0) != 10 and table.row_len(0) != 8:
            return 102, '上传的格式不正确，请下载最新模板'

        for i in range(3, table.nrows):

            title = "{}".format(str(table.cell(i, 2).value))
            precondition = str(table.cell(i, 3).value)
            step = re.sub(r'\d+、', '', table.cell(i, 4).value).split('\n')
            step_remove = [a.lstrip() for a in step if a != '']
            expect = re.sub(r'\d+、', '', table.cell(i, 5).value).split('\n')
            priority_string = (str(table.cell(i, 6).value))
            expect_remove = [a.lstrip() for a in expect]
            ctype_list = str(table.cell(i, 7).value).split(u'、')
            ctype_dict = {v: k for k, v in CTYPE.items()}
            ctype_string = '1'
            ctype_tmp_list = []
            for ctype in ctype_list:
                if ctype in ctype_dict.keys():
                    ctype_tmp_list.append(ctype_dict[ctype])
            if ctype_tmp_list:
                ctype_tmp_list = sorted(ctype_tmp_list)
                ctype_string = ','.join(ctype_tmp_list)

            temp_list = []
            for j in range(len(step_remove)):
                step_remove_dict = dict(step=step_remove[j])
                step_remove_dict['expect'] = ''
                if len(expect_remove) > j:
                    step_remove_dict['expect'] = expect_remove[j]
                temp_list.append(step_remove_dict)
            step_result = dict(step_result=temp_list)

            if priority_string == '紧急':
                priority = 0
            elif priority_string == '高':
                priority = 1
            elif priority_string == '中':
                priority = 2
            elif priority_string == '低':
                priority = 3
            else:
                priority = None
            CaseBusiness.create(module_id, ctype_string, title, precondition,
                                json.dumps(step_result, ensure_ascii=False),
                                creator, priority)

        return 0, '导入成功'

    @classmethod
    def filter_query(cls, mid=None):
        pid = request.args.get('project_id')
        title = request.args.get('title')
        priority = request.args.get('priority')
        ctype = request.args.get('ctype')
        user_ids = request.args.get('user_ids')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        module_data = request.args.get('module_data')

        ret = cls._query()
        if module_data:
            module_data = module_data.split(',')
            ret = ret.filter(Case.module_id.in_(module_data))
        if priority:
            priority = priority.split(',')
            ret = ret.filter(Case.priority.in_(priority))
        if ctype:
            ret = ret.filter(func.find_in_set(ctype, Case.ctype))
        if user_ids:
            user_ids = user_ids.split(',')
            ret = ret.filter(Case.creator.in_(user_ids))
        if title:
            ret = ret.filter(or_(Case.title.like('%{}%'.format(title)), Case.cnumber.like('%{}%'.format(title))))
        if start_time and end_time:
            ret = ret.filter(Case.creation_time.between(start_time, end_time + " 23:59:59"))
        if mid:
            ret = ret.filter(Case.module_id == mid)
            pid = None
        if pid:
            ret = ret.filter(
                Case.status == Case.ACTIVE,
                Case.module_id.in_([module_lists[0] for module_lists in db.session.query(Module.id).filter(
                    Module.project_id == pid, Module.status == Module.ACTIVE).all()])).order_by(
                desc(Case.id))
        else:
            ret = ret.filter(Case.status == Case.ACTIVE).order_by(
                desc(Case.id))
        return ret

    @classmethod
    @transfer2json(
        '?id|!cnumber|!ctype|!title|!precondition|!step_result|!creation_time|!modified_time'
        '|!is_auto|!status|!moduleid|!module|!userid|!username|!priority',
        ispagination=True
    )
    def paginate_data(cls, page_size=None, page_index=None, only_data=False, mid=None):
        query = cls.filter_query(mid=mid)
        if only_data:
            count = 0
        else:
            count = query.count()
        if page_size and page_index:
            size, index = int(page_size), int(page_index)
            query = query.limit(size).offset((index - 1) * size)
        data = query.all()
        return data, count

    @classmethod
    @transfer2json(
        '?id|!cnumber|!ctype|!title|!precondition|!step_result|!creation_time|!modified_time'
        '|!is_auto|!status|!moduleid|!module|!userid|!username|!priority',
    )
    def case_info_by_ids(cls, case_ids):
        ret = cls.filter_query().filter(Case.id.in_(case_ids[0]))
        data = ret.all()
        return data

    @classmethod
    def copy_case_by_id(cls, case_id):
        ret = Case.query.get(case_id)
        if ret:
            cls.create(ret.module_id, ret.ctype, ret.title, ret.precondition, ret.step_result, g.userid, ret.priority)
            return 0
        else:
            raise OperationFailedException
