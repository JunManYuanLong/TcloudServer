from library.api.db import EntityWithNameModel, db, EntityModel


class Phone(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1
    HOLD_DATE = 30
    ADMIN_ID = 93

    asset_id = db.Column(db.String(100))  # 资产编号
    vendor = db.Column(db.String(100))  # 制造商
    device_number = db.Column(db.String(1000))  # 设备号
    os = db.Column(db.String(100))  # 系统
    cpu = db.Column(db.String(100))  # CPU
    core = db.Column(db.String(100))  # 核数
    ram = db.Column(db.String(10))  # 内存
    rom = db.Column(db.String(10))  # 硬盘
    resolution = db.Column(db.String(100))  # 分辨率 x * y
    buy_date = db.Column(db.String(100))  # 采购时间
    region = db.Column(db.String(100))  # 地区
    status = db.Column(db.Integer, default=ACTIVE)
    borrow_id = db.Column(db.Integer)  # 持有人，默认创建者
    creator_id = db.Column(db.Integer)  # 所属人
    device_source = db.Column(db.String(1000))  # 设备来源
    device_belong = db.Column(db.String(1000))  # 设备归属


class PhoneRecord(EntityWithNameModel):
    ACTIVE = 0
    DISABLE = 1

    phone_id = db.Column(db.Integer)  # phone id
    asset_id = db.Column(db.String(100))  # 资产编号
    vendor = db.Column(db.String(100))  # 制造商
    device_number = db.Column(db.String(1000))  # 设备号
    os = db.Column(db.String(100))  # 系统
    cpu = db.Column(db.String(100))  # CPU
    core = db.Column(db.String(100))  # 核数
    ram = db.Column(db.String(10))  # 内存
    rom = db.Column(db.String(10))  # 硬盘
    resolution = db.Column(db.String(100))  # 分辨率 x * y
    buy_date = db.Column(db.String(100))  # 采购时间
    region = db.Column(db.String(100))  # 地区
    status = db.Column(db.Integer, default=ACTIVE)
    borrow_id = db.Column(db.Integer)  # 持有人，默认创建者
    creator_id = db.Column(db.Integer)  # 创建人
    device_source = db.Column(db.String(1000))  # 设备来源
    device_belong = db.Column(db.String(1000))  # 设备归属
    editor_id = db.Column(db.Integer)  # 此次记录的操作者


class PhoneBorrow(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    phone_id = db.Column(db.Integer)  # phone id
    user_list = db.Column(db.String(100))  # 申请用户列表， 以 ',' 分隔， 默认为空
    confirm_userid = db.Column(db.Integer)  # 需要确认申请人用户 ID, 0 为不需要确认


class VirtualAsset(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    BLOCKED = 2  # 封禁

    TEL = 1
    WECHAT = 2
    QQ = 3

    asset_id = db.Column(db.String(100), nullable=False)  # 虚拟资产ID
    passwd = db.Column(db.String(100))  # 明文密码
    administrator = db.Column(db.String(100))  # 持有人名字
    bind_tel = db.Column(db.String(100))
    idcard = db.Column(db.String(100))  # 持有人身份证
    status = db.Column(db.Integer, default=ACTIVE)
    asset_type = db.Column(db.Integer)
    operator = db.Column(db.String(100))  # 运营商
