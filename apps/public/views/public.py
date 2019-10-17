from flask import Blueprint, request, current_app

from apps.auth.auth_require import required
from apps.public.daos.public import (
    get_config, send_wxmessage, get_token, update_config, get_flow_config,
    create_config, get_count_online,
    get_statistics_route,
)
from apps.public.extentions import validation, parse_json_form

public = Blueprint('public', __name__)


@public.route('/config', methods=['GET'])
def get():
    """
    @api {get} /v1/public/config/ 查询 配置 列表
    @apiName GetPublicConfig
    @apiGroup 公共
    @apiDescription 查询 配置列表
    @apiParam {string} module 模块名称
    @apiParam {int} [module_type] 模块类型
    @apiParam {bool} [is_all] 是否返回全部
    @apiParam {int} project_id 配置项目 ID
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
      "code": 0,
      "data": {
        "permission_check": true,
        "platform": {
          "1": "后端",
          "2": "PHP",
          "3": "APP",
          "4": "H5",
          "5": "微信商城",
          "6": "小程序"
        },
        "send_wxmessag": true,
        "type": {
          "1": "版本需求",
          "2": "搜索推荐",
          "3": "问题修复",
          "4": "临时需求",
          "5": "优化",
          "6": "紧急需求"
        }
      }
    }
    """
    module = request.args.get('module')
    module_type = request.args.get('module_type')
    is_all = request.args.get('is_all')
    project_id = request.args.get('project_id')

    if module:
        code, data = get_config(module, module_type, is_all, project_id)
        return {
            "code": code,
            "data": data
        }
    else:
        return {
            "code": 0
        }


@public.route('/config', methods=['POST'])
@required('projectconfig_modify')
@validation('POST:config_create')
def create_config_handler():
    """
    @api {post} /v1/public/config/ 新建 项目的配置
    @apiName CreatePublicConfig
    @apiGroup 公共
    @apiDescription 新建 项目的配置
    @apiParam {string} module 模块名称
    @apiParam {int} module_type 模块类型
    @apiParam {dict} content 内容
    @apiParam {string} description 描述简介
    @apiParam {int} project_id 配置项目 ID
    @apiSuccessExample {json} Success-Request:
     HTTP/1.1 200 OK
     {
        "module": "flow_config",
        "module_type": 1,
        "description": "测试",
        "project_id": 4,
        "content":{
            "test": 1,
            "test2": {"test1": 1},
            "test3": [{
                "test1":1
            }]
        }
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
      "code": 0,
      "data": []
    }
    """
    module, module_type, content, description, projectid = parse_json_form('config_create')
    code = create_config(module, module_type, content, description, projectid)
    return {
        "code": code,
        "message": 'create config success!'
    }


@public.route('/config/<int:config_id>', methods=['POST'])
@required('projectconfig_modify')
@validation('POST:config_update')
def update_config_handler(config_id):
    """
    @api {post} /v1/public/config/{int:config_id} 更新 项目的配置
    @apiName UpdatePublicConfig
    @apiGroup 公共
    @apiDescription 更新 项目的配置
    @apiParam {string} [module] 模块名称
    @apiParam {int} [module_type] 模块类型
    @apiParam {dict} [content] 内容
    @apiParam {string} [description] 描述简介
    @apiParam {int} project_id 配置项目 ID,必需,当不存在时根据此创建（复制）
    @apiSuccessExample {json} Success-Request:
     HTTP/1.1 200 OK
     {
        "project_id": 4
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
      "code": 0,
      "data": []
    }
    """
    module, module_type, content, description, projectid = parse_json_form('config_update')
    code = update_config(config_id, module, module_type, content, description, projectid)
    return {
        "code": code,
        'data': 'success',
        "message": 'update config success!'
    }


@public.route('/wxmessage', methods=['POST'])
@required('projectconfig_modify')
@validation('POST:wxmessage_create')
def create_wxmessage():
    is_email = request.args.get('is_email')
    user_ids, text, user_emails = parse_json_form('wxmessage_create')
    code, data = send_wxmessage(user_ids, text, user_emails, is_email)
    return {
        'code': code,
        'data': data
    }


@public.route('/ossauth', methods=['GET'])
def oss_auth_handler():
    """
    @api {get} /v1/public/ossauth 获取 osstoken
    @apiName GetOssToken
    @apiGroup 公共
    @apiDescription 获取osstoken
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        code: 0,
        data: {
            accessid: "xxx",
            cdn_host: "http://tcloud-static.ywopt.com",
            dir: "static/",
            expire: 1563954221,
            host: "http://tcloud-static.oss-cn-beijing.aliyuncs.com",
            policy: "xxx",
            signature: "xxx"
        },
        message: "ok"
    }
    """
    result = get_token()

    return {
        'code': 0,
        'data': result,
        'message': 'ok'
    }


@public.route('/issue/', methods=['GET'])
def issue_query_type_handler():
    """
    @api {get} /v1/public/issue/ 获取 issue配置
    @apiName GetIssueConfig
    @apiGroup 公共
    @apiDescription 获取issue配置
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": {
            "chance": {
                "0": "必现",
                "1": "大概率",
                "2": "小概率",
                "3": "极小概率"
            },
            "type": {
                "0": "功能问题",
                "1": "界面优化",
                "2": "设计缺陷",
                "3": "安全相关",
                "4": "性能问题",
                "5": "开发修改引入",
                "6": "其他"
            }
        },
        "message": "ok"
    }
    """
    issue_config = current_app.config['ISSUE_CONFIG']
    return {
        'code': 0,
        'data': issue_config,
    }


