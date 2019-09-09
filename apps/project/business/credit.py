import json
import traceback

from flask import current_app
from sqlalchemy import func

from apps.auth.models.users import User
from apps.project.models.credit import Credit, CreditRecord
from apps.public.models.public import Config
from library.api.db import db
from library.api.transfer import transfer2json


class CreditBusiness(object):

    @classmethod
    def _query(cls):
        return Credit.query.add_columns(
            Credit.id.label('id'),
            Credit.user_id.label('user_id'),
            Credit.score.label('score'),
            Credit.status.label('status'),
        )

    @classmethod
    @transfer2json(
        '?id|!user_id|!score|!status'
    )
    def query_json_by_id(cls, id):
        return cls._query().filter(
            Credit.id == id).all()

    @classmethod
    def create(cls, user_id, score, status=0):
        try:
            t_check = Credit.query.filter(Credit.user_id == user_id).first()
            if t_check is not None:
                return 103, None
            t = Credit(
                user_id=user_id,
                score=Credit.CREDIT_SCORE_INIT,
                status=status,
            )
            db.session.add(t)
            db.session.flush()
            CreditRecordBusiness.create(user_id, Credit.CREDIT_SCORE_INIT, reason="初始化信用分", status=0)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def add_sub_score(cls, user_id, score, reason):
        try:
            t = Credit.query.filter(Credit.user_id == user_id).first()
            if t is None:
                CreditBusiness.create(user_id, score)
            t = Credit.query.filter(Credit.user_id == user_id).first()
            new_score = t.score + score  # 信用分与传进来的分数做加法计算当前新的分数
            CreditBusiness.update(user_id, new_score, t.status)
            CreditRecordBusiness.update(t, new_score, reason)
            return 0, None
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return 102, str(e)

    @classmethod
    def update(cls, user_id, score, status):
        try:
            t = Credit.query.filter(Credit.user_id == user_id).first()
            t.user_id = user_id
            t.score = score
            t.status = status
            db.session.add(t)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def delete(cls, id):
        try:
            t = Credit.query.get(id)
            if t is None:
                return 0
            t.status = Credit.DISABLE
            db.session.add(t)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    @transfer2json(
        '?id|!user_id|!score|!status',
        ispagination=True
    )
    def paginate_data(cls, page_size, page_index):
        query = cls._query()
        count = query.count()
        data = query.limit(page_size).offset((page_index - 1) * page_size).all()
        return data, count


class CreditRecordBusiness(object):

    @classmethod
    @transfer2json(
        '?id|!user_id|!score|!reason|!status|!creation_time|!modified_time'
    )
    def query_json_by_id(cls, id):
        return cls._query().filter(
            CreditRecord.user_id == id).all()

    @classmethod
    @transfer2json(
        '?id|!user_id|!score|!reason|!status|!creation_time|!modified_time'
    )
    def query_record_json(cls, user_id):
        ret = cls._query().filter(CreditRecord.user_id == user_id).order_by(CreditRecord.id).all()
        return ret

    @classmethod
    def _query(cls):
        return CreditRecord.query.add_columns(
            CreditRecord.id.label('id'),
            CreditRecord.user_id.label('user_id'),
            CreditRecord.score.label('score'),
            CreditRecord.reason.label('reason'),
            CreditRecord.status.label('status'),
            func.date_format(CreditRecord.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            func.date_format(CreditRecord.modified_time, "%Y-%m-%d %H:%i:%s").label('modified_time'),
        )

    @classmethod
    def create(cls, user_id, score, reason, status):
        t = CreditRecord(
            user_id=user_id,
            score=score,
            reason=reason,
            status=status,
        )
        db.session.add(t)

    @classmethod
    def update(cls, credit, score, reason):
        t = CreditRecord(
            user_id=credit.user_id,
            score=score,
            reason=reason,
            status=credit.status,
        )
        db.session.add(t)
        db.session.commit()

    @classmethod
    def query_record_detail(cls, user_id):
        ret = cls.query_record_json(user_id)
        if not ret:
            return []
        ret_list = []
        credit_config = Config.query.add_columns(
            Config.content.label('content')).filter(
            Config.module == 'credit', Config.module_type == 1).first()
        cnotent = json.loads(credit_config.content)
        operation_dict = cnotent['operation_dict']

        user_in_ret = User.query.get(ret[0]['user_id'])

        ret_dict = {
            'modified_time': ret[0]['creation_time'],
            'operation': "初始化 {} 信用分为 {}".format(user_in_ret.nickname, Credit.CREDIT_SCORE_INIT)
        }
        ret_list.append(ret_dict)
        for r in range(1, len(ret)):
            for asset_key, asset_value in ret[r - 1].items():
                if asset_value != ret[r][asset_key] and asset_key in operation_dict.keys():
                    current_app.logger.info(
                        "修改的字段：" + str(asset_key) + ", 字段值：" + str(asset_value) + "-->" + str(ret[r][asset_key]))

                    ret_dict = {'modified_time': ret[r]['modified_time']}
                    credit_user = User.query.get(ret[r]['user_id'])
                    if asset_key in ('score',):
                        if ret[r][asset_key] < asset_value:
                            ret_dict['operation'] = '[{}({})] 由于 ( {} )，扣除信用分 {} 分，当前信用分 {} 分'.format(
                                credit_user.nickname, credit_user.wx_userid, ret[r]['reason'],
                                Credit.CREDIT_ADD_ONCE, ret[r][asset_key])
                        else:
                            ret_dict['operation'] = '[{}({})] 由于 ( {} )，增加信用分 {} 分，当前信用分 {} 分'.format(
                                credit_user.nickname, credit_user.wx_userid, ret[r]['reason'],
                                Credit.CREDIT_ADD_ONCE, ret[r][asset_key])
                    else:
                        ret_dict['operation'] = "修改了{} {} 为 {}".format(operation_dict[asset_key], asset_value,
                                                                       ret[r][asset_key])
                    ret_list.append(ret_dict)
        ret_list = ret_list[::-1]
        current_app.logger.info(json.dumps(ret_list, ensure_ascii=False))
        return ret_list
