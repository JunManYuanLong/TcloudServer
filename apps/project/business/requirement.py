import json

from flask import request, g, current_app
from sqlalchemy import desc, asc, func, or_
from sqlalchemy.orm import aliased

from apps.auth.models.users import User
from apps.project.business.issue import IssueBusiness
from apps.project.business.tag import TagBusiness
from apps.project.models.project import Project
from apps.project.models.requirement import (
    Requirement, RequirementRecord, RequirementReview, Review,
    RequirementBindCase,
)
from apps.project.models.tag import Tag
from apps.project.models.version import Version
from apps.public.models.public import Config
from library.api.db import db
from library.api.exceptions import FieldMissingException, CannotFindObjectException, SaveObjectException
from library.api.transfer import transfer2jsonwithoutset, transfer2json
from library.notification import notification
from library.trpc import Trpc


class RequirementBusiness(object):
    user_trpc = Trpc('auth')
    public_trpc = Trpc('public')

    @classmethod
    def _query(cls):
        user_creator = aliased(User)
        user_handler = aliased(User)

        return Requirement.query.outerjoin(
            user_creator, user_creator.id == Requirement.creator).outerjoin(
            user_handler, user_handler.id == Requirement.handler).outerjoin(
            Version, Version.id == Requirement.version).add_columns(
            Requirement.id.label('id'),
            Requirement.title.label('title'),
            Requirement.project_id.label('project_id'),
            Requirement.creator.label('creator'),
            Requirement.board_status.label('board_status'),
            Requirement.status.label('status'),
            Requirement.description.label('description'),
            Requirement.comment.label('comment'),
            Requirement.priority.label('priority'),
            Requirement.requirement_type.label('requirement_type'),
            Requirement.attach.label('attach'),
            Requirement.jira_id.label('jira_id'),
            Requirement.worth.label('worth'),
            Requirement.worth_sure.label('worth_sure'),
            Requirement.report_time.label('report_time'),
            Requirement.report_expect.label('report_expect'),
            Requirement.report_real.label('report_real'),
            Version.id.label('version_id'),
            Version.title.label('version_name'),
            user_handler.id.label('handler_id'),
            user_handler.nickname.label('handler_name'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),
            func.date_format(Requirement.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
            func.date_format(Requirement.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            Requirement.parent_id.label('parent_id'),
            Requirement.review_status.label('review_status'),
            func.date_format(Requirement.expect_time, "%Y-%m-%d %H:%i:%s").label('expect_time'),
            Requirement.tag.label('tag')
        )

    @classmethod
    @transfer2jsonwithoutset(
        '?id|!title|!project_id|!version_id|!version_name|!creator_id|!creator_name|!handler_id|!handler_name|'
        '!board_status|!description|!comment|!priority|!requirement_type|!attach|!parent_id|!review_status|'
        '!jira_id|!worth|!report_time|!report_expect|!report_real|!worth_sure|!expect_time|!tag')
    def query_all_json(cls):
        projectid = request.args.get('projectid')
        versionid = request.args.get('versionid')
        rtype = request.args.get('type')
        notype = request.args.get('notype')
        requirement_id = request.args.get('requirement_id')
        worth = request.args.get('worth')
        worth_sure = request.args.get('worth_sure')
        review_status = request.args.get('review_status')
        title = request.args.get('title')
        board_status = request.args.get('board_status')
        priority = request.args.get('priority')
        handler_id = request.args.get('handler_id')
        tag = request.args.get('tag')

        ret = cls._query().filter(Requirement.status != Requirement.DISABLE)

        if title:
            ret = ret.filter(or_(Requirement.title.like(f'%{title}%'), Requirement.id.startswith(f'{title}%')))
        if priority:
            priority = priority.split(',')
            ret = ret.filter(Requirement.priority.in_(priority))
        if board_status:
            board_status = board_status.split(',')
            ret = ret.filter(Requirement.board_status.in_(board_status))
        if handler_id:
            handler_id = handler_id.split(',')
            ret = ret.filter(Requirement.handler.in_(handler_id))
        if review_status:
            ret = ret.filter(Requirement.review_status == review_status)
        if worth:
            ret = ret.filter(Requirement.worth == worth)
        if worth_sure:
            ret = ret.filter(Requirement.worth_sure == worth_sure)
        if requirement_id:
            ret = ret.filter(Requirement.id == requirement_id)
        if projectid:
            ret = ret.filter(Requirement.project_id == projectid)
        if versionid:
            ret = ret.filter(Requirement.version == versionid)
        if notype == '1':
            ret = ret.filter(Requirement.version is None)
        if notype == '0':
            ret = ret.filter(Requirement.version is not None)
        if rtype:
            ret = ret.filter(Requirement.requirement_type == rtype)
        if tag:
            ret = ret.filter(func.find_in_set(tag, Requirement.tag))
        ret = ret.order_by(asc(Requirement.id)).all()
        return ret

    @classmethod
    @transfer2json(
        '?id|!title|!project_id|!version_id|!version_name|!creator_id|!creator_name|!handler_id|!handler_name|'
        '!board_status|!comment|!priority|!requirement_type|!parent_id|!review_status|'
        '!jira_id|!worth|!report_time|!report_expect|!report_real|!worth_sure|!expect_time|!tag')
    def query_all_json_no_status(cls):
        projectid = request.args.get('projectid')
        versionid = request.args.get('versionid')
        rtype = request.args.get('type')
        notype = request.args.get('notype')
        requirement_id = request.args.get('requirement_id')
        worth = request.args.get('worth')
        worth_sure = request.args.get('worth_sure')
        title = request.args.get('title')
        board_status = request.args.get('board_status')
        priority = request.args.get('priority')
        handler_id = request.args.get('handler_id')
        user = request.args.get('user')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        tag = request.args.get('tag')

        ret = cls._query().filter(Requirement.status != Requirement.DISABLE)

        if title:
            ret = ret.filter(Requirement.title.like('%{}%'.format(title)))
        if priority:
            priority = priority.split(',')
            ret = ret.filter(Requirement.priority.in_(priority))
        if board_status:
            board_status = board_status.split(',')
            ret = ret.filter(Requirement.board_status.in_(board_status))
        if handler_id:
            handler_id = handler_id.split(',')
            ret = ret.filter(Requirement.handler.in_(handler_id))
        if worth:
            ret = ret.filter(Requirement.worth == worth)
        if worth_sure:
            ret = ret.filter(Requirement.worth_sure == worth_sure)
        if requirement_id:
            ret = ret.filter(Requirement.id == requirement_id)
        if projectid:
            ret = ret.filter(Requirement.project_id == projectid)
        if versionid:
            ret = ret.filter(Requirement.version == versionid)
        if notype == '1':
            ret = ret.filter(Requirement.version is None)
        if notype == '0':
            ret = ret.filter(Requirement.version is not None)
        if rtype:
            ret = ret.filter(Requirement.requirement_type == rtype)
        if user:
            ret = ret.filter(Requirement.handler == user)
        if tag:
            ret = ret.filter(func.find_in_set(tag, Requirement.tag))
        if start_time and end_time:
            ret = ret.filter(
                Requirement.modified_time.between(start_time, end_time + " 23:59:59"))
        ret = ret.order_by(asc(Requirement.id))

        return ret.all()

    @classmethod
    @transfer2json(
        '?id|!title|!project_id|!version_id|!version_name|!creator_id|!creator_name|!handler_id|!handler_name|'
        '!board_status|!description|!comment|!priority|!requirement_type|!attach|!parent_id|!review_status|'
        '!jira_id|!worth|!report_time|!report_expect|!report_real|!worth_sure|!expect_time|!tag')
    def query_by_id(cls, requirement_id):
        ret = cls._query().filter(Requirement.status != Requirement.DISABLE,
                                  Requirement.id == requirement_id).all()
        return ret

    @classmethod
    def query_requirement_issue_case_by_id(cls, requirement_id):
        issues = IssueBusiness.query_id_title_by_requirement_id(requirement_id)
        case_ids = RequirementBindCaseBusiness.query_case_ids_by_requirement_id(requirement_id)
        data = cls.query_by_id(requirement_id)[0]
        data['issue'] = issues
        data['case_ids'] = case_ids
        return data

    # 获取 requirement 通过 id，包含 case，issue
    @classmethod
    def query_requirement_by_id(cls, requirement_id):
        data = cls.query_requirement_issue_case_by_id(requirement_id)
        son_requirements = cls._query().filter(Requirement.status != Requirement.DISABLE,
                                               Requirement.parent_id == requirement_id).all()
        data['parent_list'] = []
        # 此处数量少的情况下，单独查询
        for son in son_requirements:
            data['parent_list'].append(cls.query_requirement_issue_case_by_id(son.id))
        return [data]

    @classmethod
    def requirement_delete(cls, requirementid):

        modifier = g.userid if g.userid else None
        req = Requirement.query.get(requirementid)

        req.status = Requirement.DISABLE
        db.session.add(req)
        RequirementRecordBusiness.modify(requirementid, req.title, req.project_id, req.version, req.board_status,
                                         req.handler,
                                         req.description, req.comment, req.priority, req.requirement_type,
                                         req.attach, req.creator, Requirement.DISABLE, modifier, req.parent_id,
                                         req.review_status, req.jira_id, req.worth, req.report_time, req.report_expect,
                                         req.report_real, req.worth_sure, req.expect_time, req.tag)
        db.session.commit()
        if req.tag:
            TagBusiness.less_reference(req.tag)
        return 0

    @classmethod
    def requirement_create(cls, title, project_id, version, handler, priority, requirement_type, attach,
                           board_status,
                           description, comment, jira_id, worth, report_time, report_expect, report_real,
                           worth_sure, case_ids, tag, expect_time=None, creator=None):
        try:
            is_repeat = Requirement.query.filter(Requirement.title == title,
                                                 Requirement.project_id == project_id,
                                                 Requirement.jira_id == jira_id,
                                                 Requirement.status != Requirement.DISABLE).first()
            if is_repeat:
                return 103
            if not creator:
                creator = g.userid if g.userid else creator
            current_app.logger.info("creator:" + str(creator))
            c = Requirement(
                title=title,
                project_id=project_id,
                version=version,
                priority=priority,
                requirement_type=requirement_type,
                attach=attach,
                creator=creator,
                board_status=board_status,
                handler=handler,
                description=description,
                comment=comment,
                modifier=creator,
                jira_id=jira_id,
                worth=worth,
                report_time=report_time,
                report_expect=report_expect,
                report_real=report_real,
                worth_sure=worth_sure,
                expect_time=expect_time,
                tag=tag
            )
            db.session.add(c)
            db.session.flush()
            RequirementRecordBusiness.create(c.id, title, project_id, version, board_status, handler, description,
                                             comment, priority, requirement_type, attach, creator,
                                             Requirement.ACTIVE,
                                             creator, 0, jira_id, worth, report_time, report_expect, report_real,
                                             worth_sure, expect_time, tag)

            if case_ids is not None:
                RequirementBindCaseBusiness.requirement_bind_cases(c.id, case_ids)

            db.session.commit()
            if tag:
                TagBusiness.add_reference(tag)

            board_config = cls.public_trpc.requests('get', '/public/config', {'module': 'tcloud', 'module_type': 1})
            text = f'''[需求创建 - {title}]
URL：{board_config}/project/{project_id}/requirement/{version}'''
            if not isinstance(handler, list):
                handler = [handler]
            notification.send_notification(handler, text, send_type=2)
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
            return 102

    @classmethod
    def requirement_children_create(cls, title, project_id, version, board_status, handler, description, comment,
                                    priority, requirement_type, attach, parent_id, jira_id, worth, report_time,
                                    report_expect, report_real, worth_sure, case_ids, tag, expect_time=None,
                                    creator=None):
        try:
            is_repeat = Requirement.query.filter(Requirement.title == title,
                                                 Requirement.project_id == project_id,
                                                 Requirement.status != Requirement.DISABLE).first()
            if is_repeat:
                return 103
            if not creator:
                creator = g.userid if g.userid else creator
            c = Requirement(
                title=title,
                project_id=project_id,
                version=version,
                priority=priority,
                requirement_type=requirement_type,
                attach=attach,
                creator=creator,
                board_status=board_status,
                handler=handler,
                description=description,
                comment=comment,
                modifier=creator,
                parent_id=parent_id,
                jira_id=jira_id,
                worth=worth,
                report_time=report_time,
                report_expect=report_expect,
                report_real=report_real,
                worth_sure=worth_sure,
                expect_time=expect_time,
                tag=tag
            )
            db.session.add(c)
            db.session.flush()
            RequirementRecordBusiness.create(c.id, title, project_id, version, board_status, handler, description,
                                             comment, priority, requirement_type, attach, creator,
                                             Requirement.ACTIVE,
                                             creator, parent_id, jira_id, worth, report_time, report_expect,
                                             report_real, worth_sure, expect_time, tag)
            if case_ids is not None:
                RequirementBindCaseBusiness.requirement_bind_cases(c.id, case_ids)

            db.session.commit()
            if tag:
                TagBusiness.add_reference(tag)
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
            return 102

    @classmethod
    def requirement_modify(cls, requirementid, title, project_id, version, board_status, handler, description, comment,
                           priority, requirement_type, attach, parent_id, jira_id, worth, report_time, report_expect,
                           report_real, worth_sure, case_ids, tag, expect_time=None, creator=None, modifier=None):
        if not modifier:
            modifier = g.userid if g.userid else modifier
        c = Requirement.query.get(requirementid)

        ret = Requirement.query.filter_by(title=title,
                                          status=Requirement.ACTIVE,
                                          project_id=c.project_id).filter(Requirement.id != requirementid).first()
        if ret:
            raise SaveObjectException('存在相同名称的需求')
        old_tag = None
        new_tag = None
        is_change_handler = False
        if c.handler != handler:
            is_change_handler = True
        c.title = title
        c.project_id = project_id
        c.version = version
        c.board_status = board_status
        c.handler = handler
        c.priority = priority
        c.requirement_type = requirement_type
        c.attach = attach
        c.description = description
        c.comment = comment
        c.modifier = modifier
        c.parent_id = parent_id
        c.jira_id = jira_id
        c.worth = worth
        c.report_time = report_time
        c.report_expect = report_expect
        c.report_real = report_real
        c.worth_sure = worth_sure
        c.expect_time = expect_time
        if c.tag != tag:
            old_tag = c.tag
            new_tag = tag
            c.tag = tag
        c.creator = creator if creator else c.creator
        db.session.add(c)
        RequirementRecordBusiness.modify(requirementid, title, project_id, version, board_status, handler,
                                         description,
                                         comment, priority, requirement_type, attach, c.creator, c.status, modifier,
                                         parent_id, c.review_status, c.jira_id, c.worth, c.report_time,
                                         c.report_expect, c.report_real, c.worth_sure, expect_time, tag)
        if case_ids is not None:
            RequirementBindCaseBusiness.requirement_bind_cases(c.id, case_ids)
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
            text = f'''[requirement处理人变更 - {title}]
{modifier_user}  修改处理人为  {handler_user}'''
            notification.send_notification(handler, text, send_type=2)
        return 0

    @classmethod
    @transfer2json(
        '?id|!title|!project_id|!version_id|!version_name|!creator_id|!creator_name|!handler_id|!handler_name|'
        '!board_status|!description|!comment|!priority|!requirement_type|!attach|!modified_time|!parent_id|'
        '!review_status|!jira_id|!worth|!report_time|!report_expect|!report_real|!worth_sure|!expect_time|!tag')
    def look_up_chidren_requirement(cls, id, project_id, version_id):
        if version_id:
            ret = cls._query().filter(Requirement.status != Requirement.DISABLE, Requirement.parent_id == id,
                                      Requirement.project_id == project_id, Requirement.version == version_id).all()
        else:
            ret = cls._query().filter(Requirement.status != Requirement.DISABLE, Requirement.parent_id == id,
                                      Requirement.project_id == project_id).all()

        return ret

    @classmethod
    @transfer2json(
        '?id|!title|!project_id|!version_id|!version_name|!creator_id|!creator_name|!handler_id|!handler_name|'
        '!board_status|!description|!comment|!priority|!requirement_type|!attach|!modified_time|!parent_id|'
        '!review_status|!jira_id|!worth|!report_time|!report_expect|!report_real|!worth_sure|!expect_time|!tag')
    def look_up_pass_chidren_requirement(cls, id, project_id, version_id, review_status):
        ret = cls._query().filter(Requirement.status != Requirement.DISABLE, Requirement.parent_id == id,
                                  Requirement.project_id == project_id)
        if version_id:
            ret = ret.filter(Requirement.version == version_id)
        if review_status:
            ret = ret.filter(Requirement.review_status == review_status)

        return ret.order_by(desc(Requirement.id)).all()

    @classmethod
    @transfer2json('?id')
    def look_up_pass_chidren_requirement_id(cls, id, project_id, version_id, review_status):
        ret = cls._query().filter(Requirement.status != Requirement.DISABLE, Requirement.parent_id == id,
                                  Requirement.project_id == project_id)
        if version_id:
            ret = ret.filter(Requirement.version == version_id)
        if review_status:
            ret = ret.filter(Requirement.review_status == review_status)

        return ret.order_by(desc(Requirement.id)).all()

    @classmethod
    def look_up_board_status(cls, id, project_id, version_id):
        requirement = cls._query().filter(Requirement.status != Requirement.DISABLE, Requirement.parent_id == id,
                                          Requirement.project_id == project_id, Requirement.version == version_id,
                                          Requirement.board_status == 5).all()
        requirement_sum = sum(r.count for r in requirement)
        return requirement_sum

    @classmethod
    def boardstatus_switch(cls, id, mstatus):
        try:
            modifier = g.userid if g.userid else None
            req = Requirement.query.get(id)
            req.board_status = mstatus
            db.session.add(req)
            c = RequirementRecord(
                requirement_id=req.id,
                title=req.title,
                project_id=req.project_id,
                version=req.version,
                priority=req.priority,
                requirement_type=req.requirement_type,
                attach=req.attach,
                creator=req.creator,
                board_status=mstatus,
                status=req.status,
                handler=req.handler,
                description=req.description,
                comment=req.comment,
                modifier=modifier,
                parent_id=req.parent_id,
                review_status=req.review_status,
                jira_id=req.jira_id,
                worth=req.worth,
                report_time=req.report_time,
                report_expect=req.report_expect,
                report_real=req.report_real,
                worth_sure=req.worth_sure,
                expect_time=req.expect_time,
                tag=req.tag
            )
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def handler_switch(cls, id, handler):
        try:
            handle = User.query.get(handler)
            if handle is None:
                return 101
            modifier = g.userid if g.userid else None
            req = Requirement.query.get(id)
            req.handler = handler
            db.session.add(req)
            c = RequirementRecord(
                requirement_id=req.id,
                title=req.title,
                project_id=req.project_id,
                version=req.version,
                priority=req.priority,
                requirement_type=req.requirement_type,
                attach=req.attach,
                creator=req.creator,
                board_status=req.board_status,
                status=req.status,
                handler=handler,
                description=req.description,
                comment=req.comment,
                modifier=modifier,
                parent_id=req.parent_id,
                review_status=req.review_status,
                jira_id=req.jira_id,
                worth=req.worth,
                report_time=req.report_time,
                report_expect=req.report_expect,
                report_real=req.report_real,
                worth_sure=req.worth_sure,
                expect_time=req.expect_time,
                tag=req.tag
            )
            db.session.add(c)
            db.session.commit()
            #             text = f'''[需求处理人修改 - {req.title}]
            # 你已被修改为处理人'''
            #             if not isinstance(handler, list):
            #                 handler = [handler]
            modifier_user = cls.user_trpc.requests('get', f'/user/{g.userid}')
            if modifier_user:
                modifier_user = modifier_user[0].get('nickname')
            handler_user = cls.user_trpc.requests('get',
                                                  f'/user/{handler if not isinstance(handler, list) else handler[0]}')
            if handler_user:
                handler_user = handler_user[0].get('nickname')
            if not isinstance(handler, list):
                handler = [handler]
            text = f'''[requirement处理人变更 - {req.title}]
{modifier_user}  修改处理人为  {handler_user}'''
            notification.send_notification(handler, text, send_type=2)
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def status_switch(cls, id, mstatus):
        try:
            modifier = g.userid if g.userid else None
            req = Requirement.query.get(id)
            req.board_status = mstatus
            db.session.add(req)
            c = RequirementRecord(
                requirement_id=req.id,
                title=req.title,
                project_id=req.project_id,
                version=req.version,
                priority=req.priority,
                requirement_type=req.requirement_type,
                attach=req.attach,
                creator=req.creator,
                board_status=req.board_status,
                status=mstatus,
                handler=req.handler,
                description=req.description,
                comment=req.comment,
                modifier=modifier,
                parent_id=req.parent_id,
                review_status=req.review_status,
                jira_id=req.jira_id,
                worth=req.worth,
                report_time=req.report_time,
                report_expect=req.report_expect,
                report_real=req.report_real,
                worth_sure=req.worth_sure,
                expect_time=req.expect_time,
                tag=req.tag
            )
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def priority_switch(cls, id, priority):
        try:
            modifier = g.userid if g.userid else None
            req = Requirement.query.get(id)
            req.priority = priority
            db.session.add(req)
            c = RequirementRecord(
                requirement_id=req.id,
                title=req.title,
                project_id=req.project_id,
                version=req.version,
                priority=priority,
                requirement_type=req.requirement_type,
                attach=req.attach,
                creator=req.creator,
                board_status=req.board_status,
                status=req.status,
                handler=req.handler,
                description=req.description,
                comment=req.comment,
                modifier=modifier,
                parent_id=req.parent_id,
                review_status=req.review_status,
                jira_id=req.jira_id,
                worth=req.worth,
                report_time=req.report_time,
                report_expect=req.report_expect,
                report_real=req.report_real,
                worth_sure=req.worth_sure,
                expect_time=req.expect_time,
                tag=req.tag
            )
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def add_comment(cls, id, comment):
        try:
            modifier = g.userid if g.userid else None
            req = Requirement.query.get(id)
            req.comment = comment
            db.session.add(req)
            c = RequirementRecord(
                requirement_id=req.id,
                title=req.title,
                project_id=req.project_id,
                version=req.version,
                priority=req.priority,
                requirement_type=req.requirement_type,
                attach=req.attach,
                creator=req.creator,
                board_status=req.board_status,
                status=req.status,
                handler=req.handler,
                description=req.description,
                comment=comment,
                modifier=modifier,
                parent_id=req.parent_id,
                review_status=req.review_status,
                jira_id=req.jira_id,
                worth=req.worth,
                report_time=req.report_time,
                report_expect=req.report_expect,
                report_real=req.report_real,
                worth_sure=req.worth_sure,
                expect_time=req.expect_time,
                tag=req.tag
            )
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def review_status_modify(cls, id):
        try:
            modifier = g.userid if g.userid else None
            req = Requirement.query.get(id)
            req.review_status = 1
            db.session.add(req)
            c = RequirementRecord(
                requirement_id=req.id,
                title=req.title,
                project_id=req.project_id,
                version=req.version,
                priority=req.priority,
                requirement_type=req.requirement_type,
                attach=req.attach,
                creator=req.creator,
                board_status=req.board_status,
                status=req.status,
                handler=req.handler,
                description=req.description,
                comment=req.comment,
                modifier=modifier,
                parent_id=req.parent_id,
                review_status=1,
                jira_id=req.jira_id,
                worth=req.worth,
                report_time=req.report_time,
                report_expect=req.report_expect,
                report_real=req.report_real,
                worth_sure=req.worth_sure,
                expect_time=req.expect_time,
                tag=req.tag
            )
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def review_modify(cls, result):
        try:

            modifier = g.userid if g.userid else None
            for re in result['pass']:
                review_id = RequirementReview.query.get(int(re))

                req = Requirement.query.get(int(review_id.requirement_id))
                req.review_status = 2
                req.modifier = modifier

                reqrecord = RequirementRecord(
                    requirement_id=req.id,
                    title=req.title,
                    project_id=req.project_id,
                    version=req.version,
                    priority=req.priority,
                    requirement_type=req.requirement_type,
                    attach=req.attach,
                    creator=req.creator,
                    board_status=req.board_status,
                    status=req.status,
                    handler=req.handler,
                    description=req.description,
                    comment=req.comment,
                    modifier=modifier,
                    parent_id=req.parent_id,
                    review_status=2,
                    jira_id=req.jira_id,
                    worth=req.worth,
                    report_time=req.report_time,
                    report_expect=req.report_expect,
                    report_real=req.report_real,
                    worth_sure=req.worth_sure,
                    expect_time=req.expect_time,
                    tag=req.tag
                )
                db.session.add(req)
                db.session.add(reqrecord)
            for re in result['fail']:
                review_id = RequirementReview.query.get(int(re))
                req = Requirement.query.get(int(review_id.requirement_id))
                req.review_status = 3
                req.modifier = modifier
                reqrecord = RequirementRecord(
                    requirement_id=req.id,
                    title=req.title,
                    project_id=req.project_id,
                    version=req.version,
                    priority=req.priority,
                    requirement_type=req.requirement_type,
                    attach=req.attach,
                    creator=req.creator,
                    board_status=req.board_status,
                    status=req.status,
                    handler=req.handler,
                    description=req.description,
                    comment=req.comment,
                    modifier=modifier,
                    parent_id=req.parent_id,
                    review_status=3,
                    jira_id=req.jira_id,
                    worth=req.worth,
                    report_time=req.report_time,
                    report_expect=req.report_expect,
                    report_real=req.report_real,
                    worth_sure=req.worth_sure,
                    expect_time=req.expect_time,
                    tag=req.tag
                )
                db.session.add(req)
                db.session.add(reqrecord)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    @transfer2json('?id|!title')
    def get_requirement_by_id_or_title(cls, id_or_title):
        project_id = request.args.get('projectid')
        ret = Requirement.query.add_columns(
            Requirement.id.label('id'),
            Requirement.title.label('title')
        ).filter(Requirement.status != Requirement.DISABLE,
                 or_(Requirement.id.like('%{}%'.format(id_or_title)),
                     Requirement.title.like('%{}%'.format(id_or_title))))
        if project_id:
            ret = ret.filter(Requirement.project_id == project_id)
        return ret.all()

    @classmethod
    def get_requirement(cls):
        # 获取所有的父需求的id
        all_data = RequirementBusiness.query_all_json_no_status()
        father_data = []
        son_data = []
        # 获取父子需求
        father_id_list = []  # 子需求生成的父id
        father_list = []  # 直接获取的父id
        review_status = request.args.get('review_status')
        if review_status and review_status.isdigit():
            review_status = int(review_status)
        else:
            return 414, ''
        if review_status:
            for i in range(0, len(all_data)):
                if all_data[i]['review_status'] == review_status:
                    if all_data[i]['parent_id'] == 0:
                        father_data.append(all_data[i])
                        father_list.append(all_data[i]['id'])
                    else:
                        son_data.append(all_data[i])
                        father_id_list.append(all_data[i]['parent_id'])
        else:
            for i in range(0, len(all_data)):
                if all_data[i]['parent_id'] == 0:
                    father_data.append(all_data[i])
                    father_list.append(all_data[i]['id'])
                else:
                    son_data.append(all_data[i])
                    father_id_list.append(all_data[i]['parent_id'])

        father_id_list = list(set(father_id_list))
        some_father_data = []
        # 通过获取的子需求获取父需求
        for i in range(0, len(all_data)):
            if all_data[i]['id'] in father_id_list and all_data[i]['id'] not in father_list:
                some_father_data.append(all_data[i])
        father_data.extend(some_father_data)

        for i in range(0, len(father_data)):
            data_list = []
            for j in range(0, len(son_data)):

                if father_data[i]['id'] == son_data[j]['parent_id']:
                    data_list.append(son_data[j])
            father_data[i]['parent_list'] = data_list
        return 0, father_data

    @classmethod
    @transfer2json(
        '?id|!title|!project_id|!version_id|!version_name|!creator_id|!creator_name|!handler_id|!handler_name|'
        '!board_status|!description|!comment|!priority|!requirement_type|!attach|!parent_id|!review_status|'
        '!jira_id|!worth|!report_time|!report_expect|!report_real|!worth_sure|!creation_time|!expect_time|!tag',
        ispagination=True
    )
    def paginate_data(cls, page_size=None, page_index=None):
        query = cls.filter_query().order_by(desc(Requirement.id))
        count = query.count()
        if page_size and page_index:
            query = query.limit(int(page_size)).offset((int(page_index) - 1) * int(page_size))
        data = query.all()
        return data, count

    @classmethod
    def filter_query(cls):
        projectid = request.args.get('projectid')
        versionid = request.args.get('versionid')
        rtype = request.args.get('type')
        notype = request.args.get('notype')
        title = request.args.get('title')
        board_status = request.args.get('board_status')
        priority = request.args.get('priority')
        handler_id = request.args.get('handler_id')
        review_status = request.args.get('review_status')
        worth = request.args.get('worth')
        worth_sure = request.args.get('worth_sure')
        requirement_id = request.args.get('requirement_id')
        id_or_title = request.args.get('id_or_title')
        user = request.args.get('user')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        tag = request.args.get('tag')
        ret = cls._query().filter(Requirement.status != Requirement.DISABLE, Requirement.parent_id == 0)
        if worth:
            ret = ret.filter(Requirement.worth == worth)
        if worth_sure:
            ret = ret.filter(Requirement.worth_sure == worth_sure)
        if projectid:
            ret = ret.filter(Requirement.project_id == projectid)
        if versionid:
            ret = ret.filter(Requirement.version == versionid)
        if notype == '1':
            ret = ret.filter(Requirement.version == None)
        if notype == '0':
            ret = ret.filter(Requirement.version != None)
        if rtype:
            ret = ret.filter(Requirement.requirement_type == rtype)
        if title:
            ret = ret.filter(or_(Requirement.title.like(f'%{title}%'), Requirement.id.startswith(f'{title}%')))
        if priority:
            priority = priority.split(',')
            ret = ret.filter(Requirement.priority.in_(priority))
        if board_status:
            board_status = board_status.split(',')
            ret = ret.filter(Requirement.board_status.in_(board_status))
        if handler_id:
            handler_id = handler_id.split(',')
            ret = ret.filter(Requirement.handler.in_(handler_id))
        if review_status:
            review_status = review_status.split(',')
            ret = ret.filter(Requirement.review_status.in_(review_status))
        if requirement_id:
            ret = ret.filter(Requirement.id.like('%{}%'.format(requirement_id)))
        if user:
            ret = ret.filter(Requirement.handler == user)
        if start_time and end_time:
            ret = ret.filter(
                Requirement.modified_time.between(start_time, end_time + " 23:59:59"))
        if id_or_title:
            ret = ret.filter(or_(Requirement.id.like('%{}%'.format(id_or_title)),
                                 Requirement.title.like('%{}%'.format(id_or_title))))
        if tag:
            ret = ret.filter(func.find_in_set(tag, Requirement.tag))
        return ret


class RequirementBindCaseBusiness(object):

    @classmethod
    def _query(cls):
        return RequirementBindCase.query.filter(
            RequirementBindCase.status == RequirementBindCase.ACTIVE).add_clomuns(
            RequirementBindCase.id.label('id'),
            RequirementBindCase.requirement_id.label('requirement_id'),
            RequirementBindCase.case_id.label('case_id')
        )

    @classmethod
    def query_case_ids_by_requirement_id(cls, requirement_id):
        all_data = RequirementBindCase.query.filter(RequirementBindCase.requirement_id == requirement_id).all()
        case_ids = []
        for data in all_data:
            case_ids.append(data.case_id)
        return case_ids

    @classmethod
    def query_requirement_ids_by_case_id(cls, case_id):
        all_data = RequirementBindCase.query.filter(RequirementBindCase.case_id == case_id).all()
        requirement_ids = []
        for data in all_data:
            requirement_ids.append(data.requirement_id)
        return requirement_ids

    @classmethod
    def create_check_exist_record(cls, requirement_id, case_id):
        record = RequirementBindCase.query.filter(RequirementBindCase.requirement_id == requirement_id,
                                                  RequirementBindCase.case_id == case_id).first()
        if record:
            record.status = RequirementBindCase.ACTIVE
            db.session.add(record)
            return True
        return False

    @classmethod
    def create_requirement_bind_case(cls, requirement_id, case_id):
        current_app.logger.info('create_requirement_bind_case')
        if not requirement_id or not case_id:
            raise FieldMissingException('requirement_id or case_id missing!')

        if cls.create_check_exist_record(requirement_id, case_id):
            return

        requirement_bind_case = RequirementBindCase(
            requirement_id=requirement_id,
            case_id=case_id
        )
        db.session.add(requirement_bind_case)

    @classmethod
    def update_requirement_bind_case(cls, this_id, requirement_id=None, case_id=None, status=0):
        current_app.logger.info(f'update_requirement_bind_case{this_id}')
        if not id and not requirement_id and not case_id:
            raise FieldMissingException('requirement_id or case_id is needed!')

        requirement_bind_case = RequirementBindCase.query.get(this_id)

        if not requirement_bind_case:
            raise CannotFindObjectException(f'not found requirement_bind_case with id {this_id}')

        requirement_bind_case.requirement_id = requirement_id or requirement_bind_case.requirement_id
        requirement_bind_case.case_id = case_id or requirement_bind_case.case_id
        requirement_bind_case.status = status
        db.session.add(requirement_bind_case)

    @classmethod
    def requirement_unbind_cases(cls, case_ids):
        for case_id in case_ids:
            cls.update_requirement_bind_case(case_id, status=RequirementBindCase.DISABLE)

    @classmethod
    def requirement_bind_cases(cls, requirement_id, case_ids):
        records = RequirementBindCase.query.filter(RequirementBindCase.requirement_id == requirement_id).all()
        unbind_case_ids = []
        current_app.logger.info(case_ids)
        for record in records:
            case_id = record.case_id
            if case_id in case_ids:
                cls.update_requirement_bind_case(record.id, status=RequirementBindCase.ACTIVE)
                case_ids.remove(case_id)
            else:
                unbind_case_ids.append(record.id)

        current_app.logger.info(case_ids)
        for case_id in case_ids:
            cls.create_requirement_bind_case(requirement_id, case_id)
        cls.requirement_unbind_cases(unbind_case_ids)

    @classmethod
    def case_unbind_requirements(cls, this_ids):
        for this_id in this_ids:
            cls.update_requirement_bind_case(this_id, status=RequirementBindCase.DISABLE)

    @classmethod
    def case_bind_requirements(cls, case_id, requirement_ids):
        records = RequirementBindCase.query.filter(RequirementBindCase.case_id == case_id).all()
        unbind_requirement_ids = []
        for record in records:
            requirement_id = record.requirement_id
            if requirement_id in requirement_ids:
                cls.update_requirement_bind_case(record.id, status=RequirementBindCase.ACTIVE)
                requirement_ids.remove(requirement_id)
            else:
                unbind_requirement_ids.append(record.id)
        current_app.logger.info(requirement_ids)

        for requirement_id in requirement_ids:
            cls.create_requirement_bind_case(requirement_id, case_id)

        cls.requirement_unbind_cases(unbind_requirement_ids)


class RequirementRecordBusiness(object):
    @classmethod
    def _query(cls):
        user_creator = aliased(User)
        user_modifier = aliased(User)
        user_handler = aliased(User)

        return RequirementRecord.query.outerjoin(
            user_creator, user_creator.id == RequirementRecord.creator).outerjoin(
            user_modifier, user_modifier.id == RequirementRecord.modifier).outerjoin(
            user_handler, user_handler.id == RequirementRecord.handler).outerjoin(
            Version, Version.id == RequirementRecord.version).add_columns(
            RequirementRecord.id.label('id'),
            RequirementRecord.requirement_id.label('requirement_id'),
            RequirementRecord.title.label('title'),
            RequirementRecord.project_id.label('project_id'),
            RequirementRecord.board_status.label('board_status'),
            RequirementRecord.status.label('status'),
            func.date_format(RequirementRecord.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(RequirementRecord.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
            RequirementRecord.description.label('description'),
            RequirementRecord.comment.label('comment'),
            RequirementRecord.priority.label('priority'),
            RequirementRecord.requirement_type.label('requirement_type'),
            RequirementRecord.attach.label('attach'),
            RequirementRecord.jira_id.label('jira_id'),
            RequirementRecord.worth.label('worth'),
            RequirementRecord.report_time.label('report_time'),
            RequirementRecord.report_expect.label('report_expect'),
            RequirementRecord.report_real.label('report_real'),
            RequirementRecord.worth_sure.label('worth_sure'),
            Version.id.label('version_id'),
            Version.title.label('version_name'),
            user_handler.id.label('handler_id'),
            user_handler.nickname.label('handler_name'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),
            user_modifier.id.label('modifier_id'),
            user_modifier.nickname.label('modifier_name'),
            RequirementRecord.parent_id.label('parent_id'),
            RequirementRecord.review_status.label('review_status'),
            RequirementRecord.tag.label('tag'),
            func.date_format(RequirementRecord.expect_time, "%Y-%m-%d %H:%i:%s").label('expect_time'),
        )

    # 新增requirement时增加历史记录
    @classmethod
    def create(cls, requirement_id, title, project_id, version, board_status, handler, description, comment, priority,
               requirement_type, attach, creator, status, modifier, parent_id, jira_id, worth, report_time,
               report_expect, report_real, worth_sure, expect_time, tag):
        c = RequirementRecord(
            requirement_id=requirement_id,
            title=title,
            project_id=project_id,
            version=version,
            priority=priority,
            requirement_type=requirement_type,
            attach=attach,
            creator=creator,
            board_status=board_status,
            handler=handler,
            description=description,
            comment=comment,
            status=status,
            modifier=modifier,
            parent_id=parent_id,
            jira_id=jira_id,
            worth=worth,
            report_time=report_time,
            report_expect=report_expect,
            report_real=report_real,
            worth_sure=worth_sure,
            expect_time=expect_time,
            tag=tag
        )
        db.session.add(c)

    # 新增requirement时增加历史记录
    @classmethod
    def modify(cls, requirement_id, title, project_id, version, board_status, handler, description, comment, priority,
               requirement_type, attach, creator, status, modifier, parent_id, review_status, jira_id, worth,
               report_time, report_expect, report_real, worth_sure, expect_time, tag):
        c = RequirementRecord(
            requirement_id=requirement_id,
            title=title,
            project_id=project_id,
            version=version,
            priority=priority,
            requirement_type=requirement_type,
            attach=attach,
            creator=creator,
            board_status=board_status,
            handler=handler,
            description=description,
            comment=comment,
            status=status,
            modifier=modifier,
            parent_id=parent_id,
            review_status=review_status,
            jira_id=jira_id,
            worth=worth,
            report_time=report_time,
            report_expect=report_expect,
            report_real=report_real,
            worth_sure=worth_sure,
            expect_time=expect_time,
            tag=tag
        )
        db.session.add(c)

    @classmethod
    @transfer2jsonwithoutset(
        '?id|!title|!project_id|!version_id|!version_name|!creator_id|!creator_name|!modifier_id|!modifier_name|'
        '!creation_time|!modified_time|!handler_id|!handler_name|!board_status|!description|!comment|!priority|'
        '!requirement_type|!attach|!parent_id|!review_status|!jira_id|!worth|!report_time|!report_expect|'
        '!report_real|!worth_sure|!expect_time|!tag')
    def query_record_json(cls, requirement_id):
        ret = cls._query().filter(RequirementRecord.requirement_id == requirement_id).order_by(
            RequirementRecord.requirement_id).all()
        return ret

    @classmethod
    def query_record_detail(cls, requirement_id):
        ret = cls.query_record_json(requirement_id)
        if not ret:
            return []
        ret_list = []
        requirement_config = Config.query.add_columns(Config.content.label('content')).filter(
            Config.module == 'requirement',
            Config.module_type == 1).first()
        requirement_config = json.loads(requirement_config.content)
        current_app.logger.info(json.dumps(requirement_config, ensure_ascii=False))
        operation_dict = requirement_config['operation_dict']
        requirement_type = requirement_config['requirement_type']
        priority = requirement_config['priority']
        handle_status = requirement_config['board_status']
        review_status = requirement_config['review_status']
        worth = requirement_config['worth']
        worth_sure = requirement_config['worth_sure']

        ret_dict = {
            'modified_time': ret[0]['creation_time'], 'modifier_id': ret[0]['creator_id'],
            'modifier_name': ret[0]['creator_name'], 'operation': "创建了需求 {}".format(ret[0]['title'])
        }
        ret_list.append(ret_dict)

        for r in range(1, len(ret)):
            for ret_key, ret_value in ret[r - 1].items():
                if ret_value != ret[r][ret_key] and ret_key in operation_dict.keys():
                    current_app.logger.info(
                        "修改的字段：" + str(ret_key) + ", 字段值：" + str(ret_value) + "-->" + str(ret[r][ret_key]))
                    # 如果comment修改后为空，则跳过
                    if ret_key == 'comment' and not ret[r][ret_key]:
                        pass
                    else:
                        ret_dict = {
                            'modified_time': ret[r]['modified_time'], 'modifier_id': ret[r]['modifier_id'],
                            'modifier_name': ret[r]['modifier_name'],
                            'operation': "修改了{} {} 为 {}".format(operation_dict[ret_key], ret_value,
                                                                ret[r][ret_key])
                        }
                        try:
                            if ret_key == 'comment':
                                ret_dict['operation'] = "添加了备注 {}".format(ret[r][ret_key])
                            if ret_key == 'requirement_type':
                                ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[ret_key],
                                                                               requirement_type[str(ret_value)],
                                                                               requirement_type[str(ret[r][ret_key])])
                            if ret_key == 'priority':
                                ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[ret_key],
                                                                               priority[str(ret_value)],
                                                                               priority[str(ret[r][ret_key])])
                            if ret_key == 'board_status':
                                ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[ret_key],
                                                                               handle_status[str(ret_value)],
                                                                               handle_status[str(ret[r][ret_key])])
                            if ret_key == 'review_status':
                                ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[ret_key],
                                                                               review_status[str(ret_value)],
                                                                               review_status[str(ret[r][ret_key])])
                            if ret_key == 'worth':
                                ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[ret_key],
                                                                               worth[str(ret_value)],
                                                                               worth[str(ret[r][ret_key])])
                            if ret_key == 'worth_sure':
                                ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[ret_key],
                                                                               worth_sure[str(ret_value)],
                                                                               worth_sure[str(ret[r][ret_key])])

                        except Exception as e:
                            current_app.logger.error(str(e))
                        ret_list.append(ret_dict)
        ret_list = ret_list[::-1]
        # current_app.logger.info(json.dumps(ret_list, ensure_ascii=False))
        return ret_list


