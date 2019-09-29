from flask import current_app
from sqlalchemy import func, desc

from apps.autotest.models.monkey import MonkeyDeviceStatus
from apps.autotest.models.performance import PerformanceTestLog, PerformanceTest
from library.api.db import db
from library.api.transfer import transfer2json


class PerformanceTestLogBusiness(object):

    @classmethod
    def _query(cls):
        return PerformanceTestLog.query.add_columns(
            PerformanceTestLog.id.label('id'),
            PerformanceTestLog.performance_test_id.label('performance_test_id'),
            PerformanceTestLog.cpu.label('cpu'),
            PerformanceTestLog.rss.label('rss'),
            PerformanceTestLog.heap_size.label('heap_alloc'),
            PerformanceTestLog.heap_alloc.label('heap_size'),
            func.date_format(PerformanceTestLog.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(PerformanceTestLog.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
        )

    @classmethod
    @transfer2json(
        '?id|!performance_test_id|!cpu|!rss|!heap_alloc|!heap_size|!creation_time'
    )
    def query_all_json(cls, limit, offset):
        ret = cls._query().order_by(desc(PerformanceTestLog.id)).limit(limit).offset(offset).all()
        return ret

    @classmethod
    @transfer2json(
        '?id|!performance_test_id|!cpu|!rss|!heap_alloc|!heap_size|!creation_time'
    )
    def query_json_by_performance_test_id(cls, performance_test_id, ):
        ret = cls._query().filter(PerformanceTestLog.performance_test_id == performance_test_id
                                  ).order_by(desc(PerformanceTestLog.id)).all()
        return ret

    @classmethod
    def create(cls, performance_test_id, cpu, rss, heap_size, heap_alloc):
        performance_test_log = PerformanceTestLog(
            performance_test_id=performance_test_id,
            cpu=cpu,
            rss=rss,
            heap_alloc=heap_alloc,
            heap_size=heap_size,
        )

        db.session.add(performance_test_log)
        db.session.commit()
        return 0, "success"

    @classmethod
    def calculate_all(cls, performance_test_id):
        infos = {
            "rss_top": 0,
            "rss_average": 0,
            "cpu_top": 0,
            "cpu_average": 0,
            "heap_alloc_top": 0,
            "heap_alloc_average": 0,
            "heap_size_top": 0,
            "heap_size_average": 0
        }
        test_log_infos = PerformanceTestLog.query.filter(
            PerformanceTestLog.performance_test_id == performance_test_id).all()
        count = 0
        for test_log in test_log_infos:
            infos['rss_top'] = max(test_log.rss, infos['rss_top'])
            infos['rss_average'] += test_log.rss
            infos['cpu_top'] = max(test_log.cpu, infos['cpu_top'])
            infos['cpu_average'] += test_log.cpu
            infos['heap_alloc_top'] = max(test_log.heap_alloc, infos['heap_alloc_top'])
            infos['heap_alloc_average'] += test_log.heap_alloc
            infos['heap_size_top'] = max(test_log.heap_size, infos['heap_size_top'])
            infos['heap_size_average'] += test_log.heap_size
            count += 1

        infos['rss_average'] = infos['rss_average'] / count if count > 0 else 0
        infos['cpu_average'] = infos['cpu_average'] / count if count > 0 else 0
        infos['heap_alloc_average'] = infos['heap_alloc_average'] / count if count > 0 else 0
        infos['heap_size_average'] = infos['heap_size_average'] / count if count > 0 else 0

        return infos


class PerformanceTestBusiness(object):
    @classmethod
    def _query(cls):
        return PerformanceTest.query.add_columns(
            PerformanceTest.id.label('id'),
            PerformanceTest.performance_id.label('performance_id'),
            PerformanceTest.run_type.label('run_type'),
            PerformanceTest.run_time.label('run_time'),
            PerformanceTest.cpu_average.label('cpu_average'),
            PerformanceTest.cpu_top.label('cpu_top'),
            PerformanceTest.rss_average.label('rss_average'),
            PerformanceTest.rss_top.label('rss_top'),
            PerformanceTest.heap_size_average.label('heap_size_average'),
            PerformanceTest.heap_size_top.label('heap_size_top'),
            PerformanceTest.heap_alloc_average.label('heap_alloc_average'),
            PerformanceTest.heap_alloc_top.label('heap_alloc_top'),
            func.date_format(PerformanceTest.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(PerformanceTest.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
        )

    @classmethod
    @transfer2json(
        '?id|!performance_id|!run_type|!run_time|!cpu_average|!cpu_top|!rss_top|!rss_average|'
        '!heap_size_average|!heap_size_top|!heap_alloc_average|!heap_alloc_top|!creation_time|!modified_time'
    )
    def query_all_json(cls, limit, offset):
        ret = cls._query().order_by(desc(PerformanceTest.id)).limit(limit).offset(offset).all()
        return ret

    @classmethod
    @transfer2json(
        '?id|!performance_id|!run_type|!run_time|!cpu_average|!cpu_top|!rss_top|!rss_average|'
        '!heap_size_average|!heap_size_top|!heap_alloc_average|!heap_alloc_top|!creation_time|!modified_time'
    )
    def query_json_by_performance_id(cls, performance_id):
        ret = cls._query().filter(PerformanceTest.performance_id == performance_id
                                  ).order_by(desc(PerformanceTest.id)).all()
        return ret

    @classmethod
    @transfer2json(
        '?id|!performance_id|!run_type|!run_time|!cpu_average|!cpu_top|!rss_top|!rss_average|'
        '!heap_size_average|!heap_size_top|!heap_alloc_average|!heap_alloc_top|!creation_time|!modified_time'
    )
    def query_json_by_performance_id_and_type(cls, performance_id, run_type):
        ret = cls._query().filter(PerformanceTest.performance_id == performance_id,
                                  PerformanceTest.run_type == run_type).all()
        return ret

    @classmethod
    def create(cls, performance_id, run_type, run_time):

        performance_temp = PerformanceTest.query.filter(PerformanceTest.performance_id == performance_id,
                                                        PerformanceTest.run_type == run_type,
                                                        PerformanceTest.run_time == run_time).first()
        if performance_temp:
            return performance_temp.id

        performance_test = PerformanceTest(
            performance_id=performance_id,
            # setup_info=setup_info,
            # base_app=base_app,
            # key_type=key_type,
            run_time=run_time,
            run_type=run_type,
            cpu_average=0,
            cpu_top=0,
            rss_average=0,
            rss_top=0,
            heap_size_average=0,
            heap_size_top=0,
            heap_alloc_average=0,
            heap_alloc_top=0,
        )
        db.session.add(performance_test)
        db.session.flush()
        rev_id = performance_test.id
        db.session.commit()
        return rev_id

    @classmethod
    def update(cls, id, cpu_average, cpu_top, rss_average, rss_top, heap_size_average, heap_size_top,
               heap_alloc_average, heap_alloc_top):

        performance_test = PerformanceTest.query.get(id)
        performance_test.cpu_average = cpu_average
        performance_test.cpu_top = cpu_top
        performance_test.rss_average = rss_average
        performance_test.rss_top = rss_top
        performance_test.heap_size_average = heap_size_average
        performance_test.heap_size_top = heap_size_top
        performance_test.heap_alloc_average = heap_alloc_average
        performance_test.heap_alloc_top = heap_alloc_top

        db.session.add(performance_test)
        db.session.commit()
        return 0, "success"

    @classmethod
    def calculate_average(cls, performance_test_id):
        try:
            infos = PerformanceTestLogBusiness.calculate_all(performance_test_id)
            cls.update(performance_test_id, infos.get('cpu_average'), infos.get('cpu_top'), infos.get('rss_average'),
                       infos.get('rss_top'), infos.get('heap_size_average'), infos.get('heap_size_top'),
                       infos.get('heap_alloc_average'), infos.get('heap_alloc_top'))
            return 0
        except Exception as e:
            current_app.logger.error(e)
            return 102

    @classmethod
    def get_all_name(cls, performance_id):
        try:
            name_list = []
            name_temp = []
            performance_tests = PerformanceTest.query.add_columns(
                PerformanceTest.id.label('id'),
                PerformanceTest.run_type.label('run_type')
            ).filter(PerformanceTest.performance_id == performance_id).all()
            for performance_test in performance_tests:
                if performance_test.run_type not in name_temp:
                    name_temp.append(performance_test.run_type)
                    name_list.append(
                        {
                            'id': performance_test.id,
                            'name': performance_test.run_type
                        }
                    )
            return name_list
        except Exception as e:
            current_app.logger.error(e)

    @classmethod
    def get_all_name_by_monkey_id(cls, performance_id):
        try:
            name_list = []
            name_temp = []
            device = MonkeyDeviceStatus.query.filter(MonkeyDeviceStatus.monkey_id == performance_id).first()

            performance_tests = PerformanceTest.query.add_columns(
                PerformanceTest.id.label('id'),
                PerformanceTest.run_type.label('run_type')
            ).filter(PerformanceTest.performance_id == device.id).all()
            for performance_test in performance_tests:
                if performance_test.run_type not in name_temp:
                    name_temp.append(performance_test.run_type)
                    name_list.append(performance_test.run_type)
            return name_list
        except Exception as e:
            current_app.logger.error(e)
