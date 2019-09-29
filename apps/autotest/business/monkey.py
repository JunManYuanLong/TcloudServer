#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import traceback
from datetime import datetime

import jenkins
from flask import current_app
from sqlalchemy import desc, func

from apps.autotest.business.performance import PerformanceTestBusiness
from apps.autotest.models.monkey import (
    Monkey, MonkeyErrorLog, MonkeyDeviceStatus, MonkeyPackage, MonkeyReport, MonkeyDeviceUsing)
from apps.tcdevices.models.tcDevices import TcDevicesnInfo
from library.api.db import db
from library.api.exceptions import (
    CreateObjectException, SaveObjectException, OperationFailedException,
    RemoveObjectException, CannotFindObjectException,
)
from library.api.transfer import transfer2json
from library.trpc import Trpc

user_trpc = Trpc('auth')


class MonkeyBusiness(object):

    @classmethod
    def _query(cls):
        return Monkey.query.add_columns(
            Monkey.id.label('id'),
            Monkey.app_name.label('app_name'),
            Monkey.app_version.label('app_version'),
            Monkey.download_app_status.label('download_app_status'),
            Monkey.package_name.label('package_name'),
            func.date_format(Monkey.begin_time, "%Y-%m-%d %H:%i:%s").label('begin_time'),
            Monkey.end_time.label('end_time'),
            Monkey.user_id.label('user_id'),
            Monkey.jenkins_url.label('jenkins_url'),
            Monkey.report_url.label('report_url'),
            Monkey.mobile_ids.label('mobile_ids'),
            Monkey.parameters.label('parameters'),
            Monkey.process.label('process'),
            Monkey.status.label('status'),
            Monkey.type_id.label('type_id'),
            Monkey.run_time.label('run_time'),
            Monkey.actual_run_time.label('actual_run_time'),
            Monkey.app_id.label('app_id'),
            func.date_format(Monkey.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            Monkey.system_device.label('system_device'),
            Monkey.login_required.label('login_required'),
            Monkey.login_username.label('login_username'),
            Monkey.login_password.label('login_password'),
            Monkey.app_install_required.label('app_install_required'),
            Monkey.cancel_status.label('cancel_status'),
            Monkey.test_type.label('test_type'),
        )

    @classmethod
    @transfer2json(
        '?id|!app_name|!package_name|!begin_time|!end_time|!user_id|!jenkins_url|!report_url|!mobile_ids|!parameters|'
        '!process|!status|!type_id|!download_app_status|!run_time|!actual_run_time|!app_id|!creation_time|'
        '!system_device|!login_required|!login_username|!login_password|!app_install_required|!cancel_status'
    )
    def query_all_json(cls, page_size, page_index, test_type=1):
        ret = cls._query().filter(Monkey.status == Monkey.ACTIVE,
                                  Monkey.test_type == test_type).order_by(
            desc(Monkey.id)).limit(page_size).offset((page_index - 1) * page_size).all()
        return ret

    @classmethod
    def query_all_count(cls, test_type=1):
        count = cls._query().filter(Monkey.status == Monkey.ACTIVE, Monkey.test_type == test_type).count()
        return count

    @classmethod
    @transfer2json(
        '?id|!app_name|!package_name|!begin_time|!end_time|!user_id|!jenkins_url|!report_url|!mobile_ids|!parameters|'
        '!process|!status|!type_id|!download_app_status|!run_time|!actual_run_time|!app_id|!creation_time|'
        '!system_device|!login_required|!login_username|!login_password|!app_install_required|!cancel_status'
    )
    def query_json_by_user_id(cls, user_id, page_size, page_index, test_type=1):
        ret = cls._query().filter(Monkey.status == Monkey.ACTIVE,
                                  Monkey.test_type == test_type,
                                  Monkey.user_id == user_id).order_by(
            desc(Monkey.id)).limit(page_size).offset((page_index - 1) * page_size).all()
        return ret

    @classmethod
    def query_count_by_user_id(cls, user_id, test_type=1):
        count = cls._query().filter(Monkey.status == Monkey.ACTIVE, Monkey.user_id == user_id,
                                    Monkey.test_type == test_type)
        current_app.logger.info(count.count())
        return count.count()

    @classmethod
    @transfer2json(
        '?id|!app_name|!package_name|!begin_time|!end_time|!user_id|!jenkins_url|!report_url|!mobile_ids|!parameters|'
        '!process|!status|!type_id|!download_app_status|!run_time|!actual_run_time|!app_id|!creation_time|'
        '!system_device|!login_required|!login_username|!login_password|!app_install_required|!cancel_status'
    )
    def query_json_by_id(cls, id):
        return cls._query().filter(
            Monkey.id == id, Monkey.status == Monkey.ACTIVE).all()

    @classmethod
    def create(cls, app_name, package_name, begin_time, end_time, user_id, jenkins_url, report_url, mobile_ids,
               parameters, process, type_id, run_time, system_device, login_required, login_username,
               login_password, app_install_required):
        try:
            mobile_ids = ','.join(mobile_ids)
            monkey = Monkey(
                app_name=app_name,
                package_name=package_name,
                begin_time=begin_time,
                end_time=end_time,
                user_id=user_id,
                jenkins_url=jenkins_url,
                report_url=report_url,
                mobile_ids=mobile_ids,
                parameters=parameters,
                process=0,
                type_id=type_id,
                status=Monkey.ACTIVE,
                run_time=run_time,
                system_device=system_device,
                login_required=login_required,
                login_username=login_username,
                login_pasword=login_password,
                app_install_required=app_install_required
            )
            db.session.add(monkey)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise CreateObjectException()

    @classmethod
    def update(cls, id, end_time, process, jenkins_url, status, app_version, begin_time, report_url, run_time,
               actual_run_time, download_app_status):
        try:
            monkey = Monkey.query.get(id)
            check_list = {
                'id': id,
                'end_time': end_time,
                'jenkins_url': jenkins_url,
                'process': process,
                'status': status,
                'app_version': app_version,
                'begin_time': begin_time,
                'report_url': report_url,
                'run_time': run_time,
                'actual_run_time': actual_run_time,
                'download_app_status': download_app_status
            }

            for key in check_list.keys():
                if check_list.get(key) is not None:
                    setattr(monkey, key, check_list.get(key))

            db.session.add(monkey)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()

    @classmethod
    def update_process(cls, id, process):
        try:
            monkey = Monkey.query.get(id)
            monkey.process = process

            db.session.add(monkey)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()

    @classmethod
    def update_jenkins_url(cls, id, jenkins_url):
        try:
            monkey = Monkey.query.get(id)
            monkey.jenkins_url = jenkins_url

            db.session.add(monkey)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()

    @classmethod
    def start_jenkins_job(cls, test_type, parameters):
        try:
            jenkins_server_url = current_app.config['CI_AUTO_MAN_JENKINS_URL']
            jenkins_server_username = current_app.config['CI_AUTO_MAN_JENKINS_AUTH']
            jenkins_server = jenkins.Jenkins(jenkins_server_url, username=jenkins_server_username.get('username'),
                                             password=jenkins_server_username.get('password'))
            if test_type == 1:
                job_name = current_app.config['CI_AUTO_MAN_JENKINS_MONKEY_JOB']
            elif test_type == 2:
                job_name = current_app.config['CI_AUTO_MAN_JENKINS_PERFORMANCE_JOB']
            jenkins_server.build_job(job_name, parameters)
            return 'Success'
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()

    @classmethod
    def start_test(cls, user_id, mobile_infos, type_id, run_time, system_device, login_required, login_username,
                   login_password, app_id, parameters, app_install_required, test_type=1, test_config=''):
        test_type = int(test_type)
        if test_type == 1:
            current_app.logger.info('start monkey test ')
            cls.start_monkey(user_id, mobile_infos, type_id, run_time, system_device, login_required, login_username,
                             login_password, app_id, parameters, app_install_required)
        elif test_type == 2:
            current_app.logger.info('start performance test ')
            cls.start_performance(user_id, mobile_infos, type_id, run_time, system_device, login_required,
                                  login_username, login_password, app_id, parameters, app_install_required,
                                  test_config)
        return 0, None

    @classmethod
    def start_performance(cls, user_id, mobile_infos, type_id, run_time, system_device, login_required, login_username,
                          login_password, app_id, parameters, app_install_required, test_config):
        try:
            current_app.logger.info('start performance test ')
            if not isinstance(mobile_infos, list):
                return 102, 'mobile_ids 参数格式不对，应为 List 格式'

            mobile_ids = []
            mobile_models = {}
            mobile_versions = {}
            mobile_resolutions = {}

            for info in mobile_infos:
                id = info.get('mobile_id')
                mobile_ids.append(id)
                mobile_models[id] = info.get('mobile_model')
                mobile_versions[id] = info.get('mobile_version')
                mobile_resolutions[id] = info.get('mobile_resolution')

            try:
                parameters = json.loads(parameters)
            except Exception as e:
                current_app.logger.warning('error when json the parameters: {}'.format(parameters))

            if not isinstance(parameters, dict):
                return 102, 'parameters 参数格式不对，应为 dict 格式'

            app_info = MonkeyPackage.query.get(app_id)

            # 创建 Monkey 示例
            monkey = Monkey(
                app_name=app_info.name,
                app_id=app_id,
                package_name=app_info.package_name,
                begin_time=datetime.now(),
                user_id=user_id,
                report_url='',
                mobile_ids=','.join(mobile_ids),
                parameters=str(parameters),
                process=0,
                type_id=type_id,
                run_time=run_time,
                system_device=system_device,
                login_required=login_required,
                login_username=login_username,
                login_password=login_password,
                app_install_required=app_install_required,
                test_type=2,
            )
            db.session.add(monkey)
            db.session.flush()

            # 创建 PerformanceDeviceStatus
            device_serial_list = []
            task_id_list = []

            # status defined
            # setup_info = db.Column(db.Integer)  # 前置条件, 表情打开：1，表情关闭：2
            # base_app = db.Column(db.Integer)  # 场景（不同的app）,微信：1，QQ：2，WPS: 3，趣键盘：4
            # key_type = db.Column(db.Integer)  # 26 : 1, 9 : 2
            # run_time = db.Column(db.Integer)  # 输入运行时间
            # all_env = [
            #     [1, 1, 1, run_time],
            #     [1, 2, 2, run_time],
            #     [2, 1, 1, run_time],
            #     [2, 2, 2, run_time],
            #     [2, 3, 1, run_time],
            #     [2, 4, 2, run_time]
            # ]

            devices_info = TcDevicesnInfo.query.all()
            for mobile_id in mobile_ids:
                current_app.logger.info(mobile_id)
                device_serial_list.append(mobile_id)

                for device in devices_info:
                    if device.serial == mobile_id:
                        task = MonkeyDeviceStatusBusiness.create(monkey.id, device.id,
                                                                 mobile_models.get(mobile_id),
                                                                 mobile_versions.get(mobile_id), device.serial,
                                                                 mobile_resolutions.get(mobile_id), run_time)
                        task_id_list.append(str(task))
                        # task_id_list[str(task)] = []
                        # for env_row in all_env:
                        #     env_id = PerformanceTestBusiness.create(task, *env_row)
                        #     task_id_list[str(task)].append(env_id)
                        break

            db.session.commit()

            jenkins_parameters = {
                'PackageName': app_info.package_name,
                'DeviceName': ','.join(device_serial_list),
                'RunMode': type_id,
                'RunTime': run_time,
                'AppDownloadUrl': app_info.oss_url,
                'DefaultAppActivity': app_info.default_activity,
                'SystemDevice': system_device,
                'LoginRequired': login_required,
                'LoginUsername': login_username,
                'LoginPassword': login_password,
                'TaskId': ",".join(task_id_list), # json.dumps(task_id_list),
                'MonkeyId': monkey.id,
                'InstallAppRequired': monkey.app_install_required,
                'TestType': 'performance',
                'TestConfig': test_config
            }

            msg = cls.start_jenkins_job(2, jenkins_parameters)

            if msg == "Success":
                current_app.logger.info('build jenkins job success')

            return 0, None

        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()

    @classmethod
    def start_monkey(cls, user_id, mobile_infos, type_id, run_time, system_device, login_required, login_username,
                     login_password, app_id, parameters, app_install_required, test_type=1):
        try:
            if not isinstance(mobile_infos, list):
                return 102, 'mobile_ids 参数格式不对，应为 List 格式'

            mobile_ids = []
            mobile_models = {}
            mobile_versions = {}
            mobile_resolutions = {}

            for info in mobile_infos:
                id = info.get('mobile_id')
                mobile_ids.append(id)
                mobile_models[id] = info.get('mobile_model')
                mobile_versions[id] = info.get('mobile_version')
                mobile_resolutions[id] = info.get('mobile_resolution')

            try:
                parameters = json.loads(parameters)
            except Exception as e:
                current_app.logger.warning('error when json the parameters: {}'.format(parameters))

            if not isinstance(parameters, dict):
                return 102, 'parameters 参数格式不对，应为 dict 格式'

            app_info = MonkeyPackage.query.get(app_id)

            # 创建 Monkey 示例
            monkey = Monkey(
                app_name=app_info.name,
                app_id=app_id,
                package_name=app_info.package_name,
                begin_time=datetime.now(),
                user_id=user_id,
                report_url='',
                mobile_ids=','.join(mobile_ids),
                parameters=str(parameters),
                process=0,
                type_id=type_id,
                run_time=run_time,
                system_device=system_device,
                login_required=login_required,
                login_username=login_username,
                login_password=login_password,
                app_install_required=app_install_required,
                test_type=1
            )

            db.session.add(monkey)
            db.session.flush()

            # 创建 MonkeyDeviceStatus
            device_serial_list = []
            task_id_list = []

            devices_info = TcDevicesnInfo.query.all()
            for mobile_id in mobile_ids:
                current_app.logger.info(mobile_id)
                device_serial_list.append(mobile_id)

                for device in devices_info:
                    if device.serial == mobile_id:
                        task = MonkeyDeviceStatusBusiness.create(monkey.id, device.id, mobile_models.get(mobile_id),
                                                                 mobile_versions.get(mobile_id), device.serial,
                                                                 mobile_resolutions.get(mobile_id), run_time)
                        task_id_list.append(str(task))
                        break

            db.session.commit()

            jenkins_parameters = {
                'PackageName': app_info.package_name,
                'DeviceName': ','.join(device_serial_list),
                'RunMode': type_id,
                'RunTime': run_time,
                'AppDownloadUrl': app_info.oss_url,
                'DefaultAppActivity': app_info.default_activity,
                'SystemDevice': system_device,
                'LoginRequired': login_required,
                'LoginUsername': login_username,
                'LoginPassword': login_password,
                'TaskId': ','.join(task_id_list),
                'MonkeyId': monkey.id,
                'InstallAppRequired': monkey.app_install_required,
                'TestType': 'monkey'
            }

            msg = cls.start_jenkins_job(1, jenkins_parameters)

            if msg == "Success":
                current_app.logger.info('build jenkins job success')

            return 0, None

        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()

    @classmethod
    def cancel_monkey(cls, monkey_id=None, task_id=None):
        try:
            # 取消所有的
            if monkey_id:
                devices = MonkeyDeviceStatus.query.add_columns(MonkeyDeviceStatus.id.label('id')).filter(
                    MonkeyDeviceStatus.monkey_id == monkey_id).all()
                for device in devices:
                    MonkeyDeviceStatusBusiness.cancel_task(device.id)
                current_monkey = Monkey.query.get(monkey_id)
                if current_monkey:
                    current_monkey.cancel_status = Monkey.ACTIVE
                    db.session.add(current_monkey)
                    db.session.commit()
                else:
                    return 101, 'monkey id not found'
            # 只取消 当前这一条
            elif task_id:
                return MonkeyDeviceStatusBusiness.cancel_task(task_id)
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise OperationFailedException()

    @classmethod
    def get_all_monkeys(cls, id, user_id, page_size, page_index, test_type=1):

        current_stage_map = {
            0: '设备状态检查中',
            1: '准备卸载 app',
            2: '准备安装 app',
            3: '锁屏状态检查中',
            4: 'app 启动中',
            5: 'app 登陆中',
            6: '运行中',
            7: '通过',
            102: '安装 app 失败',
            103: '设备锁屏，解锁失败',
            104: 'app 启动失败',
            105: 'app 登陆失败',
            106: '运行失败',
            1001: '用户取消中',
            1002: '用户取消成功',
            1003: '运行中设备离线'
        }

        if id:
            monkeys = cls.query_json_by_id(id)
            count = 1
        elif user_id:
            monkeys = cls.query_json_by_user_id(user_id, page_size, page_index, test_type)
            count = cls.query_count_by_user_id(user_id, test_type)
        else:
            monkeys = cls.query_all_json(page_size, page_index, test_type)
            count = cls.query_all_count(test_type)

        stf_devices = TcDevicesnInfo.query.all()
        monkey_packages = {package.get('id'): package for package in
                           MonkeyPackageBusiness.query_all_json_with_status_all()}
        user_infos = {user.get('userid'): user
                      for user in user_trpc.requests(method='get', path='/user', query={'base_info': True})}

        performance_tests = {}
        if test_type == 2:
            performance_tests = {performance_test.get('run_type'): performance_test
                                 for performance_test in PerformanceTestBusiness.query_all_json()}

        for monkey_data in monkeys:
            process = 0
            device_count = 0
            monkey_devices_status = MonkeyDeviceStatusBusiness.query_json_by_monkey_id(monkey_data.get('id'))

            for monkey_device_status in monkey_devices_status:
                # stf_device = TcDevicesnInfo.query.get(monkey_device_status.get('mobile_id'))
                stf_device = {}
                for temp in stf_devices:
                    if temp.id == monkey_device_status.get('mobile_id'):
                        stf_device = temp
                monkey_device_status['current_stage'] = current_stage_map.get(
                    int(monkey_device_status.get('current_stage')) + 1)
                if stf_device:
                    monkey_device_status['mobile_use_times'] = stf_device.times
                else:
                    monkey_device_status['mobile_use_times'] = 0
                process += monkey_device_status.get('process')
                device_count += 1

            if device_count == 0:
                device_count = 1

            monkey_data['monkey_device_status'] = monkey_devices_status
            monkey_data['process'] = process // device_count

            # app_info = MonkeyPackageBusiness.query_json_by_id_with_status_all(int(monkey_data.get('app_id')))[0]
            # app_info = {}
            # for app in monkey_packages:
            #     if str(app.get('id')) == str(monkey_data.get('app_id')):
            #         app_info = app
            #         break
            app_info = monkey_packages.get(monkey_data.get('app_id'))

            monkey_data['app_name'] = app_info.get('name')
            monkey_data['app_package_name'] = app_info.get('package_name')
            monkey_data['app_picture'] = app_info.get('picture')
            monkey_data['app_version'] = app_info.get('version')
            monkey_data['app_oss_url'] = app_info.get('oss_url')
            monkey_data['app_default_activity'] = app_info.get('default_activity')
            monkey_data['app_size'] = app_info.get('size')

            try:
                # user_info = user_trpc.requests(method='get', path='/user/userinfo',
                #                                query={'userid': monkey_data.get('user_id')})[0]
                # user_info = {}
                # for user in user_infos:
                #     if user.get('userid') == monkey_data.get('user_id'):
                #         user_info = user

                monkey_data['user_nickname'] = user_infos.get(monkey_data.get('user_id')).get('nickname')
            except Exception as e:
                current_app.logger.error(e)
                current_app.logger.error(traceback.format_exc())
                monkey_data['user_nickname'] = ''
            if test_type == 2:
                monkey_data['performance_test'] = performance_tests

        return monkeys, count

    @classmethod
    def get_all_name(cls, test_type=1):
        try:
            name_list = []
            monkeys = Monkey.query.add_columns(
                Monkey.id.label('id'),
                func.date_format(Monkey.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
                Monkey.app_name.label('app_name'),
                Monkey.app_version.label('app_version')
            ).filter(Monkey.status==Monkey.ACTIVE, Monkey.test_type==test_type
                     ).order_by(desc(Monkey.id)).all()
            for monkey in monkeys:
                name_list.append(
                    {
                        'id': monkey.id,
                        'name': f'{monkey.id}-{monkey.creation_time}-{monkey.app_name}-{monkey.app_version}'
                    }
                )
            return name_list
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return []

    @classmethod
    def get_performance_by_monkey_id_and_type(cls, monkey_id, run_type):
        infos = {}
        performances = MonkeyDeviceStatusBusiness.query_json_by_monkey_id(monkey_id)
        for performance in performances:
            infos[performance.get('mobile_serial')] = \
                PerformanceTestBusiness.query_json_by_performance_id_and_type(performance.get('id'), run_type)[0]
        return [infos]


class MonkeyPackageBusiness(object):

    @classmethod
    def _query(cls):
        return MonkeyPackage.query.add_columns(
            MonkeyPackage.id.label('id'),
            MonkeyPackage.name.label('name'),
            MonkeyPackage.package_name.label('package_name'),
            MonkeyPackage.oss_url.label('oss_url'),
            MonkeyPackage.picture.label('picture'),
            MonkeyPackage.version.label('version'),
            MonkeyPackage.default_activity.label('default_activity'),
            MonkeyPackage.user_id.label('user_id'),
            MonkeyPackage.status.label('status'),
            MonkeyPackage.size.label('size'),
            func.date_format(MonkeyPackage.creation_time, "%Y-%m-%d %H:%i:%s").label('upload_time'),
            MonkeyPackage.test_type.label('test_type'),
        )

    @classmethod
    @transfer2json(
        '?id|!name|!package_name|!oss_url|!picture|!version|!default_activity|!user_id|!size|!upload_time'
        '|!test_type'
    )
    def query_all_json(cls, page_size=10, page_index=1, test_type=1):
        ret = cls._query().filter(MonkeyPackage.status == MonkeyPackage.ACTIVE,
                                  MonkeyPackage.test_type == test_type).order_by(desc(MonkeyPackage.id)
                                                                                 ).limit(int(page_size)).offset(
            int(page_index - 1) * int(page_size)).all()
        return ret

    @classmethod
    def query_all_count(cls, test_type=1):
        data = cls._query().filter(MonkeyPackage.status == MonkeyPackage.ACTIVE,
                                   MonkeyPackage.test_type == test_type).count()
        return data

    @classmethod
    @transfer2json(
        '?id|!name|!package_name|!oss_url|!picture|!version|!default_activity|!user_id|!size|!upload_time'
    )
    def query_json_by_id(cls, id):
        return cls._query().filter(MonkeyPackage.status == MonkeyPackage.ACTIVE, MonkeyPackage.id == id).all()

    @classmethod
    @transfer2json(
        '?id|!name|!package_name|!oss_url|!picture|!version|!default_activity|!user_id|!size|!upload_time'
    )
    def query_json_by_id_with_status_all(cls, id):
        return cls._query().filter(MonkeyPackage.id == id).all()

    @classmethod
    @transfer2json(
        '?id|!name|!package_name|!oss_url|!picture|!version|!default_activity|!user_id|!size|!upload_time'
    )
    def query_all_json_with_status_all(cls):
        return cls._query().all()

    @classmethod
    @transfer2json(
        '?id|!name|!package_name|!oss_url|!picture|!version|!default_activity|!user_id|!size|!upload_time'
    )
    def query_json_by_user_id(cls, user_id, page_size, page_index, test_type=1):
        data = cls._query().filter(MonkeyPackage.status == MonkeyPackage.ACTIVE,
                                   MonkeyPackage.test_type == test_type,
                                   MonkeyPackage.user_id == user_id). \
            order_by(desc(MonkeyPackage.id)).limit(int(page_size)).offset(int(page_index - 1) * int(page_size)).all()
        return data

    @classmethod
    def query_count_by_user_id(cls, user_id, test_type=1):
        count = cls._query().filter(MonkeyPackage.status == MonkeyPackage.ACTIVE,
                                    MonkeyPackage.test_type == test_type,
                                    MonkeyPackage.user_id == user_id).count()
        return count

    @classmethod
    def get_monkey_packages_by_user_id(cls, user_id, page_size, page_index, test_type=1):
        if user_id:
            all = cls.query_json_by_user_id(user_id, page_size, page_index, test_type)
            count = cls.query_count_by_user_id(user_id, test_type)
        else:
            all = cls.query_all_json(page_size, page_index, test_type)
            count = cls.query_all_count(test_type)
        users = {
            user.get('userid'): user
            for user in user_trpc.requests(method='get', path='/user/', query={'base_info': True})
        }

        for package in all:
            try:
                package['user_nickname'] = users.get(package.get('user_id')).get('nickname')
            except Exception as e:
                package['user_nickname'] = ''

        return all, count

    @classmethod
    def create(cls, name, package_name, oss_url, picture, version, default_activity, user_id, size, test_type=1):
        try:
            monkey_package = MonkeyPackage(
                name=name,
                package_name=package_name,
                oss_url=oss_url,
                picture=picture,
                version=version,
                default_activity=default_activity,
                user_id=user_id,
                size=size,
                test_type=test_type or 1,
            )
            db.session.add(monkey_package)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()

    @classmethod
    def delete(cls, id):
        try:
            monkey_package = MonkeyPackage.query.get(id)
            if monkey_package:
                monkey_package.status = MonkeyPackage.DISABLE
                db.session.add(monkey_package)
                db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise RemoveObjectException()


class MonkeyReportBusiness(object):

    @classmethod
    def _query(cls):
        return MonkeyReport.query.add_columns(
            MonkeyReport.id.label('id'),
            MonkeyReport.monkey_id.label('monkey_id'),
            MonkeyReport.task_id.label('task_id'),
            MonkeyReport.report_type.label('report_type'),
            MonkeyReport.report_url.label('report_url')
        )

    @classmethod
    @transfer2json(
        '?id|!monkey_id|!task_id|!report_url|!report_type'
    )
    def query_all_json(cls, page_size, page_index):
        ret = cls._query().order_by(desc(MonkeyReport.id)). \
            limit(int(page_size)).offset(int(page_index - 1) * int(page_size)).all()
        return ret

    @classmethod
    def query_all_count(cls):
        count = cls._query().count()
        return count

    @classmethod
    @transfer2json(
        '?id|!monkey_id|!task_id|!report_url|!report_type'
    )
    def query_json_by_monkey_id(cls, monkey_id, page_size=10, page_index=1):
        return cls._query().filter(MonkeyReport.monkey_id == monkey_id). \
            limit(int(page_size)).offset(int(page_index - 1) * int(page_size)).all()

    @classmethod
    def query_count_by_monkey_id(cls, monkey_id):
        count = cls._query().filter(MonkeyReport.monkey_id == monkey_id).count()
        return count

    @classmethod
    @transfer2json(
        '?id|!monkey_id|!task_id|!report_url|!report_type'
    )
    def query_json_by_task_id(cls, task_id, page_size=10, page_index=1):
        return cls._query().filter(MonkeyReport.task_id == task_id). \
            limit(int(page_size)).offset(int(page_index - 1) * int(page_size)).all()

    @classmethod
    def query_count_by_task_id(cls, task_id):
        count = cls._query().filter(MonkeyReport.task_id == task_id).count()
        return count

    @classmethod
    def get_report(cls, monkey_id, task_id, page_size, page_index):
        if monkey_id:
            data = cls.query_json_by_monkey_id(monkey_id, page_size, page_index)
            count = cls.query_count_by_monkey_id(monkey_id)
        elif task_id:
            data = cls.query_json_by_task_id(task_id, page_size, page_index)
            count = cls.query_count_by_task_id(task_id)
        else:
            data = cls.query_all_json(page_size, page_index)
            count = cls.query_all_count()

        for report in data:
            monkey_device = MonkeyDeviceStatus.query.get(report.get('task_id'))
            if monkey_device:
                report['mobile_model'] = monkey_device.mobile_model

        return data, count

    @classmethod
    def create(cls, monkey_id, task_id, report_type, report_url):
        try:
            monkey_report = MonkeyReport(
                monkey_id=monkey_id,
                task_id=task_id,
                report_type=report_type,
                report_url=report_url
            )
            db.session.add(monkey_report)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise CreateObjectException()

    @classmethod
    def update(cls, monkey_report_id, monkey_id=None, task_id=None, report_type=None, report_url=None):
        try:
            monkey_report = MonkeyReport.query.get(monkey_report_id)
            monkey_report.monkey_id = monkey_id or monkey_report.monkey_id
            monkey_report.task_id = task_id or monkey_report.task_id
            monkey_report.report_type = report_type or monkey_report.report_type
            monkey_report.report_url = report_url or monkey_report.report_url
            db.session.add(monkey_report)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()


class MonkeyErrorLogBusiness(object):

    @classmethod
    def _query(cls):
        return MonkeyErrorLog.query.add_columns(
            MonkeyErrorLog.id.label('id'),
            MonkeyErrorLog.monkey_id.label('monkey_id'),
            MonkeyErrorLog.task_id.label('task_id'),
            MonkeyErrorLog.error_type.label('error_type'),
            MonkeyErrorLog.error_message.label('error_message'),
            MonkeyErrorLog.error_count.label('error_count')
        )

    @classmethod
    @transfer2json(
        '?id|!monkey_id|!task_id|!error_type|!error_message|!error_count'
    )
    def query_all_json(cls, page_size, page_index):
        ret = cls._query().order_by(desc(MonkeyErrorLog.id)). \
            limit(page_size).offset((page_index - 1) * page_size).all()
        return ret

    @classmethod
    def query_all_count(cls):
        count = cls._query().count()
        return count

    @classmethod
    @transfer2json(
        '?id|!monkey_id|!task_id|!error_type|!error_message|!error_count'
    )
    def query_json_by_monkey_id(cls, monkey_id, page_size, page_index):
        data = cls._query().filter(MonkeyErrorLog.monkey_id == monkey_id). \
            limit(page_size).offset((page_index - 1) * page_size).all()
        return data

    @classmethod
    def query_count_by_monkey_id(cls, monkey_id):
        count = cls._query().filter(MonkeyErrorLog.monkey_id == monkey_id).count()
        return count

    @classmethod
    @transfer2json(
        '?id|!monkey_id|!task_id|!error_type|!error_message|!error_count'
    )
    def query_json_by_task_id(cls, task_id, page_size, page_index):
        return cls._query().filter(MonkeyErrorLog.task_id == task_id). \
            limit(page_size).offset((page_index - 1) * page_size).all()

    @classmethod
    def query_count_by_task_id(cls, task_id):
        count = cls._query().filter(MonkeyErrorLog.task_id == task_id).count()
        return count

    @classmethod
    def create(cls, monkey_id, task_id, error_type, error_message, error_count):
        try:
            monkey_error_log = MonkeyErrorLog(
                monkey_id=monkey_id,
                task_id=task_id,
                error_type=error_type,
                error_message=error_message,
                error_count=error_count
            )
            db.session.add(monkey_error_log)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise CreateObjectException()


class MonkeyDeviceUsingBusiness(object):

    @classmethod
    def _query(cls):
        return MonkeyDeviceUsing.query.add_columns(
            MonkeyDeviceUsing.id.label('id'),
            MonkeyDeviceUsing.serial.label('serial'),
            MonkeyDeviceUsing.status.label('status'),
            MonkeyDeviceUsing.using.label('using')
        )

    @classmethod
    def mdyb_query(cls):
        return cls._query()

    @classmethod
    def using_device(cls, serial):
        try:
            devices = MonkeyDeviceUsing.query.filter(MonkeyDeviceUsing.serial == serial).all()
            if len(devices) == 0:
                device = MonkeyDeviceUsing(
                    serial=serial,
                    using=MonkeyDeviceUsing.ACTIVE
                )
                db.session.add(device)
                db.session.commit()
            else:
                device = devices[0]
                device.using = MonkeyDeviceUsing.ACTIVE
                db.session.add(device)
                db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise CreateObjectException()

    @classmethod
    def release_device(cls, serial):
        try:
            devices = MonkeyDeviceUsing.query.filter(MonkeyDeviceUsing.serial == serial).all()
            if len(devices) == 0:
                device = MonkeyDeviceUsing(
                    serial=serial,
                    using=MonkeyDeviceUsing.DISABLE
                )
                db.session.add(device)
                db.session.commit()
            else:
                device = devices[0]
                device.using = MonkeyDeviceUsing.DISABLE
                db.session.add(device)
                db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()


class MonkeyDeviceStatusBusiness(object):

    @classmethod
    def _query(cls):
        return MonkeyDeviceStatus.query.add_columns(
            MonkeyDeviceStatus.id.label('id'),
            MonkeyDeviceStatus.monkey_id.label('monkey_id'),
            MonkeyDeviceStatus.mobile_id.label('mobile_id'),
            MonkeyDeviceStatus.mobile_model.label('mobile_model'),
            MonkeyDeviceStatus.mobile_serial.label('mobile_serial'),
            MonkeyDeviceStatus.mobile_version.label('mobile_version'),
            MonkeyDeviceStatus.process.label('process'),
            MonkeyDeviceStatus.activity_count.label('activity_count'),
            MonkeyDeviceStatus.activity_tested_count.label('activity_tested_count'),
            MonkeyDeviceStatus.activity_all.label('activity_all'),
            MonkeyDeviceStatus.activity_tested.label('activity_tested'),
            MonkeyDeviceStatus.anr_count.label('anr_count'),
            MonkeyDeviceStatus.crash_count.label('crash_count'),
            MonkeyDeviceStatus.crash_rate.label('crash_rate'),
            MonkeyDeviceStatus.exception_count.label('exception_count'),
            MonkeyDeviceStatus.exception_run_time.label('exception_run_time'),
            MonkeyDeviceStatus.device_connect_status.label('device_connect_status'),
            MonkeyDeviceStatus.screen_lock_status.label('screen_lock_status'),
            MonkeyDeviceStatus.setup_install_app_status.label('setup_install_app_status'),
            MonkeyDeviceStatus.start_app_status.label('start_app_status'),
            MonkeyDeviceStatus.setup_uninstall_app_status.label('setup_uninstall_app_status'),
            MonkeyDeviceStatus.login_app_status.label('login_app_status'),
            MonkeyDeviceStatus.running_status.label('running_status'),
            MonkeyDeviceStatus.teardown_uninstall_app_status.label('teardown_uninstall_app_status'),
            MonkeyDeviceStatus.current_stage.label('current_stage'),
            MonkeyDeviceStatus.running_error_reason.label('running_error_reason'),
            func.date_format(MonkeyDeviceStatus.begin_time, "%Y-%m-%d %H:%i:%s").label('begin_time'),
            func.date_format(MonkeyDeviceStatus.end_time, "%Y-%m-%d %H:%i:%s").label('end_time'),
            MonkeyDeviceStatus.run_time.label('run_time'),
            MonkeyDeviceStatus.mobile_resolution.label('mobile_resolution'),
            MonkeyDeviceStatus.cancel_status.label('cancel_status')
        )

    @classmethod
    @transfer2json(
        '?id|!monkey_id|!mobile_id|!mobile_version|!mobile_serial|!process|!activity_count|!activity_tested_count|'
        '!activity_all|!activity_tested|!anr_count|!crash_count|!exception_count|!exception_run_time|'
        '!setup_install_app_status|!start_app_status|!setup_uninstall_app_status|!running_status|'
        '!login_app_status|!teardown_uninstall_app_status|!begin_time|!end_time|!run_time|!mobile_model|'
        '!device_connect_status|!screen_lock_status|!current_stage|!running_error_reason|!mobile_resolution|'
        '!cancel_status'
    )
    def query_all_json(cls, limit, offset):
        ret = cls._query().order_by(desc(MonkeyDeviceStatus.id)).limit(limit).offset(offset).all()
        return ret

    @classmethod
    @transfer2json(
        '?id|!monkey_id|!mobile_id|!mobile_version|!mobile_serial|!process|!activity_count|!activity_tested_count|'
        '!activity_all|!activity_tested|!anr_count|!crash_count|!exception_count|!exception_run_time|'
        '!setup_install_app_status|!start_app_status|!setup_uninstall_app_status|!running_status|'
        '!login_app_status|!teardown_uninstall_app_status|!begin_time|!end_time|!run_time|!mobile_model|'
        '!device_connect_status|!screen_lock_status|!current_stage|!running_error_reason|!mobile_resolution|'
        '!cancel_status'
    )
    def query_json_by_monkey_id(cls, id):
        return cls._query().filter(MonkeyDeviceStatus.monkey_id == id).all()

    @classmethod
    def query_cancel_status_by_id(cls, device_status_id):
        monkey_device_status = MonkeyDeviceStatus.query.get(device_status_id)
        rev = {
            'id': monkey_device_status.id,
            'cancel_status': monkey_device_status.cancel_status
        }
        return rev

    @classmethod
    def create_by_object(cls, monkey_device_status):
        try:
            if not isinstance(monkey_device_status, MonkeyDeviceStatus):
                return 102, None
            db.session.add(monkey_device_status)
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise CreateObjectException()

    @classmethod
    def create(cls, monkey_id, mobile_id, mobile_model, mobile_version, mobile_serial, mobile_resolution, run_time):
        try:
            monkey_device_status = MonkeyDeviceStatus(
                monkey_id=monkey_id,
                mobile_id=mobile_id,
                mobile_version=mobile_version,
                mobile_model=mobile_model,
                mobile_serial=mobile_serial,
                mobile_resolution=mobile_resolution,
                run_time=run_time,
                begin_time=None,
                end_time=None,
                activity_all='',
                activity_tested='',
                process=0,
                activity_count=0,
                activity_tested_count=0,
                anr_count=0,
                crash_count=0,
                exception_count=0,
                exception_run_time=0,
                device_connect_status=0,
                screen_lock_status=0,
                setup_install_app_status=0,
                start_app_status=0,
                running_status=0,
                setup_uninstall_app_status=0,
                login_app_status=0,
                teardown_uninstall_app_status=0,
            )
            db.session.add(monkey_device_status)
            db.session.flush()
            return monkey_device_status.id
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()

    @classmethod
    def update(cls, id, process, activity_count, activity_tested_count, activity_all, activity_tested, anr_count,
               crash_count, exception_count, exception_run_time, setup_install_app_status,
               start_app_status, begin_time, setup_uninstall_app_status, login_app_status, running_status,
               teardown_uninstall_app_status, end_time, run_time, device_connect_status, screen_lock_status,
               current_stage, running_error_reason, mobile_resolution):
        try:
            monkey_device_status = MonkeyDeviceStatus.query.get(id)

            monkey_device_status.process = process or monkey_device_status.process
            monkey_device_status.activity_count = activity_count or monkey_device_status.activity_count
            monkey_device_status.activity_tested_count = (
                    activity_tested_count or monkey_device_status.activity_tested_count)
            monkey_device_status.activity_all = activity_all or monkey_device_status.activity_all
            monkey_device_status.activity_tested = activity_tested or monkey_device_status.activity_tested
            monkey_device_status.anr_count = anr_count or monkey_device_status.anr_count
            monkey_device_status.crash_count = crash_count or monkey_device_status.crash_count
            monkey_device_status.exception_count = exception_count or monkey_device_status.exception_count
            monkey_device_status.exception_run_time = exception_run_time or monkey_device_status.exception_run_time
            monkey_device_status.end_time = end_time or monkey_device_status.end_time
            monkey_device_status.run_time = run_time or monkey_device_status.run_time
            monkey_device_status.begin_time = begin_time or monkey_device_status.begin_time
            monkey_device_status.current_stage = current_stage or monkey_device_status.current_stage
            monkey_device_status.running_error_reason = running_error_reason or monkey_device_status.running_error_reason
            monkey_device_status.mobile_resolution = mobile_resolution or monkey_device_status.mobile_resolution

            if device_connect_status is not None:
                monkey_device_status.device_connect_status = device_connect_status
                monkey_device_status.current_stage = 0
            if setup_uninstall_app_status is not None:
                monkey_device_status.setup_uninstall_app_status = setup_uninstall_app_status
                monkey_device_status.current_stage = 1
            if setup_install_app_status is not None:
                monkey_device_status.setup_install_app_status = setup_install_app_status
                monkey_device_status.current_stage = 2
            if screen_lock_status is not None:
                monkey_device_status.screen_lock_status = screen_lock_status
                monkey_device_status.current_stage = 3
            if start_app_status is not None:
                monkey_device_status.start_app_status = start_app_status
                monkey_device_status.current_stage = 4
            if login_app_status is not None:
                monkey_device_status.login_app_status = login_app_status
                monkey_device_status.current_stage = 5
            if running_status is not None:
                monkey_device_status.running_status = running_status
                monkey_device_status.current_stage = 6
            if teardown_uninstall_app_status is not None:
                monkey_device_status.teardown_uninstall_app_status = teardown_uninstall_app_status

            if monkey_device_status.setup_install_app_status == 2:
                monkey_device_status.current_stage = 101
            elif monkey_device_status.screen_lock_status == 2:
                monkey_device_status.current_stage = 102
            elif monkey_device_status.start_app_status == 2:
                monkey_device_status.current_stage = 103
            elif monkey_device_status.login_app_status == 2:
                monkey_device_status.current_stage = 104
            elif monkey_device_status.running_status == 2:
                monkey_device_status.current_stage = 105
            else:
                monkey_device_status.current_stage = current_stage or monkey_device_status.current_stage

            db.session.add(monkey_device_status)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()

    @classmethod
    def update_process(cls, id, process):
        try:
            monkey = MonkeyDeviceStatus.query.get(id)
            monkey.process = process

            db.session.add(monkey)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise SaveObjectException()

    @classmethod
    def cancel_task(cls, task_id):
        try:
            device_status = MonkeyDeviceStatus.query.get(task_id)
            if device_status:
                device_status.cancel_status = MonkeyDeviceStatus.ACTIVE
                db.session.add(device_status)
                db.session.commit()
            else:
                raise CannotFindObjectException(f'task id: {task_id} not exist')
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            raise RemoveObjectException(f'cancel monkey task : {task_id} failed')
