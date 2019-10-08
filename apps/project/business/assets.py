import json
import traceback
from datetime import timedelta

from flask import request, g, current_app
from sqlalchemy import desc, func

from apps.auth.models.users import User
from apps.project.business.credit import CreditBusiness
from apps.project.models.assets import Phone, PhoneRecord, VirtualAsset, PhoneBorrow
from apps.project.models.credit import Credit
from apps.public.models.public import Config
from library.api.db import db
from library.api.transfer import transfer2json
from library.notification import notification
from library.trpc import Trpc

user_trpc = Trpc('auth')


class PhoneBusiness(object):
    public_trpc = Trpc('public')
    user_trpc = Trpc('auth')
    message_trpc = Trpc('message')

    @classmethod
    def _query(cls):
        return Phone.query.add_columns(
            Phone.id.label('id'),
            Phone.name.label('name'),
            Phone.asset_id.label('asset_id'),
            Phone.vendor.label('vendor'),
            Phone.device_number.label('device_number'),
            Phone.os.label('os'),
            Phone.cpu.label('cpu'),
            Phone.core.label('core'),
            Phone.ram.label('ram'),
            Phone.rom.label('rom'),
            Phone.resolution.label('resolution'),
            Phone.buy_date.label('buy_date'),
            Phone.region.label('region'),
            Phone.status.label('status'),
            Phone.borrow_id.label('borrow_id'),
            Phone.creator_id.label('creator_id'),
            Phone.device_source.label('device_source'),
            Phone.device_belong.label('device_belong'),
        )

    @classmethod
    @transfer2json(
        '?id|!name|!asset_id|!vendor|!device_number|!os|!cpu|!core|!ram|!rom|!resolution|!buy_date|!region|!status|'
        '!borrow_id|!creator_id|!device_source|!device_belong'
    )
    def query_all_json(cls, page_size, page_index):
        ret = cls._query().filter(
            Phone.status == Phone.ACTIVE).order_by(
            desc(Phone.id)).limit(int(page_size)).offset(
            int(page_index - 1) * int(page_size)).all()
        return ret

    @classmethod
    def query_all_count(cls):
        count = cls._query().filter(Phone.status == Phone.ACTIVE).count()
        return count

    @classmethod
    @transfer2json(
        '?id|!name|!asset_id|!vendor|!device_number|!os|!cpu|!core|!ram|!rom|!resolution|!buy_date|!region|!status|'
        '!borrow_id|!creator_id|!device_source|!device_belong'
    )
    def query_json_by_id(cls, pid):
        return cls._query().filter(
            Phone.id == pid, Phone.status == Phone.ACTIVE).all()

    @classmethod
    def get_phone_by_id(cls, pid):
        users = user_trpc.requests(method='get', path='/user')
        phone = cls.query_json_by_id(pid)

        if len(phone) <= 0:
            return 101, 'phone not exist!'
        phone = phone[0]
        for user in users:
            if user.get('userid') == phone.get('creator_id'):
                phone['creator_nickname'] = user.get('nickname')
            if user.get('userid') == phone.get('borrow_id'):
                phone['borrow_nickname'] = user.get('nickname')
        return 0, [phone]

    @classmethod
    def send_message(cls, user_list, creator, text):
        if cls.message_trpc.requests('post', '/message',
                                     body={'send_id': creator, 'rec_id': user_list, 'content': text}):
            current_app.logger.info('发送站内信成功')
        else:
            current_app.logger.info('发送站内信失败')

    @classmethod
    def get_phone_all(cls, page_size, page_index):

        # 通过设备名称进行搜索
        name = request.args.get('name', '')
        # 通过制造商进行搜索
        vendor = request.args.get('vendor', '')
        # 通过系统进行搜索
        os = request.args.get('os', '')
        # 通过分辨率进行搜索
        resolution = request.args.get('resolution', '')
        # 通过借用人进行搜索
        borrower_id = request.args.get('borrower_id')
        # 通过持有人进行搜索
        creator_id = request.args.get('creator_id')
        # 通过 归属
        device_belong = request.args.get('device_belong', '')
        # 通过 来源
        device_source = request.args.get('device_source', '')
        # 通过 归属人
        # 获取所有 手机设备列表
        phones, count = cls.search_phone_all(name, vendor, os, resolution, borrower_id, device_belong,
                                             device_source, creator_id, page_size, page_index)
        # 获取所有用户的 基本信息
        users = {int(user.get('userid')): user
                 for user in user_trpc.requests(method='get', path='/user', query={'base_info': True})}
        # 获取所有借用关系列表
        phone_borrows = {phone_borrow.phone_id: phone_borrow for phone_borrow in PhoneBorrow.query.all()}
        data = []
        for phone in phones:
            phone_borrow = phone_borrows.get(phone.get('id'))
            if g.userid == phone.get('borrow_id'):
                phone["move_status"] = 1
            else:
                phone["move_status"] = 0

            if PhoneBusiness.in_confirm_status(phone_borrow):
                phone["move_status"] = 2

            if PhoneBusiness.need_confirm_status(phone_borrow):
                phone["confirm_status"] = 0
            else:
                phone["confirm_status"] = 1

            try:
                borrower = users.get(phone.get('borrow_id')).get("nickname")
                creator = users.get(phone.get('creator_id')).get('nickname')

                phone['borrow_nickname'] = borrower
                phone['creator_nickname'] = creator
                # 有此条借用记录
                if phone_borrow:
                    user_list = [int(uid) for uid in phone_borrow.user_list.split(',') if uid != '']
                    # 有需要确认的用户
                    if phone_borrow.confirm_userid != 0:
                        confirm_user_nickname = users.get(phone_borrow.confirm_userid).get('nickname')
                        phone['borrow_status'] = f'[{confirm_user_nickname}] 待接收'
                    # 用户借用列表
                    elif user_list:
                        user_list_temp = [users.get(userid).get('nickname') for userid in user_list]
                        phone['borrow_status'] = f'[{",".join(user_list_temp)}] 申请借用'
                        phone['move_status'] = 3 if phone["move_status"] == 1 else 0
                    # 无借用、确认、归还
                    else:
                        phone['borrow_status'] = f'[{borrower}] 持有'
                else:
                    phone['borrow_status'] = f'[{borrower}] 持有'
            except Exception as e:
                current_app.logger.error(e)
                phone['borrow_status'] = '未知'
                phone['borrow_nickname'] = '未知'

            data.append(phone)
        current_app.logger.info(data)
        return data, count

    @classmethod
    @transfer2json(
        '?id|!name|!asset_id|!vendor|!device_number|!os|!cpu|!core|!ram|!rom|!resolution|!buy_date|!region|!status|'
        '!borrow_id|!creator_id|!device_source|!device_belong'
    )
    def search_phone_json(cls, data):
        return data.all()

    @classmethod
    def search_phone_all(cls, name, vendor, os, resolution, borrower_id, device_belong, device_source, creator_id,
                         page_size, page_index):
        try:

            data_all = cls._query().filter(Phone.status == Phone.ACTIVE)
            if name != '':
                data_all = data_all.filter(Phone.name.like(f'%{name}%'))
            if vendor != '':
                data_all = data_all.filter(Phone.vendor.like(f'%{vendor}%'))
            if os != '':
                data_all = data_all.filter(Phone.os.like(f'%{os}%'))
            if resolution != '':
                data_all = data_all.filter(Phone.resolution.like(f'%{resolution}%'))
            if device_belong != '':
                data_all = data_all.filter(Phone.device_belong.like(f'%{device_belong}%'))
            if device_source != '':
                data_all = data_all.filter(Phone.device_source.like(f'%{device_source}%'))
            if borrower_id:
                data_all = data_all.filter(Phone.borrow_id == borrower_id)
            if creator_id:
                data_all = data_all.filter(Phone.creator_id == creator_id)

            count = data_all.count()
            data = cls.search_phone_json(
                data_all.order_by(desc(Phone.id)).limit(int(page_size)).offset(int(page_index - 1) * int(page_size)))
            return data, count
        except Exception as e:
            current_app.logger.error(e)

    @classmethod
    def get_holder_json(cls):
        # 获取所有持有者的信息
        try:
            data_all = []
            temp = []
            phones = Phone.query.add_columns(Phone.borrow_id.label('borrow_id')).filter(
                Phone.status == Phone.ACTIVE).all()
            for phone in phones:
                if phone.borrow_id not in temp:
                    temp.append(phone.borrow_id)
                    user = cls.user_trpc.requests('get', '/user/{}'.format(phone.borrow_id))[0]
                    data = {
                        'nickname': user.get('nickname'),
                        'id': user.get('userid')
                    }
                    data_all.append(data)
            return data_all
        except Exception as e:
            current_app.logger.error(e)

    @classmethod
    def can_move_status(cls, phone_id):
        # 判断此设备是否归属于当前用户
        phone = Phone.query.get(phone_id)
        if phone and phone.borrow_id == g.userid:
            return True
        else:
            return False

    @classmethod
    def need_confirm_status(cls, phone_borrow):
        # 判断此手机需要是否当前用户确认
        try:
            if phone_borrow is not None:
                if int(phone_borrow.confirm_userid) == g.userid:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return 101, str(e)

    @classmethod
    def in_confirm_status(cls, phone_borrow):
        # 判断此设备是否存在于确认流程中
        try:
            if phone_borrow is not None:
                if int(phone_borrow.confirm_userid) != 0:
                    return True
                return False
            else:
                return False
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return 101, str(e)

    @classmethod
    def qyweixin_email(cls, user_ids, text):
        if not isinstance(user_ids, list):
            user_ids = [user_ids]
        notification.send_notification(user_ids, text, creator=0)
        return 0, 'success'

    @classmethod
    def send_need_confirm_msg(cls, current_phone, phone_current_holder, phone_new_holder):
        deadline = PhoneBusiness.deadline(current_phone)
        new_holder_msg_text = """[TCloud] {} ({})
您有一台设备需要确认接收:
设备 : {}，
资产编号 : {},
原持有人 : {} (微信号: {})
现持有人 : {} (微信号: {})
请及时到系统中确认接收！""".format(phone_new_holder.nickname, phone_new_holder.wx_userid,
                       current_phone.name, current_phone.asset_id, phone_current_holder.nickname,
                       phone_current_holder.wx_userid, phone_new_holder.nickname,
                       phone_new_holder.wx_userid)
        # phone_current_holder 原持有人
        # phone_new_holder 确认人

        ret, msg = PhoneBusiness.qyweixin_email(phone_new_holder.id, new_holder_msg_text)
        return ret, msg

    @classmethod
    def send_cancel_move_msg(cls, current_phone, phone_current_holder, phone_new_holder):
        deadline = PhoneBusiness.deadline(current_phone)
        new_holder_msg_text = """[TCloud] {} ({})
您有一台设备由于超过 3 天没有接收，已被系统退回:
设备 : {}，
资产编号 : {},
现持有人 : {} (微信号: {})
""".format(phone_new_holder.nickname, phone_new_holder.wx_userid, current_phone.name, current_phone.asset_id,
           phone_new_holder.nickname, phone_new_holder.wx_userid)
        # phone_current_holder 原持有人
        # phone_new_holder 确认人

        ret, msg = PhoneBusiness.qyweixin_email(phone_current_holder.id, new_holder_msg_text)
        return ret, msg

    @classmethod
    def send_need_move_msg(cls, current_phone, phone_current_holder):
        new_holder_msg_text = """[TCloud] {} ({})
您有一条借用请求需要处理:
设备 : {}
资产编号 : {}
请及时到系统中处理！
请通过 TCloud->资产->流转 进行转出。""".format(phone_current_holder.nickname, phone_current_holder.wx_userid,
                                   current_phone.name, current_phone.asset_id,
                                   phone_current_holder.wx_userid)

        # phone_current_holder 当前持有人

        ret, msg = PhoneBusiness.qyweixin_email(phone_current_holder.id, new_holder_msg_text)
        return ret, msg

    @classmethod
    def send_create_msg_qywx(cls, current_phone, phone_holder):
        msg_text = """[TCloud] {} ({})
您拥有了一台新的设备:
设备 : {}，
资产编号 : {},
持有人 : {} (微信号: {})""".format(phone_holder.nickname, phone_holder.wx_userid,
                             current_phone.name, current_phone.asset_id, phone_holder.nickname,
                             phone_holder.wx_userid, )

        ret, msg = PhoneBusiness.qyweixin_email(phone_holder.id, msg_text)
        return ret, msg

    @classmethod
    def send_delay_msg_qywx(cls, current_phone, phone_holder):
        deadline = PhoneBusiness.deadline(current_phone)
        msg_text = """[TCloud] {} ({})
您拥有的一台设备需要归还:
设备 : {}，
资产编号 : {},
持有人 : {} (微信号: {})
到期时间: {}
续借 : 请到系统中点击 续借 进行续借
归还 : 请到系统中点击 退回 进行归还
过期 2 天后会根据超时时间扣除信用分！请及时归还！""".format(phone_holder.nickname, phone_holder.wx_userid,
                                     current_phone.name, current_phone.asset_id, phone_holder.nickname,
                                     phone_holder.wx_userid, deadline)

        return PhoneBusiness.qyweixin_email(phone_holder.id, msg_text)

    @classmethod
    def send_move_msg_qywx(cls, current_phone, phone_current_holder, phone_new_holder):
        if phone_new_holder.id == phone_current_holder.id:
            current_app.logger.info('[{}](资产编号:{}) 设备状态未发生状态变化'.format(current_phone.name, current_phone.asset_id))
            return
        current_holder_msg_text = """[TCloud] {} ({})
您的一台设备状态将要发生变化:
设备 : {}，
资产编号 : {},
变化 : 持有人将 由 {} (微信号: {}) 变为 {} (微信号: {})
状态 : 等待接收人确认""".format(phone_current_holder.nickname, phone_current_holder.wx_userid,
                       current_phone.name, current_phone.asset_id, phone_current_holder.nickname,
                       phone_current_holder.wx_userid, phone_new_holder.nickname,
                       phone_new_holder.wx_userid)

        ret, msg = PhoneBusiness.qyweixin_email(phone_current_holder.id, current_holder_msg_text)

        deadline = PhoneBusiness.deadline(current_phone)
        new_holder_msg_text = """[TCloud] {} ({})
您将拥有一台新的设备:
设备 : {}，
资产编号 : {},
原持有人 : {} (微信号: {})
现持有人 : {} (微信号: {})
可持有时间: {} 天
到期时间: {}
请及时到系统中确认接收！""".format(phone_new_holder.nickname, phone_new_holder.wx_userid,
                       current_phone.name, current_phone.asset_id, phone_current_holder.nickname,
                       phone_current_holder.wx_userid,
                       phone_new_holder.nickname, phone_new_holder.wx_userid, Phone.HOLD_DATE, deadline)
        # phone_current_holder 原持有人
        # phone_new_holder 新持有人

        ret, msg = PhoneBusiness.qyweixin_email(phone_new_holder.id, new_holder_msg_text)
        return ret, msg

    @classmethod
    def send_move_confirm_msg_qywx(cls, current_phone, phone_current_holder, phone_new_holder):
        if phone_new_holder.id == phone_current_holder.id:
            current_app.logger.info('[{}](资产编号:{}) 设备状态未发生状态变化'.format(current_phone.name, current_phone.asset_id))
            return
        current_holder_msg_text = """[TCloud] {} ({})
您的一台设备状态发生了变化:
设备 : {}，
资产编号 : {},
变化 : 持有人已 由 {} (微信号: {}) 变为 {} (微信号: {})
状态 : 已接收""".format(phone_current_holder.nickname, phone_current_holder.wx_userid,
                   current_phone.name, current_phone.asset_id, phone_current_holder.nickname,
                   phone_current_holder.wx_userid, phone_new_holder.nickname,
                   phone_new_holder.wx_userid)

        ret, msg = PhoneBusiness.qyweixin_email(phone_current_holder.id, current_holder_msg_text)

        deadline = PhoneBusiness.deadline(current_phone)
        new_holder_msg_text = """[TCloud] {} ({})
您拥有了一台新的设备:
设备 : {}，
资产编号 : {},
原持有人 : {} (微信号: {})
现持有人 : {} (微信号: {})
可持有时间: {} 天
到期时间: {}
状态: 已接收！""".format(phone_new_holder.nickname, phone_new_holder.wx_userid,
                   current_phone.name, current_phone.asset_id, phone_current_holder.nickname,
                   phone_current_holder.wx_userid,
                   phone_new_holder.nickname, phone_new_holder.wx_userid, Phone.HOLD_DATE, deadline)
        # phone_current_holder 原持有人
        # phone_new_holder 新持有人

        ret, msg = PhoneBusiness.qyweixin_email(phone_new_holder.id, new_holder_msg_text)
        return ret, msg

    @classmethod
    def send_return_msg_qywx(cls, current_phone, phone_current_holder, phone_new_holder):
        if phone_new_holder.id == phone_current_holder.id:
            current_app.logger.info('[{}](资产编号:{}) 设备状态未发生状态变化'.format(current_phone.name, current_phone.asset_id))
            return

        current_holder_msg_text = """[TCloud] {} ({})
您归还了一台设备:
设备 : {}，
资产编号 : {},
变化 : 持有人将 由 {} (微信号: {}) 变为 {} (微信号: {})
状态 : 等待接收人确认""".format(phone_current_holder.nickname, phone_current_holder.wx_userid,
                       current_phone.name, current_phone.asset_id,
                       phone_current_holder.nickname,
                       phone_current_holder.wx_userid,
                       phone_new_holder.nickname, phone_new_holder.wx_userid)

        PhoneBusiness.qyweixin_email(phone_current_holder.id, current_holder_msg_text)

        new_holder_msg_text = """[TCloud] {} ({})
您收到别人归还的一台设备:
设备 : {}，
资产编号 : {},
原持有人 : {} (微信号: {})
持有人 : {} (微信号: {})
状态 : 等待确认
请到系统中及时确认接收！""".format(phone_new_holder.nickname, phone_new_holder.wx_userid, current_phone.name,
                       current_phone.asset_id,
                       phone_current_holder.nickname, phone_current_holder.wx_userid,
                       phone_new_holder.nickname, phone_new_holder.wx_userid)

        ret, msg = PhoneBusiness.qyweixin_email(phone_new_holder.id, new_holder_msg_text)
        return ret, msg

    @classmethod
    def send_return_confirm_msg_qywx(cls, current_phone, phone_current_holder, phone_new_holder):
        if phone_new_holder.id == phone_current_holder.id:
            current_app.logger.info('[{}](资产编号:{}) 设备状态未发生状态变化'.format(current_phone.name, current_phone.asset_id))
            return

        current_holder_msg_text = """[TCloud] {} ({})
您成功归还了一台设备:
设备 : {}，
资产编号 : {},
变化 : 持有人已 由 {} (微信号: {}) 变为 {} (微信号: {})
状态 : 接收人已接收""".format(phone_current_holder.nickname, phone_current_holder.wx_userid,
                      current_phone.name, current_phone.asset_id, phone_current_holder.nickname,
                      phone_current_holder.wx_userid,
                      phone_new_holder.nickname, phone_new_holder.wx_userid)

        PhoneBusiness.qyweixin_email(phone_current_holder.id, current_holder_msg_text)

        new_holder_msg_text = """[TCloud] {} ({})
您已接收别人归还的一台设备:
设备 : {}，
资产编号 : {},
原持有人 : {} (微信号: {})
持有人 : {} (微信号: {})
状态 : 您已接收！""".format(phone_new_holder.nickname, phone_new_holder.wx_userid, current_phone.name, current_phone.asset_id,
                     phone_current_holder.nickname, phone_current_holder.wx_userid,
                     phone_new_holder.nickname, phone_new_holder.wx_userid)

        ret, msg = PhoneBusiness.qyweixin_email(phone_new_holder.id, new_holder_msg_text)
        return ret, msg

    @classmethod
    def deadline(cls, current_phone):
        # 根据 phone 最后一条记录计算到期时间
        phone_recorder = PhoneRecord.query.filter(PhoneRecord.phone_id == current_phone.id).order_by(
            PhoneRecord.id.desc()).first()
        deadline = phone_recorder.creation_time + timedelta(days=Phone.HOLD_DATE)  # 到期时间
        return deadline

    @classmethod
    def create(cls, name, asset_id, vendor, device_number, os, cpu, core, ram, rom, resolution, buy_date, region,
               borrow_id, device_source, device_belong, creator_id):
        try:
            t = Phone(
                name=name,
                asset_id=asset_id,
                vendor=vendor,
                device_number=device_number,
                os=os,
                cpu=cpu,
                core=core,
                ram=ram,
                rom=rom,
                resolution=resolution,
                buy_date=buy_date,
                region=region,
                borrow_id=borrow_id or g.userid,
                creator_id=creator_id or g.userid,
                device_source=device_source,
                device_belong=device_belong,
            )
            db.session.add(t)
            db.session.flush()
            PhoneRecordBusiness.create(t, g.userid)
            db.session.commit()
            phone_holder = User.query.get(t.creator_id)

            # 发送企业微信
            PhoneBusiness.send_create_msg_qywx(t, phone_holder)

            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            current_app.logger.error(traceback.format_exc())
            return 102, str(e)

    # 发起流转
    @classmethod
    def move_to_user(cls, id, borrow_id):
        try:

            t = Phone.query.get(id)
            phone_new_holder = User.query.get(borrow_id)
            phone_current_holder = User.query.get(t.borrow_id)

            # 消除对应设备已有的申请借用用户列表, 将老用户 id 放入，等待接收
            PhoneBorrowBusiness.clear_borrow_user_list(id, phone_current_holder.id)

            # 将设备的借出标志置为 1，等待接受者确认
            PhoneBorrowBusiness.add_user_to_confirm(id, phone_new_holder.id)

            # 发送企业微信
            PhoneBusiness.send_move_msg_qywx(t, phone_current_holder, phone_new_holder)

            return 0, None

        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return 102, str(e)

    # 确认流转
    @classmethod
    def move(cls, id, borrow_id):
        try:
            t = Phone.query.get(id)

            phone_new_holder = User.query.get(borrow_id)

            if not phone_new_holder:
                return 101, '要转移的用户不存在，请检查用户信息'

            t.borrow_id = borrow_id

            db.session.add(t)
            PhoneRecordBusiness.update(t, g.userid)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            return 102, str(e)

    # 退回设备
    @classmethod
    def return_to_admin(cls, id):
        try:
            # 此处返还给 创建人
            current_phone = Phone.query.get(id)

            admin_id = current_phone.creator_id

            phone_current_holder = User.query.get(current_phone.borrow_id)
            phone_new_holder = User.query.get(admin_id)

            PhoneRecordBusiness.update(current_phone, g.userid)

            # 发送企业微信
            PhoneBusiness.send_return_msg_qywx(current_phone, phone_current_holder, phone_new_holder)

            # 消除对应设备已有的申请借用用户列表, 将老用户 id 放入，等待接收
            PhoneBorrowBusiness.clear_borrow_user_list(id, phone_current_holder.id)

            # 增加 admin 到 确认名单
            PhoneBorrowBusiness.add_user_to_confirm(id, admin_id)

            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return 102, str(e)

    # 超时 3 天未接收设备，将退回
    @classmethod
    def cancel_move_to(cls, id):
        try:
            # 直接清除 phone borrow 数据
            current_phone = Phone.query.get(id)

            phone_borrow = PhoneBorrowBusiness.get_borrow_by_phone_id(phone_id=id)

            admin_id = current_phone.creator_id

            phone_current_holder = User.query.get(phone_borrow.confirm_userid)

            phone_new_holder = User.query.get(admin_id)

            # 发送企业微信
            cls.send_cancel_move_msg(current_phone, phone_current_holder, phone_new_holder)

            ret, msg = PhoneBorrowBusiness.update(phone_borrow.id, phone_borrow.phone_id, 0, '')

            return ret, msg

        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return 102, str(e)

    @classmethod
    def update(cls, id, name, asset_id, vendor, device_number, os, cpu, core, ram, rom, resolution, buy_date, region,
               borrow_id, device_source, device_belong, creator_id):
        try:
            t = Phone.query.get(id)

            t.name = name
            t.asset_id = asset_id
            t.vendor = vendor
            t.device_number = device_number
            t.os = os
            t.cpu = cpu
            t.core = core
            t.ram = ram
            t.rom = rom
            t.resolution = resolution
            t.buy_date = buy_date
            t.region = region
            t.borrow_id = borrow_id
            t.device_source = device_source
            t.device_belong = device_belong
            t.creator_id = creator_id
            db.session.add(t)
            PhoneRecordBusiness.update(t, g.userid)
            db.session.commit()

            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def delete(cls, id):
        try:
            t = Phone.query.get(id)
            if t is None:
                return 0
            t.status = Phone.DISABLE
            db.session.add(t)
            PhoneRecordBusiness.delete(t, g.userid)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)


