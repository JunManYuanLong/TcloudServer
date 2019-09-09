from library.api.db import EntityWithNameModel, db


class InterfaceCase(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    num = db.Column(db.Integer(), nullable=True, comment='用例序号')
    name = db.Column(db.String(128), nullable=True, comment='用例名称')
    desc = db.Column(db.String(256), comment='用例描述')
    func_address = db.Column(db.String(256), comment='用例需要引用的函数')
    variable = db.Column(db.Text(), comment='用例公共参数')
    times = db.Column(db.Integer(), nullable=True, comment='执行次数')
    project_id = db.Column(db.Integer, comment='所属的项目id')
    case_set_id = db.Column(db.Integer, comment='所属的用例集id')
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
