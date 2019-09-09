from library.api.db import db, EntityModel


class TrackUser(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    nickname = db.Column(db.String(100))
    wx_userid = db.Column(db.String(200))
    status = db.Column(db.Integer, default=ACTIVE)
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(30))
    weight = db.Column(db.Integer, default=1)
    track_token = db.Column(db.Text())
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer)


class TrackUpload(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    project_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    device_type = db.Column(db.Integer)
    device_typename = db.Column(db.String(200))
    device_number = db.Column(db.String(500))
    status = db.Column(db.Integer, default=ACTIVE)
