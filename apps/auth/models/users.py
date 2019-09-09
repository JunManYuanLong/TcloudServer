from library.api.db import db, EntityModel, EntityWithNameModel


class User(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    nickname = db.Column(db.String(100), nullable=True)
    wx_userid = db.Column(db.String(200))
    password = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, default=ACTIVE)
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(30))
    weight = db.Column(db.Integer, default=1)
    ext = db.Column(db.Text())
    picture = db.Column(db.String(300), nullable=True)


class UserBindProject(EntityModel):
    user_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)


class UserBindRole(EntityModel):
    user_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