class RequirementReviewBusiness(object):
    public_trpc = Trpc('public')
    message_trpc = Trpc('message')

    @classmethod
    def _req_query(cls):
        user_creator = aliased(User)
        user_handler = aliased(User)

        return RequirementReview.query.outerjoin(
            user_creator, user_creator.id == RequirementReview.creator).outerjoin(
            user_handler, user_handler.id == RequirementReview.handler).outerjoin(
            Version, Version.id == RequirementReview.version).add_columns(
            RequirementReview.id.label('id'),
            RequirementReview.requirement_id.label('requirement_id'),
            RequirementReview.review_id.label('review_id'),
            RequirementReview.title.label('title'),
            RequirementReview.project_id.label('project_id'),
            RequirementReview.board_status.label('board_status'),
            RequirementReview.status.label('status'),
            func.date_format(RequirementReview.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(RequirementReview.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
            RequirementReview.description.label('description'),
            RequirementReview.comment.label('comment'),
            RequirementReview.priority.label('priority'),
            RequirementReview.requirement_type.label('requirement_type'),
            RequirementReview.attach.label('attach'),
            RequirementReview.jira_id.label('jira_id'),
            RequirementReview.worth.label('worth'),
            RequirementReview.worth_sure.label('worth_sure'),
            RequirementReview.report_time.label('report_time'),
            RequirementReview.report_expect.label('report_expect'),
            RequirementReview.report_real.label('report_real'),
            Version.id.label('version_id'),
            Version.title.label('version_name'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),
            user_handler.id.label('handler_id'),
            user_handler.nickname.label('handler_name'),
            RequirementReview.parent_id.label('parent_id'),
            RequirementReview.review_status.label('review_status')
        )

    @classmethod
    def _query(cls):
        user_creator = aliased(User)
        user_modifier = aliased(User)
        return Review.query.outerjoin(
            user_creator, user_creator.id == Review.creator).outerjoin(
            user_modifier, user_modifier.id == Review.modifier).add_columns(
            Review.id.label('id'),
            Review.title.label('title'),
            Review.requirement_list.label('requirement_list'),
            func.date_format(Review.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            Review.project_id.label('project_id'),
            Review.version_id.label('version_id'),
            Review.reviewer.label('reviewer'),
            Review.status.label('status'),
            Review.attach.label('attach'),
            Review.comment.label('comment'),
            Review.weight.label('weight'),
            Review.review_status.label('review_status'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),
            user_modifier.id.label('modifier_id'),
            user_modifier.nickname.label('modifier_name'),

        )

    # 新建评审
    @classmethod
    def review_create(cls, title, requirement_list, project_id, version_id, creator, modifier, reviewer, status, attach,
                      comment, weight, review_status):
        try:
            creator = g.userid if g.userid else None
            reviewer_list = reviewer.split(',')
            reviewer = User.query.add_columns(User.nickname.label('nickname')).filter(User.id.in_(reviewer_list)).all()
            reviewer = [re.nickname for re in reviewer]
            req = ''
            for review in reviewer:
                req = req + review + ','
            c = Review(
                title=title,
                requirement_list=requirement_list,
                project_id=project_id,
                version_id=version_id,
                creator=creator,
                modifier=modifier,
                reviewer=req[:-1],
                status=Review.ACTIVE,
                attach=attach,
                comment=comment,
                weight=weight,
                review_status=1,
            )
            db.session.add(c)
            db.session.flush()
            requirement_list_ret = requirement_list.split(',')
            current_app.logger.info(requirement_list_ret)
            cls.requirement_review_create(c.id, requirement_list_ret)
            db.session.commit()
            board_config = Config.query.add_columns(Config.content.label('content')).filter(
                Config.module == 'tcloud',
                Config.module_type == 1).first()
            project = Project.query.add_columns(Project.name).filter(Project.id == project_id).first()
            project_name = ''
            if project:
                project_name = project.name
            if not title:
                title = '需求评审'
            text = '''[Tcloud - {}]需求评审已发起
项目: {}
参与者: {}
发起人: {}
URL: {}/project/{}/requirement/{}/review'''.format(title, project_name, req[:-1], g.nickname, board_config.content,
                                                   project_id, c.id)
            notification.send_notification(reviewer_list, text)
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    # @classmethod
    # def qyweixin_email(cls, user_ids, text, creator=None, send_type=None):
    #     is_wx = 0
    #     is_message = 0
    #     if not creator:
    #         creator = g.userid
    #     if not send_type:
    #         is_wx = 1
    #         is_message = 1
    #     if is_wx:
    #         result = cls.public_trpc.requests('post', '/public/wxmessage', body={'user_ids': user_ids, 'text': text})
    #         if result == 'success':
    #             current_app.logger.info('发送企业微信通知成功')
    #         else:
    #             current_app.logger.error('发送企业微信通知失败')
    #     if is_message:
    #         if cls.message_trpc.requests('post', '/message',
    #                                      body={'send_id': creator, 'rec_id': user_ids, 'content': text}):
    #             current_app.logger.info('发送站内信成功')
    #         else:
    #             current_app.logger.info('发送站内信失败')

    @classmethod
    def requirement_review_create(cls, review_id, requirement_id):
        try:
            for req in requirement_id:
                require = Requirement.query.get(req)
                re = RequirementReview(
                    review_id=review_id,
                    requirement_id=req,
                    title=require.title,
                    project_id=require.project_id,
                    version=require.version,
                    requirement_type=require.requirement_type,
                    creator=require.creator,
                    modifier=require.modifier,
                    handler=require.handler,
                    board_status=require.board_status,
                    status=require.status,
                    description=require.description,
                    priority=require.priority,
                    attach=require.attach,
                    comment=require.comment,
                    weight=require.weight,
                    parent_id=require.parent_id,
                    review_status=0,
                    jira_id=require.jira_id,
                    worth=require.worth,
                    report_time=require.report_time,
                    report_expect=require.report_expect,
                    report_real=require.report_real,
                    worth_sure=require.worth_sure,
                )
                db.session.add(re)
            # db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def review_modify(cls, review_id, comment, result):
        try:
            modifier = g.userid if g.userid else None
            req = Review.query.get(review_id)
            if not req:
                return 101
            req.comment = comment
            req.modifier = modifier
            req.review_status = 2
            for re in result['pass']:
                req = RequirementReview.query.get(int(re))
                req.review_status = 1
                db.session.add(req)
            for re in result['fail']:
                req = RequirementReview.query.get(int(re))
                req.review_status = 2
                db.session.add(req)
            db.session.add(req)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 106

    @classmethod
    def filter_query(cls):
        projectid = request.args.get('projectid')
        ret = cls._query().filter(Review.status != Review.DISABLE)
        ret = ret.filter(Review.project_id == projectid)

        return ret.order_by(desc(Review.id))

    @classmethod
    @transfer2jsonwithoutset(
        '?id|!title|!requirement_list|!project_id|!version_id|!creator_id|!creator_name|!modifier_id|!modifier_name|'
        '!reviewer|!status|!attach|!comment|!weight|!review_status|!creation_time', ispagination=True)
    def paginate_data(cls, page_size=None, page_index=None):
        query = cls.filter_query()
        count = query.count()
        if page_size and page_index:
            query = query.limit(int(page_size)).offset((int(page_index) - 1) * int(page_size))
        data = query.all()
        return data, count

    @classmethod
    @transfer2jsonwithoutset(
        '?id|!title|!requirement_list|!project_id|!version_id|!creator_id|!creator_name|!modifier_id|!modifier_name|'
        '!reviewer|!status|!attach|!comment|!weight|!review_status|!creation_time')
    def query_review_by_ids(cls, review_id):
        ret = cls._query().filter(Review.status != Review.DISABLE, Review.id == review_id).all()
        return ret

    @classmethod
    def query_review_by_id(cls, review_id):
        ret = cls.query_review_by_ids(review_id)
        if not ret:
            return 101, []
        requirement_detail = cls.query_require_by_id(review_id)
        child_requirement_detail = cls.query_child_require_by_id(review_id)
        temp_requirement_list = []
        for re in range(len(requirement_detail)):
            require_id = requirement_detail[re]['requirement_id']
            temp_requirement_list.append(require_id)
            requirement_detail[re]['parent_list'] = cls.look_up_chidren_requirement(review_id, require_id)
        ret[0]['requirement_detail'] = requirement_detail
        # ret.append({'requirement_detail': requirement_detail})
        for chre in range(len(child_requirement_detail)):
            if child_requirement_detail[chre]['parent_id'] not in temp_requirement_list:
                ret[0]['requirement_detail'].append(child_requirement_detail[chre])
        return 0, ret

    @classmethod
    @transfer2jsonwithoutset(
        '?id|!title|!requirement_id|!review_id|!review_status|!project_id|!version_id|!version_name|!creator_id|'
        '!creator_name|!handler_id|!handler_name|!creation_time|!modified_time|!board_status|!description|'
        '!comment|!priority|!requirement_type|!attach|!parent_id|!jira_id|!worth|!report_time|!report_expect|'
        '!report_real|!worth_sure')
    def query_require_by_id(cls, review_id):
        ret = cls._req_query().filter(RequirementReview.status != RequirementReview.DISABLE,
                                      RequirementReview.review_id == review_id,
                                      RequirementReview.parent_id == 0).order_by(
            desc(RequirementReview.id)).all()
        return ret

    @classmethod
    @transfer2jsonwithoutset(
        '?id|!title|!requirement_id|!review_id|!review_status|!project_id|!version_id|!version_name|'
        '!creator_id|!creator_name|!handler_id|!handler_name|!creation_time|!modified_time|!board_status|'
        '!description|!comment|!priority|!requirement_type|!attach|!parent_id|!jira_id|!worth|!report_time|'
        '!report_expect|!report_real|!worth_sure')
    def query_child_require_by_id(cls, review_id):
        ret = cls._req_query().filter(RequirementReview.status != RequirementReview.DISABLE,
                                      RequirementReview.review_id == review_id,
                                      RequirementReview.parent_id != 0).order_by(
            desc(RequirementReview.id)).all()
        return ret

    @classmethod
    @transfer2jsonwithoutset(
        '?id|!title|!requirement_id|!review_id|!review_status|!project_id|!version_id|!version_name|!creator_id|'
        '!creator_name|!creation_time|!modified_time|!board_status|!description|!comment|!priority|!requirement_type|'
        '!attach|!parent_id|!handler_id|!jira_id|!worth|!report_time|!report_expect|!report_real|!worth_sure')
    def look_up_chidren_requirement(cls, review_id, require_id):
        ret = cls._req_query().filter(RequirementReview.status != RequirementReview.DISABLE,
                                      RequirementReview.review_id == review_id,
                                      RequirementReview.parent_id == require_id).order_by(
            desc(RequirementReview.id)).all()
        return ret

    @classmethod
    def review_delete(cls, review_id):
        modifier = g.userid if g.userid else None
        req = Review.query.get(review_id)
        req.status = Review.DISABLE
        req.modifier = modifier
        db.session.add(req)
        db.session.commit()
        return 0

    @classmethod
    @transfer2jsonwithoutset('?requirement_id|!parent_id')
    def parent_list(cls, review_id):
        ret = cls._req_query().filter(RequirementReview.status != RequirementReview.DISABLE,
                                      RequirementReview.review_id == review_id).order_by(
            desc(RequirementReview.id)).all()
        return ret

    @classmethod
    @transfer2jsonwithoutset('?requirement_id')
    def son_list(cls, review_id, parent_id):

        ret = cls._req_query().filter(RequirementReview.status != RequirementReview.DISABLE,
                                      RequirementReview.review_id == review_id,
                                      RequirementReview.parent_id == parent_id).order_by(
            desc(RequirementReview.id)).all()
        return ret.requirement_list

    @classmethod
    @transfer2jsonwithoutset(
        '?id|!title|!requirement_id|!review_id|!review_status|!project_id|!version_id|!version_name|!creator_id|'
        '!creator_name|!creation_time|!modified_time|!board_status|!description|!comment|!priority|!requirement_type|'
        '!attach|!parent_id|!jira_id|!worth|!report_time|!report_expect|!report_real|!worth_sure')
    def query_review_status(cls, review_id, parent_id):
        ret = cls._req_query().filter(RequirementReview.status != RequirementReview.DISABLE,
                                      RequirementReview.review_id == review_id,
                                      RequirementReview.parent_id == parent_id).all()
        return ret

    @classmethod
    @transfer2jsonwithoutset(
        '?id|!title|!requirement_id|!review_id|!review_status|!project_id|!version_id|!version_name|!creator_id|'
        '!creator_name|!creation_time|!modified_time|!board_status|!description|!comment|!priority|!requirement_type|'
        '!attach|!parent_id|!jira_id|!worth|!report_time|!report_expect|!report_real|!worth_sure')
    def query_review_data(cls, review_id, requirement_id):
        ret = cls._req_query().filter(RequirementReview.status != RequirementReview.DISABLE,
                                      RequirementReview.review_id == review_id,
                                      RequirementReview.requirement_id == requirement_id).all()
        return ret
