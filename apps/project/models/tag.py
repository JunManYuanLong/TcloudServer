from library.api.db import EntityModel, db


class Tag(EntityModel):
    ACTIVE = 0  # case创建
    DISABLE = 1  # case已删除

    tag = db.Column(db.String(300))  # 标签
    project_id = db.Column(db.Integer)  # 所属项目
    status = db.Column(db.Integer, default=ACTIVE)  # 配置标签状态
    description = db.Column(db.Text())  # 配置描述
    creator = db.Column(db.String(300))  # 配置增加人
    tag_type = db.Column(db.Integer)  # 配置类型 1表示需求2任务3issue
    reference_nums = db.Column(db.Integer, default=0)  # 被引用次数，只有为0时才能被删除
    modifier = db.Column(db.String(300))  # 配置修改人
