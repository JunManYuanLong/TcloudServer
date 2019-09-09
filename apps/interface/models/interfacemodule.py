from library.api.db import EntityWithNameModel, db


class InterfaceModule(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    project_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(64), nullable=True, comment='接口模块')
    num = db.Column(db.Integer(), nullable=True, comment='模块序号')
    weight = db.Column(db.Integer, default=1)  # 权重
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
