import copy

from flask import current_app, jsonify
from sqlalchemy import desc

from apps.interface.models.interfaceproject import InterfaceProject
from apps.interface.models.interfacereport import InterfaceReport
from apps.interface.util.global_variable import *
# from apps.interface.util.http_run import RunCase
from apps.interface.util.report.report import render_html_report
from apps.interface.util.utils import *
from library.api.db import db
from library.api.transfer import transfer2json


class InterfaceReportBusiness(object):
    @classmethod
    def _query(cls):
        return InterfaceReport.query.add_columns(
            InterfaceReport.id.label('id'),
            InterfaceReport.case_names.label('case_names'),
            InterfaceReport.read_status.label('read_status'),
            InterfaceReport.project_id.label('project_id'),
            InterfaceReport.status.label('status'),
        )

    @classmethod
    @transfer2json('?id|!case_names|!read_status|!project_id|!status')
    def query_all_json(cls, limit, offset):
        ret = cls._query().filter(InterfaceReport.status == InterfaceReport.ACTIVE) \
            .order_by(desc(InterfaceReport.id)) \
            .limit(limit).offset(offset).all()
        return ret

    @classmethod
    def report_create(cls, case_names, read_status, project_id):
        try:
            m = InterfaceReport(
                case_names=case_names,
                read_status=read_status,
                project_id=project_id,
                name='0',
            )
            db.session.add(m)
            db.session.commit()
            return m.id
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def report_delete(cls, id):
        try:
            m = InterfaceReport.query.get(id)
            m.status = InterfaceReport.DISABLE
            db.session.add(m)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def report_modify(cls, id, case_names, read_status, project_id):
        try:
            m = InterfaceReport.query.get(id)
            m.case_names = case_names,
            m.read_status = read_status,
            m.project_id = project_id,
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    # @classmethod
    # def run_cases(cls,case_ids,project_name,report_status):
    #
    #     if not project_name:
    #         return jsonify({'msg': '请选择项目', 'status': 0})
    #     if not case_ids:
    #         return jsonify({'msg': '请选择用例', 'status': 0})
    #
    #     project_id = InterfaceProject.query.filter_by(name=project_name,
    #                                                   status=InterfaceProject.ACTIVE).first().id
    #     try:
    #         d = RunCase(project_id)
    #         jump_res = d.run_case(d.get_case_test(case_ids))
    #     except Exception as e:
    #         current_app.logger.info("批量运行生成报告运行的错误信息:" + str(e))
    #         return jsonify({'msg': '函数文件或者参数配置错误，请重新检查完再运行', 'status': 0})
    #
    #     if report_status:
    #         d.build_report(jump_res, case_ids)
    #     res = json.loads(jump_res)
    #
    #     return jsonify({'msg': '测试完成', 'status': 1, 'data': {'report_id': d.new_report_id, 'data': res}})

    @classmethod
    def get_report(cls, report_id, state):

        _address = REPORT_ADDRESS + str(report_id) + '.txt'

        if not os.path.exists(_address):
            report_data = InterfaceReport.query.filter_by(id=report_id, status=InterfaceReport.ACTIVE).first()
            report_data.read_status = '异常'
            db.session.commit()
            return jsonify({'msg': '报告还未生成、或生成失败', 'status': 0})

        report_data = InterfaceReport.query.filter_by(id=report_id).first()
        report_data.read_status = '已读'
        db.session.commit()
        with open(_address, 'r') as f:
            d = json.loads(f.read())

        if state == 'success':
            _d = copy.deepcopy(d['details'])
            d['details'].clear()
            for d1 in _d:
                if d1['success']:
                    d['details'].append(d1)
        elif state == 'error':
            _d = copy.deepcopy(d['details'])
            d['details'].clear()
            for d1 in _d:
                if not d1['success']:
                    d['details'].append(d1)
        return jsonify(d)

    @classmethod
    def download_report(cls, report_id, data_or_report):

        _address = REPORT_ADDRESS + str(report_id) + '.txt'
        with open(_address, 'r') as f:
            res = json.loads(f.read())
        d = render_html_report(res,
                               html_report_name='接口自动化测试报告',
                               html_report_template=r'{}/extent_report_template.html'.format(TEMP_REPORT),
                               data_or_report=data_or_report)
        return jsonify({'data': d, 'status': 1})

    @classmethod
    def del_report(cls, report_id):

        InterfaceReportBusiness.report_delete(report_id)
        address = str(report_id) + '.txt'
        if not os.path.exists(REPORT_ADDRESS + address):
            return jsonify({'msg': '删除成功', 'status': 1})
        else:
            os.remove(REPORT_ADDRESS + address)
            return jsonify({'msg': '删除成功', 'status': 1})

    @classmethod
    def find_report(cls, project_name, page, per_page):

        if not project_name:
            return jsonify({'msg': '请先选择项目', 'status': 0})

        project_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id

        report_data = InterfaceReport.query.filter_by(project_id=project_id, status=InterfaceReport.ACTIVE)
        pagination = report_data.order_by(InterfaceReport.creation_time.desc()).paginate(page, per_page=per_page,
                                                                                         error_out=False)
        report = pagination.items
        total = pagination.total
        report = [{
                      'name': c.case_names, 'project_name': project_name, 'id': c.id, 'read_status': c.read_status,
                      'address': c.creation_time.strftime('%Y-%m-%d %H:%m:%S')
                  } for c in report]

        return jsonify({'data': report, 'total': total, 'status': 1})
