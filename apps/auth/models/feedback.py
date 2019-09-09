from library.api.db import EntityModel, db


class Feedback(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    contact = db.Column(db.String(200))  # 联系方式
    creator = db.Column(db.Integer)  # 创建人
    status = db.Column(db.Integer, default=ACTIVE)  # 反馈状态
    comment = db.Column(db.Text())  # 备注
    weight = db.Column(db.Integer, default=1)  # 权重，仅作用于排序