class PhoneRecordBusiness(object):

    @classmethod
    @transfer2json(
        '?id|!phone_id|!name|!asset_id|!vendor|!creation_time|!modified_time|!device_number|!os|!cpu|!core|!ram|'
        '!rom|!resolution|!buy_date|!region|!status|!borrow_id|!creator_id|!device_source|!device_belong|!editor_id'
    )
    def query_json_by_id(cls, id):
        return cls._query().filter(
            PhoneRecord.phone_id == id, Phone.status == Phone.ACTIVE).all()

    @classmethod
    @transfer2json(
        '?id|!phone_id|!name|!asset_id|!vendor|!creation_time|!modified_time|!device_number|!os|!cpu|!core|!ram|!rom'
        '|!resolution|!buy_date|!region|!status|!borrow_id|!creator_id|!device_source|!device_belong|!editor_id'
    )
    def query_record_json(cls, phone_id):
        ret = cls._query().filter(PhoneRecord.phone_id == phone_id).order_by(PhoneRecord.id).all()
        return ret

    @classmethod
    def _query(cls):
        return PhoneRecord.query.add_columns(
            PhoneRecord.id.label('id'),
            PhoneRecord.phone_id.label('phone_id'),
            PhoneRecord.name.label('name'),
            PhoneRecord.asset_id.label('asset_id'),
            PhoneRecord.vendor.label('vendor'),
            func.date_format(PhoneRecord.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(PhoneRecord.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
            PhoneRecord.device_number.label('device_number'),
            PhoneRecord.os.label('os'),
            PhoneRecord.cpu.label('cpu'),
            PhoneRecord.core.label('core'),
            PhoneRecord.ram.label('ram'),
            PhoneRecord.rom.label('rom'),
            PhoneRecord.resolution.label('resolution'),
            PhoneRecord.buy_date.label('buy_date'),
            PhoneRecord.region.label('region'),
            PhoneRecord.status.label('status'),
            PhoneRecord.borrow_id.label('borrow_id'),
            PhoneRecord.creator_id.label('creator_id'),
            PhoneRecord.device_source.label('device_source'),
            PhoneRecord.device_belong.label('device_belong'),
            PhoneRecord.editor_id.label('editor_id'),
        )

    @classmethod
    def create(cls, t, editor_id):
        t_record = PhoneRecord(
            phone_id=t.id,
            name=t.name,
            asset_id=t.asset_id,
            vendor=t.vendor,
            device_number=t.device_number,
            os=t.os,
            cpu=t.cpu,
            core=t.core,
            ram=t.ram,
            rom=t.rom,
            resolution=t.resolution,
            buy_date=t.buy_date,
            region=t.region,
            borrow_id=t.borrow_id,
            creator_id=t.creator_id,
            device_source=t.device_source,
            device_belong=t.device_belong,
            editor_id=editor_id,
        )
        db.session.add(t_record)

    @classmethod
    def update(cls, t, editor_id):
        t_record = PhoneRecord(
            phone_id=t.id,
            name=t.name,
            asset_id=t.asset_id,
            vendor=t.vendor,
            device_number=t.device_number,
            os=t.os,
            cpu=t.cpu,
            core=t.core,
            ram=t.ram,
            rom=t.rom,
            resolution=t.resolution,
            buy_date=t.buy_date,
            region=t.region,
            borrow_id=t.borrow_id,
            creator_id=t.creator_id,
            device_source=t.device_source,
            device_belong=t.device_belong,
            editor_id=editor_id,
        )
        db.session.add(t_record)

    @classmethod
    def delete(cls, t, editor_id):
        t_record = PhoneRecord(
            phone_id=t.id,
            name=t.name,
            asset_id=t.asset_id,
            vendor=t.vendor,
            device_number=t.device_number,
            os=t.os,
            cpu=t.cpu,
            core=t.core,
            ram=t.ram,
            rom=t.rom,
            resolution=t.resolution,
            buy_date=t.buy_date,
            region=t.region,
            borrow_id=t.borrow_id,
            creator_id=t.creator_id,
            device_source=t.device_source,
            device_belong=t.device_belong,
            editor_id=editor_id,
        )
        db.session.add(t_record)

    @classmethod
    def query_record_detail(cls, phone_id):
        ret = cls.query_record_json(phone_id)
        if not ret:
            return []
        ret_list = []
        asset_config = Config.query.add_columns(Config.content.label('content')).filter(Config.module == 'asset',
                                                                                        Config.module_type == 1).first()
        content = json.loads(asset_config.content)
        operation_dict = content['operation_dict']
        # name = operation_dict.get('name')
        # asset_id = operation_dict.get('asset_id')
        # status = operation_dict.get('status')
        # borrow_id = operation_dict.get('borrow_id')

        ret_dict = {}

        user_creater = User.query.get(int(ret[0]['editor_id']))
        ret_dict['modified_time'] = ret[0]['creation_time']
        ret_dict['operation'] = "[{}({})] : 增加新的资产 {}".format(user_creater.nickname, user_creater.wx_userid,
                                                              ret[0]['name'])
        ret_list.append(ret_dict)

        current_app.logger.info(ret)

        for r in range(1, len(ret)):
            for asset_key, asset_value in ret[r - 1].items():
                if asset_key in operation_dict.keys():
                    current_app.logger.info(
                        "修改的字段：" + str(asset_key) + ", 字段值：" + str(asset_value) + "-->" + str(ret[r][asset_key]))
                    user_editor = User.query.get(int(ret[r]['editor_id']))
                    ret_dict = None
                    if asset_key in ('borrow_id',):
                        ret_dict = {'modified_time': ret[r]['modified_time']}
                        if asset_value != ret[r][asset_key]:
                            user_from = User.query.filter(User.id == int(asset_value)).first()
                            user_to = User.query.filter(User.id == int(ret[r][asset_key])).first()
                            ret_dict['operation'] = "[{}({})] : {} 由 {}({}) 变更为 {}({})".format(user_editor.nickname,
                                                                                               user_editor.wx_userid,
                                                                                               operation_dict[
                                                                                                   asset_key],
                                                                                               user_from.nickname,
                                                                                               user_from.wx_userid,
                                                                                               user_to.nickname,
                                                                                               user_to.wx_userid)
                        else:
                            # user_from = User.query.filter(User.id == int(asset_value)).first()
                            user_to = User.query.filter(User.id == int(ret[r][asset_key])).first()
                            ret_dict['operation'] = "[{}({})] : 续借了设备，{} 为 {}({})".format(user_editor.nickname,
                                                                                          user_editor.wx_userid,
                                                                                          operation_dict[asset_key],
                                                                                          user_to.nickname,
                                                                                          user_to.wx_userid)

                    else:
                        if asset_value != ret[r][asset_key]:
                            ret_dict = {
                                'modified_time': ret[r]['modified_time'],
                                'operation': "[{}({})] : 修改了{} {} 为 {}".format(user_editor.nickname,
                                                                               user_editor.wx_userid,
                                                                               operation_dict[asset_key],
                                                                               asset_value,
                                                                               ret[r][asset_key])
                            }
                    if ret_dict is not None:
                        ret_list.append(ret_dict)
        ret_list = ret_list[::-1]
        return ret_list


class VirtualAssetBusiness(object):
    @classmethod
    def _query(cls):
        return VirtualAsset.query.add_columns(
            VirtualAsset.id.label('id'),
            VirtualAsset.asset_id.label('asset_id'),
            VirtualAsset.passwd.label('passwd'),
            VirtualAsset.administrator.label('administrator'),
            VirtualAsset.bind_tel.label('bind_tel'),
            VirtualAsset.idcard.label('idcard'),
            VirtualAsset.status.label('status'),
            VirtualAsset.asset_type.label('asset_type'),
            VirtualAsset.operator.label('operator')
        )

    @classmethod
    @transfer2json(
        '?id|!asset_id|!passwd|!administrator|!idcard|!bind_tel|!status|!asset_type|!operator'
    )
    def query_json_by_id(cls, id):
        return cls._query().filter(VirtualAsset.id == id,
                                   VirtualAsset.status != VirtualAsset.DISABLE).all()

    @classmethod
    def create(cls, asset_id, passwd, administrator, bind_tel, idcard, asset_type, operator):
        try:
            va = VirtualAsset(
                asset_id=asset_id,
                passwd=passwd,
                administrator=administrator,
                bind_tel=bind_tel,
                idcard=idcard,
                asset_type=asset_type,
                operator=operator,
            )
            db.session.add(va)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def update(cls, id, asset_id, passwd, administrator, bind_tel, idcard, asset_type, operator):
        try:
            va = VirtualAsset.query.get(id)
            va.asset_id = asset_id
            va.passwd = passwd
            va.administrator = administrator
            va.bind_tel = bind_tel
            va.idcard = idcard
            va.asset_type = asset_type
            va.operator = operator
            db.session.add(va)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def delete(cls, id):
        try:
            va = VirtualAsset.query.get(id)
            if va is None:
                return 0
            va.status = VirtualAsset.DISABLE
            db.session.add(va)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    @transfer2json(
        '?id|!asset_id|!passwd|!administrator|!idcard|!bind_tel|!status|!asset_type|!operator',
        ispagination=True
    )
    def paginate_data(cls, page_size, page_index):
        asset_type = request.args.get('type')
        query = cls._query().filter(VirtualAsset.status != VirtualAsset.DISABLE)
        if asset_type:
            query = query.filter(VirtualAsset.asset_type == int(asset_type))
        count = query.count()
        data = query.order_by(desc(VirtualAsset.id)).limit(
            int(page_size)).offset(int(page_index - 1) * int(page_size)).all()
        return data, count


class PhoneBorrowBusiness(object):
    user_trpc = Trpc('auth')

    @classmethod
    def _query(cls):
        return PhoneBorrow.query.add_columns(
            PhoneBorrow.id.label('id'),
            PhoneBorrow.phone_id.label('phone_id'),
            PhoneBorrow.user_list.label('user_list'),
            PhoneBorrow.confirm_userid.label('confirm_userid'),
            func.date_format(PhoneBorrow.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(PhoneBorrow.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
        )

    @classmethod
    @transfer2json('?id|!phone_id|!user_list|!confirm_userid|!creation_time|!modified_time')
    def get_borrow_all(cls):
        phone_borrows = cls._query().all()
        return phone_borrows

    @classmethod
    def get_borrow_by_phone_id(cls, phone_id):
        phone_borrow = cls._query().filter(PhoneBorrow.phone_id == phone_id).first()
        return phone_borrow

    @classmethod
    def create(cls, phone_id, confirm_userid=0, user_list=''):
        try:
            phone_borrow = PhoneBorrow(
                phone_id=phone_id,
                user_list=user_list,
                confirm_userid=confirm_userid,
            )
            db.session.add(phone_borrow)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def update(cls, id, phone_id, confirm_userid, user_list):
        try:
            phone_borrow = PhoneBorrow.query.get(id)
            if not phone_borrow:
                cls.create(phone_id, confirm_userid, user_list)

            phone_borrow.user_list = user_list
            phone_borrow.confirm_userid = confirm_userid
            db.session.add(phone_borrow)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            return 102, str(e)

    @classmethod
    def clear_borrow_user_list(cls, phone_id, old_holder_id):
        # 清除 申请用户列表
        # 只剩 原持有者 ID
        try:
            old_holder_id = str(old_holder_id)
            phone_borrow = cls.get_borrow_by_phone_id(phone_id)
            if not phone_borrow:
                ret, msg = cls.create(phone_id, 0, old_holder_id)
            else:
                ret, msg = cls.update(phone_borrow.id, phone_borrow.phone_id, 0, old_holder_id)
            return ret, msg
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return 102, str(e)

    @classmethod
    def add_user_to_confirm(cls, phone_id, user_id):
        # 添加 用户ID 到 当前设备的 接收确认列表
        try:
            phone_borrow = cls.get_borrow_by_phone_id(phone_id)
            if not phone_borrow:
                ret, msg = cls.create(phone_id, user_id)
            else:
                ret, msg = cls.update(phone_borrow.id, phone_borrow.phone_id, user_id, phone_borrow.user_list)
            return ret, msg
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return 102, str(e)

    @classmethod
    def add_user_to_userlist(cls, phone_id, user_id):
        # 将 申请用户 ID 添加到申请列表
        try:
            phone_borrow = cls.get_borrow_by_phone_id(phone_id)
            if not phone_borrow:
                cls.create(phone_id)

            phone_borrow = cls.get_borrow_by_phone_id(phone_id)
            old_user_list = [id for id in phone_borrow.user_list.split(',')]
            user_id = str(user_id)
            if user_id not in old_user_list:
                old_user_list.append(user_id)
            else:
                return 103, "不能重复借用"
            new_user_list = ','.join(old_user_list)
            cls.update(phone_borrow.id, phone_id, 0, new_user_list)
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return 102, str(e)

    @classmethod
    @transfer2json(
        '?id|!nickname'
    )
    def get_user_list_by_phone_id(cls, phone_id):
        try:
            phone_borrow = cls.get_borrow_by_phone_id(phone_id)
            if not phone_borrow:
                return []
            user_list = [id for id in phone_borrow.user_list.split(',')]
            users = []
            for user_id in user_list:
                if len(user_id) > 0:
                    user = User.query.get(int(user_id))
                    if user:
                        users.append(user)
            return users
        except Exception as e:
            current_app.logger.error(str(e))
            current_app.logger.error(traceback.format_exc())
            return 102, str(e)

    @classmethod
    def send_borrow_msg_qywx(cls, current_phone, phone_holder, current_user):

        current_user_nickname = current_user.nickname
        current_user_wx_userid = current_user.wx_userid
        receiver_id = phone_holder.wx_userid
        msg_text = """[TCloud] {}({})
您收到一个设备借用请求:
借用的设备 : {}，
资产编号 : {},
借用人 : {} (微信号: {}),
请通过企业微信沟通，如借出，请通过 TCloud->资产->流转 进行转出。""".format(phone_holder.nickname, phone_holder.wx_userid,
                                                 current_phone.name, current_phone.asset_id, current_user_nickname,
                                                 current_user_wx_userid)
        PhoneBusiness.qyweixin_email(phone_holder.id, msg_text)

    @classmethod
    def send_borrow_continue_msg_qywx(cls, current_phone, phone_holder, current_user):
        deadline = PhoneBusiness.deadline(current_phone)
        current_user_nickname = current_user.nickname
        current_user_wx_userid = current_user.wx_userid
        receiver_id = phone_holder.wx_userid
        msg_text = """[TCloud] {} ({})
您续借了一台设备:
借用的设备 : {}，
资产编号 : {},
借用人 : {} (微信号: {})
可持有时间: {} 天
到期时间: {}""".format(phone_holder.nickname, phone_holder.wx_userid,
                   current_phone.name, current_phone.asset_id, current_user_nickname, current_user_wx_userid,
                   Phone.HOLD_DATE, deadline)
        PhoneBusiness.qyweixin_email(phone_holder.id, msg_text)

    @classmethod
    def borrow(cls, phone_id):
        # 发起借用
        try:
            ret, msg = 0, None
            current_phone = Phone.query.get(phone_id)
            if current_phone:
                current_user = User.query.get(g.userid)
                phone_holder = User.query.get(current_phone.borrow_id)
                if current_phone.borrow_id == g.userid:
                    ret, msg = PhoneBusiness.move(phone_id, phone_holder.id)
                    PhoneBorrowBusiness.send_borrow_continue_msg_qywx(current_phone, phone_holder, current_user)
                else:
                    ret, msg = PhoneBorrowBusiness.add_user_to_userlist(phone_id, g.userid)
                    if ret == 103:
                        return ret, msg
                    PhoneBorrowBusiness.send_borrow_msg_qywx(current_phone, phone_holder, current_user)
            else:
                return 101, '设备无效'
            return ret, msg
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            current_app.logger.error(e)
            return 101, e

    @classmethod
    def confirm_borrow(cls, phone_id):
        # 确认借用, admin 确认接收
        try:
            current_phone = Phone.query.get(phone_id)
            phone_borrow = cls.get_borrow_by_phone_id(phone_id)

            if int(phone_borrow.confirm_userid) != g.userid:
                return 403, '只有接收人可以确认'

            phone_current_holder = User.query.get(current_phone.borrow_id)
            phone_new_holder = User.query.get(phone_borrow.confirm_userid)

            ret, msg = PhoneBusiness.move(phone_id, int(phone_borrow.confirm_userid))

            admins = cls.user_trpc.requests('get', '/user/admin')
            current_app.logger.info('{} 确认接收设备'.format(int(phone_borrow.confirm_userid)))
            if (int(phone_borrow.confirm_userid) in admins or
                    int(phone_borrow.confirm_userid) == current_phone.creator_id):
                try:
                    PhoneBusiness.send_return_confirm_msg_qywx(current_phone, phone_current_holder, phone_new_holder)
                    reason = '成功归还了设备 {}（{}） '.format(current_phone.name, current_phone.asset_id)
                    current_app.logger.info(reason)
                    user_old_id = int(phone_borrow.user_list)
                    ret, msg = CreditBusiness.add_sub_score(user_old_id, Credit.CREDIT_ADD_ONCE, reason)
                except Exception as e:
                    current_app.logger.error(e)
            else:
                PhoneBusiness.send_move_confirm_msg_qywx(current_phone, phone_current_holder, phone_new_holder)
            ret, msg = cls.update(phone_borrow.id, phone_borrow.phone_id, 0, '')

            return ret, msg
        except Exception as e:
            current_app.logger.error(str(e))
            current_app.logger.error(traceback.format_exc())
            return 102, e
