from flask import current_app

from apps.project.models.boardconfig import BoardConfig
from library.api.db import db
from library.api.transfer import transfer2json
from public_config import BOARD_MAP


class BoardConfigBusiness(object):

    @classmethod
    def _query(cls):
        return BoardConfig.query.add_columns(
            BoardConfig.project_id.label('project_id'),
            BoardConfig.issue.label('issue'),
            BoardConfig.requirement.label('requirement'),
        )

    @classmethod
    @transfer2json('?project_id|!issue|!requirement')
    def get_by_project_id(cls, project_id):
        return cls._query().filter(BoardConfig.project_id == project_id).all()

    @classmethod
    def get(cls, project_id):
        result = cls.get_by_project_id(project_id)
        if result:
            return 0, cls.convert_config(result)
        else:
            return cls._create(project_id, cls.get_all_issues_keys(), cls.get_all_requirement_keys())

    @classmethod
    def convert_config(cls, result):
        requirement = result[0]['requirement']
        issue = result[0]['issue']
        requirement_dict = {k.strip(): BOARD_MAP['requirement'].get(int(k.strip())) for k in requirement.split(',')}
        issue_dict = {k.strip(): BOARD_MAP['issue'].get(int(k.strip())) for k in issue.split(',')}

        result[0]['requirement'] = requirement_dict
        requirement_list = requirement.split(',')
        # 处理老数据
        # if '3' in requirement_list and requirement_list[-1] != '3':
        #     requirement_list.remove('3')
        #     requirement_list.append('3')
        result[0]['requirement_sort'] = requirement_list

        result[0]['issue'] = issue_dict
        issue_list = issue.split(',')
        # if '5' in issue_list and issue_list[-1] != '5':
        #     issue_list.remove('5')
        #     issue_list.append('5')
        result[0]['issue_sort'] = issue_list

        del result[0]['project_id']
        return result

    @classmethod
    def _create(cls, project_id, issue, requirement):
        try:
            c = BoardConfig(
                project_id=project_id,
                issue=issue,
                requirement=requirement,
            )
            db.session.add(c)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)
        else:
            return 0, cls.get_all_config(issue, requirement)

    @classmethod
    def update(cls, project_id, issue, requirement):
        try:
            c = BoardConfig.query.filter(
                BoardConfig.project_id == project_id
            ).first()
            if '5' in issue:
                issue_list = issue.split(',')
                issue_list.sort()
                issue_list.remove('5')
                issue_list.append('5')
                issue = ','.join(issue_list)
            c.issue = issue
            if '3' in requirement:
                requirement_list = requirement.split(',')
                requirement_list.sort()
                requirement_list.remove('3')
                requirement_list.append('3')
                requirement = ','.join(requirement_list)
            c.requirement = requirement
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 101

    @classmethod
    def get_all_config(cls, issue, requirement):
        return [
            {
                'issue': BOARD_MAP.get('issue'),
                'issue_sort': issue.split(','),
                'requirement': BOARD_MAP.get('requirement'),
                'requirement_sort': requirement.split(','),
            }
        ]

    @classmethod
    def get_all_issues_keys(cls):
        all_issues_keys = [str(i) for i in BOARD_MAP.get('issue').keys() if i != 5]
        all_issues_keys.append('5')
        return ','.join(all_issues_keys)

    @classmethod
    def get_all_requirement_keys(cls):
        """
        因为要把3已拒绝放在最后，所以排个序
        :return: string
        """
        all_requirement_keys = [str(i) for i in BOARD_MAP.get('requirement').keys() if i != 3]
        all_requirement_keys.append('3')
        return ','.join(all_requirement_keys)
