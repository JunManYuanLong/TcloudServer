from library.api.db import EntityModel, db


class Requirement(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    # board状态：1:待办  2:处理中 3:测试中  4:待验收 5:待发布 6:延时处理

    title = db.Column(db.String(200))  # 标题
    project_id = db.Column(db.Integer)  # 项目ID
    version = db.Column(db.String(100))  # 所属版本
    # start_time = db.Column(db.TIMESTAMP)  # 任务开始时间
    # end_time = db.Column(db.TIMESTAMP)  # 任务结束时间
    requirement_type = db.Column(db.Integer)  # 类型
    creator = db.Column(db.Integer)  # 创建人
    modifier = db.Column(db.Integer)  # 修改人
    handler = db.Column(db.Integer)  # 处理人
    board_status = db.Column(db.Integer, default=DISABLE)  # 需求看板状态
    status = db.Column(db.Integer, default=ACTIVE)  # 需求状态
    description = db.Column(db.Text)  # 描述
    priority = db.Column(db.Integer)  # 优先级 0:紧急 1:高 2:中 3:低
    attach = db.Column(db.Text)  # 附件
    comment = db.Column(db.String(300))  # 备注
    weight = db.Column(db.Integer, default=1)  # 权重，仅作用于排序
    parent_id = db.Column(db.Integer, default=ACTIVE)  # 父类项目ID
    review_status = db.Column(db.Integer, default=1)  # 评审的状态 1-未评审，2-评审成功 3-评审失败
    jira_id = db.Column(db.String(300))  # jira号
    worth = db.Column(db.Integer)  # 需求价值  1:高价值 2:非高价值
    report_time = db.Column(db.String(300))  # 上线评估结果时间(天)
    report_expect = db.Column(db.Text)  # 高价值预期结果
    report_real = db.Column(db.Text)  # 高价值实际结果
    worth_sure = db.Column(db.Integer)  # 确认需求价值  1:高价值 2:非高价值
    expect_time = db.Column(db.DateTime)  # 预计完成时间
    tag = db.Column(db.String(300))


class RequirementRecord(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    # board状态：1:待办  2:处理中 3:测试中  4:待验收 5:待发布 6:延时处理

    requirement_id = db.Column(db.Integer)  # 需求ID
    title = db.Column(db.String(200))  # 标题
    project_id = db.Column(db.Integer)  # 项目ID
    version = db.Column(db.String(100))  # 所属版本
    # start_time = db.Column(db.TIMESTAMP)  # 任务开始时间
    # end_time = db.Column(db.TIMESTAMP)  # 任务结束时间
    requirement_type = db.Column(db.Integer)  # 类型
    creator = db.Column(db.Integer)  # 创建人
    modifier = db.Column(db.Integer)  # 修改人
    handler = db.Column(db.Integer)  # 处理人
    board_status = db.Column(db.Integer, default=DISABLE)  # 需求看板状态
    status = db.Column(db.Integer, default=ACTIVE)  # 需求状态
    description = db.Column(db.Text)  # 描述
    priority = db.Column(db.Integer)  # 优先级 0:紧急 1:高 2:中 3:低
    attach = db.Column(db.Text)  # 附件
    comment = db.Column(db.String(300))  # 备注
    weight = db.Column(db.Integer, default=1)  # 权重，仅作用于排序
    parent_id = db.Column(db.Integer, default=ACTIVE)  # 父类项目ID
    review_status = db.Column(db.Integer, default=1)  # 评审的状态 1-未评审，2-评审成功 3-评审失败
    jira_id = db.Column(db.String(300))  # jira号
    worth = db.Column(db.Integer)  # 需求价值  1:高价值 2:非高价值
    report_time = db.Column(db.String(300))  # 上线评估结果时间(天)
    report_expect = db.Column(db.Text)  # 高价值预期结果
    report_real = db.Column(db.Text)  # 高价值实际结果
    worth_sure = db.Column(db.Integer)  # 确认需求价值  1:高价值 2:非高价值
    expect_time = db.Column(db.DateTime)  # 预计完成时间
    tag = db.Column(db.String(300))


class RequirementReview(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    # board状态：1:待办  2:处理中 3:测试中  4:待验收 5:待发布 6:延时处理

    review_id = db.Column(db.Integer)  # 评审ID
    requirement_id = db.Column(db.Integer)  # 需求ID
    title = db.Column(db.String(200))  # 标题
    project_id = db.Column(db.Integer)  # 项目ID
    version = db.Column(db.String(100))  # 所属版本
    requirement_type = db.Column(db.Integer)  # 类型
    creator = db.Column(db.Integer)  # 创建人
    modifier = db.Column(db.Integer)  # 修改人
    handler = db.Column(db.Integer)  # 处理人
    board_status = db.Column(db.Integer, default=DISABLE)  # 需求看板状态
    status = db.Column(db.Integer, default=ACTIVE)  # 需求状态
    description = db.Column(db.Text)  # 描述
    priority = db.Column(db.Integer)  # 优先级 0:紧急 1:高 2:中 3:低
    attach = db.Column(db.Text)  # 附件
    comment = db.Column(db.String(300))  # 备注
    weight = db.Column(db.Integer, default=1)  # 权重，仅作用于排序
    parent_id = db.Column(db.Integer, default=ACTIVE)  # 父类项目ID
    review_status = db.Column(db.Integer)  # 需求评审状态 1-通过，2-未通过
    jira_id = db.Column(db.String(300))  # jira号
    worth = db.Column(db.Integer)  # 需求价值  1:高价值 2:非高价值
    report_time = db.Column(db.String(300))  # 上线评估结果时间(天)
    report_expect = db.Column(db.Text)  # 高价值预期结果
    report_real = db.Column(db.Text)  # 高价值实际结果
    worth_sure = db.Column(db.Integer)  # 确认需求价值  1:高价值 2:非高价值


class Review(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    title = db.Column(db.String(200))  # 标题
    requirement_list = db.Column(db.String(200))  # 需求ID列表
    project_id = db.Column(db.Integer)  # 项目ID
    version_id = db.Column(db.Integer)  # 版本ID
    creator = db.Column(db.Integer)  # 创建人
    modifier = db.Column(db.Integer)  # 修改人
    reviewer = db.Column(db.String(200))  # 参与人
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
    attach = db.Column(db.Text)  # 附件
    comment = db.Column(db.String(300))  # 备注
    weight = db.Column(db.Integer, default=1)  # 权重，仅作用于排序
    review_status = db.Column(db.Integer)  # 评审的状态 1-未评审，2-已评审


class RequirementBindCase(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    requirement_id = db.Column(db.Integer)  # 需求 ID
    case_id = db.Column(db.Integer)  # 用例 ID
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
