from library.api.db import EntityModel, db


class FlowInfo(EntityModel):
    ACTIVE = 0
    FINISHED = 2
    DISABLE = 1
    STOP = 3

    name = db.Column(db.String(100), nullable=False)  # 名称
    flow_type = db.Column(db.Integer)  # 流程类型：1-版本需求  2-性能优化  3-Hotfix  4-其他
    requirement_list = db.Column(db.String(300))  # 需求列表
    flow_assemble_id = db.Column(db.Integer)  # 流程集合ID
    flow_base_list = db.Column(db.String(300))  # 流程集合
    priority = db.Column(db.Integer)  # 优先级 0:紧急 1:高 2:中 3:低
    start_time = db.Column(db.TIMESTAMP)  # 任务开始时间
    end_time = db.Column(db.TIMESTAMP)  # 任务结束时间
    project_id = db.Column(db.Integer)  # 项目ID
    version_id = db.Column(db.Integer)  # 所属版本
    creator = db.Column(db.Integer)  # 创建人ID
    user_dev = db.Column(db.String(300))  # 用户
    user_prod = db.Column(db.String(300))  # 用户
    user_test = db.Column(db.String(300))  # 用户
    user_owner = db.Column(db.String(300))  # 用户
    action = db.Column(db.Text)  # 步骤
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
    weight = db.Column(db.Integer, default=1)  # 权重，仅作用于排序
    comment = db.Column(db.Text)  # 描述
    platform = db.Column(db.String(300))  # 平台
    dependence = db.Column(db.Text)  # 依赖


class FlowAssemble(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    name = db.Column(db.String(100), nullable=False)
    flow_base_list = db.Column(db.String(300))  # 流程集合
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
    flow_asstype = db.Column(db.Integer)  # 公共，项目私有
    weight = db.Column(db.Integer, default=1)  # 权重，仅作用于排序
    comment = db.Column(db.Text)  # 描述
    project_id = db.Column(db.Integer)  # 项目ID


class FlowBase(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    name = db.Column(db.String(100), nullable=False)
    step = db.Column(db.String(300))  # 步骤
    notice_type = db.Column(db.Integer)  # 消息类型
    is_send = db.Column(db.Integer)  # 是否发消息
    comment = db.Column(db.Text)  # 描述


class FlowRecord(EntityModel):
    flow_info_id = db.Column(db.Integer)  # 流程信息ID
    creator = db.Column(db.Integer)  # 创建人ID
    step_id = db.Column(db.Integer)  # 步骤
    next_step_id = db.Column(db.Integer)  # 步骤
    result = db.Column(db.String(300))  # 结果
    description = db.Column(db.String(300))  # 描述
    project_id = db.Column(db.Integer)  # 项目ID
    version_id = db.Column(db.Integer)  # 所属版本
    weight = db.Column(db.Integer, default=1)  # 权重，仅作用于排序
    comment = db.Column(db.Text)  # 备注


class FlowSource(EntityModel):
    project_id = db.Column(db.Integer)  # 项目ID
    creator = db.Column(db.Integer)  # 用户
    user_ids = db.Column(db.String(300))  # 查询的用户
    source_type = db.Column(db.Integer)  # 资源类型
    comment = db.Column(db.Text)  # 描述
