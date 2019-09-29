from library.api.db import db, EntityModel


class Issue(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    # 处理状态 {"1": "待办", "2": "处理中", "3": "测试中", "4": "已关闭", "5": "已拒绝", "6": "延时处理"}
    # "1": "待办", "2": "处理中", "3": "测试中", "4": "待验收", "5": "待发布 ", "6": "延时处理", "7": "已关闭"

    issue_number = db.Column(db.String(100))  # BUG单号
    project_id = db.Column(db.Integer)  # 所属项目
    system = db.Column(db.String(100))  # 所属系统
    version = db.Column(db.Integer)  # 所属版本
    module_id = db.Column(db.Integer)  # 所属模块
    creator = db.Column(db.Integer)  # BUG创建人ID
    modifier = db.Column(db.Integer)  # BUG修改人ID
    handler = db.Column(db.Integer)  # BUG处理人ID
    issue_type = db.Column(db.Integer)  # BUG类型 0:功能问题 1:界面优化 2:设计缺陷 3:安全相关 4:性能问题 5:开发修改引入 6:其他
    chance = db.Column(db.Integer)  # 出现机率 0:必现 1:大概率 2:小概率 3:极小概率
    level = db.Column(db.Integer)  # 级别 0:Block 1:Critical 2:Major 3:Minor 4:Trivial
    priority = db.Column(db.Integer)  # 优先级 0:紧急 1:高 2:中 3:低
    stage = db.Column(db.Integer)  # BUG引入阶段 0:需求阶段 1:开发阶段 2:测试阶段 3:生产阶段
    title = db.Column(db.String(100))  # BUG标题
    attach = db.Column(db.Text)  # BUG附件
    relate_case = db.Column(db.Integer)  # 关联用例ID
    # 处理状态 0:已创建待分配 1:已分配未处理 2:已处理待验证 3:验证通过 4:验证不通过重新打开 5:暂不处理 6:无效BUG 7:已关闭 8:其他
    handle_status = db.Column(db.Integer)
    reopen = db.Column(db.Integer, server_default='0')  # reopen次数
    status = db.Column(db.Integer, default=0)  # 状态 0:ACTIVE 1:DISABLE
    weight = db.Column(db.String(100))  # 排序
    description = db.Column(db.Text)  # BUG描述
    comment = db.Column(db.String(255))  # 备注
    repair_time = db.Column(db.String(100), nullable=True)  # 开发修复BUG的时间
    test_time = db.Column(db.String(100), nullable=True)  # 测试验证BUG的时间
    detection_chance = db.Column(db.Integer)  # 用户识别是否是故障的概率 0:明显的 1:高概率 2:中概率 3:小概率
    rank = db.Column(db.Integer)  # 故障的分数  可映射故障的等级 A (R 80-125)  B (R 45-79)  C(R 11-44) D(R 1-10)
    requirement_id = db.Column(db.Integer)  # 需求 ID
    case_covered = db.Column(db.Integer)  # 用例覆盖  0为未覆盖  1为覆盖
    tag = db.Column(db.String(300))


class IssueRecord(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    iss_id = db.Column(db.Integer)  # issueid
    issue_number = db.Column(db.String(100), nullable=False)  # BUG单号
    project_id = db.Column(db.Integer)  # 所属项目
    system = db.Column(db.String(100))  # 所属系统
    version = db.Column(db.Integer)  # 所属版本
    module_id = db.Column(db.Integer)  # 所属模块
    creator = db.Column(db.Integer)  # BUG创建人ID
    modifier = db.Column(db.Integer)  # BUG修改人ID
    handler = db.Column(db.Integer)  # BUG处理人ID
    issue_type = db.Column(db.Integer)  # BUG类型 0:功能问题 1:界面优化 2:设计缺陷 3:安全相关 4:性能问题 5:开发修改引入 6:其他
    chance = db.Column(db.Integer)  # 出现机率 0:必现 1:大概率 2:小概率 3:极小概率
    level = db.Column(db.Integer)  # 级别 0:Block 1:Critical 2:Major 3:Minor 4:Trivial
    priority = db.Column(db.Integer)  # 优先级 0:紧急 1:高 2:中 3:低
    stage = db.Column(db.Integer)  # BUG引入阶段 0:需求阶段 1:开发阶段 2:测试阶段 3:生产阶段
    title = db.Column(db.String(100))  # BUG标题
    attach = db.Column(db.Text)  # BUG附件
    relate_case = db.Column(db.Integer)  # 关联用例ID
    # 处理状态 0:已创建待分配 1:已分配未处理 2:已处理待验证 3:验证通过 4:验证不通过重新打开 5:暂不处理 6:无效BUG 7:已关闭 8:其他
    handle_status = db.Column(db.Integer)
    reopen = db.Column(db.Integer, default=0)  # reopen次数
    status = db.Column(db.Integer, default=0)  # 状态 0:ACTIVE 1:DISABLE
    weight = db.Column(db.String(100))  # 排序
    description = db.Column(db.Text)  # BUG描述
    comment = db.Column(db.String(255))  # 备注
    repair_time = db.Column(db.String(100), nullable=True)  # 开发修复BUG的时间
    test_time = db.Column(db.String(100), nullable=True)  # 测试验证BUG的时间
    detection_chance = db.Column(db.Integer)  # 用户识别是否是故障的概率 0:明显的 1:高概率 2:中概率 3:小概率
    rank = db.Column(db.Integer)  # 故障的分数 可映射故障的等级 A (R 80-125)  B (R 45-79)  C(R 11-44) D(R 1-10)
    requirement_id = db.Column(db.Integer)  # 需求 ID
    case_covered = db.Column(db.Integer)  # 用例覆盖  0为未覆盖  1为覆盖
    tag = db.Column(db.String(300))
