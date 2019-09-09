from library.api.db import EntityWithNameModel, db


class InterfaceProject(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    description = db.Column(db.String(1000), nullable=True)  # 产品描述
    status = db.Column(db.Integer, default=ACTIVE)
    weight = db.Column(db.Integer, default=1)
    ext = db.Column(db.Text())

    # name = db.Column(db.String(64), nullable=True, unique=True, comment='项目名称')
    # id = db.Column(db.Integer(), primary_key=True, comment='主键，自增')
    host = db.Column(db.String(1024), nullable=True, comment='测试环境')
    host_two = db.Column(db.String(1024), comment='开发环境')
    host_three = db.Column(db.String(1024), comment='线上环境')
    host_four = db.Column(db.String(1024), comment='备用环境')
    environment_choice = db.Column(db.String(16), comment='环境选择，first为测试，以此类推')
    principal = db.Column(db.String(512), nullable=True)
    variables = db.Column(db.String(2048), comment='项目的公共变量')
    headers = db.Column(db.String(1024), comment='项目的公共头部信息')
    all_project_id = db.Column(db.Integer, comment='项目的总id')
    user_id = db.Column(db.Integer(), nullable=True, comment='所属的用户id')

    # modules = relationship('InterfaceModule', foreign_keys='InterfaceProject.id')
    # configs = db.relationship('Config', order_by='Config.num.asc()', lazy='dynamic')
    # case_sets = db.relationship('CaseSet', order_by='CaseSet.num.asc()', lazy='dynamic')
