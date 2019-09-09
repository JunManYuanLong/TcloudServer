from library.api.db import EntityWithNameModel, db


class InterfaceReport(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    case_names = db.Column(db.String(128), nullable=True, comment='用例的名称集合')
    read_status = db.Column(db.String(16), nullable=True, comment='阅读状态')
    project_id = db.Column(db.String(16), nullable=True)
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
