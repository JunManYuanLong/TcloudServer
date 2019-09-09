from library.api.db import db, EntityModel


class Version(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    NOT_PUBLISH = 0
    IS_PUBLISH = 1

    title = db.Column(db.String(200))  # 标题
    project_id = db.Column(db.Integer)  # 项目ID
    start_time = db.Column(db.TIMESTAMP)  # 版本开始时间
    end_time = db.Column(db.TIMESTAMP)  # 版本结束时间
    publish_time = db.Column(db.TIMESTAMP)  # 版本发布时间
    creator = db.Column(db.Integer)  # 创建人
    publish_status = db.Column(db.Integer, default=NOT_PUBLISH)  # 发布状态 0：未发布 1：已发布
    status = db.Column(db.Integer, default=ACTIVE)  # 需求状态
    description = db.Column(db.String(300))  # 描述
    comment = db.Column(db.String(300))  # 备注
    weight = db.Column(db.Integer, default=1)  # 权重，仅作用于排序
