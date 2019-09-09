from library.api.db import EntityWithNameModel, db


class BoardConfig(EntityWithNameModel):
    project_id = db.Column(db.String(20))
    issue = db.Column(db.String(20), nullable=True)
    requirement = db.Column(db.String(20), nullable=True)
    hasconfig = db.Column(db.Boolean, nullable=True)
