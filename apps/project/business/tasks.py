import json
import os
import time

import xlwt
from flask import request, g, current_app
from sqlalchemy import desc, func, or_
from sqlalchemy.orm import aliased

from apps.auth.models.users import User
from apps.project.business.modules import ModuleBusiness
from apps.project.business.tag import TagBusiness
from apps.project.models.cases import Case
from apps.project.models.modules import Module
from apps.project.models.project import Project
from apps.project.models.tag import Tag
from apps.project.models.tasks import Task, TaskCase, TaskCaseRecord
from apps.project.models.version import Version
from library.api.db import db
from library.api.transfer import transfer2json, slicejson
from library.notification import notification
from library.oss import oss_upload
from library.trpc import Trpc
from public_config import CTYPE, TCLOUD_FILE_TEMP_PATH


class TaskBusiness(object):
    user_trpc = Trpc('auth')
    public_trpc = Trpc('public')

    @classmethod
    def _query(cls):
        user_creator = aliased(User)
        user_executor = aliased(User)
        return Task.query.outerjoin(
            user_creator, user_creator.id == Task.creator).outerjoin(
            user_executor, user_executor.id == Task.executor).outerjoin(
            Version, Version.id == Task.version).add_columns(
            Task.id.label('id'),
            Task.name.label('name'),
            Task.description.label('description'),
            Task.testreport.label('testreport'),
            Task.case_list.label('case_list'),
            Task.tmethod.label('tmethod'),
            Task.ttype.label('ttype'),
            Task.status.label('status'),
            func.date_format(Task.start_time, "%Y-%m-%d").label('start_time'),
            func.date_format(Task.end_time, "%Y-%m-%d").label('end_time'),
            Task.project_id.label('project_id'),
            Task.priority.label('priority'),
            Task.attach.label('attach'),
            Task.attachment.label('attachment'),
            Version.id.label('version_id'),
            Version.title.label('version_name'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),
            user_executor.id.label('executor_id'),
            user_executor.nickname.label('executor_name'),
            Task.tag.label('tag'),
        )

    @classmethod
    def filter_query(cls):
        projectid = request.args.get('projectid')
        versionid = request.args.get('versionid')
        handlerid = request.args.get('handler')
        priority = request.args.get('priority')
        status = request.args.get('status')
        title = request.args.get('title')
        tag = request.args.get('tag')
        ret = cls._query().filter(Task.status != Task.DISABLE)
        if projectid:
            ret = ret.filter(Task.project_id == projectid)
        if versionid:
            ret = ret.filter(Task.version == versionid)
        if handlerid:
            handlerid = handlerid.split(',')
            ret = ret.filter(Task.executor.in_(handlerid))
        if priority:
            priority = priority.split(',')
            ret = ret.filter(Task.priority.in_(priority))
        if status:
            status = status.split(',')
            ret = ret.filter(Task.status.in_(status))
        if title:
            ret = ret.filter(or_(Task.name.like(f'%{title}%'), Task.id.startswith(f'{title}%')))
        if tag:
            ret = ret.filter(func.find_in_set(tag, Task.tag))
        ret = ret.order_by(desc(Task.id))
        return ret

    @classmethod
    def query_task_case_json(cls, page_size=None, page_index=None):
        data, count = cls.pageinate_data(page_size, page_index)

        for a in range(len(data)):
            taskcase_status = TaskCaseDashBoardBusiness.task_case_status_dashboard(data[a]['id'])
            taskcase_status_dict = {"pass": 3, "fail": 4, "skip": 2, "unexecuted": 0}
            taskcase_status_reset = {"pass": 0, "fail": 0, "skip": 0, "unexecuted": 0}
            for key, value in taskcase_status_dict.items():
                for i in taskcase_status:
                    if i['status'] == value:
                        taskcase_status_reset[key] = int(i['count'])
            taskcase_status_reset['sum'] = sum(taskcase_status_reset.values())
            data[a]['casestatus'] = taskcase_status_reset
        return data, count

    @classmethod
    def query_task_data_filter(cls):
        tag = request.args.get('tag')
        ret = cls.query_task_case_json()
        if tag:
            tag = str(tag)
            tag_list = tag.split(',')
            copy_ret = []
            for a in range(len(ret)):
                singel_tag = ret[a]['tag']
                singel_tag_list = (str(singel_tag)).split(',')
                if len((list(set(tag_list).intersection(set(singel_tag_list))))) > 0:
                    copy_ret.append(ret[a])
            return copy_ret
        return ret

    @classmethod
    @slicejson([
        'executor|id|name|executor_id|executor_name',
        'creator|id|name|creator_id|creator_name', 'version|id|name|version_id|version_name'
    ])
    @transfer2json(
        '?id|!name|!description|~case_list|!attach|!attachment|!testreport|!tmethod|!ttype|!status|!start_time|'
        '!end_time|!priority|!project_id|@version_id|@version_name'
        '|@creator_id|@creator_name|@executor_id|@executor_name|!tag')
    def _query_borad(cls, user, start_time, end_time, project_id, version):
        ret = cls._query().filter(Task.status != Task.DISABLE)
        list_key = ['executor', 'project_id', 'version']
        list_val = [user, project_id, version]

        task_dict = dict(zip(list_key, list_val))
        for key, val in task_dict.items():
            if val != '' and val is not None:
                task = "Task.{}".format(key)
                current_app.logger.info(task, )
                ret = ret.filter(eval(task) == val)
        if start_time and end_time:
            ret = ret.filter(Task.modified_time.between(start_time, end_time + " 23:59:59"))
        ret = ret.order_by(desc(Task.id)).all()
        return ret

    @classmethod
    def query_borad(cls, user, start_time, end_time, project_id, version):
        try:
            ret = cls._query_borad(user, start_time, end_time, project_id, version)
            for i in range(len(ret)):
                ret[i]['caseinfo'] = cls.query_task_case_info(ret[i]['id'])
            return ret
        except Exception as e:
            current_app.logger.error(str(e))
            return []

    @classmethod
    def query_task_case_info(cls, taskid):
        task_case_info = TaskCase.query.add_columns(
            TaskCase.status.label('status'),
            func.count('*').label('count')). \
            filter(TaskCase.task_id == taskid and TaskCase.status != TaskCase.DISABLE). \
            group_by(TaskCase.status).all()
        detail = [dict(i) for i in map(lambda x: zip(('status', 'count'), x),
                                       zip([i.status for i in task_case_info], [i.count for i in task_case_info]))]
        return detail

    @classmethod
    @slicejson([
        'executor|id|name|executor_id|executor_name',
        'creator|id|name|creator_id|creator_name', 'version|id|name|version_id|version_name'
    ])
    @transfer2json(
        '?id|!name|!description|~case_list|!attach|!attachment|!testreport|!tmethod|!ttype|!status|!start_time|'
        '!end_time|!priority|!project_id|@version_id|@version_name'
        '|@creator_id|@creator_name|@executor_id|@executor_name|!tag')
    def query_json_by_id(cls, id):
        return cls._query().filter(Task.id == id,
                                   Task.status != Task.DISABLE).order_by(
            desc(Task.id)).all()

    @classmethod
    def query_task_case_json_by_id(cls, id):
        ret = cls.query_json_by_id(id)
        for a in range(len(ret)):
            taskcase_status = TaskCaseDashBoardBusiness.task_case_status_dashboard(ret[a]['id'])
            taskcase_status_dict = {"pass": 3, "fail": 4, "skip": 2, "unexecuted": 0}
            taskcase_status_reset = {"pass": 0, "fail": 0, "skip": 0, "unexecuted": 0}
            for key, value in taskcase_status_dict.items():
                for i in taskcase_status:
                    if i['status'] == value:
                        current_app.logger.info("key:" + key + ",value:" + str(int(i['count'])))
                        taskcase_status_reset[key] = int(i['count'])
            taskcase_status_reset['sum'] = sum(taskcase_status_reset.values())
            ret[a]['casestatus'] = taskcase_status_reset
            current_app.logger.info(ret)
        return ret

    @classmethod
    def query_task_json(cls, id):
        task = cls.query_json_by_id(id)
        for i in range(len(task)):
            # task[i]['case_list'] = TaskCaseBusiness.query_borad('','','',task[i]['id'])
            taskcase_list = TaskCase.query.add_columns(
                TaskCase.id.label('id')).filter(TaskCase.status != TaskCase.DISABLE,
                                                TaskCase.task_id == task[i]['id']).order_by(TaskCase.id).all()
            temp_list = []
            for a in taskcase_list:
                temp_list.append(a.id)
            task[i]['case_list'] = temp_list
        return task

    @classmethod
    @slicejson([
        'executor|id|name|executor_id|executor_name',
        'creator|id|name|creator_id|creator_name'
    ])
    @transfer2json(
        '?id|!name|!description|~case_list|!attach|!attachment|!testreport|!tmethod|!ttype|!status|!start_time|'
        '!end_time|!priority|!project_id|!version_id'
        '|@creator_id|@creator_name|@executor_id|@executor_name|!tag')
    def query_by_version_id(cls, version_id):
        return cls._query().filter(Task.version == version_id,
                                   Task.status != Task.DISABLE).order_by(
            desc(Task.id)).all()

    @classmethod
    def delete(cls, id):
        return cls.status_switch(id, Task.DISABLE)

    @classmethod
    def status_switch(cls, id, mstatus):
        try:
            taskcase = TaskCase.query.filter(TaskCase.status == TaskCase.ACTIVE, TaskCase.task_id == id).all()
            if taskcase and int(mstatus) is 2:
                return 106, '任务用例未全部执行！'
            task = Task.query.get(id)
            if mstatus is 1:
                current_app.logger.info('task remove,taskcase remove too.')
                for case in taskcase:
                    case.status = 1
                if task.tag:
                    TagBusiness.less_reference(task.tag)
            task.status = mstatus
            db.session.add(task, taskcase)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 106, str(e)

    @classmethod
    def testreport_switch(cls, id, testreport, attach):
        try:
            task = Task.query.get(id)
            task.testreport = testreport
            task.attach = attach
            db.session.add(task)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 106, str(e)

    @classmethod
    def priority_switch(cls, id, priority):
        try:
            task = Task.query.get(id)
            task.priority = priority
            db.session.add(task)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 106, str(e)

    @classmethod
    def create(cls, name, description, tmethod, ttype, creator, executor, start_time,
               end_time, priority, project_id, version, case_list, testreport, attach, tag, attachment):
        try:
            creator = g.userid if g.userid else None
            current_app.logger.info("creator:" + str(creator))
            task = Task(
                name=name,
                description=description,
                case_list=str(case_list),
                tmethod=tmethod,
                ttype=ttype,
                creator=creator,
                executor=executor,
                start_time=start_time,
                end_time=end_time,
                project_id=project_id,
                version=version,
                priority=priority,
                attach=attach,
                testreport=testreport,
                tag=tag,
                attachment=attachment,
            )
            db.session.add(task)
            db.session.flush()
            if isinstance(case_list, list) and case_list:
                # list去掉非数字字符
                [case_list.remove(i) for i in case_list if not isinstance(i, int)]
                TaskBusiness.relation_case(task.id, case_list, task.project_id, task.version)
            else:
                current_app.logger.info("case_list should be  a Non empty list！")
            db.session.commit()
            if tag:
                TagBusiness.add_reference(tag)

            user_list = [executor]
            board_config = cls.public_trpc.requests('get', '/public/config', {'module': 'tcloud', 'module_type': 1})
            text = f'''[任务创建 - {name}]
URL：{board_config}/project/{project_id}/version/{version}'''
            notification.send_notification(user_list, text, send_type=2)
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
            return 102

    @classmethod
    def modify(cls, id, name, description, tmethod, ttype, executor, start_time, end_time, priority, case_list,
               testreport, attach, tag, attachment):
        try:
            task = Task.query.get(id)
            old_tag = []
            new_tag = []
            is_change_executor = False
            if task.executor != executor:
                is_change_executor = True
            old_case_list = task.case_list
            old_case_list = json.loads(old_case_list)
            # 数据库数字是Unicode编码
            for i in range(len(old_case_list)):
                old_case_list[i] = int(old_case_list[i])
            [case_list.remove(i) for i in case_list if not isinstance(i, int)]
            del_list = []
            add_list = []
            for addlist in case_list:
                if addlist not in old_case_list:
                    add_list.append(addlist)
            for dellist in old_case_list:
                if dellist not in case_list:
                    del_list.append(dellist)
            current_app.logger.info("old_case_list" + str(old_case_list))
            current_app.logger.info("new_case_list" + str(case_list))
            current_app.logger.info("add_list" + str(add_list))
            current_app.logger.info("del_list" + str(del_list))
            TaskBusiness.relation_case(id, add_list, task.project_id, task.version)
            for deltaskcase in del_list:
                # 待优化
                TaskBusiness.case_delete(id, deltaskcase)
            task.name = name
            task.description = description
            task.case_list = str(case_list)
            task.tmethod = tmethod
            task.ttype = ttype
            task.executor = executor
            task.start_time = start_time
            task.end_time = end_time
            task.priority = priority
            if task.tag != tag:
                old_tag = task.tag
                new_tag = tag
                task.tag = tag
            task.attachment = attachment
            # task.testreport = testreport
            # task.attach = attach
            db.session.add(task)
            db.session.commit()

            if old_tag or new_tag:
                TagBusiness.change_reference(old_tag, new_tag)
            if is_change_executor:
                modifier_user = cls.user_trpc.requests('get', f'/user/{g.userid}')
                if modifier_user:
                    modifier_user = modifier_user[0].get('nickname')
                handler_user = cls.user_trpc.requests('get',
                                                      f'/user'
                                                      f'/{executor if not isinstance(executor, list) else executor[0]}')
                if handler_user:
                    handler_user = handler_user[0].get('nickname')
                if not isinstance(executor, list):
                    executor = [executor]
                text = f'''[task处理人修改 - {name}]
{modifier_user} 修改处理人为 {handler_user}'''
                notification.send_notification(executor, text, send_type=2)
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 102

    @classmethod
    def relation_case(cls, taskid, case_list, project_id, version):
        for case in case_list:
            cases = Case.query.filter(Case.id == case).first()
            task_case = TaskCase(
                task_id=taskid,
                cnumber=cases.cnumber,
                # executor=executor_id,
                # exe_way=exe_way,
                module_id=cases.module_id,
                project_id=project_id,
                version=version,
                ctype=cases.ctype,
                title=cases.title,
                description=cases.description,
                precondition=cases.precondition,
                step_result=cases.step_result,
                is_auto=cases.is_auto,
                priority=cases.priority,
            )
            db.session.add(task_case)
            db.session.flush()
            task_case_record = TaskCaseRecord(
                task_case_id=task_case.id,
                task_id=taskid,
                cnumber=cases.cnumber,
                # executor=executor,
                # exe_way=exe_way,
                module_id=cases.module_id,
                project_id=project_id,
                version=version,
                ctype=cases.ctype,
                title=cases.title,
                description=cases.description,
                precondition=cases.precondition,
                step_result=cases.step_result,
                is_auto=cases.is_auto,
                priority=cases.priority,
            )
            db.session.add(task_case_record)
        db.session.commit()

    @classmethod
    def case_delete(cls, task_id, case_id):
        try:
            case = Case.query.get(case_id)
            task_case = TaskCase.query.filter(TaskCase.task_id == task_id, TaskCase.cnumber == case.cnumber,
                                              TaskCase.status != TaskCase.DISABLE).first()
            current_app.logger.info(task_id)
            current_app.logger.info(task_case.id)
            task_case.status = TaskCase.DISABLE
            db.session.add(task_case)
            task_case_record = TaskCaseRecord(
                task_id=task_case.task_id,
                task_case_id=task_case.id,
                cnumber=task_case.cnumber,
                executor=task_case.executor,
                exe_way=task_case.exe_way,
                module_id=task_case.module_id,
                project_id=task_case.project_id,
                version=task_case.version,
                ctype=task_case.ctype,
                title=task_case.title,
                description=task_case.description,
                precondition=task_case.precondition,
                step_result=task_case.step_result,
                is_auto=task_case.is_auto,
                status=task_case.status,
                comment=task_case.comment,
            )
            db.session.add(task_case_record)
            db.session.commit()
            return 0
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            return 106

    @classmethod
    @transfer2json('?tag')
    def query_all_tag(cls, project_id):
        ret = cls._query().filter(Task.status != Task.DISABLE, Task.project_id == project_id)
        ret = ret.order_by(desc(Task.id)).all()

        return ret

    @classmethod
    def judge_tag_include(cls, tagid, project_id):
        ret = cls.query_all_tag(project_id)
        for i in range(0, len(ret)):
            if ret[i]['tag']:
                tag_string = str(ret[i]['tag'])
                tag_list = tag_string.split(',')
                if tagid in tag_list:
                    return True
        return False

    @classmethod
    @slicejson([
        'executor|id|name|executor_id|executor_name',
        'creator|id|name|creator_id|creator_name', 'version|id|name|version_id|version_name'
    ], ispagination=True)
    @transfer2json(
        '?id|!name|!description|~case_list|!attach|!attachment|!testreport|!tmethod|!ttype|!status|'
        '!start_time|!end_time|!priority|!project_id|@version_id|@version_name'
        '|@creator_id|@creator_name|@executor_id|@executor_name|!tag', ispagination=True)
    def pageinate_data(cls, page_size, page_index):
        query = cls.filter_query()
        count = query.count()
        data = query.limit(int(page_size)).offset((int(page_index) - 1) * int(page_size)).all()
        return data, count


