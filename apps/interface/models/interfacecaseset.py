from library.api.db import EntityWithNameModel, db


class InterfaceCaseSet(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    num = db.Column(db.Integer(), nullable=True, comment='用例集合序号')
    name = db.Column(db.String(256), nullable=True, comment='用例集名称')
    project_id = db.Column(db.Integer, comment='所属的项目id')
    # cases = db.relationship('Case', order_by='Case.num.asc()', lazy='dynamic')
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
