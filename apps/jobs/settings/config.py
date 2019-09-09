try:
    from public_config import *
except ImportError:
    pass

PORT = 9038
SERVICE_NAME = 'jobs'

SERVER_ENV = 'dev'

JOBS = [
    {  # 任务 信用积分每日检查， 每周一到每周五 早上 10:30 分运行
        # 检查每个设备的借用日期是否超时 ：发送提醒邮件，扣除信用分 1分
        'id': 'credit-check-daily',  # 任务 id, 唯一
        'func': 'apps.jobs.business.jobs:JobsBusiness.credit_check_daily',  # 路径
        'args': None,  # 参数
        'trigger': 'cron',  # 启动方式， 时间间隔
        'day_of_week': 'mon-fri',  # 周1 - 周5
        'hour': 11,  # 早上 11 点
        'minute': 30,  # 具体分钟数
    },
    {
        # cidata 数据更新
        'id': 'cijob_update',  # 任务 id, 唯一
        'func': 'apps.extention.business.cidata:CiJobBusiness.update_jenkins_data',  # 路径
        'args': None,  # 参数
        'trigger': 'interval',  # 启动方式 时间区间
        'hours': 10
    }
]