class TaskCaseBusiness(object):
    user_trpc = Trpc('auth')

    @classmethod
    def _query(cls):
        user_executor = aliased(User)
        user_handler = aliased(User)

        return TaskCase.query.outerjoin(
            Module, TaskCase.module_id == Module.id).outerjoin(
            user_executor, user_executor.id == TaskCase.executor).outerjoin(
            user_handler, user_handler.id == TaskCase.handler).add_columns(
            TaskCase.id.label('taskcaseid'),
            TaskCase.task_id.label('task_id'),
            TaskCase.exe_way.label('exe_way'),
            TaskCase.cnumber.label('cnumber'),
            TaskCase.ctype.label('ctype'),
            TaskCase.title.label('title'),
            TaskCase.description.label('description'),
            TaskCase.precondition.label('precondition'),
            TaskCase.step_result.label('step_result'),
            TaskCase.is_auto.label('is_auto'),
            TaskCase.status.label('status'),
            TaskCase.comment.label('comment'),
            TaskCase.priority.label('priority'),
            func.date_format(TaskCase.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            Module.id.label('module_id'),
            Module.name.label('module_name'),
            user_executor.id.label('executor_id'),
            user_executor.nickname.label('executor_name'),
            user_handler.id.label('handler_id'),
            user_handler.nickname.label('handler_name'),
        )

    @classmethod
    @transfer2json(
        '?taskcaseid|!task_id|!executor_id|!executor_name|!handler_id|!handler_name|!exe_way|!cnumber|!ctype|!title|'
        '!description|!precondition|!step_result|!is_auto|!status|!comment|!module_id|!module_name|!priority')
    def query_by_id(cls, task_case_id):
        ret = cls._query().filter(TaskCase.status != TaskCase.DISABLE,
                                  TaskCase.id == task_case_id).all()
        return ret

    @classmethod
    @transfer2json(
        '?taskcaseid|!task_id|!executor_id|!executor_name|!handler_id|!handler_name|!exe_way|!cnumber|!ctype|!title|'
        '!description|!precondition|!step_result|!is_auto|!status|!comment|!module_id|!module_name|!priority')
    def _query_all_json(cls):
        projectid = request.args.get('projectid')
        versionid = request.args.get('versionid')
        taskid = request.args.get('taskid')
        handlerid = request.args.get('handler')
        priority = request.args.get('priority')
        status = request.args.get('status')
        title = request.args.get('title')
        ret = cls._query().filter(TaskCase.status != TaskCase.DISABLE)
        if projectid:
            ret = ret.filter(TaskCase.project_id == projectid)
        if versionid:
            ret = ret.filter(TaskCase.version == versionid)
        if taskid:
            ret = ret.filter(TaskCase.task_id == taskid)
        if handlerid:
            handlerid = handlerid.split(',')
            ret = ret.filter(TaskCase.handler.in_(handlerid))
        if priority:
            priority = priority.split(',')
            ret = ret.filter(TaskCase.priority.in_(priority))
        if status:
            status = status.split(',')
            ret = ret.filter(TaskCase.status.in_(status))
        if title:
            ret = ret.filter(or_(TaskCase.title.like(f'%{title}%'), TaskCase.id.startswith(f'{title}%')))
        ret = ret.order_by(desc(TaskCase.id)).all()
        return ret

    @classmethod
    def query_all_json(cls):
        ret = cls._query_all_json()
        current_app.logger.info("taskcase query_all_json")
        current_app.logger.info(ret)
        module_id_list = []
        module_ret = []
        for i in range(len(ret)):
            module_id_list.append(ret[i]['module_id'])
        module_id_list = list(set(module_id_list))
        for i in range(len(module_id_list)):
            module_ret.append(dict(module_id=module_id_list[i], info=[]))
        for i in range(len(ret)):
            for a in range(len(module_ret)):
                if ret[i]['module_id'] == module_ret[a]['module_id']:
                    module_ret[a]['info'].append(ret[i])
                    module_ret[a]['module_name'] = ret[i]['module_name']
        return module_ret

    @classmethod
    @transfer2json(
        '?taskcaseid|!task_id|!executor_id|!executor_name|!handler_id|!handler_name|!exe_way|!cnumber|!ctype|'
        '!title|!description|!precondition|!step_result|!is_auto|'
        '!status|!comment|!module_id|!module_name|!priority')
    def _query_borad(cls, user, project_id, version, task_id):
        ret = cls._query().filter(TaskCase.status != TaskCase.DISABLE)
        list_key = ['executor', 'project_id', 'version', 'task_id']
        list_val = [user, project_id, version, task_id]

        task_dict = dict(zip(list_key, list_val))
        for key, val in task_dict.items():
            if val != '' and val is not None:
                taskcase = "TaskCase.{}".format(key)
                current_app.logger.info(taskcase)
                ret = ret.filter(eval(taskcase) == val)
        ret = ret.all()
        return ret

    @classmethod
    def query_borad(cls, user, project_id, version, task_id):
        try:
            ret = cls._query_borad(user, project_id, version, task_id)
            return ret
        except Exception as e:
            current_app.logger.error(str(e))
            return []

    @classmethod
    def delete(cls, task_case_id):
        try:
            task_case = TaskCase.query.get(task_case_id)
            task_case.status = TaskCase.DISABLE
            db.session.add(task_case)
            task_case_record = TaskCaseRecord(
                task_id=task_case.task_id,
                task_case_id=task_case.id,
                cnumber=task_case.cnumber,
                executor=task_case.executor,
                exe_way=task_case.exe_way,
                module_id=task_case.module_id,
                project_id=task_case.project_id,
                version=task_case.version,
                ctype=task_case.ctype,
                title=task_case.title,
                description=task_case.description,
                precondition=task_case.precondition,
                step_result=task_case.step_result,
                is_auto=task_case.is_auto,
                status=task_case.status,
                comment=task_case.comment,
                priority=task_case.priority,

            )
            db.session.add(task_case_record)
            db.session.commit()
            return 0
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def modify(cls, task_case_id, module_id, project_id, version, executor, exe_way, ctype, title, description,
               precondition, step_result, is_auto, status, comment, priority):
        try:
            task_case = TaskCase.query.get(task_case_id)
            task_case.executor = executor
            task_case.exe_way = exe_way
            task_case.module_id = module_id
            # task_case.cnumber = cnumber,
            # task_case.project_id = project_id
            # task_case.version = version
            task_case.ctype = ctype
            task_case.title = title
            task_case.description = description
            task_case.precondition = precondition
            task_case.step_result = step_result
            task_case.is_auto = is_auto
            task_case.status = status
            task_case.comment = comment
            task_case.priority = priority,
            db.session.add(task_case)
            TaskCaseRecordBusiness.create(task_case_id, task_case.task_id, module_id, version, executor, exe_way, ctype,
                                          title, description, precondition, step_result, is_auto, status, comment,
                                          priority)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
            return 102

    @classmethod
    def status_switch(cls, id, mstatus):
        try:
            task_case = TaskCase.query.get(id)
            task_case.status = mstatus
            db.session.add(task_case)
            task_case_record = TaskCaseRecord(
                task_id=task_case.task_id,
                task_case_id=task_case.id,
                cnumber=task_case.cnumber,
                executor=task_case.executor,
                exe_way=task_case.exe_way,
                module_id=task_case.module_id,
                project_id=task_case.project_id,
                version=task_case.version,
                ctype=task_case.ctype,
                title=task_case.title,
                description=task_case.description,
                precondition=task_case.precondition,
                step_result=task_case.step_result,
                is_auto=task_case.is_auto,
                status=mstatus,
                comment=task_case.comment,
                priority=task_case.priority,

            )
            db.session.add(task_case_record)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def add_comment(cls, id, comment):
        try:
            task_case = TaskCase.query.get(id)
            task_case.comment = comment
            db.session.add(task_case)
            task_case_record = TaskCaseRecord(
                task_id=task_case.task_id,
                task_case_id=task_case.id,
                cnumber=task_case.cnumber,
                executor=task_case.executor,
                exe_way=task_case.exe_way,
                module_id=task_case.module_id,
                project_id=task_case.project_id,
                version=task_case.version,
                ctype=task_case.ctype,
                title=task_case.title,
                description=task_case.description,
                precondition=task_case.precondition,
                step_result=task_case.step_result,
                is_auto=task_case.is_auto,
                status=task_case.status,
                comment=comment,
                priority=task_case.priority,

            )
            db.session.add(task_case_record)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def assign_task_case(cls, project_id, case_list, handler):
        try:
            handle = User.query.get(handler)
            if handle is None:
                return 101
            modifier = g.userid if g.userid else None
            for task_case_id in case_list:
                task_case = TaskCase.query.filter(TaskCase.id == task_case_id, TaskCase.project_id == project_id,
                                                  TaskCase.status != TaskCase.DISABLE).first()
                if task_case is None:
                    return 101
                task_case.handler = handler
                task_case_record = TaskCaseRecord(
                    task_id=task_case.task_id,
                    task_case_id=task_case.id,
                    cnumber=task_case.cnumber,
                    handler=handler,
                    exe_way=task_case.exe_way,
                    module_id=task_case.module_id,
                    project_id=task_case.project_id,
                    version=task_case.version,
                    ctype=task_case.ctype,
                    title=task_case.title,
                    description=task_case.description,
                    precondition=task_case.precondition,
                    step_result=task_case.step_result,
                    is_auto=task_case.is_auto,
                    status=task_case.status,
                    comment=task_case.comment,
                    modifier=modifier,
                    priority=task_case.priority,
                )
                db.session.add(task_case, task_case_record)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def priority_switch(cls, id, priority):
        try:
            task_case = TaskCase.query.get(id)
            task_case.priority = priority
            db.session.add(task_case)
            task_case_record = TaskCaseRecord(
                task_id=task_case.task_id,
                task_case_id=task_case.id,
                cnumber=task_case.cnumber,
                executor=task_case.executor,
                exe_way=task_case.exe_way,
                module_id=task_case.module_id,
                project_id=task_case.project_id,
                version=task_case.version,
                ctype=task_case.ctype,
                title=task_case.title,
                description=task_case.description,
                precondition=task_case.precondition,
                step_result=task_case.step_result,
                is_auto=task_case.is_auto,
                status=task_case.status,
                comment=task_case.comment,
            )
            db.session.add(task_case_record)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def priority_batch_switch(cls, project_id, case_list, priority):
        try:
            # 优先级 0:紧急 1:高 2:中 3:低
            if priority not in [0, 1, 2, 3]:
                return 106
            modifier = g.userid if g.userid else None
            for task_case_id in case_list:
                task_case = TaskCase.query.filter(TaskCase.id == task_case_id, TaskCase.project_id == project_id,
                                                  TaskCase.status != TaskCase.DISABLE).first()
                if task_case is None:
                    return 101
                task_case.priority = priority
                task_case_record = TaskCaseRecord(
                    task_id=task_case.task_id,
                    task_case_id=task_case.id,
                    cnumber=task_case.cnumber,
                    handler=task_case.handler,
                    exe_way=task_case.exe_way,
                    module_id=task_case.module_id,
                    project_id=task_case.project_id,
                    version=task_case.version,
                    ctype=task_case.ctype,
                    title=task_case.title,
                    description=task_case.description,
                    precondition=task_case.precondition,
                    step_result=task_case.step_result,
                    is_auto=task_case.is_auto,
                    status=task_case.status,
                    comment=task_case.comment,
                    modifier=modifier,
                    priority=priority,
                )
                db.session.add(task_case, task_case_record)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
        return 106

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
    def query_by_project_id_total_taskcase(cls, pid):
        ret = cls._query_total_taskcase().filter(Module.status == Module.ACTIVE,
                                                 Module.project_id == pid,
                                                 TaskCase.status != TaskCase.DISABLE).order_by(
            desc(Module.id)).group_by(TaskCase.module_id).all()
        return ret

    @classmethod
    def query_by_project_task_case_1(cls):
        pid = request.args.get('projectid')
        total_ret = cls.query_by_project_id_total_taskcase(pid)
        module_case = cls._query_all_json()
        for t in range(len(total_ret)):
            total_ret[t]['info'] = []
            for mc in module_case:
                if total_ret[t]['id'] == mc['module_id']:
                    total_ret[t]['info'].append(mc)

        total_ret = ModuleBusiness.converter(total_ret)
        taskcase_ret = []
        for ret in total_ret:
            if ret['info']:
                taskcase_ret.append(ret)
            elif 'modules' in ret and ret['modules']:
                for module in ret['modules']:
                    if module['info']:
                        taskcase_ret.append(ret)
            total_ret = taskcase_ret
        total_ret = sorted(total_ret, key=lambda x: x['id'], reverse=True)
        return total_ret

    @classmethod
    def query_by_project_task_case_2(cls):
        pid = request.args.get('projectid')
        total_ret = cls.query_by_project_id_total_taskcase(pid)
        module_case = cls._query_all_json()
        for t in range(len(total_ret)):
            total_ret[t]['info'] = []
            for mc in module_case:
                if total_ret[t]['id'] == mc['module_id']:
                    total_ret[t]['info'].append(mc)

        taskcase_ret = []
        for ret in total_ret:
            if ret['info']:
                taskcase_ret.append(ret)
            total_ret = taskcase_ret
        total_ret = sorted(total_ret, key=lambda x: x['id'], reverse=True)
        return total_ret

    @classmethod
    @transfer2json(
        '?taskcaseid|!task_id|!executor_id|!executor_name|!handler_id|!handler_name|!exe_way|!cnumber|!ctype|!title|'
        '!description|!precondition|!step_result|!is_auto|!status|!comment|!module_id|!module_name|!priority|!creation_time')
    def taskcase_query_all_json(cls, taskid, parent_module=''):
        ret = cls._query().filter(TaskCase.status != TaskCase.DISABLE)
        if taskid:
            ret = ret.filter(TaskCase.task_id == taskid).order_by(desc(TaskCase.module_id))
        if parent_module:
            ret = ret.filter(Module.parent_id is not None).group_by(TaskCase.module_id)
        ret = ret.all()
        return ret

    @classmethod
    def export(cls, project_id, task_id):
        module_name = []
        taskcase_data = cls.taskcase_query_all_json(task_id)
        workbook = xlwt.Workbook()
        alignment = xlwt.Alignment()
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        alignment.horz = xlwt.Alignment.HORZ_LEFT
        alignment.vert = xlwt.Alignment.VERT_TOP

        style = xlwt.XFStyle()
        style.alignment = alignment
        red_style = "font:colour_index red;"
        red_style = xlwt.easyxf(red_style)

        try:
            task_info = Task.query.filter(Task.id == task_id).first()
            sheet_name = task_info.name
            sheet_name = sheet_name.replace('/', '').replace('\\', '').replace(':', '').replace('?', '').replace(
                '*', '').replace('[', '').replace(']', '')
            sheet = workbook.add_sheet(sheet_name[:30], cell_overwrite_ok=True)
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, {"url": ''}, '未找到相关用例'

        for i in (2, 4, 5):
            sheet.col(i).width = 256 * 30
        sheet.col(1).width = 256 * 13
        sheet.col(3).width = 256 * 13
        sheet.col(11).width = 256 * 12
        # 初始化Excel的前3行
        project_name = Project.query.get(project_id).name
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
        sheet.write(2, 8, '测试结果(Pass/Fail)')
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
        case_result = []
        creator_list = []
        creation_time_list = []

        ret = cls.taskcase_query_all_json(task_id, '1')
        module_id_list = []
        for i in range(len(ret)):
            module_id_list.append(ret[i]['module_id'])
        module_id_list = list(set(module_id_list))

        for case_count in range(0, len(taskcase_data)):
            if taskcase_data[case_count]['module_id'] in module_id_list:
                parent_module_data = Module.query.get(taskcase_data[case_count]['module_id']).name
                module_name.append(f"{parent_module_data}/{taskcase_data[case_count]['module_name']}")
            else:
                module_name.append(taskcase_data[case_count]['module_name'])
            creation_time_list.append(taskcase_data[case_count]['creation_time'])
            creator_list.append(taskcase_data[case_count]['handler_name'])
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

            if (str(taskcase_data[case_count]['status'])).isdigit():
                if int(taskcase_data[case_count]['status']) == 0:
                    case_result.append('')
                elif int(taskcase_data[case_count]['status']) == 2:
                    case_result.append('Skip')
                elif int(taskcase_data[case_count]['status']) == 3:
                    case_result.append('Pass')
                elif int(taskcase_data[case_count]['status']) == 4:
                    case_result.append('Fail')
                else:
                    case_result.append('')
            else:
                case_result.append('')

        for i in range(3, len(taskcase_data) + 3):
            sheet.write(i, 0, cnumber_list[i - 3], style)
            sheet.write(i, 1, module_name[i - 3], style)
            sheet.write(i, 2, case_description_list[i - 3], style)
            sheet.write(i, 3, precondition_list[i - 3], style)
            sheet.write(i, 4, opearating_steps_list[i - 3], style)
            sheet.write(i, 5, expect_result_list[i - 3], style)
            sheet.write(i, 6, priority_list[i - 3], style)
            sheet.write(i, 7, ctype_list[i - 3], style)
            if case_result[i - 3] == 'Fail':
                sheet.write(i, 8, case_result[i - 3], red_style)
            else:
                sheet.write(i, 8, case_result[i - 3], style)
            sheet.write(i, 10, creator_list[i - 3], style)
            sheet.write(i, 11, creation_time_list[i - 3], style)

        dir_path = f'{TCLOUD_FILE_TEMP_PATH}/task'
        if not os.path.exists(TCLOUD_FILE_TEMP_PATH):
            os.mkdir(TCLOUD_FILE_TEMP_PATH)

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        user_id = g.userid
        file_path = f'{dir_path}/taskcase-{str(user_id)}.xls'
        workbook.save(file_path)
        url = oss_upload(path=file_path, project_name='taskcase_export',
                         file_name=str(int(time.time())) + '.xls', user_id=user_id)
        return 0, {"url": url}, ''


class TaskCaseRecordBusiness(object):
    @classmethod
    def _query(cls):
        user_executor = aliased(User)
        user_handler = aliased(User)

        return TaskCaseRecord.query.outerjoin(
            Module, Module.id == TaskCaseRecord.module_id).outerjoin(
            user_executor, user_executor.id == TaskCaseRecord.executor).outerjoin(
            user_handler, user_handler.id == TaskCaseRecord.handler).add_columns(
            TaskCaseRecord.id.label('taskcaserecordid'),
            TaskCaseRecord.task_case_id.label('task_case_id'),
            TaskCaseRecord.task_id.label('task_id'),
            TaskCaseRecord.exe_way.label('exe_way'),
            TaskCaseRecord.cnumber.label('cnumber'),
            TaskCaseRecord.ctype.label('ctype'),
            TaskCaseRecord.title.label('title'),
            TaskCaseRecord.description.label('description'),
            TaskCaseRecord.precondition.label('precondition'),
            TaskCaseRecord.step_result.label('step_result'),
            TaskCaseRecord.is_auto.label('is_auto'),
            TaskCaseRecord.status.label('status'),
            TaskCaseRecord.comment.label('comment'),
            TaskCaseRecord.priority.label('priority'),
            Module.id.label('module_id'),
            Module.name.label('module_name'),
            user_executor.id.label('executor_id'),
            user_executor.nickname.label('executor_name'),
            user_handler.id.label('handler_id'),
            user_handler.nickname.label('handler_name'),
        )

    @classmethod
    @transfer2json(
        '?taskcaserecordid|!task_case_id|!task_id|!executor_id|!executor_name|!handler_id|!handler_name|!exe_way|'
        '!cnumber|!ctype|!title|!description|!precondition|!step_result'
        '|!is_auto|!status|!comment|!module_id|!module_name|!priority')
    def query_by_task_case_record(cls, task_case_id):
        ret = cls._query().filter(TaskCaseRecord.task_case_id == task_case_id).all()
        return ret

    @classmethod
    def query_by_task_case_id(cls, task_case_id):
        ret = cls.query_by_task_case_record(task_case_id)
        return ret

    @classmethod
    def delete(cls, task_case_record_id):
        task_case_record = TaskCaseRecord.query.get(task_case_record_id)
        task_case_record.status = TaskCaseRecord.DISABLE
        db.session.add(task_case_record)
        db.session.commit()
        return 0

    @classmethod
    def create(cls, task_case_id, task_id, module_id, version, executor, exe_way, ctype, title, description,
               precondition, step_result, is_auto, status, comment, priority):
        try:
            task_case_record = TaskCaseRecord(
                task_id=task_id,
                task_case_id=task_case_id,
                executor=executor,
                exe_way=exe_way,
                module_id=module_id,
                version=version,
                ctype=ctype,
                title=title,
                description=description,
                precondition=precondition,
                step_result=step_result,
                is_auto=is_auto,
                status=status,
                comment=comment,
                priority=priority,
            )
            db.session.add(task_case_record)
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)


