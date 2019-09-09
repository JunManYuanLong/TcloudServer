from flask import request, Blueprint, g

from apps.auth.auth_require import rpc_required
from apps.message.daos.message import (
    create_by_one2one, get_all_message_by_user_id, get_5_message_by_user_id, change_status,
    get_all_read_message_by_user_id, get_all_unread_message_by_user_id, delete_status,
)
from apps.message.extentions import validation, parse_json_form, parse_list_args2
from library.api.exceptions import OperationPermissionDeniedException

message = Blueprint('message', __name__)

"""
新建站内信时，查询接收者未读总数，发到redis
删除、修改状态是也查询总数，发到redis
"""


# TODO 给站内信加上权限，开发期间先关掉

@message.route('/', methods=['POST'])
@rpc_required
@validation('POST:message_create')
def create():
    """
    @api {post} /v1/message 新增 站内信
    @apiName CreateMessage
    @apiGroup 站内信
    @apiDescription 流程创建等模块中调用该接口创建站内信
    @apiParam {int} send_id 发送者
    @apiParam {int} rec_id 接收者
    @apiParam {string} content 内容
    @apiParamExample {json} Request-Example:
    {
       "send_id": 1,
       "rec_id": [96,97,98]
       "content": "你被选中了"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
       "code": 0,
       "data": [],
       "message": ""
     }
    @apiErrorExample {json} Error-Response:
     HTTP/1.1 200 OK
     {
       "code": 102,
       "data": [],
       "message": "save object error"
     }
    """
    send_id, rec_ids, content, message_type, group = parse_json_form('message_create')
    if rec_ids and '' not in rec_ids and None not in rec_ids:
        code = create_by_one2one(send_id, rec_ids, content, message_type, group)
    else:
        code = 102
    return {'code': code}


@message.route('/', methods=['GET'])
def get():
    """
    @api {get} /v1/message 获取 站内信
    @apiName GetMessage
    @apiGroup 站内信
    @apiDescription 获取站内信，通过参数获得最近10个或者全部
    @apiParam {int} user 当前用户id
    @apiParam {int} [isall] 是否获取全部，为1获取全部，不填或0获取最近5个(未读不足5个时，再加已读的到5个)
    @apiParam {int} [page_size] 分页-单页数目
    @apiParam {int} [page_index] 分页-页数
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "content": "[Tcloud - 测试站内信3]",
                "create_time": "2019-07-10 18:58:04",
                "id": 10,
                "status": 0
            },
            {
                "content": "[Tcloud - 测试站内信2]",
                "create_time": "2019-07-10 17:44:51",
                "id": 3,
                "status": 0
            }
        ],
        "page_index": 1,
        "page_size": 10,
        "total": 12,
        "message": "ok"
    }
    """
    user = request.args.get('user')
    if user != str(g.userid):
        raise OperationPermissionDeniedException
    isall = request.args.get('isall')
    page_size, page_index = parse_list_args2()
    if isall:
        code, data, total = get_all_message_by_user_id(user, page_size, page_index)
    else:
        code, data, total = get_5_message_by_user_id(user)
    return {'code': code, 'data': data, 'page_index': page_index, 'page_size': page_size, 'total': total}


@message.route('/status', methods=['GET'])
def get_by_status():
    """
    @api {get} /v1/message/status 获取 站内信通过状态
    @apiName GetMessageByStatus
    @apiGroup 站内信
    @apiDescription 根据状态获取站内信
    @apiParam {int} user 当前用户id
    @apiParam {int} [isread] 根据状态获取站内信，为1时获取所有已读，不填或者0获取未读
    @apiParam {int} [page_size] 分页-单页数目
    @apiParam {int} [page_index] 分页-页数
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "content": "[Tcloud - 测试站内信3]",
                "create_time": "2019-07-10 18:58:04",
                "id": 10,
                "status": 0
            },
            {
                "content": "[Tcloud - 测试站内信2]",
                "create_time": "2019-07-10 17:44:51",
                "id": 3,
                "status": 0
            }
        ],
        "page_index": 1,
        "page_size": 10,
        "total": 12
        "message": "ok"
    }
    """
    user = request.args.get('user')
    if user != str(g.userid):
        raise OperationPermissionDeniedException
    isread = request.args.get('isread')
    page_size, page_index = parse_list_args2()
    if isread == '1':
        code, data, total = get_all_read_message_by_user_id(user, page_size, page_index)
    else:
        code, data, total = get_all_unread_message_by_user_id(user, page_size, page_index)
    return {'code': code, 'data': data, 'page_index': page_index, 'page_size': page_size, 'total': total}


@message.route('/', methods=['PUT'])
def modify():
    """
    @api {put} /v1/message 修改 站内信状态
    @apiName ModifyMessageStatus
    @apiGroup 站内信
    @apiDescription 修改站内信状态
    @apiParam {int} user 当前用户id
    @apiParam {int} id 站内信id，example:1,2,3,4
    @apiParam {int} [isall] 为1时，标记所有通知已读
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    user = request.args.get('user')
    if user != str(g.userid):
        raise OperationPermissionDeniedException
    message_ids = request.args.get('id')
    isall = request.args.get('isall')
    if isall == '1':
        code, info = change_status(user, isall=isall)
    else:
        code, info = change_status(user, message_ids=message_ids)
    return {'code': code, 'message': info}


@message.route('/', methods=['DELETE'])
def delete():
    """
    @api {delete} /v1/message 删除 站内信状态
    @apiName DeleteMessageStatus
    @apiGroup 站内信
    @apiDescription 删除站内信状态
    @apiParam {int} user 当前用户id
    @apiParam {int} id 站内信id example:1,2,3,4
    @apiParam {int} [isall] 为1时，标记所有通知已读
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    user = request.args.get('user')
    if user != str(g.userid):
        raise OperationPermissionDeniedException
    message_ids = request.args.get('id')
    isall = request.args.get('isall')
    if isall == '1':
        code, info = delete_status(user, isall=isall)
    else:
        code, info = delete_status(user, message_ids=message_ids)
    return {'code': code, 'message': info}
