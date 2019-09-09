from library.api.db import EntityModel, db


class CiJob(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    number = db.Column(db.Integer)  # job number
    url = db.Column(db.String(300))  # job url
    ci_id = db.Column(db.Integer)  # ci id
    start_name = db.Column(db.String(300))  # 触发者
    status = db.Column(db.Integer, default=ACTIVE)
    report = db.Column(db.String(300))  # 报告url
    run_date = db.Column(db.TIMESTAMP)  # 运行日期
    run_time = db.Column(db.String(300))  # 运行时长
    job_count = db.Column(db.Integer)  # job 的数量
    job_accuracy = db.Column(db.String(300))  # job的正确率
