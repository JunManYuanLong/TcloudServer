from library.api.db import EntityModel, db


class CiData(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    name = db.Column(db.String(200))  # job name
    accuracy = db.Column(db.String(10))  # 项目正确率
    case_count = db.Column(db.Integer)  # 用例个数
    nextBuildNumber = db.Column(db.Integer)  # 下一个执行number
    # is_executing = db.Column(db.Integer)  # 0 未执行,1正在执行
    status = db.Column(db.Integer, default=ACTIVE)
    description = db.Column(db.String(500))  # job 的描述
