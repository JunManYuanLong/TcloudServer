from library.api.db import db, EntityModel


class Role(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, default=ACTIVE)
    weight = db.Column(db.Integer, default=1)
    comment = db.Column(db.String(300))  # 备注


class RoleBindAbility(EntityModel):
    role_id = db.Column(db.Integer)
    ability_id = db.Column(db.Integer)
