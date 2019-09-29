from library.api.db import EntityWithNameModel, db, EntityModel


class Project(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    description = db.Column(db.String(1000), nullable=True)  # 产品描述
    status = db.Column(db.Integer, default=ACTIVE)
    weight = db.Column(db.Integer, default=1)
    ext = db.Column(db.Text())
    logo = db.Column(db.String(2048), comment='信息logo')  # 产品logo url


class ProjectBindBusiness(EntityModel):
    project_id = db.Column(db.Integer)  # 项目ID
    business_id = db.Column(db.Integer)  # 业务ID
    ext = db.Column(db.Text())
