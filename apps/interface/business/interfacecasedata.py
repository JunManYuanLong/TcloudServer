from flask import current_app
from sqlalchemy import desc

from apps.interface.models.interfacecasedata import InterfaceCaseData
from library.api.db import db
from library.api.transfer import transfer2json


class InterfaceCaseDataBusiness(object):

    @classmethod
    def _query(cls):
        return InterfaceCaseData.query.add_columns(
            InterfaceCaseData.id.label('id'),
            InterfaceCaseData.num.label('num'),
            InterfaceCaseData.execute_status.label('execute_status'),
            InterfaceCaseData.name.label('name'),
            InterfaceCaseData.up_func.label('up_func'),
            InterfaceCaseData.down_func.label('down_func'),
            InterfaceCaseData.time.label('time'),
            InterfaceCaseData.param.label('param'),
            InterfaceCaseData.status_param.label('status_param'),
            InterfaceCaseData.variable.label('variable'),
            InterfaceCaseData.json_variable.label('json_variable'),
            InterfaceCaseData.status_variables.label('status_variables'),
            InterfaceCaseData.extract.label('extract'),
            InterfaceCaseData.status_extract.label('status_extract'),
            InterfaceCaseData.validate.label('validate'),
            InterfaceCaseData.status_validate.label('status_validate'),
            InterfaceCaseData.case_id.label('case_id'),
            InterfaceCaseData.api_msg_id.label('api_msg_id'),
            InterfaceCaseData.status.label('status'),
        )

    @classmethod
    @transfer2json('?id|!num|!execute_status|!name|!up_func|!down_func|!time|!param|!status_param|'
                   '!variable|!json_variable|!status_variables|!extract|!status_extract|!validate|'
                   '!status_validate|!case_id|!api_msg_id|!status')
    def query_all_json(cls, limit, offset):
        ret = cls._query().filter(InterfaceCaseData.status == InterfaceCaseData.ACTIVE) \
            .order_by(desc(InterfaceCaseData.id)) \
            .limit(limit).offset(offset).all()
        return ret

    @classmethod
    def casedata_create(cls, num, status, name, up_func, down_func, time, param, status_param, variable, json_variable,
                        status_variables, extract, status_extract, validate, status_validate, case_id, api_msg_id):
        try:
            m = InterfaceCaseData(
                num=num,
                status=status,
                name=name,
                up_func=up_func,
                down_func=down_func,
                time=time,
                param=param,
                status_param=status_param,
                variable=variable,
                json_variable=json_variable,
                status_variables=status_variables,
                extract=extract,
                status_extract=status_extract,
                validate=validate,
                status_validate=status_validate,
                case_id=case_id,
                api_msg_id=api_msg_id,

            )
            db.session.add(m)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def casedata_delete(cls, id):
        try:
            m = InterfaceCaseData.query.get(id)
            m.execute_status = InterfaceCaseData.DISABLE
            db.session.add(m)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def casedata_modify(cls, id, num, status, name, up_func, down_func, time, param, status_param, variable,
                        json_variable, status_variables, extract, status_extract, validate, status_validate):
        try:
            m = InterfaceCaseData.query.get(id)
            m.num = num,
            m.status = status,
            m.name = name,
            m.up_func = up_func,
            m.down_func = down_func,
            m.time = time,
            m.param = param,
            m.status_param = status_param,
            m.variable = variable,
            m.json_variable = json_variable,
            m.status_variables = status_variables,
            m.extract = extract,
            m.status_extract = status_extract,
            m.validate = validate,
            m.status_validate = status_validate,
            db.session.add(m)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)
