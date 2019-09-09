from library.api.db import db, EntityModel


class Credit(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    CREDIT_DATE = 33
    CREDIT_SCORE_INIT = 100
    CREDIT_ADD_ONCE = 1
    CREDIT_SUB_ONCE = -1

    user_id = db.Column(db.Integer)  # 用户 id
    score = db.Column(db.Integer, default=100)  # 信用分
    status = db.Column(db.Integer, default=0)  # 状态 0：可用，1：无效


class CreditRecord(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    user_id = db.Column(db.Integer)  # 用户 id
    score = db.Column(db.Integer)  # 信用分
    score_operation = db.Column(db.Integer)  # 信用分操作
    reason = db.Column(db.String(1000))  # 加减分数原因
    status = db.Column(db.Integer, default=0)  # 状态 0：可用，1：无效
