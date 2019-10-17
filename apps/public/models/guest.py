from library.api.db import EntityModel, db


class Guest(EntityModel):
    ip = db.Column(db.String(30))  # 访客ip
    platform = db.Column(db.String(30))  # 访客平台
    browser = db.Column(db.String(30))  # 访客浏览器
    string = db.Column(db.String(100))  # 访客agent
    version = db.Column(db.String(30))  # 访客版本
    count = db.Column(db.Integer, default=1)  # 访问次数
