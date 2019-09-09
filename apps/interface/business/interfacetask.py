import datetime

from flask import current_app, jsonify
from sqlalchemy import desc

from apps.interface.models.interfacecase import InterfaceCase
from apps.interface.models.interfacecaseset import InterfaceCaseSet
from apps.interface.models.interfaceproject import InterfaceProject
from apps.interface.models.interfacetask import InterfaceTask
from apps.interface.util.email.SendEmail import SendEmail
from apps.interface.util.global_variable import TEMP_REPORT
from apps.interface.util.http_run import RunCase
from apps.interface.util.report.report import render_html_report
from apps.interface.util.utils import *
from library.api.db import db
from library.api.transfer import transfer2json


class InterfaceTaskBusiness(object):

    @classmethod
    def _query(cls):
        return InterfaceTask.query.add_columns(
            InterfaceTask.id.label('id'),
            InterfaceTask.task_name.label('task_name'),
            InterfaceTask.task_config_time.label('task_config_time'),
            InterfaceTask.set_id.label('set_id'),
            InterfaceTask.case_id.label('case_id'),
            InterfaceTask.task_type.label('task_type'),
            InterfaceTask.task_to_email_address.label('task_to_email_address'),
            InterfaceTask.task_send_email_address.label('task_send_email_address'),
            InterfaceTask.status.label('status'),
            InterfaceTask.project_id.label('project_id'),
            InterfaceTask.delete_status.label('delete_status'),

        )

    @classmethod
    @transfer2json(
        '?id|!task_name|!task_config_time|!set_id|!case_id|!task_type|!task_to_email_address|'
        '!task_send_email_address|!status|!project_id|!delete_status')
    def query_all_json(cls, limit, offset):
        ret = cls._query().filter(InterfaceTask.delete_status == InterfaceTask.ACTIVE) \
            .order_by(desc(InterfaceTask.id)) \
            .limit(limit).offset(offset).all()
        return ret

    @classmethod
    def task_create(cls, task_name, task_config_time, set_id, case_id, task_type, task_to_email_address,
                    task_send_email_address, status, project_id):
        try:
            m = InterfaceTask(
                task_name=task_name,
                task_config_time=task_config_time,
                set_id=set_id,
                case_id=case_id,
                task_type=task_type,
                task_to_email_address=task_to_email_address,
                task_send_email_address=task_send_email_address,
                status=status,
                project_id=project_id,
            )
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def task_delete(cls, id):
        try:
            m = InterfaceTask.query.get(id)
            m.delete_status = InterfaceTask.DISABLE
            db.session.add(m)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def task_modify(cls, id, task_name, task_config_time, set_id, case_id, task_type, task_to_email_address,
                    task_send_email_address, status, project_id):
        try:
            m = InterfaceTask.query.get(id)
            m.task_name = task_name,
            m.task_config_time = task_config_time,
            m.set_id = set_id,
            m.case_id = case_id,
            m.task_type = task_type,
            m.task_to_email_address = task_to_email_address,
            m.task_send_email_address = task_send_email_address,
            m.status = status,
            m.project_id = project_id,
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def aps_test(cls, project_name, case_ids, send_address=None, send_password=None, task_to_address=None):
        project_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id
        d = RunCase(project_id)
        jump_res = d.run_case(d.get_case_test(case_ids))
        d.build_report(jump_res, case_ids)
        res = json.loads(jump_res)

        if send_address:
            task_to_address = task_to_address.split(',')
            file = render_html_report(res,
                                      html_report_name='{}接口自动化测试报告'.format(
                                          datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')),
                                      html_report_template=r'{}/extent_report_template.html'.format(TEMP_REPORT),
                                      data_or_report=False)
            s = SendEmail(send_address, send_password, task_to_address, file)
            s.send_email()
        return d

    @classmethod
    def run_task(cls, ids):

        _data = InterfaceTask.query.filter_by(id=ids, delete_status=InterfaceTask.ACTIVE).first()
        case_ids = []
        if len(json.loads(_data.case_id)) != 0:
            case_ids += [i['id'] for i in json.loads(_data.case_id)]
        else:
            if len(json.loads(_data.case_id)) == 0 and len(json.loads(_data.set_id)) == 0:
                project_id = InterfaceProject.query.filter_by(name=_data.project_id,
                                                              status=InterfaceProject.ACTIVE).first().id
                _set_ids = [_set.id for _set in
                            InterfaceCaseSet.query.filter_by(project_id=project_id,
                                                             status=InterfaceCaseSet.ACTIVE).order_by(
                                InterfaceCaseSet.num.asc()).all()]
            else:
                _set_ids = [i['id'] for i in json.loads(_data.set_id)]
            for set_id in _set_ids:
                for case_data in InterfaceCase.query.filter_by(case_set_id=set_id,
                                                               status=InterfaceCase.ACTIVE).order_by(
                    InterfaceCase.num.asc()).all():
                    case_ids.append(case_data.id)
        project_name = InterfaceProject.query.filter_by(id=_data.project_id,
                                                        status=InterfaceProject.ACTIVE).first().name
        result = cls.aps_test(project_name, case_ids)

        return jsonify({'msg': '测试成功', 'status': 1, 'data': {'report_id': result.new_report_id}})

    @classmethod
    def start_task(cls, ids):

        _data = InterfaceTask.query.filter_by(id=ids, delete_status=InterfaceTask.ACTIVE).first()

        config_time = change_cron(_data.task_config_time)
        case_ids = []
        if len(json.loads(_data.case_id)) != 0:
            case_ids += [i['id'] for i in json.loads(_data.case_id)]
        else:
            if len(json.loads(_data.case_id)) == 0 and len(json.loads(_data.set_id)) == 0:
                project_id = InterfaceProject.query.filter_by(id=_data.project_id,
                                                              status=InterfaceProject.ACTIVE).first().id
                _set_ids = [_set.id for _set in
                            InterfaceCaseSet.query.filter_by(project_id=project_id,
                                                             status=InterfaceCaseSet.ACTIVE).order_by(
                                InterfaceCaseSet.num.asc()).all()]
            else:
                _set_ids = [i['id'] for i in json.loads(_data.set_id)]
            for set_id in _set_ids:
                for case_data in InterfaceCase.query.filter_by(case_set_id=set_id,
                                                               status=InterfaceCase.ACTIVE).order_by(
                    InterfaceCase.num.asc()).all():
                    case_ids.append(case_data.id)
        project_name = InterfaceProject.query.filter_by(id=_data.project_id,
                                                        status=InterfaceProject.ACTIVE).first().name

        current_app.apscheduler.add_job(func=cls.aps_test, trigger='cron',
                                        args=[project_name, case_ids, _data.task_send_email_address,
                                              _data.email_password,
                                              _data.task_to_email_address],
                                        id=str(ids), **config_time)  # 添加任务
        # jobs = current_app.apscheduler.get_jobs()

        _data.status = '启动'
        db.session.commit()

        return jsonify({'msg': '启动成功', 'status': 1})

    @classmethod
    def add_task(cls, project_name, set_ids, case_ids, task_id, name, to_email, send_email, password, num, time_config):

        task_type = 'cron'

        if not project_name:
            return jsonify({'msg': '请选择项目', 'status': 0})
        project_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id
        num = auto_num(num, InterfaceTask, project_id=project_id, delete_status=InterfaceTask.ACTIVE)
        # 0 0 1 * * *
        if not (not to_email and not send_email and not password) and not (to_email and send_email and password):
            return jsonify({'msg': '发件人、收件人、密码3个必须都为空，或者都必须有值', 'status': 0})

        if len(time_config.strip().split(' ')) != 6:
            return jsonify({'msg': 'cron格式错误', 'status': 0})

        if task_id:
            old_task_data = InterfaceTask.query.filter_by(id=task_id, delete_status=InterfaceTask.ACTIVE).first()
            if InterfaceTask.query.filter_by(
                    task_name=name,
                    delete_status=InterfaceTask.ACTIVE
            ).first() and name != old_task_data.task_name:
                return jsonify({'msg': '任务名字重复', 'status': 0})
            else:
                old_task_data.project_id = project_id
                old_task_data.set_id = json.dumps(set_ids)
                old_task_data.case_id = json.dumps(case_ids)
                old_task_data.task_name = name
                old_task_data.task_type = task_type
                old_task_data.task_to_email_address = to_email
                old_task_data.task_send_email_address = send_email
                old_task_data.email_password = password
                old_task_data.num = num
                if old_task_data.status != '创建' and old_task_data.task_config_time != time_config:
                    current_app.apscheduler.reschedule_job(str(task_id), trigger='cron',
                                                           **change_cron(time_config))  # 修改任务
                    old_task_data.status = '启动'

                old_task_data.task_config_time = time_config
                db.session.commit()
                return jsonify({'msg': '修改成功', 'status': 1})
        else:

            if InterfaceTask.query.filter_by(task_name=name, delete_status=InterfaceTask.ACTIVE).first():
                return jsonify({'msg': '任务名字重复', 'status': 0})
            else:
                new_task = InterfaceTask(task_name=name,
                                         project_id=project_id,
                                         set_id=json.dumps(set_ids),
                                         case_id=json.dumps(case_ids),
                                         email_password=password,
                                         task_type=task_type,
                                         task_to_email_address=to_email,
                                         task_send_email_address=send_email,
                                         task_config_time=time_config,
                                         num=num,
                                         name='0')
                db.session.add(new_task)
                db.session.commit()
                return jsonify({'msg': '新建成功', 'status': 1})

    @classmethod
    def edit_task(cls, task_id):

        c = InterfaceTask.query.filter_by(id=task_id, delete_status=InterfaceTask.ACTIVE).first()
        _data = {
            'num': c.num, 'task_name': c.task_name, 'task_config_time': c.task_config_time,
            'task_type': c.task_type,
            'set_ids': json.loads(c.set_id), 'case_ids': json.loads(c.case_id),
            'task_to_email_address': c.task_to_email_address, 'task_send_email_address': c.task_send_email_address,
            'password': c.email_password
        }

        return jsonify({'data': _data, 'status': 1})

    @classmethod
    def find_task(cls, project_name, task_name, page, per_page):
        if not project_name:
            return jsonify({'msg': '请先选择项目', 'status': 0})

        project_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id

        if task_name:
            _data = InterfaceTask.query.filter_by(project_id=project_id, delete_status=InterfaceTask.ACTIVE).filter(
                InterfaceTask.task_name.like('%{}%'.format(task_name))).all()
            total = len(_data)
            if not _data:
                return jsonify({'msg': '没有该任务', 'status': 0})
        else:
            tasks = InterfaceTask.query.filter_by(project_id=project_id, delete_status=InterfaceTask.ACTIVE)
            pagination = tasks.order_by(InterfaceTask.id.asc()).paginate(page, per_page=per_page, error_out=False)
            _data = pagination.items
            total = pagination.total
        task = [{
                    'task_name': c.task_name, 'task_config_time': c.task_config_time,
                    'id': c.id, 'task_type': c.task_type, 'status': c.status
                } for c in _data]
        return jsonify({'data': task, 'total': total, 'status': 1})

    @classmethod
    def del_task(cls, ids):
        _edit = InterfaceTask.query.filter_by(id=ids, delete_status=InterfaceTask.ACTIVE).first()
        if _edit.status != '创建':
            return jsonify({'msg': '请先移除任务', 'status': 0})

        InterfaceTaskBusiness.task_delete(ids)
        return jsonify({'msg': '删除成功', 'status': 1})

    @classmethod
    def pause_task(cls, ids):

        _data = InterfaceTask.query.filter_by(id=ids, delete_status=InterfaceTask.ACTIVE).first()
        _data.status = '暂停'

        # jobs = current_app.apscheduler.get_jobs()

        current_app.apscheduler.pause_job(str(ids))  # 添加任务

        # jobs = current_app.apscheduler.get_jobs()
        db.session.commit()

        return jsonify({'msg': '暂停成功', 'status': 1})

    @classmethod
    def resume_task(cls, ids):
        _data = InterfaceTask.query.filter_by(id=ids, delete_status=InterfaceTask.ACTIVE).first()
        _data.status = '启动'
        current_app.apscheduler.resume_job(str(ids))  # 添加任务
        db.session.commit()
        return jsonify({'msg': '恢复成功', 'status': 1})

    @classmethod
    def remove_task(cls, ids):

        _data = InterfaceTask.query.filter_by(id=ids, delete_status=InterfaceTask.ACTIVE).first()
        current_app.apscheduler.remove_job(str(ids))  # 添加任务
        _data.status = '创建'
        db.session.commit()
        return jsonify({'msg': '移除成功', 'status': 1})
