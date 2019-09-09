from flask import request

from apps.flow.business.deploy import DeployBusiness, DeployRecordBusiness, DeployLogBusiness
from apps.flow.extentions import validation, parse_json_form, parse_list_args2
from library.api.render import json_detail_render, json_list_render2
from library.api.tBlueprint import tblueprint

bpname = 'deploy'
bpname_relate = 'flow'
view_permission = f'{bpname_relate}_view'
modify_permission = f'{bpname_relate}_modify'
deploy = tblueprint(bpname, __name__, bpname=bpname_relate)


@deploy.route('/getserver', methods=['GET'])
def deploy_get_server_handler():
    """
    @api {get} /v1/deploy/getserver 获取服务列表
    @apiName deployGetServer
    @apiGroup Deploy
    @apiDescription 获取服务列表
    @apiParam {int} project_id 项目id
    @apiParamExample {json} Request-Example:
    {
        "project_id": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "default_branch": "master",
                "git_origin": "ssh://git@git.innotechx.com:7999/x/pt-cluster.git",
                "id": 369,
                "is_increment": 0,
                "is_short": false,
                "name": "ptgate-sx",
                "node_list": [
                    {
                        "id": 293,
                        "name": "sx-79",
                        "private_id": "192.168.18.79",
                        "version": "0.0.35"
                    },
                    {
                        "id": 269,
                        "name": "sx-64",
                        "private_id": "192.168.18.64",
                        "version": "0.0.12"
                    }
                ],
                "project_id": 27,
                "project_name": "萌推开发测试组"
            },
            {
                "default_branch": "develop",
                "git_origin": "ssh://git@git.innotechx.com:7999/x/pt-promote.git",
                "id": 542,
                "is_increment": 0,
                "is_short": false,
                "name": "pt-sp-sx",
                "node_list": [
                    {
                        "id": 269,
                        "name": "sx-64",
                        "private_id": "192.168.18.64",
                        "version": "0.0.12"
                    },
                    {
                        "id": 293,
                        "name": "sx-79",
                        "private_id": "192.168.18.79",
                        "version": "0.0.35"
                    }
                ],
                "project_id": 27,
                "project_name": "萌推开发测试组"
            }
        ],
        "message": "查询成功"
    }
    """
    code, data, message = DeployBusiness.get_server()

    return json_detail_render(code, data, message)


@deploy.route('/getnode', methods=['GET'])
def deploy_get_node_handler():
    """
    @api {get} /v1/deploy/getnode 获取节点列表
    @apiName deployGetNode
    @apiGroup Deploy
    @apiDescription 获取节点列表
    @apiParam {int} project_id 项目id
    @apiParamExample {json} Request-Example:
    {
        "project_id": 1,
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 101,
        "data": [],
        "message": "can not find object"
    }
    """
    code, data, message = DeployBusiness.get_node()

    return json_detail_render(code, data, message)


@deploy.route('/', methods=['POST'])
@validation('POST:deploy_create')
def deploy_create_handler():
    """
    @api {post} /v1/deploy 创建数据
    @apiName deployCreate
    @apiGroup Deploy
    @apiDescription 创建数据
    @apiParam {int} project_id 项目id
    @apiParam {list} server_list 服务列表
    @apiParam {list} node_list 节点列表
    @apiParam {string} branch 分支
    @apiParam {int} flow_id  流程id
    @apiParamExample {json} Request-Example:
    {
        "project_id": 1,
        "server_list": [],
        "node_list": [],
        "branch": "",
        "flow_id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 101,
        "data": [
            {
                deploy_id: None
            }
        ],
        "message": "can not find object"
    }
    """
    project_id, server_list, node_list, branch, flow_id = parse_json_form('deploy_create')

    code, deploy_id = DeployBusiness.create(project_id, server_list, node_list, branch, flow_id)

    if code == 101:
        return json_detail_render(code, [{'deploy_id': deploy_id}], '此服务正在部署请稍后')

    return json_detail_render(code, [{'deploy_id': deploy_id}])


