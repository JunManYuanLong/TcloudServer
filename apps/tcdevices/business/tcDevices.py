import datetime
import json
import math
import time
import uuid

import requests
from flask import request, g, current_app
from sqlalchemy import desc, func

from apps.auth.models.users import User
from apps.autotest.business.monkey import MonkeyDeviceUsingBusiness
from apps.autotest.models.monkey import MonkeyDeviceUsing
from apps.public.models.public import Config
from apps.tcdevices.models.tcDevices import TcDevices, TcDevicesnInfo
from library.api.db import db
from library.api.transfer import transfer2json
from public_config import TCDEVICE_PIC


class TcDevicesBusiness(object):
    @classmethod
    def devices_info(cls, use_type, manufacturer, model, platform, version, serial, resolution, devices_uuid):
        try:
            user_id = g.userid if g.userid else None
            use_time = ''
            current_app.logger.info("user_id:" + str(user_id))
            temp_uuid = str(uuid.uuid1())
            if use_type == 1:
                devices = TcDevices(
                    uuid=temp_uuid,
                    user_id=user_id,
                    use_type=use_type,
                    manufacturer=manufacturer,
                    model=model,
                    platform=platform,
                    version=version,
                    serial=serial,
                    resolution=resolution,
                    use_time=use_time,
                )
                ret = TcDevicesnInfo.query.filter(TcDevicesnInfo.serial == serial).first()
                if ret and devices_uuid != '1':
                    ret.times = int(ret.times) + 1
                    db.session.add(ret)
                db.session.add(devices)
                db.session.commit()
                return 0, temp_uuid
            if use_type == 2:
                devices_ret = TcDevices.query.filter(TcDevices.uuid == devices_uuid, TcDevices.user_id == user_id,
                                                     TcDevices.use_type == 1).order_by(desc(TcDevices.id)).first()
                # 异常数据，直接返回
                if not devices_ret:
                    return 0, []
                uuid_ret = TcDevices.query.filter(TcDevices.uuid == devices_uuid, TcDevices.use_type == 2).first()
                start_use_time = devices_ret.creation_time
                use_time = datetime.datetime.now() - start_use_time
                use_time = str(int(math.ceil(use_time.seconds / 60.0)))
                now_time = int(time.time())
                current_app.logger.info('use_time:' + str(use_time))
                if int(use_time) <= 0 or int(use_time) == 1440:
                    use_time = 1
                # 本次使用第一次上报
                current_app.logger.info(uuid_ret)
                if not uuid_ret:
                    devices = TcDevices(
                        uuid=devices_uuid,
                        user_id=user_id,
                        use_type=use_type,
                        using=now_time,
                        manufacturer=manufacturer,
                        model=model,
                        platform=platform,
                        version=version,
                        serial=serial,
                        resolution=resolution,
                        use_time=use_time,
                    )
                    db.session.add(devices)
                    db.session.commit()
                    return 0, []
                utime = 0
                # 本次使用非第一次上报，不插入新数据，只更新时间
                if uuid_ret:
                    current_app.logger.info('本次使用非第一次上报')
                    utime = uuid_ret.use_time
                    uuid_ret.use_time = use_time
                    uuid_ret.using = now_time
                    db.session.add(uuid_ret)
                # 更新信息表的时间，时长相加
                ret = TcDevicesnInfo.query.filter(TcDevicesnInfo.serial == serial).first()
                if ret:
                    ret_time = int(ret.use_time)
                    temp_time = int(int(use_time) - int(utime))
                    if temp_time > 0:
                        ret_time = ret_time + temp_time
                    ret.use_time = ret_time
                    db.session.add(ret)
                db.session.commit()
                return 0, []

        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
            return 102, []

    @classmethod
    def get_devices(cls):
        now_time = int(time.time())
        now_devices = TcDevices.query.filter(TcDevices.use_type == 2, TcDevices.using != 0).all()
        stf_rets = Config.query.add_columns(
            Config.content.label('content'),
            Config.module_type).filter(
            Config.module == 'stf').all()
        stf_token, stf_devices = None, None
        for stf_ret in stf_rets:
            if stf_ret.module_type == 3:
                stf_token = json.loads(stf_ret.content)
            elif stf_ret.module_type == 1:
                stf_devices = json.loads(stf_ret.content)

        session_list = []
        for now_device in now_devices:
            diff_time = int(now_time - now_device.using)
            current_app.logger.info(
                'now_time:{}\nold_time:{}\ndiff_time:{}'.format(str(now_time), str(now_device.using), str(diff_time)))
            if diff_time >= 6:
                cls.disconnect_devices(now_device.serial, stf_token)
                now_device.using = 0
                session_list.append(now_device)

        if session_list:
            for i in session_list:
                db.session.add(i)
            db.session.commit()

        devices_info = cls.stf_devices(stf_devices)
        ret = TcDevicesnInfo.query.all()
        devices = devices_info['devices']
        monkey_devices = MonkeyDeviceUsingBusiness.mdyb_query().all()
        devices_serial_list = [ret_device.serial for ret_device in ret]
        ret_nickname = User.query.add_columns(
            User.nickname,
            User.name).all()
        nickname_dict = {i.name: i.nickname for i in ret_nickname}
        tcdevicesn_info_session_list = []
        for i in range(len(devices)):
            if devices[i]['serial'] not in devices_serial_list:
                try:
                    comment = devices[i]['manufacturer'] + devices[i]['model']
                except KeyError:
                    comment = ''
                    current_app.logger.info("设备manufacturer找不到：" + str(devices[i]['serial']))
                tc = TcDevicesnInfo(
                    serial=devices[i]['serial'],
                    times=0,
                    use_time=0,
                    pic=TCDEVICE_PIC,
                    comment=comment
                )
                tcdevicesn_info_session_list.append(tc)
            devices[i]['times'] = 0
            devices[i]['use_time'] = 0
            devices[i]['nickname'] = ''
            for ret_device in ret:
                if devices[i]['serial'] == ret_device.serial:
                    devices[i]['times'] = ret_device.times
                    devices[i]['use_time'] = ret_device.use_time
                    devices[i]['pic'] = ret_device.pic
            if devices[i]['owner'] and 'name' in devices[i]['owner']:
                devices[i]['nickname'] = nickname_dict.get(devices[i]['owner']['name'], devices[i]['owner']['name'])

            for monkey_device in monkey_devices:
                if monkey_device.serial == devices[i].get('serial') and monkey_device.using == MonkeyDeviceUsing.ACTIVE:
                    devices[i]['nickname'] = 'Monkey'
                    devices[i]['owner'] = {
                        'name': 'Monkey',
                        'group': 'Monkey',
                        'email': 'Monkey'
                    }
        if tcdevicesn_info_session_list:
            for i in tcdevicesn_info_session_list:
                db.session.add(i)
            db.session.commit()
        return devices

    @classmethod
    def stf_devices(cls, stf_devices):
        current_app.logger.info(json.dumps(stf_devices, ensure_ascii=False))
        url = stf_devices['URL']
        headers = stf_devices['headers']
        ret = requests.get(url, headers=headers)
        return ret.json()

    @classmethod
    def stf_token(cls):
        name = request.args.get('name')
        stf_token = Config.query.add_columns(Config.content.label('content')).filter(
            Config.module == 'stf',
            Config.module_type == 2).first()
        stf_token = json.loads(stf_token.content)
        current_app.logger.info(json.dumps(stf_token, ensure_ascii=False))
        url = stf_token['URL'] + '?name=' + name
        ret = requests.get(url)
        ret = json.loads(ret.content)
        current_app.logger.info(json.dumps(ret, ensure_ascii=False))
        return ret

    @classmethod
    def disconnect_devices(cls, serial, stf_token=None):
        try:
            current_app.logger.info(f'--------serial-------\n{serial}\n{json.dumps(stf_token, ensure_ascii=False)}')
            if not stf_token:
                stf_token = Config.query.add_columns(Config.content.label('content')).filter(
                    Config.module == 'stf',
                    Config.module_type == 3).first()
                stf_token = json.loads(stf_token.content)
            url = stf_token['URL']
            if serial:
                url += serial
            headers = stf_token['headers']
            ret = requests.delete(url, headers=headers)
            # ret = json.loads(ret.content)
            ret = ret.json()
            current_app.logger.info(json.dumps(ret, ensure_ascii=False))
            return ret
        except Exception as e:
            current_app.logger.error(e)
            return []

    @classmethod
    def _query(cls):
        return TcDevicesnInfo.query.add_columns(
            TcDevicesnInfo.id.label('id'),
            TcDevicesnInfo.comment.label('comment'),
            TcDevicesnInfo.serial.label('serial'),
            TcDevicesnInfo.times.label('times'),
            TcDevicesnInfo.use_time.label('use_time'),
        )

    @classmethod
    @transfer2json('?id|!comment|!serial|!times|!use_time')
    def query_all_json(cls):
        return cls._query().filter().order_by(desc(TcDevicesnInfo.times), desc(TcDevicesnInfo.use_time)).all()

    @classmethod
    def _user_query(cls):
        return TcDevices.query.outerjoin(
            User, User.id == TcDevices.user_id).add_columns(
            TcDevices.id.label('id'),
            TcDevices.manufacturer.label('manufacturer'),
            TcDevices.model.label('model'),
            TcDevices.platform.label('platform'),
            TcDevices.version.label('version'),
            TcDevices.serial.label('serial'),
            TcDevices.resolution.label('resolution'),
            TcDevices.use_time.label('use_time'),
            func.date_format(TcDevices.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            User.id.label('user_id'),
            User.nickname.label('user_name'),
        )

    @classmethod
    @transfer2json(
        '?id|!manufacturer|!model|!platform|!version|!serial|!resolution|!use_time|!user_id|!user_name|!creation_time')
    def query_user_all_json(cls):
        user_id = request.args.get('userid')
        ret = cls._user_query().filter(TcDevices.using == 0, TcDevices.use_type == 2)
        if user_id:
            ret = ret.filter(TcDevices.user_id == user_id)
        return ret.order_by(desc(TcDevices.id)).all()

    @classmethod
    def query_dashboard(cls):
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        devices_use_time = TcDevices.query.add_columns(
            func.date_format(TcDevices.creation_time, "%Y-%m-%d").label('creation_time'),
            func.sum(TcDevices.use_time).label('count')).filter(
            TcDevices.using == 0, TcDevices.use_type == 2)
        if start_time and end_time:
            devices_use_time = devices_use_time.filter(
                TcDevices.creation_time.between(start_time, end_time + " 23:59:59"))
        devices_use_time = devices_use_time.group_by(func.date_format(TcDevices.creation_time, "%Y-%m-%d")).order_by(
            desc(func.date_format(TcDevices.creation_time, "%Y-%m-%d"))).all()
        devices_use_time = [dict(i) for i in map(lambda x: zip(('date', 'use_time'), x),
                                                 zip([i.creation_time for i in devices_use_time],
                                                     [int(i.count) for i in devices_use_time]))]

        devices_times = TcDevices.query.add_columns(
            func.date_format(TcDevices.creation_time, "%Y-%m-%d").label('creation_time'),
            func.count('*').label('count')).filter(TcDevices.using == 0, TcDevices.use_type == 2)
        if start_time and end_time:
            devices_times = devices_times.filter(TcDevices.creation_time.between(start_time, end_time + " 23:59:59"))
        devices_times = devices_times.group_by(func.date_format(TcDevices.creation_time, "%Y-%m-%d")).order_by(
            desc(func.date_format(TcDevices.creation_time, "%Y-%m-%d"))).all()
        devices_times = [dict(i) for i in map(lambda x: zip(('date', 'times'), x),
                                              zip([i.creation_time for i in devices_times],
                                                  [i.count for i in devices_times]))]

        detail = [dict(devices_use_time=devices_use_time, devices_times=devices_times, )]
        return detail
