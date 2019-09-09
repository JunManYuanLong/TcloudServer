from library.api.db import EntityWithNameModel, db


class InterfaceCaseData(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1
    num = db.Column(db.Integer(), nullable=True, comment='步骤序号，执行顺序按序号来')
    status = db.Column(db.String(16), comment='状态，true表示执行，false表示不执行')
    name = db.Column(db.String(128), comment='步骤名称')
    up_func = db.Column(db.String(256), comment='步骤执行前的函数')
    down_func = db.Column(db.String(256), comment='步骤执行后的函数')
    time = db.Column(db.Integer(), default=1, comment='执行次数')
    param = db.Column(db.Text(), default=u'[]')
    status_param = db.Column(db.String(64), default=u'[true, true]')
    variable = db.Column(db.Text())
    json_variable = db.Column(db.Text())
    status_variables = db.Column(db.String(64))
    extract = db.Column(db.String(2048))
    status_extract = db.Column(db.String(64))
    validate = db.Column(db.String(2048))
    status_validate = db.Column(db.String(64))
    case_id = db.Column(db.Integer)
    api_msg_id = db.Column(db.Integer)
    execute_status = db.Column(db.Integer, default=ACTIVE)  # 状态
