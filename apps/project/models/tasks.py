from library.api.db import EntityWithNameModel, EntityModel, db


class Task(EntityWithNameModel):
    # 任务状态 0:任务创建 1:任务已删除 2:任务已完成 3:任务被拒绝
    ACTIVE = 0  # 任务创建，待审核状态
    DISABLE = 1  # 任务已删除
    FINISH = 2  # 任务已完成
    REJECT = 3  # 任务被拒绝

    STATUS_HOLDING = 2  # 任务审核通过，待执行
    STATUS_DOING = 3  # 任务执行中
    STATUS_REJECT = 4  # 任务拒绝
    STATUS_DONE = 5  # 任务已完成

    description = db.Column(db.String(300))  # 任务描述
    testreport = db.Column(db.Text())  # 测试报告
    tmethod = db.Column(db.String(50))  # 任务方法：自动化 or 人工测试
    ttype = db.Column(db.String(50))  # 任务类型：功能测试，兼容性测试...
    status = db.Column(db.Integer, default=ACTIVE)  # 任务状态
    case_list = db.Column(db.Text())  # case列表
    creator = db.Column(db.Integer)  # 创建任务的人
    executor = db.Column(db.Integer)  # 执行任务的人
    priority = db.Column(db.Integer)  # 优先级 0:紧急 1:高 2:中 3:低
    start_time = db.Column(db.TIMESTAMP)  # 任务开始时间
    end_time = db.Column(db.TIMESTAMP)  # 任务结束时间
    project_id = db.Column(db.Integer)  # 项目ID
    version = db.Column(db.Integer)  # 所属版本
    ext = db.Column(db.Text())
    attach = db.Column(db.Text())  # 附件: 用例测试完成后的测试附件
    attachment = db.Column(db.String(300))  # 附件：新建修改任务的时候上传的 附件文件
    tag = db.Column(db.String(300))  # 标签


class TaskCase(EntityModel):
    ACTIVE = 0  # case创建
    DISABLE = 1  # case已删除
    SKIP = 2  # 跳过
    GOOD = 3  # case执行通过
    NOTGOOD = 4  # case执行不通过

    task_id = db.Column(db.Integer)  # 关联的taskID
    executor = db.Column(db.Integer)  # 用例执行者保存的为用户id
    exe_way = db.Column(db.Integer)  # 执行方式，0:批量执行 1:单个执行

    SMOKING_CASE = 0
    FUNCTION_CASE = 1

    title = db.Column(db.String(300))  # 标题
    cnumber = db.Column(db.String(100))  # 编号
    module_id = db.Column(db.Integer)  # 用例模块
    feature_id = db.Column(db.Integer)  # 子模块
    ctype = db.Column(db.String(10))  # 用例类型
    description = db.Column(db.String(300))  # 用例描述
    precondition = db.Column(db.Text())  # 前置条件
    step_result = db.Column(db.Text())  # 用例步骤及预期结果 json->string格式存入
    is_auto = db.Column(db.Integer, default=DISABLE)  # 是否可转自动化
    status = db.Column(db.Integer, default=ACTIVE)  # 用例任务状态
    comment = db.Column(db.String(300))  # 备注
    version = db.Column(db.Integer)  # 所属版本
    project_id = db.Column(db.Integer)  # 所属项目
    modifier = db.Column(db.Integer)  # 修改人ID
    handler = db.Column(db.Integer)  # 处理人ID
    priority = db.Column(db.Integer)  # 优先级 0:紧急 1:高 2:中 3:低


class TaskCaseRecord(EntityModel):
    ACTIVE = 0  # case创建
    DISABLE = 1  # case已删除
    SKIP = 2  # 跳过
    GOOD = 3  # case执行通过
    NOTGOOD = 4  # case执行不通过

    task_case_id = db.Column(db.Integer)  # 关联的task_case_id
    task_id = db.Column(db.Integer)  # 关联的taskID
    executor = db.Column(db.Integer)  # 用例执行者保存的为用户id
    exe_way = db.Column(db.Integer)  # 执行方式，0:批量执行 1:单个执行

    SMOKING_CASE = 0
    FUNCTION_CASE = 1

    title = db.Column(db.String(300))  # 标题
    cnumber = db.Column(db.String(100))  # 编号
    module_id = db.Column(db.Integer)  # 用例模块
    feature_id = db.Column(db.Integer)  # 子模块
    ctype = db.Column(db.String(10))  # taskcase用例类型
    description = db.Column(db.String(300))  # 用例描述
    precondition = db.Column(db.Text())  # 前置条件
    step_result = db.Column(db.Text())  # 用例步骤及预期结果 json->string格式存入
    is_auto = db.Column(db.Integer, default=DISABLE)  # 是否可转自动化
    status = db.Column(db.Integer, default=ACTIVE)  # 用例任务状态
    comment = db.Column(db.String(300))  # 备注
    version = db.Column(db.Integer)  # 所属版本
    project_id = db.Column(db.Integer)  # 所属项目
    modifier = db.Column(db.Integer)  # 修改人ID
    handler = db.Column(db.Integer)  # 处理人ID
    priority = db.Column(db.Integer)  # 优先级 0:紧急 1:高 2:中 3:低
