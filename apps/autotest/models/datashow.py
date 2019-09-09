from library.api.db import EntityModel, db


# 数据显示属性
class DataShowFields(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    DATA_MAP = {
        1: "数据来源",
        2: "手机类型",
        3: "apk 版本",
        4: "内核版本",
        5: "系统版本",
        6: "词库版本",
        7: "语料库版本",
    }

    data_type = db.Column(db.Integer)  # 数据类型
    data_value = db.Column(db.String(100))  # 数据值


# 响应时间 内核 录屏
class DataShowResponseKernelRecord(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    data_source = db.Column(db.String(100))  # 数据来源
    phone_model = db.Column(db.String(100))  # 手机类型
    apk_version = db.Column(db.String(100))  # apk 版本
    kernel_version = db.Column(db.String(100))  # 内核版本
    system_version = db.Column(db.String(100))  # 系统版本
    thesaurus_version = db.Column(db.String(100))  # 词库版本
    corpus_version = db.Column(db.String(100))  # 语料库版本

    key_9_and_26 = db.Column(db.String(100))  # 9 键 26 键
    average = db.Column(db.String(100))  # 平均值
    line_90_percent = db.Column(db.String(100))  # 90% line
    line_95_percent = db.Column(db.String(100))  # 95% line
    creator = db.Column(db.Integer)  # 创建人
    comment = db.Column(db.String(1000))  # 备注
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
    show_in_chart = db.Column(db.Integer, default=ACTIVE)  # 是否显示在 图表中


# 首页首词正确率
class DataShowFirstPageFirstWordCorrectRate(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    data_source = db.Column(db.String(100))  # 数据来源
    phone_model = db.Column(db.String(100))  # 手机类型
    apk_version = db.Column(db.String(100))  # apk 版本
    kernel_version = db.Column(db.String(100))  # 内核版本
    system_version = db.Column(db.String(100))  # 系统版本
    thesaurus_version = db.Column(db.String(100))  # 词库版本
    corpus_version = db.Column(db.String(100))  # 语料库版本

    key_9_and_26 = db.Column(db.String(100))  # 9 键 26 键
    first_word_correct_rate = db.Column(db.String(100))  # 首词正确率
    first_page_correct_rate = db.Column(db.String(100))  # 首页正确率
    creator = db.Column(db.Integer)  # 创建人
    comment = db.Column(db.String(1000))  # 备注
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
    show_in_chart = db.Column(db.Integer, default=ACTIVE)  # 是否显示在 图表中


# 响应时间
class DataShowResponseLog(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    data_source = db.Column(db.String(100))  # 数据来源
    phone_model = db.Column(db.String(100))  # 手机类型
    apk_version = db.Column(db.String(100))  # apk 版本
    kernel_version = db.Column(db.String(100))  # 内核版本
    system_version = db.Column(db.String(100))  # 系统版本
    thesaurus_version = db.Column(db.String(100))  # 词库版本
    corpus_version = db.Column(db.String(100))  # 语料库版本

    key_9_kernel_click_time_average = db.Column(db.String(100))  # 9键点击请求内核响应平均时间
    key_26_kernel_click_time_average = db.Column(db.String(100))  # 26 键点击请求内核响应平均时间
    key_9_kernel_response_time = db.Column(db.String(100))  # 9 键点击请求内核响应时间
    key_26_kernel_response_time = db.Column(db.String(100))  # 26 键点击请求内核响应时间
    cpu_average = db.Column(db.String(100))  # cpu 平均值
    ram_average = db.Column(db.String(100))  # 内存 平均值
    battery_use = db.Column(db.String(100))  # 耗电量
    creator = db.Column(db.Integer)  # 创建人
    comment = db.Column(db.String(1000))  # 备注
    status = db.Column(db.Integer, default=ACTIVE)  # 状态
    show_in_chart = db.Column(db.Integer, default=ACTIVE)  # 是否显示在 图表中
