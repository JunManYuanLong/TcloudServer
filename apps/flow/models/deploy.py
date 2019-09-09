from library.api.db import EntityModel, db


class Deploy(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    project_id = db.Column(db.Integer)  # 项目id
    server_list = db.Column(db.String(500))  # 服务list
    node_list = db.Column(db.String(500))  # node list
    status = db.Column(db.Integer, default=ACTIVE)
    branch = db.Column(db.String(500))  # 分支
    flow_id = db.Column(db.Integer)  # 流程id
    user_id = db.Column(db.Integer)  # user_id


class DeployRecord(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    project_id = db.Column(db.Integer)  # 项目id
    server_id = db.Column(db.Integer)  # 服务 id
    node_id = db.Column(db.Integer)  # node id
    status = db.Column(db.Integer, default=ACTIVE)
    version = db.Column(db.String(100))  # 部署生成的version
    branch = db.Column(db.String(100))  # 分支
    result = db.Column(db.Integer, default=ACTIVE)  # 分支的结果 0 编译中 1 打包失败 2发布失败 3重启失败 4成功
    deploy_id = db.Column(db.Integer)  # 部署的id
    flow_id = db.Column(db.Integer)  # 流程id
    server_name = db.Column(db.String(500))  # 服务名字
    node_name = db.Column(db.String(500))  # 节点名字


class DeployLog(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    project_id = db.Column(db.Integer)  # 项目id
    comment = db.Column(db.Text)  # 备注的内容
    flow_id = db.Column(db.Integer)  # 流程id
    result = db.Column(db.String(500))  # 结果
    name = db.Column(db.String(500))  # 流程名字
    use_id = db.Column(db.Integer)  # 用户id
    deploy_id = db.Column(db.Integer)  # 部署的id
    user_name = db.Column(db.String(500))  # 用户名字
    result_id = db.Column(db.Integer)  # id
    status = db.Column(db.Integer, default=ACTIVE)
    log_type = db.Column(db.Integer)  # 日志类型
