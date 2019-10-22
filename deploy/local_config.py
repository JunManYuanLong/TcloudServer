# 环境 ： dev 开发环境
TCLOUD_ENV = 'dev'
# 服务 ： dev 开发环境
SERVER_ENV = 'dev'

# SQL 连接字符串
SQLALCHEMY_DATABASE_URI = 'mysql://root:tc123456@mysql:3306/demo?charset=utf8'

# 密钥相关
SECRET = '####'
ALGORITHM = 'HS256'
TSECRET = '####'
SALT = 'asjdia8938jf9wf8923'

# 任务设置
JOBS = [
        {  # 任务 例子：资产配置检查
        'id': 'credit-check-daily',  # 任务 id, 唯一
        'func': 'apps.jobs.business.jobs:JobsBusiness.credit_check_daily',  # 路径
        'args': None,  # 参数
        'trigger': 'interval',  # 启动方式， 时间间隔
        'seconds': 1000 # 秒数
        }]

# redis 配置
REDIS_HOST = 'localhost'
REDIS_PORT = 32768
REDIS_PASSWORD = ''
REDIS_DB = 0

# OSS 配置
OSSAccessKeyId = 'osskey'
OSSAccessKeySecret = 'osskeysecret'
OSS_ENDPOINT = 'http://oss.test.com'
OSS_BUCTET_NAME = 'oss-name'
OSSHost = 'http://tcloud.test.com'
CMSHost = 'http://tcloud.test.com'

# 测试环境数据上报
CID = ""
SIGN_KEY = ""
RAND = ""
LOG_REPORT_URL = ""

# jenkins 配置
CI_AUTO_MAN_JENKINS_URL = 'http://jenkins_url.com'
CI_AUTO_MAN_JENKINS_AUTH = {
    "username": "username",
    "password": "password"
}
CI_AUTO_MAN_JENKINS_MONKEY_JOB = 'monkey'
CI_REPORT_FILE_ADRESS = "http://oss_ci_report_url"
CI_JOB_ADDRESS = "http://jenkins_url.com/job"

# jira 配置
JIRA_URL = 'http://jira_url'
JIRA_AUTH = ('tcloud', 'tcloud')

# 企业微信应用配置凭证
CORP_ID = 'secret'
# 企业微信发送url，需要企业进行配置
QYWXHost = 'https://qywxurl/'
WX_MESSAGE_URL = ''