# 获取需求类型值
@public.route('/requirement/', methods=['GET'])
def requirement_query_type_handler():
    """
    @api {get} /v1/public/requirement/ 获取 requirement配置
    @apiName GetRequirementConfig
    @apiGroup 公共
    @apiDescription 获取requirement配置
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": {
            "type": {
                "0": "功能需求",
                "1": "优化需求",
                "2": "自动化需求",
                "3": "性能需求",
                "4": "兼容性需求",
                "5": "报表需求",
                "6": "临时需求",
                "7": "紧急需求",
                "8": "新功能需求",
                "9": "其他"
            }
        },
        "message": "ok"
    }
    """
    requirement_config = current_app.config['REQUIREMENT_CONFIG']
    return {
        'code': 0,
        'data': requirement_config,
    }


# 获取用例类型值
@public.route('/case/', methods=['GET'])
def case_query_type_handler():
    """
    @api {get} /v1/public/case/ 获取 case配置
    @apiName GetCaseConfig
    @apiGroup 公共
    @apiDescription 获取case配置
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": {
            "ctype": {
                "1": "功能回归",
                "2": "冒烟",
                "3": "UI自动化",
                "4": "接口自动化",
                "5": "新功能"
            },
            "priority": {
                "0": "紧急",
                "1": "高",
                "2": "中",
                "3": "低"
            }
        },
        "message": "ok"
    }
    """
    case_config = current_app.config['CASE_CONFIG']
    return {
        'code': 0,
        'data': case_config,
    }


# 获取任务配置
@public.route('/task/', methods=['GET'])
def task_query_type_handler():
    """
    @api {get} /v1/public/task/ 获取 task配置
    @apiName GetTaskConfig
    @apiGroup 公共
    @apiDescription 获取task配置
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": {
            "priority": {
                "0": "紧急",
                "1": "高",
                "2": "中",
                "3": "低"
            },
            "status": {
                "0": "新增",
                "1": "已完成",
                "2": "已拒绝"
            }
        },
        "message": "ok"
    }
    """
    task_config = current_app.config['TASK_CONFIG']
    return {
        'code': 0,
        'data': task_config,
    }


# 统一返回配置
@public.route('/projectconfig/', methods=['GET'])
def get_all_config():
    """
        @api {get} /v1/public/projectconfig/ 获取 全部配置
        @apiName GetProjectConfig
        @apiGroup 公共
        @apiDescription 获取全部配置
        @apiSuccessExample {json} Success-Response:
         HTTP/1.1 200 OK
         {
            "code": 0,
            "data": {
                "case_config": {
                },
                "issue_config": {
                },
                "requirement_config": {
                },
                "task_config": {
                }
              },
            "message": "ok"
        }
        """
    issue_config = current_app.config['ISSUE_CONFIG']
    requirement_config = current_app.config['REQUIREMENT_CONFIG']
    case_config = current_app.config['CASE_CONFIG']
    task_config = current_app.config['TASK_CONFIG']
    return {
        'code': 0,
        'data': {
            'issue_config': issue_config,
            'requirement_config': requirement_config,
            'case_config': case_config,
            'task_config': task_config
        }
    }


@public.route('/flow/', methods=['GET'])
def flow_query_type_handler():
    """
    @api {get} /v1/public/flow/ 获取 flow配置
    @apiName GetFlowConfig
    @apiGroup 公共
    @apiDescription 获取flow配置
    @apiParam {int} [projectid] 当前项目id
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": {
            "platform": {
                "1": "后端",
                "2": "PHP",
                "3": "APP",
                "4": "H5",
                "5": "微信商城",
                "6": "小程序"
            },
            "type": {
                "1": "版本需求",
                "2": "搜索推荐",
                "3": "问题修复",
                "4": "临时需求",
                "5": "优化",
                "6": "紧急需求"
            }
        },
        "message": "ok"
    }
    """
    project_id = request.args.get('projectid')
    if not project_id:
        project_id = 0
    code, flow_config = get_flow_config(project_id)
    return {
        'code': code,
        'data': flow_config,
    }


@public.route('/online/', methods=['GET'])
def online_count():
    """
    @api {get} /v1/public/online/ 获取 在线人数
    @apiName GetOnline
    @apiGroup 公共
    @apiDescription 获取10分钟内在线人数
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": {
            "count": 3
        },
        "message": "ok"
    }
    """
    code, data = get_count_online()
    return {'code': code, 'data': data}


@public.route('/route/statistics/', methods=['GET'])
def route_statistics():
    """
    @api {get} /v1/route/statistics/ 获取 各个接口的调用次数
    @apiName GetRouteStatistics
    @apiGroup 公共
    @apiDescription 获取各个接口的调用次数
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": {
            "boardconfig": {
                "4": "3"
            },
            "datashow": {
                "correction/first": "2",
                "fields": "2",
                "resource/22": "1",
                "resource/upload/22": "1",
                "response/kernel": "2"
            },
            "public": {
                "config": "9",
                "config/5": "1",
                "flow": "1",
                "online": "5",
                "ossauth": "15",
                "projectconfig": "1",
                "route/statistics": "4"
            }
        },
        "message": "ok"
    }
    """
    code, data = get_statistics_route()
    return {'code': code, 'data': data}
