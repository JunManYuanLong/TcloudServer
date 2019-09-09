import json
import time

import jenkins
from flask import request, current_app
from sqlalchemy import desc

from apps.extention.models.cidata import CiData
from apps.extention.models.cijob import CiJob
from apps.public.models.public import Config
from library.api.db import db
from library.api.transfer import transfer2json
from library.trpc import Trpc


class CiDataBusiness(object):
    @classmethod
    def _query(cls):
        return CiData.query.add_columns(
            CiData.id.label('id'),
            CiData.name.label('name'),
            CiData.case_count.label('case_count'),
            CiData.nextBuildNumber.label('nextBuildNumber'),
            CiData.status.label('status'),
            CiData.accuracy.label('accuracy'),
            CiData.description.label('description'),
        )

    @classmethod
    @transfer2json(
        '?id|!name|!case_count|!nextBuildNumber|!status|!accuracy|!description')
    def query_all_json(cls):
        return cls._query().filter(CiData.status == CiData.ACTIVE).all()

    @classmethod
    @transfer2json(
        '?id|!name|!case_count|!nextBuildNumber|!status|!accuracy|!description')
    def query_json_by_id(cls, ciid):
        return cls._query().filter(CiData.id == ciid, CiData.status == CiData.ACTIVE).all()

    @classmethod
    @transfer2json(
        '?id|!name|!case_count|!nextBuildNumber|!status|!accuracy|!description')
    def query_description_by_id(cls, ciid):
        return cls._query().filter(CiData.id == ciid, CiData.status == CiData.ACTIVE).all()

    @classmethod
    def create(cls, name, case_count, next_build_number, accuracy, description):
        try:
            ci = CiData(
                name=name,
                case_count=case_count,
                nextBuildNumber=next_build_number,
                accuracy=accuracy,
                description=description,
            )
            db.session.add(ci)
            db.session.commit()

            return 0, ci.id, ci.name
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def update(cls, id, name, case_count, next_build_number, accuracy, description):
        try:
            ci = CiData.query.get(id)
            ci.name = name
            ci.case_count = case_count
            ci.nextBuildNumber = next_build_number
            ci.accuracy = accuracy
            ci.description = description

            db.session.add(ci)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def delete(cls, id):
        try:
            ci = CiData.query.get(id)
            if ci is None:
                return 0
            ci.status = CiData.DISABLE
            db.session.add(ci)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)


