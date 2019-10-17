try:
    from local_config import *
except ImportError:
    pass

# 有效时间
SESSION_TIME = 7 * 24 * 60 * 60
# 请求头验证Key
AUTH_KEY = 'Authorization'
# 项目名称
PROJECT_NAME = 'tcloud'

# 配置 sql 修改进行追踪
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 启用任务调度
SCHEDULER_API_ENABLED = True

# Response 的 message 和 code 的配置
MSG_MAP = {
    0: 'ok',

    101: 'can not find object',
    102: 'save object error',
    103: '标题或名称重复',
    104: 'can not create object',
    105: 'remove failed',
    106: 'operate failed',
    108: 'permission denied',
    109: 'project permission denied',
    110: '无此操作权限，请联系管理员',

    201: 'field required',
    202: 'field length error',

    301: 'password wrong',
    303: 'username or password wrong',

    403: 'not allowed',
    404: 'not found',
    410: 'auth expired',
    411: 'auth error',
    412: 'not login',
    413: 'username is not exist or password error',
    414: 'invalid data',
}

# ISO 时间配置格式
ISOTIMEFORMAT = '%Y-%m-%d %X'

# 优先级
PRIORITY = {
    0: '紧急',
    1: '高',
    2: '中',
    3: '低'
}

# 测试类型
CTYPE = {
    '1': '功能回归',
    '2': '冒烟',
    '3': 'UI自动化',
    '4': '接口自动化',
    '5': '新功能'
}

# 需求的配置
REQUIREMENT_CONFIG = {
    'status': {
        0: '规划中',
        1: '实现中',
        2: '测试中',
        3: '已拒绝',
        4: '待验收',
        5: '待发布',
        6: '完成'
    },
    'type': {
        0: '功能需求',
        1: '优化需求',
        2: '自动化需求',
        3: '性能需求',
        4: '兼容性需求',
        5: '报表需求',
        6: '临时需求',
        7: '紧急需求',
        8: '新功能需求',
        9: '其他'
    },
    'priority': PRIORITY
}

# 用例的配置
CASE_CONFIG = {
    'ctype': CTYPE,
    'priority': PRIORITY
}

# 任务的配置
TASK_CONFIG = {
    'status': {
        0: '新增',
        2: '已完成',
        3: '已拒绝'
    },
    'priority': PRIORITY

}

# 缺陷的配置
ISSUE_CONFIG = {
    'status': {
        1: '待办',
        2: '修复中',
        3: '测试中',
        4: '已关闭',
        5: '已拒绝',
        6: '延时处理'
    },
    'type': {
        0: '功能问题',
        1: '界面优化',
        2: '设计缺陷',
        3: '安全相关',
        4: '性能问题',
        5: '开发修改引入',
        6: '其他'
    },
    'systems': {
        1: 'ANDROID',
        2: 'IOS',
        3: '后端',
        4: 'H5',
        5: '小程序',
        6: 'WEB端',
        7: '其他'
    },
    'level': {
        0: '阻塞',
        1: '严重',
        2: '重要',
        3: '次要',
        4: '微小'
    },
    'chance': {
        0: '必现',
        1: '大概率',
        2: '小概率',
        3: '极小概率'
    },
    'detection_chance': {
        0: '明显的',
        1: '高概率',
        2: '中概率',
        3: '小概率'
    },
    'priority': PRIORITY
}

# 看板配置
BOARD_MAP = {
    'issue': ISSUE_CONFIG['status'],
    'requirement': REQUIREMENT_CONFIG['status']
}

# 临时文件夹路径
TCLOUD_FILE_TEMP_PATH = '/tmp/tcloud'

# 默认的 sft 设备图片
TCDEVICE_PIC = 'http://picture-url.test/devices_pic/default.png'

TCDEVICE_TIMEOUT = 3

ROUTE_STATISTICS = 'route_'
USER_ONLINE = 'ol_'
