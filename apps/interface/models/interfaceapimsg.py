from library.api.db import db, EntityWithNameModel


class InterfaceApiMsg(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    num = db.Column(db.Integer(), nullable=True, comment='接口序号')
    name = db.Column(db.String(128), nullable=True, comment='接口名称')
    desc = db.Column(db.String(256), nullable=True, comment='接口描述')
    variable_type = db.Column(db.String(32), nullable=True, comment='参数类型选择')
    status_url = db.Column(db.String(32), nullable=True, comment='基础url,序号对应项目的环境')
    up_func = db.Column(db.String(128), comment='接口执行前的函数')
    down_func = db.Column(db.String(128), comment='接口执行后的函数')
    method = db.Column(db.String(32), nullable=True, comment='请求方式')
    variable = db.Column(db.Text(), comment='form-data形式的参数')
    json_variable = db.Column(db.Text(), comment='json形式的参数')
    param = db.Column(db.Text(), comment='url上面所带的参数')
    url = db.Column(db.String(256), nullable=True, comment='接口地址')
    extract = db.Column(db.String(2048), comment='提取信息')
    validate = db.Column(db.String(2048), comment='断言信息')
    header = db.Column(db.String(2048), comment='头部信息')
    module_id = db.Column(db.Integer, comment='所属的接口模块id')
    project_id = db.Column(db.Integer, nullable=True, comment='所属的项目id')
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