class CiJobBusiness(object):
    public_trpc = Trpc('public')

    @classmethod
    def _query(cls):
        return CiJob.query.add_columns(
            CiJob.id.label('id'),
            CiJob.number.label('number'),
            CiJob.url.label('url'),
            CiJob.ci_id.label('ci_id'),
            CiJob.start_name.label('start_name'),
            CiJob.status.label('status'),
            CiJob.report.label('report'),
            CiJob.run_date.label('run_date'),
            CiJob.run_time.label('run_time'),
            CiJob.job_count.label('job_count'),
            CiJob.job_accuracy.label('job_accuracy'),
        )

    @classmethod
    @transfer2json(
        '?id|!number|!url|!ci_id|!start_name|!status|!report|!run_date|!run_time|!job_count|!job_accuracy')
    def query_all_json(cls):
        return cls._query().filter(CiJob.status == CiJob.ACTIVE).order_by(desc(CiJob.id)).all()

    @classmethod
    @transfer2json(
        '?id|!number|!url|!ci_id|!start_name|!status|!report|!run_date|!run_time|!job_count|!job_accuracy')
    def query_number_all(cls, ciid):
        return cls._query().filter(CiJob.status == CiJob.ACTIVE, CiJob.ci_id == ciid).all()

    @classmethod
    @transfer2json(
        '?id|!number|!url|!ci_id|!start_name|!status|!report|!run_date|!run_time|!job_count|!job_accuracy')
    def query_number_id(cls, number, ciid):
        return cls._query().filter(CiJob.status == CiJob.ACTIVE, CiJob.number == number, CiJob.ci_id == ciid).all()

    @classmethod
    @transfer2json(
        '?id|!number|!url|!ci_id|!start_name|!status|!report|!run_date|!run_time|!job_count|!job_accuracy')
    def query_json_by_id(cls, id, page_size, page_index):

        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        start_name = request.args.get('start_name')
        return cls._query().filter(CiJob.ci_id == id,
                                   CiJob.status == CiJob.ACTIVE, CiJob.run_date.between(start_time, end_time),
                                   CiJob.start_name.like('%{}%'.format(start_name))).order_by(desc(CiJob.id)).limit(
            int(page_size)).offset(
            int(page_index - 1) * int(page_size)).all()

    @classmethod
    def query_count(cls, id):
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        start_name = request.args.get('start_name')
        return CiJob.query.filter(CiJob.ci_id == id, CiJob.status == CiJob.ACTIVE,
                                  CiJob.run_date.between(start_time, end_time),
                                  CiJob.start_name.like('%{}%'.format(start_name))).count()

    @classmethod
    def create(cls, number, url, ci_id, start_name, report, run_date, run_time, job_count, job_accuracy):
        try:
            cijob = CiJob(
                number=number,
                url=url,
                ci_id=ci_id,
                start_name=start_name,
                report=report,
                run_date=run_date,
                run_time=run_time,
                job_count=job_count,
                job_accuracy=job_accuracy,
            )
            db.session.add(cijob)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def update(cls, id, number, url, ci_id, start_name, report, run_date, run_time, job_count, job_accuracy):
        try:
            cijob = CiJob.query.get(id)
            cijob.number = number
            cijob.url = url
            cijob.ci_id = ci_id
            cijob.start_name = start_name
            cijob.report = report
            cijob.run_date = run_date
            cijob.run_time = run_time
            cijob.job_count = job_count
            cijob.job_accuracy = job_accuracy

            db.session.add(cijob)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def delete(cls, id):
        try:
            cijob = CiJob.query.get(id)
            if cijob is None:
                return 0
            cijob.status = CiJob.DISABLE
            db.session.add(cijob)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def gain_jenkins_server(cls):

        jenkins_config = cls.public_trpc.requests('get', '/public/config', {'module': 'jenkins', 'module_type': 2})
        if not jenkins_config:
            return None
        run_dict = json.loads(jenkins_config)
        jenkins_server_url = run_dict['url']
        user_id = run_dict['user_id']
        api_token = run_dict['api_token']

        server = jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)

        return server

    @classmethod
    def job_update_data(cls, ciid, ciname, job_data, cijob_number_list, server):
        for i in range(0, len(job_data)):

            run_list = []
            queue_info = server.get_queue_info()
            if len(queue_info) > 0:
                for info_count in range(0, len(queue_info)):
                    if 'task' in queue_info[info_count] and 'name' in queue_info[info_count]['task']:
                        run_list.append(queue_info[info_count]['task']['name'])

            run_build_list = server.get_running_builds()
            for list_count in range(0, len(run_build_list)):
                if 'name' in run_build_list[list_count]:
                    run_list.append(run_build_list[list_count]['name'])

            if ciname in run_list:
                continue

            if job_data[i]['number'] and int(job_data[i]['number']) not in cijob_number_list:
                build_data = server.get_build_info(ciname, job_data[i]['number'])

                # 触发时间
                tss1 = build_data['timestamp'] / 1000
                tss1 = time.localtime(tss1)
                run_date = time.strftime("%Y-%m-%d %H:%M:%S", tss1)

                # 运行时长
                run_time = build_data['duration'] / 1000

                # 触发者
                name = 'timer'

                if (build_data and 'actions' in build_data and build_data['actions'] and 'causes' in
                        build_data['actions'][0] and build_data['actions'][0]['causes'] and len(
                            build_data['actions']) > 0 and len(build_data['actions'][0]['causes']) > 0):
                    if 'userName' in build_data['actions'][0]['causes'][0]:
                        name = build_data['actions'][0]['causes'][0]['userName']
                    else:
                        start_name = build_data['actions'][0]['causes'][0]['shortDescription']
                        start_name_list = start_name.split(' ')
                        if len(start_name_list) > 2:
                            name = start_name_list[2]
                report = ''

                job_count = 0
                job_accuracy = 0

                # 获取report
                logo_info = (server.get_build_console_output(ciname, job_data[i]['number']))

                if '/' in logo_info and '$$$$$$' in logo_info:

                    logo_info_list = logo_info.split('/')

                    time_content = logo_info_list[-1][0:10]

                    logo_data = logo_info.split('$$$$$$')

                    if len(logo_data) == 3:
                        logger_info = ((logo_data[1]).strip().encode("utf-8"))
                        logger_info = str(logger_info, 'utf-8')
                        logger_info = logger_info.replace("'", '"')

                        if 'testsRun' in logger_info and 'html' not in logger_info:
                            data_dict = json.loads(logger_info)
                            job_true_count = int(data_dict['successes'])
                            job_count = int(data_dict['testsRun'])
                            if job_true_count != 0 and job_count != 0:
                                job_accuracy = round(job_true_count / (job_count * 1.0), 4)

                                if time_content.isdigit():
                                    # file = "http://ctsssource.oss-cn-shanghai.aliyuncs.com/api_report/"
                                    file = current_app.config['CI_REPORT_FILE_ADRESS']
                                    time_array = time.localtime(int(time_content))
                                    report = file + time.strftime("%Y-%m-%d", time_array) + '/' + time_content + '.html'
                job_really_url = ''
                job_url = job_data[i]['url']
                job_url_list = job_url.split('job')
                if len(job_url_list) > 1:
                    ci_job_address = current_app.config['CI_JOB_ADDRESS']
                    # job_really_url = 'http://ci.automancloud.com/job' + job_url_list[1]
                    job_really_url = ci_job_address + job_url_list[1]
                cls.create(job_data[i]['number'], job_really_url, ciid, name, report, run_date, run_time, job_count,
                           job_accuracy)

    @classmethod
    def run(cls, project_id, run_list):

        run_dict, run_name_dict = CiJobBusiness.gain_run_dict(project_id)
        if len(run_dict) == 0 and len(run_dict) < len(run_list):
            return 102, [], 'empty'
        run_name_list = []
        for i in range(0, len(run_list)):
            run_name_list.append(run_dict[str(run_list[i])])
        if len(run_name_list) == 0:
            return 102, [], 'empty'

        server = CiJobBusiness.gain_jenkins_server()
        if not server:
            return 101, [], 'server 错误'
        # job_info = server.get_jobs()
        data = []
        run_build_list = server.get_running_builds()
        isexcute = False
        run_list = []
        for build_count in range(0, len(run_build_list)):
            if 'name' in run_build_list[build_count]:
                run_list.append(run_build_list[build_count]['name'])

        queue_info = server.get_queue_info()

        for info_count in range(0, len(queue_info)):
            if 'task' in queue_info[info_count] and 'name' in queue_info[info_count]['task']:
                run_list.append(queue_info[info_count]['task']['name'])

        for i in range(0, len(run_name_list)):
            if run_name_list[i] in run_list:
                isexcute = True
                # 判断是否正在执行
            data_dict_singel = {}

            if isexcute:
                data_dict_singel['isexcuting'] = True
                data_dict_singel['job'] = run_name_list[i]
                data_id = int(list(run_dict.keys())[list(run_dict.values()).index(run_name_list[i])])
                data_dict_singel['id'] = data_id
                data_dict_singel['name'] = run_name_dict[str(data_id)]

                data.append(data_dict_singel)
                # 若未执行则执行
            else:
                server.build_job(run_name_list[i])
                data_dict_singel['isexcuting'] = False
                data_dict_singel['job'] = run_name_list[i]
                data_id = int(list(run_dict.keys())[list(run_dict.values()).index(run_name_list[i])])
                data_dict_singel['id'] = data_id
                data_dict_singel['name'] = run_name_dict[str(data_id)]
                data.append(data_dict_singel)

        return 0, data, 'ok'

    @classmethod
    def gain_report(cls, project_id, run_list):

        run_dict, run_name_dict = CiJobBusiness.gain_run_dict(project_id)
        if len(run_dict) == 0 and len(run_dict) < len(run_list):
            return 102, [], 'empty'
        run_name_list = []
        for i in range(0, len(run_list)):
            run_name_list.append(run_dict[str(run_list[i])])
        if len(run_name_list) == 0:
            return 102, [], 'empty'

        server = CiJobBusiness.gain_jenkins_server()
        if not server:
            return 101, [], 'server 错误'
        job_info = server.get_jobs()

        run_build_list = []
        run_list = []
        queue_info = server.get_queue_info()
        if len(queue_info) > 0:
            for i in range(0, len(queue_info)):
                if 'task' in queue_info[i] and 'name' in queue_info[i]['task']:
                    run_list.append(queue_info[i]['task']['name'])

        run_build_list = server.get_running_builds()
        for i in range(0, len(run_build_list)):
            if 'name' in run_build_list[i]:
                run_list.append(run_build_list[i]['name'])

        isexcute = False

        run_list = list(set(run_list))

        data = []
        for m in range(0, len(job_info)):
            for i in range(0, len(run_name_list)):

                if run_name_list[i] in run_list:
                    isexcute = True

                if job_info[m]['fullname'] == run_name_list[i]:
                    # 判断是否正在执行
                    data_dict = {}
                    if isexcute:
                        data_dict['isexcuting'] = True
                        data_dict['url'] = ''
                        data_dict['job'] = run_name_list[i]
                        data_id = int(list(run_dict.keys())[list(run_dict.values()).index(run_name_list[i])])
                        data_dict['id'] = data_id
                        data_dict['name'] = run_name_dict[str(data_id)]

                        data.append(data_dict)
                    # 若未执行则执行
                    else:
                        number = server.get_job_info(job_info[m]['fullname'])['lastBuild']['number']
                        logo_info = (server.get_build_console_output(job_info[m]['fullname'], number))
                        if '/' in logo_info and '$$$$$$' in logo_info:
                            logo_info_list = logo_info.split('/')
                            time_content = logo_info_list[-1][0:10]
                            logo_data = logo_info.split('$$$$$$')
                            if time_content.isdigit():
                                file = "http://ctsssource.oss-cn-shanghai.aliyuncs.com/api_report/"
                                time_array = time.localtime(int(time_content))
                                report = file + time.strftime("%Y-%m-%d", time_array) + '/' + time_content + '.html'
                                data_dict['isexcuting'] = False
                                data_dict['url'] = report
                                data_dict['job'] = run_name_list[i]
                                data_id = int(list(run_dict.keys())[list(run_dict.values()).index(run_name_list[i])])
                                data_dict['id'] = data_id
                                data_dict['name'] = run_name_dict[str(data_id)]
                                data.append(data_dict)

                            else:
                                data_dict['isexcuting'] = False
                                data_dict['url'] = ''
                                data_dict['job'] = run_name_list[i]
                                data_id = int(list(run_dict.keys())[list(run_dict.values()).index(run_name_list[i])])
                                data_dict['id'] = data_id
                                data_dict['name'] = run_name_dict[str(data_id)]
                                data.append(data_dict)
                        else:
                            data_dict['isexcuting'] = False
                            data_dict['url'] = ''
                            data_dict['job'] = run_name_list[i]
                            data_id = int(list(run_dict.keys())[list(run_dict.values()).index(run_name_list[i])])
                            data_dict['id'] = data_id
                            data_dict['name'] = run_name_dict[str(data_id)]
                            data.append(data_dict)

        return 0, data, 'ok'

    @classmethod
    def gain_run_dict(cls, project_id):

        run_name_list = []
        run_job_dict = {}
        run_name_dict = {}

        jenkins_config = Config.query.add_columns(Config.content.label('content')).filter(
            Config.module == 'jenkins',
            Config.module_type == 1).first()
        run_dict = json.loads(jenkins_config.content)
        if str(project_id) in run_dict.keys():
            project_list = run_dict[str(project_id)]
            for i in range(0, len(project_list)):
                run_name_list.append(project_list[i]['job'])
                project_dict = {str(project_list[i]['id']): project_list[i]['job']}
                run_job_dict = run_job_dict.copy()
                run_job_dict.update(project_dict)

                project_name_dict = {str(project_list[i]['id']): project_list[i]['name']}
                run_name_dict = run_name_dict.copy()
                run_name_dict.update(project_name_dict)
        return run_job_dict, run_name_dict

    @classmethod
    def jobs_config_data(cls):

        jenkins_config = cls.public_trpc.requests('get', '/public/config', {'module': 'jenkins', 'module_type': 3})

        run_dict = json.loads(jenkins_config)

        jobs_list = run_dict['job']

        return jobs_list

    @classmethod
    def update_jenkins_data(cls):

        cidata_list = CiDataBusiness.query_all_json()
        cidata_name_list = []
        for i in range(0, len(cidata_list)):
            cidata_name_list.append("{}".format(cidata_list[i]['name']))

        server = CiJobBusiness.gain_jenkins_server()
        if not server:
            return 101, [], 'server 错误'

        job_info = cls.jobs_config_data()

        # ci数据更新
        for m in range(0, len(job_info)):

            if job_info[m] and server.job_exists(job_info[m]):
                job_name = job_info[m]
                job_true_count = 0
                job_count = 0
                builds = server.get_job_info(job_name, depth=0, fetch_all_builds=False)['builds']

                for j in range(0, len(builds)):
                    # 一共有多少个case
                    logo_info = (server.get_build_console_output(job_name, builds[j]['number']))

                    if '$$$$$$' in logo_info:
                        logo_data = logo_info.split('$$$$$$')
                        if len(logo_data) == 3:
                            logger_info = ((logo_data[1]).strip().encode("utf-8"))
                            logger_info = str(logger_info, 'utf-8')
                            logger_info = logger_info.replace("'", '"')
                            if 'testsRun' in logger_info and 'html' not in logger_info:
                                data_dict = json.loads(logger_info)
                                job_true_count = job_true_count + data_dict['successes']
                                job_count = job_count + data_dict['testsRun']
                # 增加正确率
                if job_count == 0:
                    accuracy = 0
                else:
                    accuracy = round(job_true_count / (job_count * 1.0), 4)
                # 下一次执行的number
                next_build_number = server.get_job_info(job_name, depth=0, fetch_all_builds=False)['nextBuildNumber']

                # job描述
                job_config = server.get_job_config(job_name)
                root = job_config.split('description')
                description = 'jenkins'
                if len(root) > 1:
                    description = root[1].strip('>').strip('</')

                if job_info[m] not in cidata_name_list:

                    code, ciid, ciname = CiDataBusiness.create(
                        job_name, job_count, next_build_number, accuracy, description)

                    cijob_number_list = []
                    cijob_all_data = CiJobBusiness.query_number_all(int(ciid))

                    for j in range(0, len(cijob_all_data)):
                        cijob_number_list.append(int(cijob_all_data[j]['number']))

                    if code == 0:
                        builds = sorted(builds, key=lambda e: e.__getitem__('number'))
                        ciname = "{}".format(ciname)
                        CiJobBusiness.job_update_data(ciid, ciname, builds, cijob_number_list, server)
                if job_info[m] in cidata_name_list:
                    ciid = 1
                    for id_count in range(0, len(cidata_list)):
                        if job_info[m] == "{}".format(cidata_list[id_count]['name']):
                            ciid = cidata_list[id_count]['id']
                    CiDataBusiness.update(ciid, job_name, job_count, next_build_number, accuracy, description)

        for mn in range(0, len(cidata_list)):
            ciname = "{}".format(cidata_list[mn]['name'])
            if ciname in job_info and server.job_exists(ciname):

                cijob_number_list_info = []

                cijob_all_data = CiJobBusiness.query_number_all(int(cidata_list[mn]['id']))

                for j in range(0, len(cijob_all_data)):
                    cijob_number_list_info.append(int(cijob_all_data[j]['number']))

                builds_info = server.get_job_info(ciname)['builds']

                builds_info = sorted(builds_info, key=lambda e: e.__getitem__('number'))

                builds_info_really = []

                for i in range(0, len(builds_info)):
                    if builds_info[i]['number'] not in cijob_number_list_info:
                        builds_info_really.append(builds_info[i])

                if len(builds_info_really) == 0:
                    continue

                CiJobBusiness.job_update_data(int(cidata_list[mn]['id']), ciname,
                                              builds_info_really, cijob_number_list_info, server)