@deploy.route('/update/result', methods=['POST'])
@validation('POST:deploy_result')
def update_deploy_result():
    """
    @api {get} /v1/deploy/update/result 更新部署结果
    @apiName deployUpdateResult
    @apiGroup Deploy
    @apiDescription 更新部署结果
    @apiParam {int} deploy_id 部署id
    @apiParam {list} result 部署结果
    @apiParamExample {json} Request-Example:
    {
        "deploy_id": 1,
        result: []
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    deploy_id, result = parse_json_form('deploy_result')

    code = DeployRecordBusiness.modify_result(result, deploy_id)

    # DeployRecordBusiness.run_automan(deploy_id)

    # 写入部署日志,等结果部署完成之后再写入结果

    single_data = DeployRecordBusiness.not_init_data(deploy_id)
    if len(single_data) == 0:
        delopy_data = DeployRecordBusiness.query_record_deploy(deploy_id)
        if len(delopy_data) > 0:
            DeployLogBusiness.deploy_data(delopy_data, deploy_id)

    # DeployRecordBusiness.run_automan(deploy_id)

    # 写入自动化日志

    # DeployLogBusiness.automan_data(auto_man_data[1],deploy_id)

    return json_detail_render(code, [], 'ok')


@deploy.route('/new_data', methods=['GET'])
def gain_deploy_data():
    """
    @api {get} /v1/deploy/new_data 获取当前deploy_id 的信息
    @apiName deployNew_data
    @apiGroup Deploy
    @apiDescription 获取当前deploy_id 的信息
    @apiParam {int} project_id 项目id
    @apiParam {int} flow_id 流程id
    @apiParam {int} deploy_id 部署id
    @apiParamExample {json} Request-Example:
    {
        "project_id": 45,
        "flow_id": 1,
        "deploy_id": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "branch": "develop",
                "deploy_id": 160,
                "flow_id": 232,
                "id": 179,
                "node_id": 31,
                "node_name": "yn-244",
                "project_id": 4,
                "result": 1,
                "server_id": 45,
                "server_name": "submarine-test",
                "status": 0,
                "version": "1.1.75"
            }
        ],
        "message": "成功"
    }
    """

    data = DeployRecordBusiness.query_deploy_id_json()

    combine_data = {'is_one_Key': 1, 'data': data}

    single_data = DeployRecordBusiness.is_one_key()
    if len(single_data) == 0:
        combine_data['is_one_Key'] = 0

    return json_detail_render(0, combine_data)


@deploy.route('/history_data', methods=['GET'])
def gain_old_data():
    """
    @api {get} /v1/deploy/history_data 获取历史部署记录
    @apiName deployHistory_data
    @apiGroup Deploy
    @apiDescription 获取历史部署记录
    @apiParam {int} server_id 服务id
    @apiParamExample {json} Request-Example:
    {
        "project_id": 4,
        "flow_id": 232,
        "page_size": 10,
        "page_index": 1
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "branch": "develop",
                "deploy_id": 160,
                "flow_id": 232,
                "id": 179,
                "node_id": 31,
                "node_name": "yn-244",
                "project_id": 4,
                "result": 1,
                "server_id": 45,
                "server_name": "submarine-test",
                "status": 0,
                "version": "1.1.75"
            },
            {
                "branch": "develop",
                "deploy_id": 159,
                "flow_id": 232,
                "id": 178,
                "node_id": 31,
                "node_name": "yn-244",
                "project_id": 4,
                "result": 4,
                "server_id": 45,
                "server_name": "submarine-test",
                "status": 0,
                "version": "1.1.74"
            }
        ],
        "message": "ok",
        "page_index": 1,
        "page_size": 10,
        "total": 2
    }
    """
    page_size, page_index = parse_list_args2()
    project_id = request.args.get('project_id')
    flow_id = request.args.get('flow_id')
    data = DeployRecordBusiness.query_all_json(page_size, page_index)

    count = DeployRecordBusiness.query_all_count(project_id, flow_id)

    return json_list_render2(0, data, page_size, page_index, count)


@deploy.route('/check_log', methods=['GET'])
def check_log_data():
    """
    @api {get} /v1/deploy/check_log 查看历史日志
    @apiName deployCheck_log
    @apiGroup Deploy
    @apiDescription 查看历史日志
    @apiParam {int} record_id 记录id
    @apiParamExample {json} Request-Example:
    {
        "record_id": 179
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": {
            "command": {
                "status": 0,
                "stderr": "",
                "stdout": ""
            },
            "compile": {
                "status": 0,
                "stderr": "",
                "stdout": ""
            },
            "deploy": {
                "status": 0,
                "stderr": "",
                "stdout": ""
            },
            "refresh": {
                "status": 0,
                "stderr": "",
                "stdout": ""
            },
            "restart": {
                "status": 0,
                "stderr": "",
                "stdout": ""
            }
        },
        "message": "成功"
    }
    """

    code, data, message = DeployRecordBusiness.check_log_data()
    return json_detail_render(code, data, message)


@deploy.route('/branch', methods=['GET'])
def update_branch():
    """
    @api {get} /v1/deploy/branch 获取分支信息
    @apiName deployBranch
    @apiGroup Deploy
    @apiDescription 获取分支信息
    @apiParam {int} server_id 服务id
    @apiParamExample {json} Request-Example:
    {
        "server_id": 45
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            "20190604",
            "master",
            "develop",
            "release/inno",
            "dev/push",
            "release/cpc"
        ],
        "message": "成功"
    }
    """
    code, data, message = DeployBusiness.get_branch()

    return json_detail_render(code, data, message)
