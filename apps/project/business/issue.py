import datetime
import json
import os
import traceback
from itertools import groupby

import xlwt
from flask import g, request, current_app
from sqlalchemy import desc, func, or_
from sqlalchemy.orm import aliased

from apps.auth.models.users import User, UserBindRole
from apps.project.business.tag import TagBusiness
from apps.project.models.issue import Issue, IssueRecord
from apps.project.models.modules import Module
from apps.project.models.project import Project
from apps.project.models.requirement import Requirement
from apps.project.models.version import Version
from apps.public.models.public import Config
from library.api.db import db
from library.api.exceptions import SaveObjectException
from library.api.transfer import transfer2json, slicejson
from library.notification import notification
from library.oss import oss_upload
from library.trpc import Trpc
from public_config import PRIORITY, ISSUE_CONFIG, TCLOUD_FILE_TEMP_PATH


class IssueBusiness(object):
    user_trpc = Trpc('auth')
    public_trpc = Trpc('public')

    @classmethod
    def _query(cls):
        user_creator = aliased(User)
        user_modifier = aliased(User)
        user_handler = aliased(User)

        return Issue.query.outerjoin(
            user_creator, user_creator.id == Issue.creator).outerjoin(
            user_modifier, user_modifier.id == Issue.modifier).outerjoin(
            user_handler, user_handler.id == Issue.handler).outerjoin(
            Version, Version.id == Issue.version).outerjoin(
            Module, Module.id == Issue.module_id).outerjoin(
            Requirement, Requirement.id == Issue.requirement_id).add_columns(
            Module.name.label('module_name'),
            Issue.id.label('issueid'),
            Issue.issue_number.label('issue_number'),
            Issue.project_id.label('project_id'),
            Issue.system.label('system'),
            Version.id.label('version_id'),
            Version.title.label('version_name'),
            Issue.module_id.label('module_id'),
            Issue.creator.label('creator'),
            Issue.modifier.label('modifier'),
            Issue.handler.label('handler'),
            Issue.issue_type.label('issue_type'),
            Issue.chance.label('chance'),
            Issue.level.label('level'),
            Issue.priority.label('priority'),
            Issue.stage.label('stage'),
            Issue.title.label('title'),
            Issue.attach.label('attach'),
            Issue.handle_status.label('handle_status'),
            Issue.reopen.label('reopen'),
            Issue.status.label('status'),
            Issue.weight.label('weight'),
            Issue.description.label('description'),
            Issue.comment.label('comment'),
            Issue.repair_time.label('repair_time'),
            Issue.test_time.label('test_time'),
            func.date_format(Issue.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(Issue.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
            Issue.detection_chance.label('detection_chance'),
            Issue.rank.label('rank'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),
            user_modifier.id.label('modifier_id'),
            user_modifier.nickname.label('modifier_name'),
            user_handler.id.label('handler_id'),
            user_handler.nickname.label('handler_name'),
            Issue.requirement_id.label('requirement_id'),
            Requirement.title.label('requirement_title'),
            Issue.case_covered.label('case_covered'),
            Issue.tag.label('tag')
        )

    @classmethod
    def filter_query(cls):
        project_id = request.args.get('project_id')
        version_id = request.args.get('versionid')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        creator_id_args = request.args.get('creator_id', '')
        creator_id = creator_id_args.split(',') if creator_id_args != '' else []
        title = request.args.get('title')
        handler_id_args = request.args.get('handler_id', '')
        handler_id = handler_id_args.split(',') if handler_id_args != '' else []
        handle_status_args = request.args.get('handle_status', '')
        handle_status = handle_status_args.split(',') if handle_status_args != '' else []
        module_id_args = request.args.get('module_id', '')
        module_id = module_id_args.split(',') if module_id_args != '' else []
        priority_args = request.args.get('priority', '')
        priority = priority_args.split(',') if priority_args != '' else []
        level_args = request.args.get('level', '')
        level = level_args.split(',') if level_args != '' else []
        user = request.args.get('user')
        case_covered = request.args.get('case_covered')
        tag = request.args.get('tag')
        ret = cls._query().filter(Issue.status == Issue.ACTIVE)
        if project_id:
            ret = ret.filter(Issue.project_id == project_id)
        if version_id:
            ret = ret.filter(Issue.version == version_id)
        if creator_id:
            ret = ret.filter(Issue.creator.in_(creator_id))
        if title:
            ret = ret.filter(or_(Issue.title.like(f'%{title}%'), Issue.issue_number.like(f'%{title}%')))
        if handler_id:
            ret = ret.filter(Issue.handler.in_(handler_id))
        if handle_status:
            ret = ret.filter(Issue.handle_status.in_(handle_status))
        if module_id:
            ret = ret.filter(Issue.module_id.in_(module_id))
        if priority:
            ret = ret.filter(Issue.priority.in_(priority))
        if level:
            ret = ret.filter(Issue.level.in_(level))
        if user:
            ret = ret.filter(Issue.handler == user)
        if case_covered:
            ret = ret.filter(Issue.case_covered == case_covered)
        if tag:
            ret = ret.filter(func.find_in_set(tag, Issue.tag))
        if start_time and end_time:
            ret = ret.filter(
                Issue.modified_time.between(start_time, end_time + " 23:59:59"))
        ret = ret.order_by(desc(Issue.modified_time))
        return ret

    @classmethod
    @slicejson(['creator|id|name|creator_id|creator_name', 'modifier|id|name|modifier_id|modifier_name',
                'handler|id|name|handler_id|handler_name', 'version|id|name|version_id|version_name',
                'module|id|name|module_id|module_name'], ispagination=True)
    @transfer2json(
        '?issueid|!issue_number|!project_id|!system|@version_id|@version_name|@module_id|@module_name|'
        '!creator|!handler|!issue_type|!chance|!level|!priority|!stage|!title|!attach|!handle_status|'
        '!reopen|!status|!weight|!description|!comment|!creation_time|!modified_time|!repair_time|'
        '!test_time|!detection_chance|!rank|@creator_id|@creator_name|@modifier_id|@modifier_name|'
        '@handler_id|@handler_name|!requirement_id|!requirement_title|!case_covered|!tag', ispagination=True)
    def paginate_data(cls, page_size=None, page_index=None, only_data=False):
        query = cls.filter_query()
        count = query.count()
        if page_size and page_index:
            query = query.limit(int(page_size)).offset(int(page_index - 1) * int(page_size))
        data = query.all()
        if only_data:
            return data
        return data, count

    @classmethod
    @slicejson(['creator|id|name|creator_id|creator_name', 'modifier|id|name|modifier_id|modifier_name',
                'handler|id|name|handler_id|handler_name', 'version|id|name|version_id|version_name',
                'module|id|name|module_id|module_name'], ispagination=True)
    @transfer2json(
        '?issueid|!issue_number|!project_id|!system|@version_id|@version_name|@module_id|@module_name|'
        '!creator|!handler|!issue_type|!chance|!level|!priority|!stage|!title|!attach|!handle_status|'
        '!reopen|!status|!weight|!description|!comment|!creation_time|!modified_time|!repair_time|'
        '!test_time|@creator_id|@creator_name|@modifier_id|@modifier_name|@handler_id|@handler_name|'
        '!requirement_id|!requirement_title|!case_covered|!tag', ispagination=True)
    def paginate_data_by_rid(cls, page_size, page_index, requirement_id):
        query = cls._query().filter(Issue.status == Issue.ACTIVE, Issue.requirement_id == requirement_id)
        count = query.count()
        data = query.order_by(desc(Issue.id)).limit(int(page_size)).offset(int(page_index - 1) * int(page_size)).all()
        return data, count

    # 根据id查询issue记录
    @classmethod
    @slicejson(['creator|id|name|creator_id|creator_name', 'modifier|id|name|modifier_id|modifier_name',
                'handler|id|name|handler_id|handler_name', 'version|id|name|version_id|version_name',
                'module|id|name|module_id|module_name'])
    @transfer2json(
        '?issueid|!issue_number|!project_id|!system|@version_id|@version_name|@module_id|@module_name|'
        '!creator|!handler|!issue_type|!chance|!level|!priority|!stage|!title|!attach|!handle_status|'
        '!reopen|!status|!weight|!description|!comment|!creation_time|!modified_time|!repair_time|'
        '!test_time|@creator_id|@creator_name|@modifier_id|@modifier_name|@handler_id|@handler_name|'
        '!requirement_id|!requirement_title|!case_covered|!tag')
    def query_by_id(cls, id):
        return cls._query().filter(Issue.id == id, Issue.status == Issue.ACTIVE).all()

    @classmethod
    @transfer2json('?issueid|!title|!handle_status')
    def query_id_title_by_requirement_id(cls, requirement_id):
        ret = cls._query().filter(Issue.status == Issue.ACTIVE, Issue.requirement_id == requirement_id).order_by(
            desc(Issue.id)).all()
        return ret

    @classmethod
    def delete(cls, id):
        iss = Issue.query.get(id)
        if iss is None:
            return 0
        modifier = g.userid if g.userid else None
        current_app.logger.info("modifier：" + str(modifier))
        iss.status = Issue.DISABLE
        db.session.add(iss)
        issue_record = IssueRecord(
            iss_id=iss.id,
            issue_number="T" + str(iss.id),
            system=iss.system,
            version=iss.version,
            project_id=iss.project_id,
            module_id=iss.module_id,
            creator=iss.creator,
            modifier=modifier,
            handler=iss.handler,
            issue_type=iss.issue_type,
            chance=iss.chance,
            level=iss.level,
            priority=iss.priority,
            stage=iss.stage,
            title=iss.title,
            attach=iss.attach,
            status=Issue.DISABLE,
            handle_status=iss.handle_status,
            reopen=iss.reopen,
            description=iss.description,
            comment=iss.comment,
            repair_time=iss.repair_time,
            test_time=iss.test_time,
            detection_chance=iss.detection_chance,
            rank=iss.rank,
            requirement_id=iss.requirement_id,
            case_covered=iss.case_covered,
            tag=iss.tag
        )
        db.session.add(issue_record)
        db.session.commit()
        if iss.tag:
            TagBusiness.less_reference(iss.tag)
        return 0

    @classmethod
    def create(cls, system, version, project_id, module_id, creator, modifier, handler, issue_type, chance, level,
               priority, stage, title, attach, handle_status, description, comment, detection_chance,
               requirement_id, case_covered, tag):
        # 创建issue的初始状态只能是2，1
        handle_status = 1
        if handler:
            handle_status = 2

        ret = Issue.query.filter_by(title=title, project_id=project_id, status=Issue.ACTIVE).first()
        if ret:
            raise SaveObjectException('存在相同名称的缺陷')
        creator = g.userid if g.userid else None
        current_app.logger.info("creator:" + str(creator))
        rank_type = cls.gain_rank(level, chance)

        try:
            c = Issue(
                system=system,
                version=version,
                project_id=project_id,
                module_id=module_id,
                creator=creator,
                handler=handler,
                issue_type=issue_type,
                chance=chance,
                level=level,
                priority=priority,
                stage=stage,
                title=title,
                attach=attach,
                handle_status=handle_status,
                description=description,
                # comment=comment,
                detection_chance=detection_chance,
                rank=rank_type,
                requirement_id=requirement_id,
                case_covered=case_covered,
                tag=tag
            )
            db.session.add(c)
            db.session.flush()
            c.issue_number = "T" + str(c.id)
            current_app.logger.info("current_id: " + str(c.id))
            IssueRecordBusiness.create(c.id, system, project_id, version, module_id, creator, modifier, handler,
                                       issue_type, chance, level,
                                       priority, stage, title, attach, handle_status, description, comment,
                                       detection_chance, requirement_id, case_covered, tag)
            db.session.add(c)
            db.session.commit()

            if tag:
                TagBusiness.add_reference(tag)

            if not isinstance(handler, list):
                handler = [handler]
            board_config = cls.public_trpc.requests('get', '/public/config', {'module': 'tcloud', 'module_type': 1})
            project = Project.query.add_columns(Project.name).filter(Project.id == project_id).first()
            project_name = ''
            if project:
                project_name = project.name
            text = f'''[issue创建 - {title}]
项目：{project_name}
URL：{board_config}/project/{project_id}/issue/{version}'''
            notification.send_notification(handler, text)
            return 0
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            return 102

    @classmethod
    def modify(cls, id, system, version, project_id, module_id, modifier, handler, issue_type, chance, level,
               priority, stage, title, attach, handle_status, description, comment, detection_chance,
               requirement_id, case_covered, tag):
        current_app.logger.info("id:" + str(id))
        iss = Issue.query.get(id)
        if iss is None:
            return 101

        ret = Issue.query.filter_by(title=title,
                                    status=Issue.ACTIVE,
                                    project_id=iss.project_id).filter(Issue.id != id).first()
        if ret:
            raise SaveObjectException('存在相同名称的缺陷')

        is_change_handler = False
        if iss.handler != handler:
            is_change_handler = True
        modifier = g.userid if g.userid else None
        current_app.logger.info("modifier：" + str(modifier))
        flag = cls.status_switch_auth(iss.handle_status, handle_status)
        # 判断是否有权限操作
        if not flag:
            return 110

        # 计算reopen次数，repair_time和test_time
        reopen, repair_time, test_time = cls.operation_authority(id, handle_status)
        rank_type = cls.gain_rank(level, chance)
        old_tag = None
        new_tag = None
        iss.system = system,
        iss.version = version,
        iss.project_id = project_id,
        iss.module_id = module_id,
        iss.modifier = modifier,
        iss.handler = handler,
        iss.issue_type = issue_type,
        iss.chance = chance,
        iss.level = level,
        iss.priority = priority,
        iss.stage = stage,
        iss.title = title,
        iss.attach = attach,
        iss.handle_status = handle_status,
        iss.reopen = reopen,
        iss.description = description,
        # iss.comment = comment,
        iss.repair_time = repair_time,
        iss.test_time = test_time,
        iss.detection_chance = detection_chance,
        iss.rank = rank_type
        iss.requirement_id = requirement_id
        iss.case_covered = case_covered
        if iss.tag != tag:
            old_tag = iss.tag
            new_tag = tag
            iss.tag = tag
        db.session.add(iss)
        IssueRecordBusiness.modify(id, system, project_id, version, module_id, iss.creator, modifier, handler,
                                   issue_type, chance, level, priority, stage, title, attach, handle_status,
                                   description, iss.comment, reopen, repair_time, test_time, detection_chance,
                                   requirement_id, case_covered, tag)
        db.session.commit()

        if old_tag or new_tag:
            TagBusiness.change_reference(old_tag, new_tag)

        if is_change_handler:
            modifier_user = cls.user_trpc.requests('get', f'/user/{g.userid}')
            if modifier_user:
                modifier_user = modifier_user[0].get('nickname')
            handler_user = cls.user_trpc.requests('get',
                                                  f'/user'
                                                  f'/{handler if not isinstance(handler, list) else handler[0]}')
            if handler_user:
                handler_user = handler_user[0].get('nickname')
            if not isinstance(handler, list):
                handler = [handler]
            text = f'''[issue处理人变更 - {title}]
{modifier_user} 修改处理人为 {handler_user}'''
            notification.send_notification(handler, text, send_type=2)
        return 0

    @classmethod
    def export(cls):
        all_issue = cls.filter_query()
        workbook = xlwt.Workbook()
        alignment = xlwt.Alignment()
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        alignment.horz = xlwt.Alignment.HORZ_LEFT
        alignment.vert = xlwt.Alignment.VERT_TOP

        style = xlwt.XFStyle()
        style.alignment = alignment
        time_now = datetime.datetime.now().strftime('%Y%m%d.%H%M%S')
        xlsx_name = f'Issues-{str(g.userid)}-{time_now}.xls'
        sheet_name = f'Issues'
        sheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)
        titles = ["Bug ID", "标题", "版本", "模块", "类型", "Reopen次数", "创建时间", "更新时间", "优先级",
                  "级别", "创建人", "处理人", "状态", "需求ID", "需求名称", "用例覆盖"]

        for i, title in enumerate(titles):
            sheet.write(0, i, title)

        for i, issue in enumerate(all_issue):
            i += 1
            sheet.write(i, 0, issue.issue_number)
            sheet.write(i, 1, issue.title)
            sheet.write(i, 2, issue.version_name)
            sheet.write(i, 3, issue.module_name)
            sheet.write(i, 4, ISSUE_CONFIG.get('type').get(issue.issue_type))
            sheet.write(i, 5, issue.reopen)
            sheet.write(i, 6, issue.creation_time)
            sheet.write(i, 7, issue.modified_time)
            sheet.write(i, 8, PRIORITY.get(issue.priority))
            sheet.write(i, 9, ISSUE_CONFIG.get('level').get(issue.level))
            sheet.write(i, 10, issue.creator_name)
            sheet.write(i, 11, issue.handler_name)
            sheet.write(i, 12, ISSUE_CONFIG.get('status').get(issue.handle_status))
            sheet.write(i, 13, issue.requirement_id)
            sheet.write(i, 14, issue.requirement_title)
            case_covered = issue.case_covered
            case_covered_info = ''
            if case_covered == 0:
                case_covered_info = '否'
            elif case_covered == 1:
                case_covered_info = '是'
            sheet.write(i, 15, case_covered_info)

        dir_path = f'{TCLOUD_FILE_TEMP_PATH}/issue/'

        if not os.path.exists(TCLOUD_FILE_TEMP_PATH):
            os.mkdir(TCLOUD_FILE_TEMP_PATH)

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        file_path = f'{dir_path}/{xlsx_name}'
        workbook.save(file_path)

        url = oss_upload(path=file_path, project_name='issue_export',
                         file_name=xlsx_name, user_id=g.userid)
        return url

    # 返回用户的roles列表，如[1，2]  1:admin 2:dev
    @classmethod
    def query_role(cls, userid):
        roles = UserBindRole.query.add_columns(UserBindRole.role_id.label('role_id')).filter(
            UserBindRole.user_id == userid).all()
        roles_list = []
        for ret in roles:
            roles_list.append(ret.role_id)
        return roles_list

    # issue的reopen, repair_time, test_time计算
    @classmethod
    def operation_authority(cls, issueid, after_status):
        ret = Issue.query.add_columns(Issue.handle_status.label('handle_status'), Issue.reopen.label('reopen'),
                                      Issue.repair_time.label('repair_time'),
                                      Issue.test_time.label('test_time')).filter(
            Issue.status == Issue.ACTIVE, Issue.id == issueid).order_by(desc(Issue.id)).first()
        if ret is None:
            current_app.logger.info("修改对象已删除")
        before_status = ret.handle_status
        reopen = ret.reopen
        repair_time = ret.repair_time
        test_time = ret.test_time

        # before, after : 测试中->修复中；已关闭->修复中
        reopen_status = [(3, 2), (4, 2)]

        # 验证不通过重新打开,reopen+1
        if (before_status, after_status) in reopen_status:
            reopen = reopen + 1

        dev_finish_status = [3]
        test_finish_status = [4]
        current_app.logger.info("handle_status:" + str(after_status))
        now_time = datetime.datetime.now()

        # 如果在开发修复完成的状态
        if after_status in dev_finish_status:
            ret = IssueRecord.query.add_columns(IssueRecord.creation_time.label('creation_time')).filter(
                IssueRecord.status == IssueRecord.ACTIVE, IssueRecord.iss_id == issueid,
                IssueRecord.handle_status.in_([2])).order_by(
                IssueRecord.creation_time).first()
            if ret is None:
                current_app.logger.info("修改状态为开发修复完成状态3，没有找到状态为2的数据")
                return reopen, repair_time, test_time
            # 防止并发时时间相减为负
            if now_time >= ret.creation_time:
                repair_time = str(now_time - ret.creation_time)[:-7]
            else:
                repair_time = '0:00:00'
        # 如果在测试验证完成的状态
        if after_status in test_finish_status:
            ret = IssueRecord.query.add_columns(IssueRecord.creation_time.label('creation_time')).filter(
                IssueRecord.status == IssueRecord.ACTIVE, IssueRecord.iss_id == issueid,
                IssueRecord.handle_status == 3).order_by(
                desc(IssueRecord.creation_time)).first()
            if ret is None:
                current_app.logger.info("修改状态为测试验证完成状态4，没有找到状态为3的数据")
                return reopen, repair_time, test_time
            # 防止并发时时间相减为负
            if now_time >= ret.creation_time:
                test_time = str(now_time - ret.creation_time)[:-7]
            else:
                test_time = '0:00:00'
        current_app.logger.info("repair_time:" + str(repair_time))
        current_app.logger.info("test_time:" + str(test_time))
        return reopen, repair_time, test_time

    @classmethod
    def status_switch_auth(cls, before_status, after_status):
        flag = False
        if g.is_admin:
            return True
        modifier_role_row = cls.user_trpc.requests('get', '/user/{}'.format(g.userid),
                                                   query={'project_id': g.projectid})
        if not modifier_role_row:
            return flag
        modifier_role = [i['name'] for i in modifier_role_row[0]['role']]

        if 'admin' in modifier_role or 'owner' in modifier_role:
            current_app.logger.info("admin status switch auth")
            return True
        issue_config = Config.query.add_columns(Config.content.label('content')).filter(
            Config.module == 'issue',
            Config.module_type == 2).first()
        issue_config = json.loads(issue_config.content)
        current_app.logger.info(json.dumps(issue_config, ensure_ascii=False))

        if 'test' in modifier_role:
            # board状态：1:待办  2:处理中 3:测试中  4:完成 5:已拒绝 6:延时处理
            tester_status_switch = issue_config['test']
            if [before_status, after_status] in tester_status_switch:
                flag = True
        if 'dev' in modifier_role:
            dev_status_switch = issue_config['dev']
            if [before_status, after_status] in dev_status_switch:
                flag = True
        return flag

    @classmethod
    def status_switch(cls, id, mstatus):
        try:
            iss = Issue.query.get(id)
            before_status = iss.handle_status
            after_status = mstatus
            modifier = g.userid if g.userid else None
            current_app.logger.info("modifier：" + str(modifier))
            current_app.logger.info("before_status:" + str(before_status))
            current_app.logger.info("after_status:" + str(after_status))

            flag = cls.status_switch_auth(before_status, after_status)
            # 判断是否有权限操作
            if not flag:
                return 110

            reopen, repair_time, test_time = cls.operation_authority(id, mstatus)
            iss.handle_status = mstatus
            iss.reopen = reopen
            iss.test_time = test_time
            iss.repair_time = repair_time
            issue_record = IssueRecord(
                iss_id=iss.id,
                issue_number="T" + str(iss.id),
                system=iss.system,
                version=iss.version,
                project_id=iss.project_id,
                module_id=iss.module_id,
                creator=iss.creator,
                modifier=modifier,
                handler=iss.handler,
                issue_type=iss.issue_type,
                chance=iss.chance,
                level=iss.level,
                priority=iss.priority,
                stage=iss.stage,
                title=iss.title,
                attach=iss.attach,
                status=iss.status,
                handle_status=mstatus,
                reopen=reopen,
                description=iss.description,
                comment=iss.comment,
                repair_time=repair_time,
                test_time=test_time,
                detection_chance=iss.detection_chance,
                rank=iss.rank,
                requirement_id=iss.requirement_id,
                case_covered=iss.case_covered,
                tag=iss.tag
            )
            db.session.add(iss)
            db.session.add(issue_record)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def handler_switch(cls, id, handler):
        try:
            iss = Issue.query.get(id)
            if iss is None:
                return 101
            modifier = g.userid if g.userid else None
            current_app.logger.info("modifier：" + str(modifier))
            current_app.logger.info(iss.handler)
            iss.handler = handler
            issue_record = IssueRecord(
                iss_id=iss.id,
                issue_number="T" + str(iss.id),
                system=iss.system,
                version=iss.version,
                project_id=iss.project_id,
                module_id=iss.module_id,
                creator=iss.creator,
                modifier=modifier,
                handler=handler,
                issue_type=iss.issue_type,
                chance=iss.chance,
                level=iss.level,
                priority=iss.priority,
                stage=iss.stage,
                title=iss.title,
                attach=iss.attach,
                status=iss.status,
                handle_status=iss.handle_status,
                reopen=iss.reopen,
                description=iss.description,
                comment=iss.comment,
                repair_time=iss.repair_time,
                test_time=iss.test_time,
                detection_chance=iss.detection_chance,
                rank=iss.rank,
                requirement_id=iss.requirement_id,
                case_covered=iss.case_covered,
                tag=iss.tag
            )
            db.session.add(iss)
            db.session.add(issue_record)
            current_app.logger.info("issue_record add success!")
            db.session.commit()
            # text = f'''[issue处理人修改 - {iss.title}]
            # 你已被修改为处理人'''
            #             if not isinstance(handler, list):
            #                 handler = [handler]
            #             notification.send_notification(handler, text, send_type=2)

            modifier_user = cls.user_trpc.requests('get', f'/user/{g.userid}')
            if modifier_user:
                modifier_user = modifier_user[0].get('nickname')
            handler_user = cls.user_trpc.requests('get',
                                                  f'/user/{handler if not isinstance(handler, list) else handler[0]}')
            if handler_user:
                handler_user = handler_user[0].get('nickname')
            if not isinstance(handler, list):
                handler = [handler]
            text = f'''[issue处理人变更 - {iss.title}]
{modifier_user} 修改处理人为 {handler_user}'''
            notification.send_notification(handler, text, send_type=2)
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def level_switch(cls, id, level):
        try:
            iss = Issue.query.get(id)
            if iss is None:
                return 101
            modifier = g.userid if g.userid else None
            current_app.logger.info("modifier：" + str(modifier))
            rank = cls.gain_rank(level[0], iss.chance)
            iss.level = level
            iss.rank = rank
            issue_record = IssueRecord(
                iss_id=iss.id,
                issue_number="T" + str(iss.id),
                system=iss.system,
                version=iss.version,
                project_id=iss.project_id,
                module_id=iss.module_id,
                creator=iss.creator,
                modifier=modifier,
                handler=iss.handler,
                issue_type=iss.issue_type,
                chance=iss.chance,
                level=level,
                priority=iss.priority,
                stage=iss.stage,
                title=iss.title,
                attach=iss.attach,
                status=iss.status,
                handle_status=iss.handle_status,
                reopen=iss.reopen,
                description=iss.description,
                comment=iss.comment,
                repair_time=iss.repair_time,
                test_time=iss.test_time,
                detection_chance=iss.detection_chance,
                rank=rank,
                requirement_id=iss.requirement_id,
                case_covered=iss.case_covered,
                tag=iss.tag
            )
            db.session.add(iss)
            db.session.add(issue_record)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def priority_switch(cls, id, priority):
        try:
            iss = Issue.query.get(id)
            if iss is None:
                return 101
            modifier = g.userid if g.userid else None
            current_app.logger.info("modifier：" + str(modifier))
            iss.priority = priority
            issue_record = IssueRecord(
                iss_id=iss.id,
                issue_number="T" + str(iss.id),
                system=iss.system,
                version=iss.version,
                project_id=iss.project_id,
                module_id=iss.module_id,
                creator=iss.creator,
                modifier=modifier,
                handler=iss.handler,
                issue_type=iss.issue_type,
                chance=iss.chance,
                level=iss.level,
                priority=priority,
                stage=iss.stage,
                title=iss.title,
                attach=iss.attach,
                status=iss.status,
                handle_status=iss.handle_status,
                reopen=iss.reopen,
                description=iss.description,
                comment=iss.comment,
                repair_time=iss.repair_time,
                test_time=iss.test_time,
                detection_chance=iss.detection_chance,
                rank=iss.rank,
                requirement_id=iss.requirement_id,
                case_covered=iss.case_covered,
                tag=iss.tag
            )
            db.session.add(iss)
            db.session.add(issue_record)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def relation_issue(cls, task_case_id, id):
        try:
            task_case = Issue.query.get(task_case_id)
            if task_case is None:
                return 101
            iss = Issue.query.get(id)
            if iss is None:
                return 101
            modifier = g.userid if g.userid else None
            current_app.logger.info("modifier：" + str(modifier))
            iss.relate_case = task_case_id
            issue_record = IssueRecord(
                iss_id=iss.id,
                issue_number="T" + str(iss.id),
                system=iss.system,
                version=iss.version,
                project_id=iss.project_id,
                module_id=iss.module_id,
                creator=iss.creator,
                modifier=modifier,
                handler=iss.handler,
                issue_type=iss.issue_type,
                chance=iss.chance,
                level=iss.level,
                priority=iss.priority,
                stage=iss.stage,
                title=iss.title,
                attach=iss.attach,
                status=iss.status,
                handle_status=iss.handle_status,
                reopen=iss.reopen,
                description=iss.description,
                comment=iss.comment,
                repair_time=iss.repair_time,
                test_time=iss.test_time,
                relate_case=task_case_id,
                detection_chance=iss.detection_chance,
                rank=iss.rank,
                requirement_id=iss.requirement_id,
                case_covered=iss.case_covered,
                tag=iss.tag
            )
            db.session.add(iss)
            db.session.add(issue_record)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def add_comment(cls, id, comment):
        try:
            iss = Issue.query.get(id)
            if iss is None:
                return 101
            modifier = g.userid if g.userid else None
            current_app.logger.info("modifier：" + str(modifier))
            iss.comment = comment
            db.session.add(iss)
            issue_record = IssueRecord(
                iss_id=iss.id,
                issue_number="T" + str(iss.id),
                system=iss.system,
                version=iss.version,
                project_id=iss.project_id,
                module_id=iss.module_id,
                creator=iss.creator,
                modifier=modifier,
                handler=iss.handler,
                issue_type=iss.issue_type,
                chance=iss.chance,
                level=iss.level,
                priority=iss.priority,
                stage=iss.stage,
                title=iss.title,
                attach=iss.attach,
                status=iss.status,
                handle_status=iss.handle_status,
                reopen=iss.reopen,
                description=iss.description,
                comment=comment,
                repair_time=iss.repair_time,
                test_time=iss.test_time,
                detection_chance=iss.detection_chance,
                rank=iss.rank,
                requirement_id=iss.requirement_id,
                case_covered=iss.case_covered,
                tag=iss.tag
            )
            db.session.add(issue_record)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def gain_rank(cls, level, chance):

        # 计算rank
        data_dict = {"0": 5, "1": 4, "2": 3, "3": 2, "4": 1}
        severity = data_dict[str(level)]
        occurrence = data_dict[str(chance)]
        rank_type = severity * occurrence
        return rank_type

    @classmethod
    def issue_bind_requirement(cls, issue_id, requirement_id):
        try:
            issue = Issue.query.get(issue_id)
            issue.requirement_id = requirement_id

            issue_record = IssueRecord(
                iss_id=issue.id,
                issue_number="T" + str(issue.id),
                system=issue.system,
                version=issue.version,
                project_id=issue.project_id,
                module_id=issue.module_id,
                creator=issue.creator,
                modifier=g.userid if g.userid else None,
                handler=issue.handler,
                issue_type=issue.issue_type,
                chance=issue.chance,
                level=issue.level,
                priority=issue.priority,
                stage=issue.stage,
                title=issue.title,
                attach=issue.attach,
                status=issue.status,
                handle_status=issue.handle_status,
                reopen=issue.reopen,
                description=issue.description,
                comment=issue.comment,
                repair_time=issue.repair_time,
                test_time=issue.test_time,
                detection_chance=issue.detection_chance,
                rank=issue.rank,
                requirement_id=issue.requirement_id,
                case_covered=issue.case_covered,
                tag=issue.tag
            )

            db.session.add(issue)
            db.session.add(issue_record)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return 106, str(e)


class IssueRecordBusiness(object):
    @classmethod
    def _query(cls):
        user_creator = aliased(User)
        user_modifier = aliased(User)
        user_handler = aliased(User)

        return IssueRecord.query.outerjoin(
            user_creator, user_creator.id == IssueRecord.creator).outerjoin(
            user_modifier, user_modifier.id == IssueRecord.modifier).outerjoin(
            user_handler, user_handler.id == IssueRecord.handler).outerjoin(
            Version, Version.id == IssueRecord.version).outerjoin(
            Module, Module.id == IssueRecord.module_id).outerjoin(
            Requirement, Requirement.id == IssueRecord.requirement_id).add_columns(
            Module.name.label('module_name'),
            IssueRecord.id.label('issuerecordid'),
            IssueRecord.iss_id.label('iss_id'),
            IssueRecord.issue_number.label('issue_number'),
            IssueRecord.project_id.label('project_id'),
            IssueRecord.system.label('system'),
            Version.id.label('version_id'),
            Version.title.label('version_name'),
            IssueRecord.module_id.label('module_id'),
            IssueRecord.creator.label('creator'),
            IssueRecord.modifier.label('modifier'),
            IssueRecord.handler.label('handler'),
            IssueRecord.issue_type.label('issue_type'),
            IssueRecord.chance.label('chance'),
            IssueRecord.level.label('level'),
            IssueRecord.priority.label('priority'),
            IssueRecord.stage.label('stage'),
            IssueRecord.title.label('title'),
            IssueRecord.attach.label('attach'),
            IssueRecord.handle_status.label('handle_status'),
            IssueRecord.reopen.label('reopen'),
            IssueRecord.status.label('status'),
            IssueRecord.weight.label('weight'),
            IssueRecord.description.label('description'),
            IssueRecord.comment.label('comment'),
            IssueRecord.repair_time.label('repair_time'),
            IssueRecord.test_time.label('test_time'),
            func.date_format(IssueRecord.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(IssueRecord.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
            IssueRecord.detection_chance.label('detection_chance'),
            IssueRecord.rank.label('rank'),
            IssueRecord.requirement_id.label('requirement_id'),
            IssueRecord.case_covered.label('case_covered'),
            IssueRecord.tag.label('tag'),
            Requirement.title.label('requirement_title'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),
            user_modifier.id.label('modifier_id'),
            user_modifier.nickname.label('modifier_name'),
            user_handler.id.label('handler_id'),
            user_handler.nickname.label('handler_name'),
        )

    @classmethod
    @slicejson(['creator|id|name|creator_id|creator_name', 'modifier|id|name|modifier_id|modifier_name',
                'handler|id|name|handler_id|handler_name', 'version|id|name|version_id|version_name',
                'module|id|name|module_id|module_name'])
    @transfer2json(
        '?issuerecordid|!iss_id|!issue_number|!project_id|!system|@version_id|@version_name|@module_id|'
        '@module_name|!creator|!handler|!issue_type|!chance|!level|!priority|!stage|!title|!attach|'
        '!handle_status|!reopen|!status|!weight|!description|!comment|!creation_time|!modified_time|!repair_time|'
        '!test_time|!detection_chance|!rank|@creator_id|@creator_name|@modifier_id|@modifier_name|@handler_id|'
        '@handler_name|!requirement_id|!requirement_title|!tag')
    def query_all_json(cls):
        projectid = request.args.get('projectid')
        versionid = request.args.get('versionid')
        ret = cls._query().filter(IssueRecord.status == IssueRecord.ACTIVE)
        if projectid:
            ret = ret.filter(IssueRecord.project_id == projectid)
        if versionid:
            ret = ret.filter(IssueRecord.version == versionid)
        ret = ret.order_by(desc(IssueRecord.id)).all()
        return ret

    # 新增issue时增加历史记录
    @classmethod
    def create(cls, iss_id, system, project_id, version, module_id, creator, modifier, handler, issue_type, chance,
               level, priority, stage, title, attach, handle_status, description, comment, detection_chance,
               requirement_id, case_covered, tag):

        rank = cls.gain_rank(level, chance)
        c = IssueRecord(
            iss_id=iss_id,
            issue_number="T" + str(iss_id),
            system=system,
            version=version,
            project_id=project_id,
            module_id=module_id,
            creator=creator,
            # modifier=modifier,
            handler=handler,
            issue_type=issue_type,
            chance=chance,
            level=level,
            priority=priority,
            stage=stage,
            title=title,
            attach=attach,
            handle_status=handle_status,
            # reopen=reopen,
            description=description,
            # comment=comment,
            # repair_time=repair_time,
            # test_time=test_time,
            detection_chance=detection_chance,
            rank=rank,
            requirement_id=requirement_id,
            case_covered=case_covered,
            tag=tag
        )
        db.session.add(c)

    # 修改issue时增加历史记录
    @classmethod
    def modify(cls, iss_id, system, project_id, version, module_id, creator, modifier, handler, issue_type, chance,
               level, priority, stage, title, attach, handle_status, description, comment, reopen, repair_time,
               test_time, detection_chance, requirement_id, case_covered, tag):
        rank = cls.gain_rank(level, chance)
        c = IssueRecord(
            iss_id=iss_id,
            issue_number="T" + str(iss_id),
            system=system,
            version=version,
            project_id=project_id,
            module_id=module_id,
            creator=creator,
            modifier=modifier,
            handler=handler,
            issue_type=issue_type,
            chance=chance,
            level=level,
            priority=priority,
            stage=stage,
            title=title,
            attach=attach,
            handle_status=handle_status,
            description=description,
            reopen=reopen,
            comment=comment,
            repair_time=repair_time,
            test_time=test_time,
            detection_chance=detection_chance,
            rank=rank,
            requirement_id=requirement_id,
            case_covered=case_covered,
            tag=tag
        )
        db.session.add(c)

    # 查询issue列表(每个issue_number的最新记录)
    @classmethod
    def query_json_by_number(cls, limit, offset):
        aissue = Issue.query.add_columns(db.func.max(Issue.id).label('issueid')).group_by(Issue.issue_number).subquery()
        ret = cls._query().filter(or_(Issue.id == aissue.c.issueid, Issue.status == Issue.ACTIVE)).order_by(
            desc(Issue.id)).limit(limit).offset(offset).all()

        # issue_number_ret = Issue.query.add_columns(
        #     db.func.max(Issue.id).label('issueid')).group_by(Issue.issue_number).all()
        # issue_number = [i.issueid for i in issue_number_ret]
        # ret = Issue.query.filter(Issue.id.in_(issue_number)).order_by(Issue.id).all()
        return ret

    @classmethod
    @transfer2json(
        '?issuerecordid|!iss_id|!system|!module_name|!handler|!issue_type|!chance|!level|!priority|!stage|'
        '!title|!attach|!handle_status|!status|!description|!comment|!creation_time|!modified_time|!test_time|'
        '!detection_chance|!rank|!creator_name|!creator_id|!modifier_id|!modifier_name|!handler_name|!requirement_id|'
        '!requirement_title|!tag')
    def query_record_json(cls, issue_id):
        ret = cls._query().filter(IssueRecord.iss_id == issue_id).order_by(IssueRecord.id).all()
        return ret

    @classmethod
    def query_record_detail(cls, issue_id):
        ret = cls.query_record_json(issue_id)
        if not ret:
            return []
        ret_list = []
        issue_config = Config.query.add_columns(Config.content.label('content')).filter(Config.module == 'issue',
                                                                                        Config.module_type == 1).first()
        issue_config = json.loads(issue_config.content)
        current_app.logger.info(json.dumps(issue_config, ensure_ascii=False))
        operation_dict = issue_config['operation_dict']

        values_dict = dict(
            chance=issue_config['chance'],
            issue_type=issue_config['issue_type'],
            level=issue_config['level'],
            priority=issue_config['priority'],
            handle_status=issue_config['handle_status'],
            system=issue_config['system'],
            detection_chance=issue_config['detection_chance'],
        )

        ret_dict = {
            'modified_time': ret[0]['creation_time'], 'modifier_id': ret[0]['creator_id'],
            'modifier_name': ret[0]['creator_name'], 'operation': "创建了BUG {}".format(ret[0]['title'])
        }
        ret_list.append(ret_dict)
        for r in range(1, len(ret)):
            for issue_key, issue_value in ret[r - 1].items():
                if issue_value != ret[r][issue_key] and issue_key in operation_dict.keys():
                    current_app.logger.info(
                        "修改的字段：" + str(issue_key) + ", 字段值：" + str(issue_value) + "-->" + str(ret[r][issue_key]))
                    # 如果comment修改后为空，则跳过
                    if issue_key == 'comment' and not ret[r][issue_key]:
                        pass
                    else:
                        ret_dict = {
                            'modified_time': ret[r]['modified_time'], 'modifier_id': ret[r]['modifier_id'],
                            'modifier_name': ret[r]['modifier_name'],
                            'operation': "修改了{} {} 为 {}".format(operation_dict[issue_key], issue_value,
                                                                ret[r][issue_key])
                        }
                        try:
                            if issue_key == 'comment':
                                ret_dict['operation'] = "添加了备注 {}".format(ret[r][issue_key])

                            elif issue_key in values_dict.keys():
                                ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[issue_key],
                                                                               values_dict.get(issue_key).get(
                                                                                   str(issue_value)),
                                                                               values_dict.get(issue_key).get(
                                                                                   str(ret[r][issue_key])))
                            elif issue_key == "requirement_id":
                                if issue_value in ['', None]:
                                    ret_dict['operation'] = f"""初始绑定到需求 ：【 ID:{ret[r][issue_key]} · {ret[r].get(
                                        'requirement_title')} 】"""
                                else:
                                    ret_dict['operation'] = f"""绑定的需求由 【 ID:{issue_value} · {ret[r - 1].get(
                                        'requirement_title')} 】 变为 【 ID:{ret[r][issue_key]} · {ret[r].get(
                                        'requirement_title')} 】"""

                            # if issue_key == 'chance':
                            #     ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[issue_key],
                            #                                                    chance[str(issue_value)],
                            #                                                    chance[str(ret[r][issue_key])])
                            # if issue_key == 'issue_type':
                            #     ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[issue_key],
                            #                                                    issue_type[str(issue_value)],
                            #                                                    issue_type[str(ret[r][issue_key])])
                            # if issue_key == 'priority':
                            #     ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[issue_key],
                            #                                                    priority[str(issue_value)],
                            #                                                    priority[str(ret[r][issue_key])])
                            # if issue_key == 'level':
                            #     ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[issue_key],
                            #                                                    level[str(issue_value)],
                            #                                                    level[str(ret[r][issue_key])])
                            # if issue_key == 'handle_status':
                            #     ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[issue_key],
                            #                                                    handle_status[str(issue_value)],
                            #                                                    handle_status[str(ret[r][issue_key])])
                            # if issue_key == 'system':
                            #     ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[issue_key],
                            #                                                    system[str(issue_value)],
                            #                                                    system[str(ret[r][issue_key])])
                            # if issue_key == 'detection_chance':
                            #     ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[issue_key],
                            #                                                    detection_chance[str(issue_value)],
                            #                                                    detection_chance[str(ret[r][issue_key])])
                        except Exception as e:
                            current_app.logger.error(str(e))
                        ret_list.append(ret_dict)
        ret_list = ret_list[::-1]
        current_app.logger.info(json.dumps(ret_list, ensure_ascii=False))
        return ret_list

    @classmethod
    def gain_rank(cls, level, chance):

        # 计算rank
        data_dict = {"0": 5, "1": 4, "2": 3, "3": 2, "4": 1}
        severity = data_dict[str(level)]
        occurrence = data_dict[str(chance)]
        rank_type = severity * occurrence

        return rank_type


class IssueDashBoardBusiness(object):
    user_trpc = Trpc('auth')

    @classmethod
    def issue_all_tester_dashboard(cls, start_date, end_date, testers=None):
        # 查询测试人员每天创建的issue个数
        if not testers:
            testers = cls.user_trpc.requests('get', '/user/role/3')
        detaillist = []
        dashboard_ret = Issue.query.add_columns(
            func.date_format(Issue.creation_time, "%Y-%m-%d").label('creation_time'),
            Issue.creator.label('creator'),
            func.count('*').label('count')). \
            filter(Issue.creation_time.between(start_date, end_date + " 23:59:59")). \
            group_by(func.date_format(Issue.creation_time, "%Y-%m-%d"), Issue.creator).order_by(
            desc(Issue.creator)).all()

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
    def issue_all_tester_dashboard_for_project(cls, data_temp, project_id, start_date, end_date):
        issues = Issue.query.filter(Issue.creation_time.between(start_date, end_date + " 23:59:59"),
                                    Issue.project_id == project_id,
                                    Issue.status != Issue.DISABLE,
                                    Issue.creator.in_(list(data_temp.keys()))
                                    ).all()
        for issue in issues:
            data_temp[issue.creator]["issue_count"] += 1
        return data_temp

    @classmethod
    def issue_project_dashboard(cls, start_date, end_date):
        issuesum_dashboard_ret = Issue.query.add_columns(
            Issue.project_id.label('project_id'),
            func.count('*').label('count')). \
            filter(Issue.creation_time.between(start_date, end_date + " 23:59:59")). \
            filter(Issue.status != Issue.DISABLE).group_by(Issue.project_id).all()
        detail = [
            dict(
                issuesum=[
                    dict(i)
                    for i in map(lambda x: zip(('project_id', 'count'), x),
                                 zip([i.project_id for i in issuesum_dashboard_ret],
                                     [i.count for i in issuesum_dashboard_ret]))
                ]
            )
        ]
        return detail

    @classmethod
    def issue_status_dashboard(cls, start_date, end_date):
        # issue的状态分布
        status_dashboard_ret = Issue.query.add_columns(
            func.date_format(Issue.creation_time, "%Y-%m-%d").label('creation_time'),
            Issue.handle_status.label('handle_status'),
            func.count('*').label('count')). \
            filter(Issue.creation_time.between(start_date, end_date + " 23:59:59")). \
            group_by(func.date_format(Issue.creation_time, "%Y-%m-%d"), Issue.handle_status).all()
        detail = [
            dict(
                handle_status=[
                    dict(i)
                    for i in map(lambda x: zip(('date', 'handle_status', 'count'), x),
                                 zip([i.creation_time for i in status_dashboard_ret],
                                     [i.handle_status for i in status_dashboard_ret],
                                     [i.count for i in status_dashboard_ret]))
                ])
        ]
        return detail[0]

    @classmethod
    def issue_priority_dashboard(cls, start_date, end_date):
        # issue的优先级分布
        priority_dashboard_ret = Issue.query.add_columns(
            func.date_format(Issue.creation_time, "%Y-%m-%d").label('creation_time'), Issue.priority.label('priority'),
            func.count('*').label('count')). \
            filter(Issue.creation_time.between(start_date, end_date + " 23:59:59")). \
            group_by(func.date_format(Issue.creation_time, "%Y-%m-%d"), Issue.priority).all()
        detail = [
            dict(
                priority=[
                    dict(i)
                    for i in map(lambda x: zip(('date', 'priority', 'count'), x),
                                 zip([i.creation_time for i in priority_dashboard_ret],
                                     [i.priority for i in priority_dashboard_ret],
                                     [i.count for i in priority_dashboard_ret]))
                ])
        ]
        return detail[0]

    # 看板根据pro_id查询issue各个状态的数量
    @classmethod
    def issue_project_id_dashboard(cls, pro_id):
        ret = Issue.query.add_columns(
            Issue.version.label('version'),
            Issue.handle_status.label('handle_status'),
            func.count('*').label('count')).filter(Issue.project_id == pro_id, Issue.status == Issue.ACTIVE).group_by(
            Issue.version, Issue.handle_status).all()
        temp_ret = []
        ret_label = ['version', 'handle_status', 'count']
        # 得到未分组的字典
        for i in ret:
            temp_ret.append(dict(zip(ret_label, [i.version, i.handle_status, i.count])))
            current_app.logger.info(temp_ret)
        # 字典分组统计,即去重
        dict_group = groupby(temp_ret, key=lambda x: x['version'])
        summary = []
        for version, items in dict_group:
            ret_dict = {'version': version, 'detail': []}
            temp = []
            for item in items:
                ret_dict['detail'].append(item)
                temp.append(item['count'])
                item.pop('version')
            ret_dict['total'] = int(sum(temp))
            summary.append(ret_dict)
        current_app.logger.info(summary)
        detail = [
            dict(
                project_id=pro_id,
                info=summary,
            )
        ]
        return detail

    @classmethod
    def issue_dashboard(cls, start_date, end_date):
        issue_close_dashboard = cls.issue_close_dashboard(start_date, end_date)
        issue_open_dashboard = cls.issue_open_dashboard(start_date, end_date)
        issue_close_dashboard['open_issue'] = issue_open_dashboard['open_issue']
        return issue_close_dashboard

    @classmethod
    def issue_close_dashboard(cls, start_date, end_date):
        close_issue_dashboard_ret = Issue.query.add_columns(
            func.date_format(Issue.creation_time, "%Y-%m-%d").label('creation_time'),
            func.count('*').label('count')). \
            filter(Issue.creation_time.between(start_date, end_date + " 23:59:59")). \
            filter(Issue.handle_status == 4).group_by(func.date_format(Issue.creation_time, "%Y-%m-%d")).all()
        detail = [
            dict(
                close_issue=[
                    dict(i)
                    for i in map(lambda x: zip(('date', 'count'), x),
                                 zip([i.creation_time for i in close_issue_dashboard_ret],
                                     [i.count for i in close_issue_dashboard_ret]))
                ])
        ]
        return detail[0]

    @classmethod
    def issue_open_dashboard(cls, start_date, end_date):
        open_issue_dashboard_ret = Issue.query.add_columns(
            func.date_format(Issue.creation_time, "%Y-%m-%d").label('creation_time'),
            func.count('*').label('count')). \
            filter(Issue.creation_time.between(start_date, end_date + " 23:59:59")). \
            filter(Issue.handle_status != 4).group_by(func.date_format(Issue.creation_time, "%Y-%m-%d")).all()
        detail = [
            dict(
                open_issue=[
                    dict(i)
                    for i in map(lambda x: zip(('date', 'count'), x),
                                 zip([i.creation_time for i in open_issue_dashboard_ret],
                                     [i.count for i in open_issue_dashboard_ret]))
                ])
        ]
        return detail[0]
