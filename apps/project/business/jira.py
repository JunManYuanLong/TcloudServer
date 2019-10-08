import json
import traceback

from flask import current_app, request
from jira import Issue
from sqlalchemy import func

from apps.project.business.requirement import RequirementBusiness
from apps.project.business.version import VersionBusiness
from apps.project.extentions import jira
from apps.project.models.jira import Jira
from apps.project.models.project import Project
from apps.project.models.requirement import Requirement
from apps.project.models.version import Version
from library.api.db import db
from library.api.exceptions import CreateObjectException, CannotFindObjectException
from library.api.transfer import transfer2json
from library.trpc import Trpc


class JiraBusiness(object):
    user_trpc = Trpc('auth')
    flow_trpc = Trpc('flow')

    @classmethod
    def _query(cls):
        return Jira.query.add_columns(
            Jira.id.label('id'),
            Jira.params.label('params'),
            Jira.result.label('result'),
            Jira.key_id.label('key_id'),
            Jira.key_type.label('key_type'),
            func.date_format(Jira.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(Jira.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
        )

    @classmethod
    @transfer2json(
        '?id|!params|!creation_time|!modified_time|!result|!key_id|!key_type'
    )
    def query_all_json(cls, page_size, page_index):
        ret = cls._query().limit(page_size).offset((page_index - 1) * page_size).all()
        return ret

    @classmethod
    def query_all_count(cls):
        ret = cls._query().count()
        return ret

    @classmethod
    @transfer2json(
        '?id|!params|!creation_time|!modified_time|!result|!key_id|!key_type'
    )
    def query_json_by_id(cls, id):
        return cls._query().filter(
            Jira.id == id).all()

    @classmethod
    def create(cls, params, result, key_id, key_type):
        try:
            t = Jira(
                params=params,
                result=result,
                key_type=key_type,
                key_id=key_id,
            )
            db.session.add(t)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            raise CreateObjectException(str(e))

    @classmethod
    def get_version_by_title(cls, issue, project_id):
        version_title = issue.fields.fixVersions[0].name if issue.fields.fixVersions else None
        if version_title is None:
            # raise CannotFindObjectException(f'issue {issue} does not have fixVersion ! please check the issue !')
            current_app.logger.warning(f'issue {issue} does not have fixVersion ! please check the issue !')
            return None
        version = Version.query.filter(Version.title == version_title,
                                       Version.project_id == project_id).first()
        if version:
            version_id = version.id
        else:

            fix_version = jira.version(issue.fields.fixVersions[0].id)
            start_time = fix_version.startDate if fix_version and hasattr(fix_version, "startDate") else None
            end_time = fix_version.releaseDate if fix_version and hasattr(fix_version, "releaseDate") else None
            VersionBusiness.version_create(title=version_title,
                                           project_id=project_id,
                                           start_time=start_time,
                                           end_time=end_time,
                                           description="jira create",
                                           creator=1,)  # 默认的 版本创建人 1
            version_id = cls.get_version_by_title(issue, project_id)
        return version_id

    @classmethod
    def get_priority(cls, issue):
        priority_map = {
            '紧急': 0, '重要': 1, '次要': 2, '微小': 3
        }
        if hasattr(issue.fields.priority, 'name') and issue.fields.priority.name:
            return priority_map.get(issue.fields.priority.name, 3)

    @classmethod
    def get_user(cls, wxemail):
        user = cls.user_trpc.requests('get', '/user/userinfo/wxemail', query={'email': wxemail})
        if user:
            return user[0].get('userid')
        current_app.logger.warning(f'tcloud not found the user with wxemail {wxemail}')
        return None

    @classmethod
    def get_handler(cls, issue):
        handler = issue.fields.assignee
        if handler and hasattr(handler, 'emailAddress') and handler.emailAddress:
            return cls.get_user(handler.emailAddress)
        else:
            current_app.logger.warning(f'issue {issue} not have assignee {handler} or assignee not have emailAddress')
            return None

    @classmethod
    def get_creator(cls, issue):
        creator = issue.fields.creator
        if creator and hasattr(creator, 'emailAddress') and creator.emailAddress:
            return cls.get_user(creator.emailAddress)
        else:
            current_app.logger.warning(f'issue {issue} not have reporter {creator} or reporter not have emailAddress')
            return None

    @classmethod
    def get_modifier(cls, modifier_name):
        return cls.get_user(modifier_name)

    @classmethod
    def get_project(cls, issue):
        project = issue.fields.project
        if project and hasattr(project, 'name') and project.name:
            project_in_tc = Project.query.filter(Project.name == project.name).first()
            if project_in_tc:
                return project_in_tc.id
            else:
                raise CannotFindObjectException(f'project {project} not found in system!')
        else:
            raise CannotFindObjectException(f'project {project} not have name property!')

    @classmethod
    def get_status(cls, issue):
        return 0

    @classmethod
    def get_worth(cls, issue):
        worth_map = {
            "高价值需求": 1, "非高价值需求": 2
        }
        worth = None
        if hasattr(issue.fields, "customfield_10812") and issue.fields.customfield_10812 is not None:
            worth = issue.fields.customfield_10812.value
        else:
            for field in dir(issue.fields):
                issue_field = getattr(issue.fields, field)
                if (field.startswith('customfield_') and hasattr(issue_field, 'value') and
                        issue_field.value in ['高价值需求', '非高价值需求']):
                    worth = issue_field.value
                    break
        if worth:
            return worth_map.get(worth)
        else:
            current_app.logger.warning(f'issue {issue} not have worth infos, so make worth to 非高价值需求')
            return 2

    @classmethod
    def issue_to_requirement_fields(cls, issue: Issue, modifier=None):
        project_id = cls.get_project(issue)
        return dict(
            title=issue.fields.summary,
            project_id=project_id,
            version=cls.get_version_by_title(issue, project_id),
            handler=cls.get_handler(issue),
            priority=cls.get_priority(issue),
            requirement_type=None,
            attach="{\"images\":[],\"files\":[],\"videos\":[]}",
            board_status=cls.get_status(issue),
            description=issue.fields.description,
            comment=None,
            jira_id=issue.key,
            worth=cls.get_worth(issue),
            report_time=None,
            report_expect=None,
            report_real=None,
            worth_sure=None,
            case_ids=None,
            expect_time=None,
            creator=cls.get_creator(issue),
            modifier=cls.get_modifier(modifier) if modifier is not None else None,
            tag=None,
        )

    @classmethod
    def requirement_create_handler(cls, issue):
        requirement_dict = cls.issue_to_requirement_fields(issue)
        params = []
        for key in ['title', 'project_id', 'version', 'handler', 'priority', 'requirement_type', 'attach',
                    'board_status', 'description', 'comment', 'jira_id', 'worth', 'report_time', 'report_expect',
                    'report_real', 'worth_sure', 'case_ids', "tag", "expect_time", 'creator']:
            value = requirement_dict.get(key)
            params.append(value)
        return RequirementBusiness.requirement_create(*params)

    @classmethod
    def requirement_update_handler(cls, requirement, issue, modifier):
        requirement_dict = cls.issue_to_requirement_fields(issue, modifier)
        params = []
        for key in ["title", "project_id", "version", "board_status", "handler", "description", "comment",
                    "priority", "requirement_type", "attach", "parent_id", "jira_id", "worth", "report_time",
                    "report_expect", "report_real", "worth_sure", "case_ids", "tag", "expect_time", "creator",
                    "modifier", ]:
            value = requirement_dict.get(key)
            if value is None:
                params.append(getattr(requirement, key, None))
            else:
                params.append(value)
        return RequirementBusiness.requirement_modify(requirement.id, *params)

    @classmethod
    def requirement_handler(cls, key):
        jira_result = None
        requirement_id = None
        user_id = request.args.get('user_id', '')
        user_key = request.args.get('user_key', '')
        try:
            issues = jira.search_issues(f'key={key}')
            if issues:
                issue = issues[0]
                requirement = Requirement.query.filter(Requirement.jira_id == str(issue)).first()
                if requirement:
                    cls.requirement_update_handler(requirement, issue, user_key)
                    requirement_id = requirement.id
                else:
                    rev = cls.requirement_create_handler(issue)
                    current_app.logger.info(rev)
                    requirement = Requirement.query.filter(Requirement.jira_id == str(issue)).first()
                    requirement_id = requirement.id
            else:
                jira_result = f'{user_id} {user_key} - jira cannot found issue with key : {key}'
                raise CannotFindObjectException(jira_result)

            jira_result = f"{user_id} {user_key} - {key} success"
            return 0
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            jira_result = f'{user_id} {user_key} - {key} - {str(e)}'
            raise e
        finally:
            cls.create(key, jira_result, requirement_id, Jira.KEY_MAP.get('requirement'))

    @classmethod
    def get_requirement_by_jira_key(cls, jira_key):
        requirement = Requirement.query.filter(Requirement.jira_id == jira_key).first()
        return requirement

    @classmethod
    def get_assemble_type(cls, issue):
        assemble_map = {
            "客户端": 1,
            "H5&服务端": 2,
            "Skiptest": 3,
            "hotfix": 4,
            "hotfix(需QA验证)": 5,
        }
        assemble = None
        if hasattr(issue.fields, "customfield_10826") and issue.fields.customfield_10826 is not None:
            assemble = issue.fields.customfield_10826.value
        else:
            for field in dir(issue.fields):
                issue_field = getattr(issue.fields, field)
                if (field.startswith('customfield_') and hasattr(issue_field, 'value') and
                        issue_field.value in list(assemble_map.keys())):
                    assemble = issue_field.value
                    break
        if assemble:
            return assemble_map.get(assemble, 1)
        else:
            current_app.logger.warning(f'issue {issue} not have assemble infos, so make assemble to H5&服务端')
            return 2

    @classmethod
    def get_platform(cls, issue):
        platform_map = {
            "后端": 1,
            "PHP": 2,
            "APP": 3,
            "H5": 4,
            "微信商城": 5,
            "小程序": 6
        }
        platform = None
        if hasattr(issue.fields, "customfield_10827") and issue.fields.customfield_10827 is not None:
            platform = [platform_map.get(test.value) for test in issue.fields.customfield_10827]
        else:
            for field in dir(issue.fields):
                issue_field = getattr(issue.fields, field)
                if (field.startswith('customfield_') and hasattr(issue_field, 'value') and
                        issue_field.value in list(platform_map.keys())):
                    platform = [platform_map.get(test.value) for test in issue_field.value]
                    break
        if platform:
            return platform
        else:
            current_app.logger.warning(f'issue {issue} not have platform infos, so make platform to [后端]')
            return [1]

    @classmethod
    def get_dependence(cls, issue):
        dependence = None
        if hasattr(issue.fields, "customfield_10829") and issue.fields.customfield_10829 is not None:
            dependence = issue.fields.customfield_10829
        else:
            current_app.logger.warning(f'issue {issue} not have dependence infos, so make platform to ""')
            dependence = ""
        return dependence

    @classmethod
    def make_comment(cls, requirement):
        if requirement is None:
            return ""
        comment = [{
            "id": requirement.id,
            "title": requirement.title,
            "jira_id": requirement.jira_id
        }]
        return json.dumps(comment)

    @classmethod
    def flow_handler(cls, key):
        requirement = cls.get_requirement_by_jira_key(key)
        if not requirement:
            cls.requirement_handler(key)
            requirement = cls.get_requirement_by_jira_key(key)

        jira_result = None
        user_id = request.args.get('user_id', '')
        user_key = request.args.get('user_key', '')
        try:
            issues = jira.search_issues(f'key={key}')
            if issues:
                issue = issues[0]
                assmble_type = cls.get_assemble_type(issue)
                handler = cls.get_handler(issue)
                creator = cls.get_creator(issue)
                if assmble_type == 1:
                    jira_result = f'{user_id} {user_key} - flow would not create because of assmble_type is 1: {key}'
                    return
                data = {
                    "name": f'{key} - {issue.fields.summary}',
                    "flow_type": 1,
                    "user_test": [cls.get_user("wuliping@innotechx.com")],
                    "requirement_list": str(requirement.id),
                    "flow_assemble_id": cls.get_assemble_type(issue),
                    "project_id": cls.get_project(issue),
                    "user_dev": [handler] if handler else [],
                    "user_owner": [handler] if handler else [],
                    "user_prod": [creator] if creator else [],
                    "platform": cls.get_platform(issue),
                    "dependence": cls.get_dependence(issue),
                    "comment": cls.make_comment(requirement),
                    "jira_id": key,
                    "creator": cls.get_creator(issue)
                }
            else:
                jira_result = f'{user_id} {user_key} - jira cannot found issue with key : {key}'
                raise CannotFindObjectException(jira_result)
            response = cls.flow_trpc.requests('post', '/flow/', body=data)
            if isinstance(response, dict):
                if response.get('code') == 0:
                    jira_result = f"{user_id} {user_key} - {key} success"
                else:
                    jira_result = f"{user_id} {user_key} - {key} {response.get('message', 'nothing in message')}"
            else:
                jira_result = f"{user_id} {user_key} - {key} unknown!"
            return 0
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            jira_result = f'{user_id} {user_key} - {key} - {str(e)}'
            raise e
        finally:
            cls.create(key, jira_result, requirement.id, Jira.KEY_MAP.get('flow'))