class TaskDashBoardBusiness(object):
    user_trpc = Trpc('auth')

    @classmethod
    def task_case_all_tester_dashboard(cls, start_date, end_date, testers=None):
        # # 查询测试人员每天执行的case个数
        if not testers:
            testers = cls.user_trpc.requests('get', '/user/role/3')
        detaillist = []
        dashboard_ret = TaskCase.query.add_columns(
            func.date_format(TaskCase.creation_time, "%Y-%m-%d").label('creation_time'),
            TaskCase.handler.label('handler'),
            func.count('*').label('count')). \
            filter(TaskCase.creation_time.between(start_date, end_date + " 23:59:59")). \
            filter(TaskCase.handler != None, TaskCase.status != TaskCase.ACTIVE).group_by(
            func.date_format(TaskCase.creation_time, "%Y-%m-%d"), TaskCase.handler).order_by(
            desc(TaskCase.handler)).all()

        for tester in testers:
            userid = tester.get('userid')
            nickname = tester.get('nickname')
            picture = tester.get('picture')
            info = []
            for da in dashboard_ret:
                if userid == da.handler:
                    info.append({"date": da.creation_time, "count": da.count})
            detail = [
                dict(
                    userid=userid,
                    nickname=nickname,
                    picture=picture,
                    info=info)
            ]
            detaillist.extend(detail)
        return detaillist

    @classmethod
    def task_project_dashboard(cls, start_date, end_date):
        tasksum_dashboard_ret = Task.query.add_columns(
            Task.project_id.label('project_id'),
            func.count('*').label('count')). \
            filter(Task.creation_time.between(start_date, end_date + " 23:59:59")). \
            filter(Task.status != Task.DISABLE).group_by(Task.project_id).all()
        detail = [
            dict(
                tasksum=[
                    dict(i)
                    for i in map(lambda x: zip(('project_id', 'count'), x),
                                 zip([i.project_id for i in tasksum_dashboard_ret],
                                     [i.count for i in tasksum_dashboard_ret]))
                ]
            )
        ]
        return detail

    @classmethod
    def task_case_project_dashboard(cls, start_date, end_date):
        casesum_dashboard_ret = TaskCase.query.add_columns(
            TaskCase.project_id.label('project_id'),
            func.count('*').label('count')). \
            filter(TaskCase.creation_time.between(start_date, end_date + " 23:59:59")). \
            filter(TaskCase.status != Task.DISABLE).group_by(TaskCase.project_id).all()
        detail = [
            dict(
                casesum=[
                    dict(i)
                    for i in map(lambda x: zip(('project_id', 'count'), x),
                                 zip([i.project_id for i in casesum_dashboard_ret],
                                     [i.count for i in casesum_dashboard_ret]))
                ]
            )
        ]
        return detail


class TaskCaseDashBoardBusiness(object):
    @classmethod
    def task_case_status_dashboard(cls, taskid):
        casesum_dashboard_ret = TaskCase.query.add_columns(
            TaskCase.status.label('status'),
            func.count('*').label('count')). \
            filter(TaskCase.status != Task.DISABLE, TaskCase.task_id == taskid).group_by(TaskCase.status).all()
        detail = [
            dict(i)
            for i in map(lambda x: zip(('status', 'count'), x),
                         zip([i.status for i in casesum_dashboard_ret],
                             [i.count for i in casesum_dashboard_ret]))
        ]
        # current_app.logger.info(detail)
        return detail
