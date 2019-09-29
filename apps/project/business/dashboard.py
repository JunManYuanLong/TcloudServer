from apps.project.business.cases import CaseBusiness
from apps.project.business.issue import IssueDashBoardBusiness
from apps.project.business.tasks import TaskDashBoardBusiness
from library.trpc import Trpc


class DashboardBusiness(object):
    user_trpc = Trpc('auth')

    @classmethod
    def team_work_dashboard(cls, begin_date, end_date):
        testers = cls.user_trpc.requests('get', '/user/role/3')
        exc_case_info_list = TaskDashBoardBusiness.task_case_all_tester_dashboard(
            begin_date, end_date, testers=testers)
        create_issue_info_list = IssueDashBoardBusiness.issue_all_tester_dashboard(
            begin_date, end_date, testers=testers)
        create_case_info_list = CaseBusiness.case_all_tester_dashboard(
            begin_date, end_date, testers=testers)
        exc_case_info_list.sort(key=lambda z: z['userid'])
        create_issue_info_list.sort(key=lambda x: x['userid'])
        create_case_info_list.sort(key=lambda y: y['userid'])
        results = []
        for index in range(len(exc_case_info_list)):
            result = dict(
                userid=exc_case_info_list[index].get('userid'),
                nickname=exc_case_info_list[index].get('nickname'),
                picture=exc_case_info_list[index].get('picture'),
                exc_cases=exc_case_info_list[index].get('info'),
                submit_issues=create_issue_info_list[index].get('info'),
                create_cases=create_case_info_list[index].get('info'))
            results.append(result)
        return results

    @classmethod
    def team_case_issue_dashboard(cls, project_id, begin_date, end_date):
        testers = cls.user_trpc.requests('get', '/user/projectandrole', query={'project_id': project_id, 'role_id': 3})
        data_temp = {}
        for tester in testers:
            userid = int(tester.get('userid'))
            nickname = tester.get('nickname')
            data_temp[userid] = dict(
                userid=userid,
                nickname=nickname,
                issue_count=0,
                case_count=0
            )
        data_temp = IssueDashBoardBusiness.issue_all_tester_dashboard_for_project(
            data_temp, project_id, begin_date, end_date)
        data_temp = CaseBusiness.case_all_tester_dashboard_for_project(
            data_temp, project_id, begin_date, end_date)
        return list(data_temp.values())
