from datetime import datetime, timedelta
from flask import request, g, current_app
from sqlalchemy import desc, func

from apps.autotest.models.datashow import (
    DataShowFields, DataShowResponseKernelRecord,
    DataShowFirstPageFirstWordCorrectRate, DataShowResponseLog,
)
from library.api.db import db
from library.api.exceptions import (
    CreateObjectException, CannotFindObjectException,
)
from library.api.transfer import transfer2json
from library.trpc import Trpc

user_trpc = Trpc('auth')


class DataShowFieldsBusiness(object):

    @classmethod
    def _query(cls):
        return DataShowFields.query.add_columns(
            DataShowFields.id.label('id'),
            DataShowFields.data_type.label('data_type'),
            DataShowFields.data_value.label('data_value'),
        )

    @classmethod
    def query_all_json(cls):
        ret = cls._query().order_by(desc(DataShowFields.id)).all()
        rev = {r.data_type: [] for r in ret}
        for r in ret:
            rev[r.data_type].append({
                'id': r.id,
                'value': r.data_value
            })
        return rev

    @classmethod
    def query_all_data(cls):
        ret = cls._query().order_by(desc(DataShowFields.id)).all()
        rev = {str(r.id): r.data_value for r in ret}
        return rev

    @classmethod
    def create(cls, data_type, data_value):
        data_field = DataShowFields.query.filter(DataShowFields.data_type == data_type,
                                                 DataShowFields.data_value == data_value).all()
        if data_field:
            raise CreateObjectException(f'数据 {data_value} 已存在')

        data_field = DataShowFields(
            data_type=data_type,
            data_value=data_value
        )
        db.session.add(data_field)
        db.session.commit()
        return 0


