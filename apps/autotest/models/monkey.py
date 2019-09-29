#!/usr/bin/python
# -*- coding: utf-8 -*-


# monkey 任务
from library.api.db import EntityModel, db


class Monkey(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    TEST_TYPE = {'monkey': 1, 'performance': 2}

    app_name = db.Column(db.String(100))  # app 名称，例如：萌推
    package_name = db.Column(db.String(100))  # 要测试的包名
    app_version = db.Column(db.String(100))  # app 版本
    app_id = db.Column(db.Integer)  # app package id

    download_app_status = db.Column(db.Integer)  # app 下载状态

    begin_time = db.Column(db.TIMESTAMP)  # 开始时间
    end_time = db.Column(db.TIMESTAMP)  # 结束时间

    jenkins_url = db.Column(db.String(100))  # jenkins 构建任务的 url
    report_url = db.Column(db.String(100))  # 需要请求进行报告的 url

    user_id = db.Column(db.Integer)  # 触发用户 ID
    mobile_ids = db.Column(db.String(100))  # 设备的 IDs

    parameters = db.Column(db.String(1000))  # 请求的参数

    process = db.Column(db.Integer)  # 完成度 %100

    status = db.Column(db.Integer, default=ACTIVE)  # 状态 可用 0，不可用 1

    type_id = db.Column(db.Integer)  # monkey 类型 ID
    run_time = db.Column(db.Integer)  # 运行时间
    actual_run_time = db.Column(db.Integer)  # 实际运行时间
    app_install_required = db.Column(db.Integer)  # 是否需要安装 app

    system_device = db.Column(db.Integer)  # 是否是 系统设备
    login_required = db.Column(db.Integer)  # 是否需要登陆
    login_username = db.Column(db.String(100))  # 登陆 用户名
    login_password = db.Column(db.String(100))  # 登陆 密码
    cancel_status = db.Column(db.Integer, default=DISABLE)  # 是否cancel 此次monkey，默认 1，0为确认

    test_type = db.Column(db.Integer)  # 测试类型  monkey：1， performance：2

# monkey log
class MonkeyErrorLog(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    monkey_id = db.Column(db.Integer)  # monkey id
    task_id = db.Column(db.Integer)  # monkey device id
    error_type = db.Column(db.String(100))  # error log 类型
    error_message = db.Column(db.TEXT)  # error message
    error_count = db.Column(db.Integer)  # error show count in test


# monkey log
class MonkeyReport(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    monkey_id = db.Column(db.Integer)  # monkey id
    task_id = db.Column(db.Integer)  # monkey device id
    report_type = db.Column(db.Integer, default=1)  # report 类型，1 bug_report
    report_url = db.Column(db.String(1000))  # report url on oss


# monkey packages
class MonkeyPackage(EntityModel):
    ACTIVE = 0
    DISABLE = 1
    PACKAGE_TYPE = {'monkey': 1, 'performance': 2}

    name = db.Column(db.String(100))  # package name
    package_name = db.Column(db.String(100))  # android package name
    oss_url = db.Column(db.String(200))  # package oss url
    picture = db.Column(db.Text)  # package picture
    version = db.Column(db.String(200))  # picture url
    default_activity = db.Column(db.String(100))  # default activity
    user_id = db.Column(db.Integer)  # upload user id
    status = db.Column(db.Integer, default=ACTIVE)  # package status
    size = db.Column(db.String(200))  # package size
    test_type = db.Column(db.Integer)  # test type : monkey=1,performance=2


# monkey device using
class MonkeyDeviceUsing(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    serial = db.Column(db.String(100))  # serial number
    status = db.Column(db.Integer, default=ACTIVE)  # status
    using = db.Column(db.Integer, default=DISABLE)  # not using


# monkey device status
class MonkeyDeviceStatus(EntityModel):
    ACTIVE = 0
    DISABLE = 1

    monkey_id = db.Column(db.Integer)  # monkey id
    mobile_id = db.Column(db.Integer)  # mobile id
    mobile_serial = db.Column(db.String(100))  # 序列号
    mobile_model = db.Column(db.String(100))  # mobile_model
    mobile_version = db.Column(db.String(100))  # mobile version

    process = db.Column(db.Integer)  # 进程

    activity_count = db.Column(db.Integer)  # 测试的当前包的 Activity 数量
    activity_tested_count = db.Column(db.Integer)  # 当前包的 已经测试的 Activity 数量
    activity_all = db.Column(db.String(10000))  # 测试的当前 app 的 activity
    activity_tested = db.Column(db.String(10000))  # 测试的当前包的 已经测试过得 activity

    anr_count = db.Column(db.Integer)  # anr 数量
    crash_count = db.Column(db.Integer)  # crash 数量
    crash_rate = db.Column(db.Integer)  # crash 比率

    exception_count = db.Column(db.Integer)  # exception 数量
    exception_run_time = db.Column(db.Integer)  # exception 运行时间

    # 状态 0：未开始, 1:成功, 2:失败
    device_connect_status = db.Column(db.Integer)  # 设备连接状态
    screen_lock_status = db.Column(db.Integer)  # 设备锁屏状态
    setup_install_app_status = db.Column(db.Integer)  # 安装 app
    start_app_status = db.Column(db.Integer)  # 启动 app
    setup_uninstall_app_status = db.Column(db.Integer)  # 卸载 app
    login_app_status = db.Column(db.Integer)  # 登录 app
    running_status = db.Column(db.Integer)  # 运行状态
    teardown_uninstall_app_status = db.Column(db.Integer)  # 最后卸载 app

    current_stage = db.Column(db.Integer, default=0)  # 当前执行的具体步骤

    begin_time = db.Column(db.TIMESTAMP)  # 开始时间
    end_time = db.Column(db.TIMESTAMP)  # 结束时间
    run_time = db.Column(db.Integer)  # 运行时间

    running_error_reason = db.Column(db.String(1000))  # 运行失败的具体原因
    mobile_resolution = db.Column(db.String(100))  # device 分辨率

    cancel_status = db.Column(db.Integer, default=DISABLE)  # 取消此设备的构建，默认 1，取消为 0


