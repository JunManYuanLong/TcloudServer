from library.api.db import db, EntityModel


class Jira(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    KEY_MAP = {
        "requirement": 1,
        "flow": 2
    }

    params = db.Column(db.String(1000))  # jira 请求的参数
    result = db.Column(db.String(100))  # jira 请求结果
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
    key_type = db.Column(db.Integer)  # 1: requirement 2: flow
    key_id = db.Column(db.Integer)  # requirement_id or flow_id
