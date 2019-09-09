from library.api.db import db, EntityModel


class TcDevices(EntityModel):
    uuid = db.Column(db.String(100))  # 唯一标识
    user_id = db.Column(db.Integer)  # 用户
    use_type = db.Column(db.Integer)  # 使用类型 ：1连接 2断开 3查看
    using = db.Column(db.Integer)  # 时间戳
    manufacturer = db.Column(db.String(100))  # 制造商
    model = db.Column(db.String(100))  # 设备型号
    platform = db.Column(db.String(100))  # 平台
    version = db.Column(db.String(100))  # 系统版本
    serial = db.Column(db.String(100))  # 序列号
    resolution = db.Column(db.String(100))  # 分辨率
    use_time = db.Column(db.String(100))  # 使用时间


class TcDevicesnInfo(EntityModel):
    serial = db.Column(db.String(100))  # 序列号
    times = db.Column(db.Integer)  # 使用次数
    use_time = db.Column(db.String(100))  # 累计使用时间
    pic = db.Column(db.String(200))  # 设备图片
    comment = db.Column(db.String(200))  # 设备描述
