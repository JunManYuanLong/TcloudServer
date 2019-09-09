from library.api.db import db, EntityModel


class Case(EntityModel):
    SMOKING_CASE = 0
    FUNCTION_CASE = 1

    ACTIVE = 0
    DISABLE = 1

    cnumber = db.Column(db.String(100))  # 编号
    module_id = db.Column(db.Integer)  # 用例模块
    ctype = db.Column(db.String(10))  # 用例类型
    title = db.Column(db.String(300))  # 标题
    description = db.Column(db.String(300))  # 用例描述
    precondition = db.Column(db.Text())  # 前置条件
    step_result = db.Column(db.Text())  # 用例步骤及预期结果 json->string格式存入
    is_auto = db.Column(db.Integer, default=DISABLE)  # 是否可转自动化
    status = db.Column(db.Integer, default=ACTIVE)  # 用例状态
    creator = db.Column(db.Integer)  # 创建人
    priority = db.Column(db.Integer)  # 优先级 0:紧急 1:高 2:中 3:低
