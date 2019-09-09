from flask import Blueprint, request

from apps.interface.business.interfacetask import InterfaceTaskBusiness

interfacetask = Blueprint('interfacetask', __name__)


# todo 暂时未调用

@interfacetask.route('/run', methods=['POST'])
def run_task():
    """
    @api {post} /v1/interfacetask/run InterfaceTask_单次运行任务
    @apiName interfaceTaskRun
    @apiGroup Interface
    @apiDescription 单次运行任务
    @apiParam {int} id 任务id
    @apiParamExample {json} Request-Example:
    {
        "id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "data": {
            "report_id": 1,
        },
        "status": 1,
        "msg": "测试成功"
    }
    """
    data = request.json
    ids = data.get('id')
    jsondata = InterfaceTaskBusiness.run_task(ids)
    return jsondata


@interfacetask.route('/start', methods=['POST'])
def start_task():
    """
    @api {post} /v1/interfacetask/start InterfaceTask_任务开启
    @apiName interfaceTaskStart
    @apiGroup Interface
    @apiDescription 任务开启
    @apiParam {int} id  任务id
    @apiParamExample {json} Request-Example:
    {
        "id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "status": 1,
        "msg": "启动成功"
    }
    """
    data = request.json
    ids = data.get('id')

    jsondata = InterfaceTaskBusiness.start_task(ids)
    return jsondata


@interfacetask.route('/add', methods=['POST'])
def add_task():
    """
    @api {post} /v1/interfacetask/add InterfaceTask_任务添加、修改
    @apiName interfaceTaskAdd
    @apiGroup Interface
    @apiDescription 任务添加、修改
    @apiParam {string} projectName  项目名称
    @apiParam {int} setIds  设置id
    @apiParam {int} caseIds  case id
    @apiParam {int} id  task id
    @apiParam {string} name  任务名称
    @apiParam {string} toEmail  收到邮件人
    @apiParam {string} sendEmail  发送邮件人
    @apiParam {string} password  发送邮件密码
    @apiParam {int} num  排序
    @apiParam {string} timeConfig  cron 配置
    @apiParamExample {json} Request-Example:
    {
        "project_name": "",
        "setIds": 1,
        "caseIds": 1,
        "task_id": 1,
        "name": "",
        "toEmail": "",
        "sendEmail": "",
        "password": "",
        "num": "",
        "timeConfig": ""
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "status": 0,
        "msg": "请选择项目"
    }
    """
    data = request.json
    project_name = data.get('projectName')
    set_ids = data.get('setIds')
    case_ids = data.get('caseIds')
    task_id = data.get('id')
    name = data.get('name')
    to_email = data.get('toEmail')
    send_email = data.get('sendEmail')
    password = data.get('password')
    num = data.get('num')
    time_config = data.get('timeConfig')

    jsondata = InterfaceTaskBusiness.add_task(project_name, set_ids, case_ids, task_id, name,
                                              to_email, send_email, password, num, time_config)
    return jsondata


@interfacetask.route('/edit', methods=['POST'])
def edit_task():
    """
    @api {post} /v1/interfacetask/edit InterfaceTask_返回待编辑任务信息
    @apiName interfaceTaskEdit
    @apiGroup Interface
    @apiDescription 返回待编辑任务信息
    @apiParam {int} id  task id
    @apiParamExample {json} Request-Example:
    {
        "id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "status": 1,
        "data": {}
    }
    """
    data = request.json
    task_id = data.get('id')
    jsondata = InterfaceTaskBusiness.edit_task(task_id)
    return jsondata


@interfacetask.route('/find', methods=['POST'])
def find_task():
    """
    @api {post} /v1/interfacetask/find InterfaceTask_查找任务信息
    @apiName interfaceTaskFind
    @apiGroup Interface
    @apiDescription 查找任务信息
    @apiParam {string} projectName  项目名称
    @apiParam {string} taskName  任务名称
    @apiParam {int} page  页面index
    @apiParam {int} sizePage 页面数量
    @apiParamExample {json} Request-Example:
    {
        "projectName": "",
        "taskName": "",
        "page": 1,
        "sizePage": 10
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "请先选择项目",
        "status": 0
    }
    """
    data = request.json
    project_name = data.get('projectName')
    task_name = data.get('taskName')
    page = data.get('page') if data.get('page') else 1
    per_page = data.get('sizePage') if data.get('sizePage') else 10

    jsondata = InterfaceTaskBusiness.find_task(project_name, task_name, page, per_page)
    return jsondata


@interfacetask.route('/del', methods=['POST'])
def del_task():
    """
    @api {post} /v1/interfacetask/del InterfaceTask_删除任务信息
    @apiName interfaceTaskDel
    @apiGroup Interface
    @apiDescription 删除任务信息
    @apiParam {int} id  任务id
    @apiParamExample {json} Request-Example:
    {
        "id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "删除成功",
        "status": 1
    }
    """
    data = request.json
    ids = data.get('id')

    jsondata = InterfaceTaskBusiness.del_task(ids)
    return jsondata


@interfacetask.route('/pause', methods=['POST'])
def pause_task():
    """
    @api {post} /v1/interfacetask/pause InterfaceTask_暂停任务
    @apiName interfaceTaskPause
    @apiGroup Interface
    @apiDescription 暂停任务
    @apiParam {int} id 任务id
    @apiParamExample {json} Request-Example:
    {
        "id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "暂停成功",
        "status": 1
    }
    """
    data = request.json
    ids = data.get('id')
    jsondata = InterfaceTaskBusiness.pause_task(ids)
    return jsondata


@interfacetask.route('/resume', methods=['POST'])
def resume_task():
    """
    @api {post} /v1/interfacetask/resume InterfaceTask_恢复任务
    @apiName interfaceTaskResume
    @apiGroup Interface
    @apiDescription 恢复任务
    @apiParam {int} id  任务id
    @apiParamExample {json} Request-Example:
    {
        "id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "恢复成功",
        "status": 1
    }
    """
    data = request.json
    ids = data.get('id')
    jsondata = InterfaceTaskBusiness.resume_task(ids)
    return jsondata


@interfacetask.route('/remove', methods=['POST'])
def remove_task():
    """
    @api {post} /v1/interfacetask/remove InterfaceTask_移除任务
    @apiName interfaceTaskRemove
    @apiGroup Interface
    @apiDescription 移除任务
    @apiParam {int} id 任务id
    @apiParamExample {json} Request-Example:
    {
        "id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "msg": "移除成功",
        "status": 1
    }
    """
    data = request.json
    ids = data.get('id')
    jsondata = InterfaceTaskBusiness.remove_task(ids)

    return jsondata
