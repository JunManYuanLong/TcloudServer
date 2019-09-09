from library.api.db import db, EntityWithNameModel


class Module(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    project_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text())  # 描述
    weight = db.Column(db.Integer, default=1)  # 权重
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
    parent_id = db.Column(db.Integer, nullable=True)  # 二级
