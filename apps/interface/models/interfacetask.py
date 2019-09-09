from library.api.db import EntityWithNameModel, db


class InterfaceTask(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1
    num = db.Column(db.Integer(), comment='任务序号')
    task_name = db.Column(db.String(64), comment='任务名称')
    task_config_time = db.Column(db.String(256), nullable=True, comment='cron表达式')
    set_id = db.Column(db.String(2048))
    case_id = db.Column(db.String(2048))
    task_type = db.Column(db.String(16))
    task_to_email_address = db.Column(db.String(256), comment='收件人邮箱')
    task_send_email_address = db.Column(db.String(256), comment='发件人邮箱')
    email_password = db.Column(db.String(256), comment='发件人邮箱密码')
    status = db.Column(db.String(16), default=u'创建', comment='任务的运行状态，默认是创建')
    project_id = db.Column(db.String(16), nullable=True)
    delete_status = db.Column(db.Integer, default=ACTIVE)  # 状态
