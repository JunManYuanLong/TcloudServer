from library.api.db import EntityModel, db


class Config(EntityModel):
    module = db.Column(db.String(100))  # 模块
    module_type = db.Column(db.Integer)  # 模块的类型
    content = db.Column(db.Text)  # 内容
    description = db.Column(db.Text)  # 描述
    projectid = db.Column(db.Integer)  # 项目id


class RouteStatistics(EntityModel):
    route = db.Column(db.String(100))  # 接口
    service = db.Column(db.String(30))  # 服务
    method = db.Column(db.String(30))  # 请求方式
    count = db.Column(db.Integer, default=1)  # 次数
