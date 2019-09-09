from library.api.db import EntityWithNameModel, db


class InterfaceConfig(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    num = db.Column(db.Integer(), nullable=True, comment='配置序号')
    name = db.Column(db.String(128), comment='配置名称')
    variables = db.Column(db.String(21000), comment='配置参数')
    func_address = db.Column(db.String(128), comment='配置函数')
    project_id = db.Column(db.Integer, comment='所属的项目id')
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
