from flask import request, current_app
from sqlalchemy import desc, func

from apps.auth.models.users import User, UserBindProject
from apps.project.business.dashboard import DashboardBusiness
from apps.project.models.issue import Issue
from apps.project.models.project import Project
from apps.project.models.requirement import Requirement
from apps.project.models.tasks import TaskCase, Task
from apps.project.models.version import Version
from library.api.db import db
from library.api.exceptions import SaveObjectException, CannotFindObjectException
from library.api.render import row2list
from library.api.transfer import transfer2json, slicejson, transfer2jsonwithoutset
from library.trpc import Trpc


class ProjectBusiness(object):
    user_trpc = Trpc('auth')

    @classmethod
    def _query(cls):
        return Project.query.outerjoin(
            UserBindProject, UserBindProject.project_id == Project.id).outerjoin(
            User, User.id == UserBindProject.user_id).add_columns(
            Project.id.label('id'),
            Project.name.label('name'),
            Project.description.label('description'),
            Project.weight.label('weight'),
            Project.status.label('status'),
            Project.logo.label('logo'),
            User.id.label('user_id'),
            User.nickname.label('nickname'),
        )

    @classmethod
    @slicejson(['user|id|nickname|user_id|nickname'])
    @transfer2jsonwithoutset('?id|!name|!description|!status|!weight|!logo|@user_id|@nickname')
    def query_all_json(cls):
        userid = request.args.get('userid')
        ret = cls._query().filter(Project.status == Project.ACTIVE)
        if userid:
            ret = ret.filter(UserBindProject.user_id == userid)
        ret = ret.order_by(
            desc(Project.weight)).order_by(Project.id).all()

        return ret

    @classmethod
    @slicejson(['user|id|nickname|user_id|nickname'])
    @transfer2json('?id|!name|!description|!status|!weight|!logo|@user_id|@nickname')
    def query_json_by_id(cls, id):
        return cls._query().filter(Project.id == id,
                                   Project.status == Project.ACTIVE).order_by(
            desc(Project.weight)).all()

    @classmethod
    def create_new_project(cls, name, description, logo):
        ret = Project.query.filter_by(name=name, status=Project.ACTIVE).first()
        if ret:
            raise SaveObjectException('存在相同名称的项目')

        p = Project(
            name=name,
            description=description,
            logo=logo,
        )
        db.session.add(p)
        db.session.commit()
        return 0, None

    @classmethod
    def modify(cls, id, name, description, weight, logo):
        ret = Project.query.filter_by(name=name,
                                      status=Project.ACTIVE).filter(Project.id != id).first()
        if ret:
            raise SaveObjectException('存在相同名称的项目')

        project = Project.query.get(id)
        if not project:
            raise CannotFindObjectException

        if project.status == Project.ACTIVE:
            try:
                project.name = name
                project.description = description
                project.weight = weight
                project.logo = logo
                db.session.add(project)
                db.session.commit()
                return 0, None
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(str(e))
                return 102, str(e)
        else:
            return 101, "The Project's Status is DISABLE!"

    @classmethod
    def close_project(cls, id):
        project = Project.query.get(id)
        project.status = Project.DISABLE
        db.session.add(project)
        db.session.commit()
        return 0

    @classmethod
    def bind_users(cls, pid, userids):
        try:
            [db.session.delete(item) for item in UserBindProject.query.filter_by(project_id=pid).all()]
            [db.session.add(UserBindProject(user_id=uid, project_id=pid)) for uid in userids]
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def detach_users(cls, pid, userids):
        try:
            [db.session.delete(item) for item in UserBindProject.query.filter_by(project_id=pid, user_id=userids).all()]
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def add_users(cls, pid, userids):
        try:
            [db.session.add(UserBindProject(user_id=uid, project_id=pid)) for uid in userids]
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def detach_users_all(cls, userids):
        try:
            [db.session.delete(item) for item in UserBindProject.query.filter_by(user_id=userids).all()]
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def index(cls, id):
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        project_id = id
        tester_data = DashboardBusiness.team_case_issue_dashboard(project_id, start_time, str(end_time))
        # 需求总数随版本的趋势图
        requirement = Requirement.query.outerjoin(
            Version, Version.id == Requirement.version).add_columns(
            Requirement.version.label('version_id'),
            Version.title.label('version_title'),
            func.count('*').label('count')
        ).filter(
            Requirement.project_id == id, Requirement.status != Requirement.DISABLE,
            Version.status != Version.DISABLE, Requirement.parent_id == 0
        )
        # issue总数随版本的趋势图
        issue = Issue.query.outerjoin(
            Version, Version.id == Issue.version).add_columns(
            Issue.version.label('version_id'),
            Version.title.label('version_title'),
            func.count('*').label('count')
        ).filter(
            Issue.project_id == id, Issue.status != Issue.DISABLE, Version.status != Version.DISABLE
        )
        # issue打开数随版本的趋势图
        issue_open = Issue.query.outerjoin(
            Version, Version.id == Issue.version).add_columns(
            Issue.version.label('version_id'),
            func.count('*').label('count')
        ).filter(
            Issue.project_id == id, Issue.status != Issue.DISABLE, Issue.handle_status != 4,
            Version.status != Version.DISABLE
        )
        # task总数随版本的趋势图
        task = Task.query.outerjoin(
            Version, Version.id == Task.version).add_columns(
            Task.version.label('version_id'),
            Version.title.label('version_title'),
            func.count('*').label('count')
        ).filter(
            Task.project_id == id, Task.status != Task.DISABLE, Version.status != Version.DISABLE)
        taskcase = TaskCase.query.outerjoin(
            Version, Version.id == TaskCase.version).add_columns(
            TaskCase.version.label('version_id'),
            Version.title.label('version_title'),
            func.count('*').label('count')
        ).filter(
            TaskCase.project_id == id, TaskCase.status != TaskCase.DISABLE, Version.status != Version.DISABLE
        )
        # issue的状态分布
        issue_status_ret = Issue.query.outerjoin(
            Version, Version.id == Issue.version).add_columns(
            Issue.handle_status.label('handle_status'),
            func.count('*').label('count')
        ).filter(
            Issue.project_id == id, Issue.status != Issue.DISABLE, Version.status != Version.DISABLE
        )

        # issue的rank分布
        issue_rank_ret = Issue.query.outerjoin(
            Version, Version.id == Issue.version).add_columns(
            Issue.rank.label('rank')
        ).filter(
            Issue.project_id == id, Issue.status != Issue.DISABLE, Version.status != Version.DISABLE
        )

        # 每天新建和关闭的issue总数
        create_count = Issue.query.add_columns(
            func.date_format(Issue.creation_time, "%Y-%m-%d").label('creation_time'),
            func.count('*').label('count')
        ).filter(
            Issue.project_id == id, Issue.status != Issue.DISABLE
        )
        finish_count = Issue.query.add_columns(
            func.date_format(Issue.modified_time, "%Y-%m-%d").label('modified_time'),
            func.count('*').label('count')
        ).filter(
            Issue.project_id == id, Issue.status != Issue.DISABLE
        )

        # 根据时间过滤数据
        if start_time and end_time:
            requirement = requirement.filter(Version.start_time.between(start_time, end_time + " 23:59:59"))
            issue = issue.filter(Version.start_time.between(start_time, end_time + " 23:59:59"))
            issue_open = issue_open.filter(Version.start_time.between(start_time, end_time + " 23:59:59"))
            task = task.filter(Version.start_time.between(start_time, end_time + " 23:59:59"))
            taskcase = taskcase.filter(Version.start_time.between(start_time, end_time + " 23:59:59"))
            issue_status_ret = issue_status_ret.filter(Issue.creation_time.between(start_time, end_time + " 23:59:59"))
            issue_rank_ret = issue_rank_ret.filter(Version.start_time.between(start_time, end_time + " 23:59:59"))
            create_count = create_count.filter(
                Issue.creation_time.between(start_time, end_time + " 23:59:59")
            )
            finish_count = finish_count.filter(
                Issue.handle_status == 4,
                Issue.modified_time.between(start_time, end_time + " 23:59:59")
            )

        requirement = requirement.group_by(Requirement.version).order_by(desc(Version.id)).all()
        issue = issue.group_by(Issue.version).order_by(desc(Version.id)).all()
        issue_open = issue_open.group_by(Issue.version).order_by(desc(Version.id)).all()
        task = task.group_by(Task.version).order_by(desc(Version.id)).all()
        taskcase = taskcase.group_by(TaskCase.version).all()
        issue_status_ret = issue_status_ret.group_by(Issue.handle_status).all()
        # issue_rank_ret = issue_rank_ret.group_by(Issue.version).order_by(desc(Version.id)).all()
        issue_rank_ret = issue_rank_ret.order_by(desc(Version.id)).all()

        # 计算总数
        requirement_sum = sum(r.count for r in requirement)
        task_sum = sum(r.count for r in task)
        taskcase_sum = sum(r.count for r in taskcase)
        issue_sum = sum(r.count for r in issue)

        # 计算rank的总值
        issue_count = []
        issue_rank = []
        issue_all_rank = []
        temp = 0
        for i in range(0, len(issue)):
            issue_count.append(int(issue[i].count))

        for i in range(0, len(issue_rank_ret)):
            if isinstance(issue_rank_ret[i].rank, int):
                issue_rank.append(int(issue_rank_ret[i].rank))
            else:
                issue_rank.append(0)

        for i in range(0, len(issue_count)):
            sumcount = 0
            for j in range(temp, temp + issue_count[i]):
                if j < len(issue_rank):
                    sumcount = sumcount + issue_rank[j]
                else:
                    sumcount = 0
            temp = j + 1
            issue_all_rank.append(sumcount)

        # 处理汇总数据
        issue_status = [dict(i) for i in map(lambda x: zip(('handle_status', 'count'), x),
                                             zip([i.handle_status for i in issue_status_ret],
                                                 [i.count for i in issue_status_ret]))]
        requirement_info = [dict(i) for i in map(lambda x: zip(('version_id', 'version_title', 'count'), x),
                                                 zip([i.version_id for i in requirement],
                                                     [i.version_title for i in requirement],
                                                     [i.count for i in requirement]))]
        task_info = [dict(i) for i in map(lambda x: zip(('version_id', 'version_title', 'count'), x),
                                          zip([i.version_id for i in task], [i.version_title for i in task],
                                              [i.count for i in task]))]
        issue_info = [dict(i) for i in map(lambda x: zip(('version_id', 'version_title', 'count'), x),
                                           zip([i.version_id for i in issue], [i.version_title for i in issue],
                                               [i.count for i in issue]))]
        issue_open_info = [dict(i) for i in map(lambda x: zip(('version_id', 'open'), x),
                                                zip([i.version_id for i in issue_open], [i.count for i in issue_open]))]

        for i in range(len(issue_info)):
            issue_info[i]['open'] = 0
            for a in range(len(issue_open_info)):
                if int(issue_open_info[a]['version_id']) == int(issue_info[i]['version_id']):
                    issue_info[i]['open'] = issue_open_info[a]['open']
            if len(issue_info) == len(issue_all_rank):
                issue_info[i]['rank'] = issue_all_rank[i]
            else:
                issue_info[i]['rank'] = 0

        create_count = create_count.group_by(func.date_format(Issue.creation_time, "%Y-%m-%d")).all()
        create_issue_count = row2list(create_count)
        finish_count = finish_count.group_by(func.date_format(Issue.modified_time, "%Y-%m-%d")).all()
        finish_issue_count = row2list(finish_count)

        detail = [
            dict(
                requirement_sum=requirement_sum,
                issue_sum=issue_sum,
                task_sum=task_sum,
                requirement_info=requirement_info,
                issue_info=issue_info,
                task_info=task_info,
                issue_status=issue_status,
                taskcase_sum=taskcase_sum,
                tester_data=tester_data,
                create_issue_count=create_issue_count,
                finish_issue_count=finish_issue_count
            )
        ]
        return detail
