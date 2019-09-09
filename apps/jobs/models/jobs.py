from library.api.db import EntityModel, db


class JobsRecord(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    job_id = db.Column(db.String(100))  # Job id
    result = db.Column(db.String(1000))  # Job 结果
    log = db.Column(db.Text)  # Job log
