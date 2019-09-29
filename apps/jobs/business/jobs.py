import json
import traceback
from datetime import datetime

from sqlalchemy import func

from apps.auth.models.users import User
from apps.jobs.models.jobs import JobsRecord
from apps.project.business.assets import PhoneBorrowBusiness, PhoneBusiness
from apps.project.business.credit import CreditBusiness
from apps.project.models.assets import Phone, PhoneRecord
from apps.project.models.credit import Credit
from library.api.db import db
from library.api.transfer import transfer2json
from library.trpc import Trpc


class JobsBusiness(object):
    user_trpc = Trpc('auth')

    @classmethod
    def credit_check_daily(cls):
        db.app.logger.info('credit-check-daily start')
        job = {
            'id': 'credit-check-daily'
        }
        hold_time = Phone.HOLD_DATE  # 可持有时间
        credit_time = Credit.CREDIT_DATE  # 信用分 计算时间
        result = 'success'  # 默认 job 结果
        log = ''
        try:
            with db.app.app_context():
                phones = Phone.query.filter(Phone.status == Phone.ACTIVE)
                log_template_admin = '持有用户 {}({}) 是 admin，不需要提醒！'
                log_template_creator = '持有用户 {}({}) 是 创建者，不需要提醒！'
                log_template_normal = '持有用户 {}({}) 在使用期限内，不需要提醒！'
                log_template_delay = '持有用户 {}({}) 已经超出使用期限，需要提醒！'
                log_dict = {}  # 以 phone.id 作为 key，记录对应设备状态

                confirm_delay_time = 1  # 24 hours
                confirm_delay_reset_time = confirm_delay_time * 3  # 3 days

                admins = cls.user_trpc.requests('get', '/user/admin')
                for phone in phones:
                    phone_holder = User.query.get(phone.borrow_id)
                    phone_recorder = PhoneRecord.query.filter(PhoneRecord.phone_id == phone.id). \
                        order_by(PhoneRecord.id.desc()).first()

                    # 查询 确认时间 过长发送提醒
                    phone_borrow = PhoneBorrowBusiness.get_borrow_by_phone_id(phone.id)
                    if phone_borrow:
                        if int(phone_borrow.confirm_userid) != 0:
                            phone_new_holder = User.query.get(phone_borrow.confirm_userid)

                            date_now = datetime.now()
                            date_confirm_hold = (date_now - datetime.strptime(phone_borrow.modified_time,
                                                                              '%Y-%m-%d %H:%M:%S')).days  # 计算天
                            if date_confirm_hold > confirm_delay_reset_time:
                                PhoneBusiness.cancel_move_to(phone.id)
                            elif date_confirm_hold > confirm_delay_time:
                                PhoneBusiness.send_need_confirm_msg(phone, phone_holder, phone_new_holder)
                            else:  # 如果没有超时，不发送
                                pass
                        else:  # 如果是0，判断借用人是否为空，如果不是则 发送 被借用人 提醒转出信息
                            users = PhoneBorrowBusiness.get_user_list_by_phone_id(phone.id)
                            user_id_list = [int(user.get('id')) for user in users]
                            if len(user_id_list) >= 1 and phone.borrow_id not in user_id_list:
                                date_now = datetime.now()
                                date_confirm_hold = (date_now - datetime.strptime(phone_borrow.modified_time,
                                                                                  '%Y-%m-%d %H:%M:%S')).days
                                if date_confirm_hold > confirm_delay_time:
                                    PhoneBusiness.send_need_move_msg(phone, phone_holder)
                                else:  # 如果没有超时，不发送
                                    pass
                    else:  # 如果没有借用信息，则不处理
                        pass

                    # 查询过期发送提醒: 如果 当前持有者 是 admin 或者 是创建者 则不提醒， admin 用户之间互借不提醒
                    if phone_holder.id in admins:
                        log_dict[phone.id] = log_template_admin.format(phone_holder.nickname, phone_holder.wx_userid)
                        db.app.logger.info(f'[{phone.id}] here is admin ({phone_holder.id} - {phone.creator_id})')
                        continue
                    elif phone_holder.id == phone.creator_id:
                        log_dict[phone.id] = log_template_creator.format(phone_holder.nickname, phone_holder.wx_userid)
                        db.app.logger.info(f'[{phone.id}] here is creator ({phone_holder.id} - {phone.creator_id})')
                        continue
                    else:
                        date_now = datetime.now()  # 当前时间
                        date_borrow = phone_recorder.creation_time  # 借入时间
                        deadline = PhoneBusiness.deadline(phone)  # 到期时间
                        date_holder_hold = (date_now - date_borrow).days  # 持有者已经持有时间
                        date_hold_over = date_holder_hold - hold_time  # 持有超出时间
                        date_hold_over_credit = date_holder_hold - credit_time  # 持有超出信用分时间
                        db.app.logger.info("持有时间: {}".format(date_holder_hold))
                        if date_hold_over > 0:  # 如果 '已经持有时间' > '可持有时间', 发送提醒
                            PhoneBusiness.send_delay_msg_qywx(phone, phone_holder)
                            log_dict[phone.id] = log_template_delay.format(phone_holder.nickname,
                                                                           phone_holder.wx_userid)
                        else:  # 如果 还在可以持有时间范围内， 则不发信息
                            log_dict[phone.id] = log_template_normal.format(phone_holder.nickname,
                                                                            phone_holder.wx_userid)

                        if date_hold_over_credit > 0:  # 如果 '已持有时间' > '信用分时间', 减分, 目前不发减分提醒
                            reason = '设备 {}({}) 超出归还期限 {} 已有 {} 天'.format(phone.name, phone.asset_id, deadline,
                                                                          date_hold_over_credit)
                            CreditBusiness.add_sub_score(phone_holder.id, -1, reason)
        except Exception as e:
            db.app.logger.error(str(e))
            db.app.logger.error(traceback.format_exc())
            result = 'error: {}'.format(str(e))

        JobsRecordBusiness.create(job['id'], result, log_dict)

        db.app.logger.info('credit-check-daily stop')


class JobsRecordBusiness(object):

    @classmethod
    def _query(cls):
        return JobsRecord.query.add_columns(
            JobsRecord.id.label('id'),
            JobsRecord.job_id.label('job_id'),
            JobsRecord.result.label('result'),
            JobsRecord.log.label('log'),
            func.date_format(JobsRecord.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(JobsRecord.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
        )

    @classmethod
    @transfer2json(
        '?id|!job_id|!result|!log|!creation_time|!modified_time'
    )
    def query_all_json(cls, limit, offset):
        ret = cls._query().limit(limit).offset(offset).all()
        return ret

    @classmethod
    @transfer2json(
        '?id|!job_id|!result|!log|!creation_time|!modified_time'
    )
    def query_json_by_id(cls, id):
        return cls._query().filter(
            JobsRecord.id == id).all()

    @classmethod
    @transfer2json(
        '?id|!job_id|!result|!log|!creation_time|!modified_time'
    )
    def query_json_by_job_id(cls, id):
        return cls._query().filter(
            JobsRecord.job_id == id).all()

    @classmethod
    def create(cls, job_id, result, log):
        try:

            t = JobsRecord(
                job_id=job_id,
                result=result,
                log=log if isinstance(log, str) else json.dumps(log, ensure_ascii=False),
            )
            db.session.add(t)
            db.session.commit()
            return 0, None
        except Exception as e:
            db.app.logger.error(str(e))
            return 102, str(e)