class DataShowResponseKernelRecordBusiness(object):

    @classmethod
    def _query(cls):
        return DataShowResponseKernelRecord.query.add_columns(
            DataShowResponseKernelRecord.id.label('id'),
            DataShowResponseKernelRecord.data_source.label('data_source'),
            DataShowResponseKernelRecord.phone_model.label('phone_model'),
            DataShowResponseKernelRecord.apk_version.label('apk_version'),
            DataShowResponseKernelRecord.kernel_version.label('kernel_version'),
            DataShowResponseKernelRecord.system_version.label('system_version'),
            DataShowResponseKernelRecord.thesaurus_version.label('thesaurus_version'),
            DataShowResponseKernelRecord.corpus_version.label('corpus_version'),
            DataShowResponseKernelRecord.key_9_and_26.label('key_9_and_26'),
            DataShowResponseKernelRecord.average.label('average'),
            DataShowResponseKernelRecord.line_90_percent.label('line_90_percent'),
            DataShowResponseKernelRecord.line_95_percent.label('line_95_percent'),
            DataShowResponseKernelRecord.creator.label('creator'),
            DataShowResponseKernelRecord.comment.label('comment'),
            func.date_format(DataShowResponseKernelRecord.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            DataShowResponseKernelRecord.show_in_chart.label('show_in_chart'),
        )

    @classmethod
    @transfer2json('?id|!data_source|!phone_model|!apk_version|!kernel_version|!system_version|!thesaurus_version'
                   '|!corpus_version|!key_9_and_26|!average|!line_90_percent|!line_95_percent|!creator|!comment'
                   '|!creation_time|!show_in_chart')
    def query_all_json(cls, data):
        return data

    @classmethod
    def query_chart_data(cls, date_time):
        data = cls._query().filter(
                DataShowResponseKernelRecord.status == DataShowResponseKernelRecord.ACTIVE,
            )
        if date_time == '0':
            data = data.filter(
                DataShowResponseKernelRecord.show_in_chart == DataShowResponseKernelRecord.ACTIVE).all()
        else:
            if date_time == '1': # senven_days
                day = 7
            elif date_time == '2': # one_month
                day = 30
            end_time = datetime.now().strftime('%Y-%m-%d')
            begin_time = datetime.strptime(end_time, "%Y-%m-%d") - timedelta(days=day)
            data = data.filter(
                DataShowResponseKernelRecord.creation_time.between(begin_time, end_time+" 23:00:00")
            ).group_by(DataShowResponseKernelRecord.apk_version).all()

        list_of_fields = ['data_source', 'phone_model', 'apk_version', 'kernel_version', 'system_version',
                          'thesaurus_version', 'corpus_version']
        fields = DataShowFieldsBusiness.query_all_data()
        data = cls.query_all_json(data)
        for d in data:
            for field in list_of_fields:
                d[field] = fields.get(str(d[field]))
        return data

    @classmethod
    def query_all_data(cls, page_size, page_index):
        data_source = request.args.get('data_source', '')
        phone_model = request.args.get('phone_model', '')
        apk_version = request.args.get('apk_version', '')
        kernel_version = request.args.get('kernel_version', '')
        system_version = request.args.get('system_version', '')
        thesaurus_version = request.args.get('thesaurus_version', '')
        corpus_version = request.args.get('corpus_version', '')
        list_of_fields = ['data_source', 'phone_model', 'apk_version', 'kernel_version', 'system_version',
                          'thesaurus_version', 'corpus_version']

        user_infos = {user.get('userid'): user
                      for user in user_trpc.requests(method='get', path='/user', query={'base_info': True})}

        data = cls._query().filter(DataShowResponseKernelRecord.status == DataShowResponseKernelRecord.ACTIVE)

        if data_source != '':
            data = data.filter(DataShowResponseKernelRecord.data_source == data_source)
        if phone_model != '':
            data = data.filter(DataShowResponseKernelRecord.phone_model == phone_model)
        if apk_version != '':
            data = data.filter(DataShowResponseKernelRecord.apk_version == apk_version)
        if kernel_version != '':
            data = data.filter(DataShowResponseKernelRecord.kernel_version == kernel_version)
        if system_version != '':
            data = data.filter(DataShowResponseKernelRecord.system_version == system_version)
        if thesaurus_version != '':
            data = data.filter(DataShowResponseKernelRecord.thesaurus_version == thesaurus_version)
        if corpus_version != '':
            data = data.filter(DataShowResponseKernelRecord.corpus_version == corpus_version)

        count = data.count()
        data_ = data.order_by(
            desc(DataShowResponseKernelRecord.id)).limit(page_size).offset((page_index - 1) * page_size).all()
        data = cls.query_all_json(data_)
        fields = DataShowFieldsBusiness.query_all_data()
        for d in data:
            for field in list_of_fields:
                d[field] = fields.get(str(d[field]))
            if d['creator']:
                d['creator_nickname'] = user_infos.get(int(d['creator']), {}).get('nickname')
            else:
                d['creator_nickname'] = ''

        return data, count

    @classmethod
    def disable_others(cls, apk_version_id, show_in_chart):
        if show_in_chart == 0:
            datas = DataShowResponseKernelRecord.query.filter(
                DataShowResponseKernelRecord.apk_version == apk_version_id,
                DataShowResponseKernelRecord.show_in_chart == 0).all()
            for data in datas:
                data.show_in_chart = 1
                db.session.add(data)
            db.session.commit()

    @classmethod
    def create(cls, params):
        (data_source, phone_model, apk_version, kernel_version, system_version, thesaurus_version, corpus_version,
         key_9_and_26, average, line_90_percent, line_95_percent, comment, show_in_chart) = params
        cls.disable_others(apk_version, show_in_chart)
        data_show_response = DataShowResponseKernelRecord(
            data_source=data_source,
            phone_model=phone_model,
            apk_version=apk_version,
            kernel_version=kernel_version,
            system_version=system_version,
            thesaurus_version=thesaurus_version,
            corpus_version=corpus_version,
            key_9_and_26=key_9_and_26,
            average=average,
            line_90_percent=line_90_percent,
            line_95_percent=line_95_percent,
            creator=g.userid,
            comment=comment,
            status=0,
            show_in_chart=show_in_chart
        )
        try:
            db.session.add(data_show_response)
            db.session.commit()
        except Exception:
            raise CreateObjectException('创建数据失败！')
        return 0

    @classmethod
    def update(cls, id, params):
        (data_source, phone_model, apk_version, kernel_version, system_version, thesaurus_version, corpus_version,
         key_9_and_26, average, line_90_percent, line_95_percent, comment, show_in_chart) = params

        cls.disable_others(apk_version, show_in_chart)
        data_show_response = DataShowResponseKernelRecord.query.get(id)

        if not data_show_response:
            raise CannotFindObjectException('数据不存在！')
        data_show_response.data_source = data_source
        data_show_response.phone_model = phone_model
        data_show_response.apk_version = apk_version
        data_show_response.kernel_version = kernel_version
        data_show_response.system_version = system_version
        data_show_response.thesaurus_version = thesaurus_version
        data_show_response.corpus_version = corpus_version
        data_show_response.key_9_and_26 = key_9_and_26
        data_show_response.average = average
        data_show_response.line_90_percent = line_90_percent
        data_show_response.line_95_percent = line_95_percent
        data_show_response.comment = comment
        data_show_response.show_in_chart = show_in_chart
        try:
            db.session.add(data_show_response)
            db.session.commit()
        except Exception:
            raise CreateObjectException('更新数据失败！')
        return 0

    @classmethod
    def delete(cls, id):
        data_show_response = DataShowResponseKernelRecord.query.get(id)
        data_show_response.status = 1
        try:
            db.session.add(data_show_response)
            db.session.commit()
        except Exception:
            raise CreateObjectException('删除数据失败！')
        return 0


class DataShowFirstPageFirstWordCorrectRateBusiness(object):

    @classmethod
    def _query(cls):
        return DataShowFirstPageFirstWordCorrectRate.query.add_columns(
            DataShowFirstPageFirstWordCorrectRate.id.label('id'),
            DataShowFirstPageFirstWordCorrectRate.data_source.label('data_source'),
            DataShowFirstPageFirstWordCorrectRate.phone_model.label('phone_model'),
            DataShowFirstPageFirstWordCorrectRate.apk_version.label('apk_version'),
            DataShowFirstPageFirstWordCorrectRate.kernel_version.label('kernel_version'),
            DataShowFirstPageFirstWordCorrectRate.system_version.label('system_version'),
            DataShowFirstPageFirstWordCorrectRate.thesaurus_version.label('thesaurus_version'),
            DataShowFirstPageFirstWordCorrectRate.corpus_version.label('corpus_version'),
            DataShowFirstPageFirstWordCorrectRate.key_9_and_26.label('key_9_and_26'),
            DataShowFirstPageFirstWordCorrectRate.first_word_correct_rate.label('first_word_correct_rate'),
            DataShowFirstPageFirstWordCorrectRate.first_page_correct_rate.label('first_page_correct_rate'),
            DataShowFirstPageFirstWordCorrectRate.creator.label('creator'),
            DataShowFirstPageFirstWordCorrectRate.comment.label('comment'),
            func.date_format(
                DataShowFirstPageFirstWordCorrectRate.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            DataShowFirstPageFirstWordCorrectRate.show_in_chart.label('show_in_chart'),
        )

    @classmethod
    @transfer2json('?id|!data_source|!phone_model|!apk_version|!kernel_version|!system_version|!thesaurus_version'
                   '|!corpus_version|!key_9_and_26|!first_word_correct_rate|!first_page_correct_rate'
                   '|!creator|!comment|!creation_time|!show_in_chart')
    def query_all_json(cls, data):
        return data

    @classmethod
    def query_chart_data(cls, date_time):
        data = cls._query().filter(
            DataShowFirstPageFirstWordCorrectRate.status == DataShowFirstPageFirstWordCorrectRate.ACTIVE,
        )
        if date_time == '0':
            data = data.filter(
                DataShowFirstPageFirstWordCorrectRate.show_in_chart == DataShowFirstPageFirstWordCorrectRate.ACTIVE).all()
        else:
            if date_time == '1':  # senven_days
                day = 7
            elif date_time == '2':  # one_month
                day = 30
            end_time = datetime.now().strftime('%Y-%m-%d')
            begin_time = datetime.strptime(end_time, "%Y-%m-%d") - timedelta(days=day)
            data = data.filter(
                DataShowFirstPageFirstWordCorrectRate.creation_time.between(begin_time, end_time+" 23:00:00")
            ).group_by(DataShowFirstPageFirstWordCorrectRate.apk_version).all()

        list_of_fields = ['data_source', 'phone_model', 'apk_version', 'kernel_version', 'system_version',
                          'thesaurus_version', 'corpus_version']
        fields = DataShowFieldsBusiness.query_all_data()
        data = cls.query_all_json(data)
        for d in data:
            for field in list_of_fields:
                d[field] = fields.get(str(d[field]))
        return data

    @classmethod
    def query_all_data(cls, page_size, page_index):
        data_source = request.args.get('data_source', '')
        phone_model = request.args.get('phone_model', '')
        apk_version = request.args.get('apk_version', '')
        kernel_version = request.args.get('kernel_version', '')
        system_version = request.args.get('system_version', '')
        thesaurus_version = request.args.get('thesaurus_version', '')
        corpus_version = request.args.get('corpus_version', '')
        list_of_fields = ['data_source', 'phone_model', 'apk_version', 'kernel_version', 'system_version',
                          'thesaurus_version', 'corpus_version']

        user_infos = {user.get('userid'): user
                      for user in user_trpc.requests(method='get', path='/user', query={'base_info': True})}
        data = cls._query().filter(
            DataShowFirstPageFirstWordCorrectRate.status == DataShowFirstPageFirstWordCorrectRate.ACTIVE)

        if data_source != '':
            data = data.filter(DataShowFirstPageFirstWordCorrectRate.data_source == data_source)
        if phone_model != '':
            data = data.filter(DataShowFirstPageFirstWordCorrectRate.phone_model == phone_model)
        if apk_version != '':
            data = data.filter(DataShowFirstPageFirstWordCorrectRate.apk_version == apk_version)
        if kernel_version != '':
            data = data.filter(DataShowFirstPageFirstWordCorrectRate.kernel_version == kernel_version)
        if system_version != '':
            data = data.filter(DataShowFirstPageFirstWordCorrectRate.system_version == system_version)
        if thesaurus_version != '':
            data = data.filter(DataShowFirstPageFirstWordCorrectRate.thesaurus_version == thesaurus_version)
        if corpus_version != '':
            data = data.filter(DataShowFirstPageFirstWordCorrectRate.corpus_version == corpus_version)

        count = data.count()
        data_ = data.order_by(
            desc(DataShowFirstPageFirstWordCorrectRate.id)).limit(page_size).offset((page_index - 1) * page_size).all()
        data = cls.query_all_json(data_)
        fields = DataShowFieldsBusiness.query_all_data()
        for d in data:
            for field in list_of_fields:
                d[field] = fields.get(str(d[field]))
            if d['creator']:
                d['creator_nickname'] = user_infos.get(int(d['creator']), {}).get('nickname')
            else:
                d['creator_nickname'] = ''
        return data, count

    @classmethod
    def disable_others(cls, apk_version_id, show_in_chart):
        if show_in_chart == 0:
            datas = DataShowFirstPageFirstWordCorrectRate.query.filter(
                DataShowFirstPageFirstWordCorrectRate.apk_version == apk_version_id,
                DataShowFirstPageFirstWordCorrectRate.show_in_chart == 0).all()
            for data in datas:
                data.show_in_chart = 1
                db.session.add(data)
            db.session.commit()

    @classmethod
    def create(cls, params):
        (data_source, phone_model, apk_version, kernel_version, system_version, thesaurus_version, corpus_version,
         key_9_and_26, first_word_correct_rate, first_page_correct_rate, comment, show_in_chart) = params
        cls.disable_others(apk_version, show_in_chart)
        data_show_response = DataShowFirstPageFirstWordCorrectRate(
            data_source=data_source,
            phone_model=phone_model,
            apk_version=apk_version,
            kernel_version=kernel_version,
            system_version=system_version,
            thesaurus_version=thesaurus_version,
            corpus_version=corpus_version,
            key_9_and_26=key_9_and_26,
            first_word_correct_rate=first_word_correct_rate,
            first_page_correct_rate=first_page_correct_rate,
            creator=g.userid,
            comment=comment,
            status=0,
            show_in_chart=show_in_chart,
        )
        try:
            db.session.add(data_show_response)
            db.session.commit()
        except Exception:
            raise CreateObjectException('创建数据失败！')
        return 0

    @classmethod
    def update(cls, id, params):
        (data_source, phone_model, apk_version, kernel_version, system_version, thesaurus_version, corpus_version,
         key_9_and_26, first_word_correct_rate, first_page_correct_rate, comment, show_in_chart) = params

        cls.disable_others(apk_version, show_in_chart)
        data_show = DataShowFirstPageFirstWordCorrectRate.query.get(id)

        if not data_show:
            raise CannotFindObjectException('数据不存在！')
        data_show.data_source = data_source
        data_show.phone_model = phone_model
        data_show.apk_version = apk_version
        data_show.kernel_version = kernel_version
        data_show.system_version = system_version
        data_show.thesaurus_version = thesaurus_version
        data_show.corpus_version = corpus_version
        data_show.key_9_and_26 = key_9_and_26
        data_show.first_word_correct_rate = first_word_correct_rate
        data_show.first_page_correct_rate = first_page_correct_rate
        data_show.comment = comment
        data_show.show_in_chart = show_in_chart
        try:
            db.session.add(data_show)
            db.session.commit()
        except Exception:
            raise CreateObjectException('更新数据失败！')
        return 0

    @classmethod
    def delete(cls, id):
        data_show_response = DataShowFirstPageFirstWordCorrectRate.query.get(id)
        data_show_response.status = 1
        try:
            db.session.add(data_show_response)
            db.session.commit()
        except Exception:
            raise CreateObjectException('删除数据失败！')
        return 0


class DataShowResponseLogBusiness(object):

    @classmethod
    def _query(cls):
        return DataShowResponseLog.query.add_columns(
            DataShowResponseLog.id.label('id'),
            DataShowResponseLog.data_source.label('data_source'),
            DataShowResponseLog.phone_model.label('phone_model'),
            DataShowResponseLog.apk_version.label('apk_version'),
            DataShowResponseLog.kernel_version.label('kernel_version'),
            DataShowResponseLog.system_version.label('system_version'),
            DataShowResponseLog.thesaurus_version.label('thesaurus_version'),
            DataShowResponseLog.corpus_version.label('corpus_version'),
            DataShowResponseLog.key_9_kernel_click_time_average.label('key_9_kernel_click_time_average'),
            DataShowResponseLog.key_26_kernel_click_time_average.label('key_26_kernel_click_time_average'),
            DataShowResponseLog.key_9_kernel_response_time.label('key_9_kernel_response_time'),
            DataShowResponseLog.key_26_kernel_response_time.label('key_26_kernel_response_time'),
            DataShowResponseLog.cpu_average.label('cpu_average'),
            DataShowResponseLog.ram_average.label('ram_average'),
            DataShowResponseLog.battery_use.label('battery_use'),
            DataShowResponseLog.creator.label('creator'),
            DataShowResponseLog.comment.label('comment'),
            func.date_format(
                DataShowResponseLog.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            DataShowResponseLog.show_in_chart.label('show_in_chart'),
        )

    @classmethod
    @transfer2json('?id|!data_source|!phone_model|!apk_version|!kernel_version|!system_version|!thesaurus_version'
                   '|!corpus_version|!key_9_kernel_click_time_average|!key_26_kernel_click_time_average'
                   '|!key_9_kernel_response_time|!key_26_kernel_response_time|!cpu_average|!ram_average|!battery_use'
                   '|!creator|!comment|!creation_time|!show_in_chart')
    def query_all_json(cls, data):
        return data

    @classmethod
    def query_chart_data(cls, date_time):
        data = cls._query().filter(
            DataShowResponseLog.status == DataShowResponseLog.ACTIVE,
        )
        if date_time == '0':
            data = data.filter(
                DataShowResponseLog.show_in_chart == DataShowResponseLog.ACTIVE).all()
        else:
            if date_time == '1':  # senven_days
                day = 7
            elif date_time == '2':  # one_month
                day = 30
            end_time = datetime.now().strftime('%Y-%m-%d')
            begin_time = datetime.strptime(end_time, "%Y-%m-%d") - timedelta(days=day)
            data = data.filter(
                DataShowResponseLog.creation_time.between(begin_time, end_time+" 23:00:00")
            ).group_by(DataShowResponseLog.apk_version).all()

        list_of_fields = ['data_source', 'phone_model', 'apk_version', 'kernel_version', 'system_version',
                          'thesaurus_version', 'corpus_version']
        fields = DataShowFieldsBusiness.query_all_data()
        data = cls.query_all_json(data)
        for d in data:
            for field in list_of_fields:
                d[field] = fields.get(str(d[field]))
        return data

    @classmethod
    def query_all_data(cls, page_size, page_index):
        data_source = request.args.get('data_source', '')
        phone_model = request.args.get('phone_model', '')
        apk_version = request.args.get('apk_version', '')
        kernel_version = request.args.get('kernel_version', '')
        system_version = request.args.get('system_version', '')
        thesaurus_version = request.args.get('thesaurus_version', '')
        corpus_version = request.args.get('corpus_version', '')
        list_of_fields = ['data_source', 'phone_model', 'apk_version', 'kernel_version', 'system_version',
                          'thesaurus_version', 'corpus_version']

        user_infos = {user.get('userid'): user
                      for user in user_trpc.requests(method='get', path='/user', query={'base_info': True})}
        data = cls._query().filter(
            DataShowResponseLog.status == DataShowResponseLog.ACTIVE)

        if data_source != '':
            data = data.filter(DataShowResponseLog.data_source == data_source)
        if phone_model != '':
            data = data.filter(DataShowResponseLog.phone_model == phone_model)
        if apk_version != '':
            data = data.filter(DataShowResponseLog.apk_version == apk_version)
        if kernel_version != '':
            data = data.filter(DataShowResponseLog.kernel_version == kernel_version)
        if system_version != '':
            data = data.filter(DataShowResponseLog.system_version == system_version)
        if thesaurus_version != '':
            data = data.filter(DataShowResponseLog.thesaurus_version == thesaurus_version)
        if corpus_version != '':
            data = data.filter(DataShowResponseLog.corpus_version == corpus_version)

        count = data.count()
        data_ = data.order_by(
            desc(DataShowResponseLog.id)).limit(page_size).offset((page_index - 1) * page_size).all()
        data = cls.query_all_json(data_)
        fields = DataShowFieldsBusiness.query_all_data()
        for d in data:
            for field in list_of_fields:
                d[field] = fields.get(str(d[field]))
            if d['creator']:
                d['creator_nickname'] = user_infos.get(int(d['creator']), {}).get('nickname')
            else:
                d['creator_nickname'] = ''

        return data, count

    @classmethod
    def disable_others(cls, apk_version_id, show_in_chart):
        if show_in_chart == 0:
            datas = DataShowResponseLog.query.filter(
                DataShowResponseLog.apk_version == apk_version_id,
                DataShowResponseLog.show_in_chart == 0).all()
            for data in datas:
                data.show_in_chart = 1
                db.session.add(data)
            db.session.commit()

    @classmethod
    def create(cls, params):
        (data_source, phone_model, apk_version, kernel_version, system_version, thesaurus_version, corpus_version,
         key_9_kernel_click_time_average, key_26_kernel_click_time_average, key_9_kernel_response_time,
         key_26_kernel_response_time, cpu_average, ram_average, battery_use, comment, show_in_chart) = params
        cls.disable_others(apk_version, show_in_chart)
        data_show_response = DataShowResponseLog(
            data_source=data_source,
            phone_model=phone_model,
            apk_version=apk_version,
            kernel_version=kernel_version,
            system_version=system_version,
            thesaurus_version=thesaurus_version,
            corpus_version=corpus_version,
            key_9_kernel_click_time_average=key_9_kernel_click_time_average,
            key_26_kernel_click_time_average=key_26_kernel_click_time_average,
            key_9_kernel_response_time=key_9_kernel_response_time,
            key_26_kernel_response_time=key_26_kernel_response_time,
            ram_average=ram_average,
            cpu_average=cpu_average,
            battery_use=battery_use,
            creator=g.userid,
            comment=comment,
            status=0,
            show_in_chart=show_in_chart,
        )
        try:
            db.session.add(data_show_response)
            db.session.commit()
        except Exception:
            raise CreateObjectException('创建数据失败！')
        return 0

    @classmethod
    def update(cls, id, params):
        (data_source, phone_model, apk_version, kernel_version, system_version, thesaurus_version, corpus_version,
         key_9_kernel_click_time_average, key_26_kernel_click_time_average, key_9_kernel_response_time,
         key_26_kernel_response_time, cpu_average, ram_average, battery_use, comment, show_in_chart) = params

        data_show = DataShowResponseLog.query.get(id)
        cls.disable_others(apk_version, show_in_chart)
        if not data_show:
            raise CannotFindObjectException('数据不存在！')

        data_show.data_source = data_source
        data_show.phone_model = phone_model
        data_show.apk_version = apk_version
        data_show.kernel_version = kernel_version
        data_show.system_version = system_version
        data_show.thesaurus_version = thesaurus_version
        data_show.corpus_version = corpus_version
        data_show.key_9_kernel_click_time_average = key_9_kernel_click_time_average
        data_show.key_26_kernel_click_time_average = key_26_kernel_click_time_average
        data_show.key_9_kernel_response_time = key_9_kernel_response_time
        data_show.key_26_kernel_response_time = key_26_kernel_response_time
        data_show.ram_average = ram_average
        data_show.cpu_average = cpu_average
        data_show.battery_use = battery_use
        data_show.comment = comment
        data_show.show_in_chart = show_in_chart

        try:
            db.session.add(data_show)
            db.session.commit()
        except Exception:
            raise CreateObjectException('更新数据失败！')
        return 0

    @classmethod
    def delete(cls, id):
        data_show_response = DataShowResponseLog.query.get(id)
        data_show_response.status = 1
        try:
            db.session.add(data_show_response)
            db.session.commit()
        except Exception:
            raise CreateObjectException('删除数据失败！')
        return 0
