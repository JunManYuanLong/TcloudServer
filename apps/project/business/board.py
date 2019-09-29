import json

import requests
from flask import request, g, current_app
from sqlalchemy import desc, func
from sqlalchemy.orm import aliased

from apps.auth.models.users import User
from apps.project.models.issue import Issue
from apps.project.models.modules import Module
from apps.project.models.tasks import Task, TaskCase
from apps.project.models.version import Version
from apps.public.models.public import Config
from library.api.transfer import transfer2json


class BoardBusiness(object):
    @classmethod
    @transfer2json(
        '?id|!name|!description|!tmethod|!ttype|!status|!start_time|!end_time|!priority|!version_id|!version_name'
        '|!creator_id|!creator_name|!executor_id|!executor_name|!project_id',
        ispagination=True)
    def task_query(cls, projectid, userid, status, iscreator, page_size, page_index, title):
        # 0:创建,1:任务已删除,2:任务已完成
        user_creator = aliased(User)
        user_executor = aliased(User)
        ret = Task.query.outerjoin(
            user_creator, user_creator.id == Task.creator).outerjoin(
            user_executor, user_executor.id == Task.executor).outerjoin(
            Version, Version.id == Task.version).add_columns(
            Task.id.label('id'),
            Task.name.label('name'),
            Task.description.label('description'),
            Task.tmethod.label('tmethod'),
            Task.ttype.label('ttype'),
            Task.status.label('status'),
            func.date_format(Task.start_time, "%Y-%m-%d").label('start_time'),
            func.date_format(Task.end_time, "%Y-%m-%d").label('end_time'),
            Task.priority.label('priority'),
            Task.project_id.label('project_id'),
            Version.id.label('version_id'),
            Version.title.label('version_name'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),
            user_executor.id.label('executor_id'),
            user_executor.nickname.label('executor_name'),
        )
        if projectid:
            ret = ret.filter(Task.project_id == projectid)
        if iscreator:
            ret = ret.filter(Task.creator == userid)
        else:
            ret = ret.filter(Task.executor == userid)
        if title not in ["", None]:
            ret = ret.filter(Task.name.like(f'%{title}%'))
        ret = ret.filter(Task.status.in_(status))
        result = ret.order_by(desc(Task.id)
                              ).limit(int(page_size)).offset(int(page_index - 1) * int(page_size)).all()
        count = ret.count()
        return result, count

    @classmethod
    @transfer2json(
        '?taskcaseid|!task_id|!executor_id|!executor_name|!handler_id|!handler_name|!exe_way|!cnumber|!ctype|!title|'
        '!description|!precondition|!step_result|!is_auto|!status|!comment|!module_id|!module_name|!project_id',
        ispagination=True
    )
    def task_case_query(cls, projectid, userid, status, iscreator, page_size, page_index, title):
        # 0:case创建,1:case已删除,2:跳过,3:case执行通过,4:case执行不通过
        user_executor = aliased(User)
        user_handler = aliased(User)

        ret = TaskCase.query.outerjoin(
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
            TaskCase.project_id.label('project_id'),
            Module.id.label('module_id'),
            Module.name.label('module_name'),
            user_executor.id.label('executor_id'),
            user_executor.nickname.label('executor_name'),
            user_handler.id.label('handler_id'),
            user_handler.nickname.label('handler_name'),
        )
        if projectid:
            ret = ret.filter(TaskCase.project_id == projectid)
        if iscreator is 1:
            ret = ret.filter(TaskCase.handler == userid)
        else:
            ret = ret.filter(TaskCase.executor == userid)
        if title not in ["", None]:
            ret = ret.filter(TaskCase.title.like(f'%{title}%'))
        ret = ret.filter(TaskCase.status.in_(status))
        result = ret.order_by(desc(TaskCase.id)
                              ).limit(int(page_size)).offset(int(page_index - 1) * int(page_size)).all()
        count = ret.count()
        return result, count

    @classmethod
    @transfer2json('?id|!issue_number|!title|!handle_status|!description|!chance|!level|!priority|!stage'
                   '|!version_id|!version_name|!creator_id|!creator_name|!handler_id|!handler_name|!project_id',
                   ispagination=True
                   )
    def issue_query(cls, projectid, userid, status, iscreator, page_size, page_index, title):
        # 处理状态 {"1": "待办", "2": "处理中", "3": "测试中", "4": "已关闭", "5": "已拒绝", "6": "延时处理"}
        user_creator = aliased(User)
        user_handler = aliased(User)
        ret = Issue.query.outerjoin(
            user_creator, user_creator.id == Issue.creator).outerjoin(
            user_handler, user_handler.id == Issue.handler).outerjoin(
            Version, Version.id == Issue.version).add_columns(
            Issue.id.label('id'),
            Issue.issue_number.label('issue_number'),
            Issue.title.label('title'),
            Issue.handle_status.label('handle_status'),
            Issue.description.label('description'),
            Issue.chance.label('chance'),
            Issue.level.label('level'),
            Issue.priority.label('priority'),
            Issue.stage.label('stage'),
            Issue.project_id.label('project_id'),
            Version.id.label('version_id'),
            Version.title.label('version_name'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),
            user_handler.id.label('handler_id'),
            user_handler.nickname.label('handler_name'),
        )
        if projectid:
            ret = ret.filter(Issue.project_id == projectid)
        if iscreator:
            ret = ret.filter(Issue.creator == userid)
        else:
            ret = ret.filter(Issue.handler == userid)
        if title not in ["", None]:
            ret = ret.filter(Issue.title.like(f'%{title}%'))
        ret = ret.filter(Issue.handle_status.in_(status), Issue.status == Issue.ACTIVE)
        result = ret.order_by(desc(Issue.id)
                              ).limit(int(page_size)).offset(int(page_index - 1) * int(page_size)).all()
        count = ret.count()
        return result, count

    @classmethod
    def board_config(cls):
        user_id = g.userid if g.userid else None
        board_config = Config.query.add_columns(Config.content.label('content')).filter(Config.module == 'board',
                                                                                        Config.module_type == 1).first()
        board_config = json.loads(board_config.content)
        current_app.logger.info('board_config:' + str(board_config))
        return user_id, board_config

    @classmethod
    def user_create(cls, page_size, page_index, r_type, title):
        project_id = request.args.get('projectid')
        user_id, board_config = cls.board_config()
        ret = None
        count = 0
        if r_type == "task":
            ret, count = cls.task_query(project_id, user_id, board_config['create']['task'], 1, page_size,
                                        page_index, title)
        # task_case_ret = cls.task_case_query(projectid, user_id, board_config['create']['task_case'], 1)
        if r_type == "issue":
            ret, count = cls.issue_query(project_id, user_id, board_config['create']['issue'], 1, page_size,
                                         page_index, title)

        return ret, count

    @classmethod
    def user_unfinish(cls, page_size, page_index, r_type, title):
        project_id = request.args.get('projectid')
        user_id, board_config = cls.board_config()
        ret = None
        count = 0
        if r_type == "task":
            ret, count = cls.task_query(project_id, user_id, board_config['unfinish']['task'], 0, page_size, page_index,
                                        title)
        if r_type == "task_case":
            ret, count = cls.task_case_query(project_id, user_id, board_config['unfinish']['task_case'],
                                             1, page_size, page_index, title)
        if r_type == "issue":
            ret, count = cls.issue_query(project_id, user_id, board_config['unfinish']['issue'], 0, page_size,
                                         page_index, title)
        return ret, count

    @classmethod
    def user_finish(cls, page_size, page_index, r_type, title):
        project_id = request.args.get('projectid')
        user_id, board_config = cls.board_config()
        ret = None
        count = 0

        if r_type == "task":
            ret, count = cls.task_query(project_id, user_id, board_config['finish']['task'], 0, page_size, page_index,
                                        title)
        if r_type == "task_case":
            ret, count = cls.task_case_query(project_id, user_id, board_config['finish']['task_case'], 1,
                                             page_size, page_index, title)
        if r_type == "issue":
            ret, count = cls.issue_query(project_id, user_id, board_config['finish']['issue'], 0, page_size,
                                                 page_index, title)

        return ret, count

    @classmethod
    def stf_devices(cls):
        stf_devices = Config.query.add_columns(Config.content.label('content')).filter(
            Config.module == 'stf',
            Config.module_type == 1).first()
        stf_devices = json.loads(stf_devices.content)
        current_app.logger.info(json.dumps(stf_devices, ensure_ascii=False))
        url = stf_devices['URL']
        headers = stf_devices['headers']
        ret = requests.get(url, headers=headers)
        ret = json.loads(ret.content)
        # logger.info(json.dumps(ret, ensure_ascii=False))
        return ret