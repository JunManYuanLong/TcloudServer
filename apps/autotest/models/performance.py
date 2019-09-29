

# performance device status
from library.api.db import EntityModel, db
#
#
# class PerformanceDeviceStatus(EntityModel):
#     ACTIVE = 0
#     DISABLE = 1
#
#     monkey_id = db.Column(db.Integer)  # monkey id
#     mobile_id = db.Column(db.Integer)  # mobile id
#     mobile_serial = db.Column(db.String(100))  # 序列号
#     mobile_model = db.Column(db.String(100))  # mobile_model
#     mobile_version = db.Column(db.String(100))  # mobile version
#
#     process = db.Column(db.Integer)  # 进程
#
#     # 状态 0：未开始, 1:成功, 2:失败
#     device_connect_status = db.Column(db.Integer)  # 设备连接状态
#     screen_lock_status = db.Column(db.Integer)  # 设备锁屏状态
#     setup_install_app_status = db.Column(db.Integer)  # 安装 app
#     start_app_status = db.Column(db.Integer)  # 启动 app
#     setup_uninstall_app_status = db.Column(db.Integer)  # 卸载 app
#     login_app_status = db.Column(db.Integer)  # 登录 app
#     running_status = db.Column(db.Integer)  # 运行状态
#     teardown_uninstall_app_status = db.Column(db.Integer)  # 最后卸载 app
#
#     current_stage = db.Column(db.Integer, default=0)  # 当前执行的具体步骤
#
#     begin_time = db.Column(db.TIMESTAMP)  # 开始时间
#     end_time = db.Column(db.TIMESTAMP)  # 结束时间
#     run_time = db.Column(db.Integer)  # 运行时间
#
#     running_error_reason = db.Column(db.String(1000))  # 运行失败的具体原因
#     mobile_resolution = db.Column(db.String(100))  # device 分辨率
#
#     cancel_status = db.Column(db.Integer, default=DISABLE)  # 取消此设备的构建，默认 1，取消为 0


# performance test infos
class PerformanceTest(EntityModel):
    ACTIVATE = 0
    DISABLE = 1
    VALUE_MAPS = {
        "setup_info": {"open": 1, "close": 2},
        "base_app": {"WeChat": 1, "QQ": 2, "WPS": 3, "QJP": 4},
        "key_type": {"9": 1, "26": 2}
    }

    performance_id = db.Column(db.Integer)  # performance id

    # setup_info = db.Column(db.Integer)  # 前置条件, 表情打开：1，表情关闭：2
    # base_app = db.Column(db.Integer)  # 场景（不同的app）,微信：1，QQ：2，WPS: 3，趣键盘：4
    # key_type = db.Column(db.Integer)  # 26 : 1, 9 : 2
    run_time = db.Column(db.Integer)  # 输入运行时间
    run_type = db.Column(db.String(500))  # 测试场景

    # status of performance here
    cpu_average = db.Column(db.Float)  # cpu 均值
    cpu_top = db.Column(db.Float)  # cpu 峰值
    rss_average = db.Column(db.Float)  # rss 均值
    rss_top = db.Column(db.Float)  # rss 峰值
    heap_size_average = db.Column(db.Float)  # heap_size 均值
    heap_size_top = db.Column(db.Float)  # heap_size 峰值
    heap_alloc_average = db.Column(db.Float)  # heap_alloc 均值
    heap_alloc_top = db.Column(db.Float)  # heap_alloc 峰值


# performance test logs
class PerformanceTestLog(EntityModel):
    ACTIVATE = 0
    DISABLE = 1

    performance_test_id = db.Column(db.Integer)  # performance test id
    cpu = db.Column(db.Float)  # cpu 实时数据
    rss = db.Column(db.Float)  # rss 实时数据
    heap_size = db.Column(db.Float)  # heap size 实时数据
    heap_alloc = db.Column(db.Float)  # heap alloc 实时数据




