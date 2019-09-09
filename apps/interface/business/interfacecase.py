import json
import re

from flask import current_app, jsonify
from sqlalchemy import desc, asc

from apps.interface.business.interfacecasedata import InterfaceCaseDataBusiness
from apps.interface.models.interfaceapimsg import InterfaceApiMsg
from apps.interface.models.interfacecase import InterfaceCase
from apps.interface.models.interfacecasedata import InterfaceCaseData
from apps.interface.models.interfacecaseset import InterfaceCaseSet
from apps.interface.models.interfaceproject import InterfaceProject
from apps.interface.util.utils import extract_variables, convert, check_case, auto_num, num_sort
from library.api.db import db
from library.api.transfer import transfer2json


class InterfaceCaseBusiness(object):

    @classmethod
    def _query(cls):
        return InterfaceCase.query.add_columns(
            InterfaceCase.id.label('id'),
            InterfaceCase.num.label('num'),
            InterfaceCase.name.label('name'),
            InterfaceCase.desc.label('desc'),
            InterfaceCase.func_address.label('func_address'),
            InterfaceCase.variable.label('variable'),
            InterfaceCase.times.label('times'),
            InterfaceCase.project_id.label('project_id'),
            InterfaceCase.case_set_id.label('case_set_id'),
            InterfaceCase.status.label('status'),
        )

    @classmethod
    @transfer2json('?id|!num|!name|!desc|!func_address|!variable|!times|!project_id|!case_set_id|!status')
    def query_all_json(cls, limit, offset):
        ret = cls._query().filter(InterfaceCase.status == InterfaceCase.ACTIVE) \
            .order_by(desc(InterfaceCase.id)) \
            .limit(limit).offset(offset).all()
        return ret

    @classmethod
    def case_create(cls, num, name, desc, func_address, variable, times, project_id, case_set_id):
        try:
            m = InterfaceCase(
                num=num,
                name=name,
                desc=desc,
                func_address=func_address,
                variable=variable,
                times=times,
                project_id=project_id,
                case_set_id=case_set_id,
            )
            db.session.add(m)
            db.session.commit()
            return m.id
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def case_delete(cls, id):
        try:
            m = InterfaceCase.query.get(id)
            m.status = InterfaceCase.DISABLE
            db.session.add(m)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def case_modify(cls, id, name, desc, func_address, variable, times, project_id, case_set_id):
        try:
            m = InterfaceCase.query.get(id)
            m.name = name,
            m.desc = desc,
            m.func_address = func_address,
            m.variable = variable,
            m.times = times,
            m.project_id = project_id,
            m.case_set_id = case_set_id,
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def add_case(cls, name, desc, ids, times, case_set_id, func_address, project, variable, api_cases, number):

        if not name:
            return jsonify({'msg': '用例名称不能为空', 'status': 0})
        if not case_set_id:
            return jsonify({'msg': '请选择用例集', 'status': 0})
        if re.search(r'\${(.*?)}', '{}{}'.format(variable, json.dumps(api_cases)), flags=0) and not func_address:
            return jsonify({'msg': '参数引用函数后，必须引用函数文件', 'status': 0})

        project_data = InterfaceProject.query.filter_by(name=project, status=InterfaceProject.ACTIVE).first()
        project_id = project_data.id
        merge_variable = json.dumps(json.loads(variable) + json.loads(project_data.variables))
        _temp_check = extract_variables(convert(json.loads(merge_variable)))

        if _temp_check:
            return jsonify({'msg': '参数引用${}在业务变量和项目公用变量均没找到'.format(',$'.join(_temp_check)), 'status': 0})

        try:
            cases_check = check_case(api_cases, func_address)
        except Exception as e:
            current_app.logger.info("用例集接口运行的错误信息:" + str(e))
            return jsonify({'msg': '函数或接口参数错误，请检查后提交', 'status': 0})

        if cases_check:
            return jsonify({'msg': cases_check, 'status': 0})

        variable_check = check_case(variable, func_address)
        if variable_check:
            return jsonify({'msg': variable_check, 'status': 0})

        num = auto_num(number, InterfaceCase, project_id=project_id, case_set_id=case_set_id,
                       status=InterfaceCase.ACTIVE)
        if ids:
            old_data = InterfaceCase.query.filter_by(id=ids, status=InterfaceCase.ACTIVE).first()
            old_num = old_data.num
            if InterfaceCase.query.filter_by(name=name, project_id=project_id,
                                             case_set_id=case_set_id,
                                             status=InterfaceCase.ACTIVE).first() and name != old_data.name:
                return jsonify({'msg': '用例名字重复', 'status': 0})
            else:

                list_data_id = InterfaceCaseSet.query.filter_by(id=case_set_id,
                                                                status=InterfaceCaseSet.ACTIVE).first().id
                list_data = InterfaceCase.query.filter_by(case_set_id=list_data_id,
                                                          status=InterfaceCase.ACTIVE).order_by(
                    asc(InterfaceCase.num)).all()
                num_sort(num, old_num, list_data, old_data)

                InterfaceCaseBusiness.case_modify(ids, name, desc, func_address, variable, times, project_id,
                                                  case_set_id)

            for _num, c in enumerate(api_cases):
                if c.get('id'):

                    InterfaceCaseDataBusiness.casedata_modify(c.get('id'), _num, json.dumps(c['status']),
                                                              c['case_name'],
                                                              c['up_func'], c['down_func'], c['time'],
                                                              json.dumps(c['param']),
                                                              json.dumps(c['statusCase']['param']),
                                                              json.dumps(c['variable']), c['json_variable'],
                                                              json.dumps(c['statusCase']['variable']),
                                                              json.dumps(c['extract']),
                                                              json.dumps(c['statusCase']['extract']),
                                                              json.dumps(c['validate']),
                                                              json.dumps(c['statusCase']['validate']))
                else:

                    InterfaceCaseDataBusiness.casedata_create(_num, json.dumps(c['status']), c['case_name'],
                                                              c['up_func'],
                                                              c['down_func'], c['time'], json.dumps(c['param']),
                                                              json.dumps(c['statusCase']['param']),
                                                              json.dumps(c['statusCase']['variable']),
                                                              c['json_variable'],
                                                              json.dumps(c['statusCase']['variable']),
                                                              json.dumps(c['extract']),
                                                              json.dumps(c['statusCase']['extract']),
                                                              json.dumps(c['validate']),
                                                              json.dumps(c['statusCase']['validate']), ids,
                                                              c['apiMsgId'])

            return jsonify({'msg': '修改成功', 'status': 1})
        else:
            if InterfaceCase.query.filter_by(name=name, project_id=project_id, case_set_id=case_set_id,
                                             status=InterfaceCase.ACTIVE).first():
                return jsonify({'msg': '用例名字重复', 'status': 0})
            elif InterfaceCase.query.filter_by(num=num, project_id=project_id, case_set_id=case_set_id,
                                               status=InterfaceCase.ACTIVE).first():
                return jsonify({'msg': '编号重复', 'status': 0})
            else:

                case_id = InterfaceCaseBusiness.case_create(num, name, desc, func_address, variable, times, project_id,
                                                            case_set_id)
                for _num, c in enumerate(api_cases):
                    InterfaceCaseDataBusiness.casedata_create(_num, json.dumps(c['status']), c['case_name'],
                                                              c['up_func'],
                                                              c['down_func'], c['time'], json.dumps(c['param']),
                                                              json.dumps(c['statusCase']['param']),
                                                              json.dumps(c['statusCase']['variable']),
                                                              c['json_variable'],
                                                              json.dumps(c['statusCase']['variable']),
                                                              json.dumps(c['extract']),
                                                              json.dumps(c['statusCase']['extract']),
                                                              json.dumps(c['validate']),
                                                              json.dumps(c['statusCase']['validate']), case_id,
                                                              c['apiMsgId'])
                return jsonify({'msg': '新建成功', 'status': 1, 'case_id': case_id})

    @classmethod
    def find_case(cls, project_name, case_name, set_id, page, per_page):

        if not project_name:
            return jsonify({'msg': '请选择项目', 'status': 0})

        project_id = InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first().id

        if case_name:
            cases = InterfaceCase.query.filter_by(case_set_id=set_id, status=InterfaceCase.ACTIVE,
                                                  project_id=project_id).filter(
                InterfaceCase.name.like('%{}%'.format(case_name))).all()
            total = len(cases)
            if not cases:
                return jsonify({'msg': '没有该用例', 'status': 0})
        else:
            cases = InterfaceCase.query.filter_by(case_set_id=set_id, status=InterfaceCase.ACTIVE,
                                                  project_id=project_id)
            pagination = cases.order_by(InterfaceCase.num.asc()).paginate(page, per_page=per_page, error_out=False)
            cases = pagination.items
            total = pagination.total
        cases = [{'num': c.num, 'name': c.name, 'label': c.name, 'leaf': True, 'desc': c.desc, 'sceneId': c.id}
                 for c in cases]
        return jsonify({'data': cases, 'total': total, 'status': 1})

    @classmethod
    def del_case(cls, case_id):

        wait_del_case_data = InterfaceCase.query.filter_by(id=case_id, status=InterfaceCase.ACTIVE).first()
        # if current_user.id != Project.query.filter_by(id=wait_del_case_data.project_id).first().user_id:
        #     return jsonify({'msg': '不能删除别人项目下的用例', 'status': 0})

        _del_data = InterfaceCaseData.query.filter_by(case_id=case_id, execute_status=InterfaceCaseData.ACTIVE).all()
        if _del_data:
            for d in _del_data:
                InterfaceCaseDataBusiness.casedata_delete(d.id)

        InterfaceCaseBusiness.case_delete(case_id)
        db.session.delete(wait_del_case_data)
        return jsonify({'msg': '删除成功', 'status': 1})

    @classmethod
    def edit_case(cls, case_id, status):

        _data = InterfaceCase.query.filter_by(id=case_id, status=InterfaceCase.ACTIVE).first()
        cases = InterfaceCaseData.query.filter_by(case_id=case_id, execute_status=InterfaceCaseData.ACTIVE).order_by(
            InterfaceCaseData.num.asc()).all()
        case_data = []
        for case in cases:
            if status:
                case_id = ''
            else:
                case_id = case.id
            case_data.append(
                {
                    'num': case.num,
                    'name': InterfaceApiMsg.query.filter_by(id=case.api_msg_id,
                                                            status=InterfaceApiMsg.ACTIVE).first().name,
                    'desc': InterfaceApiMsg.query.filter_by(id=case.api_msg_id,
                                                            status=InterfaceApiMsg.ACTIVE).first().desc,
                    'apiMsgId': case.api_msg_id,
                    'id': case_id,
                    'status': json.loads(case.status),
                    'variableType': InterfaceApiMsg.query.filter_by(id=case.api_msg_id,
                                                                    status=InterfaceApiMsg.ACTIVE).first().variable_type,
                    'case_name': case.name,
                    'time': case.time,
                    'up_func': case.up_func,
                    'down_func': case.down_func,
                    'variable': json.loads(case.variable),
                    'json_variable': case.json_variable,
                    'param': json.loads(case.param),
                    'extract': json.loads(case.extract),
                    'validate': json.loads(case.validate),
                    'statusCase': {
                        'variable': json.loads(case.status_variables),
                        'extract': json.loads(case.status_extract),
                        'validate': json.loads(case.status_validate),
                        'param': json.loads(case.status_param)
                    },
                })
        _data2 = {
            'num': _data.num, 'name': _data.name, 'desc': _data.desc, 'cases': case_data,
            'setId': _data.case_set_id,
            'func_address': json.loads(_data.func_address), 'times': _data.times
        }
        if _data.variable:
            _data2['variable'] = json.loads(_data.variable)
        else:
            _data2['variable'] = []
        return jsonify({'data': _data2, 'status': 1})
