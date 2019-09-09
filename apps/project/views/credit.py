from flask import Blueprint

from apps.project.business.credit import CreditBusiness, CreditRecordBusiness
from apps.project.extentions import parse_json_form, parse_list_args2
from library.api.render import json_detail_render, json_list_render2

bpname = 'credit'
credit = Blueprint(bpname, __name__)


@credit.route('/', methods=['GET'])
def credit_index_handler():
    """
    @api {GET} /v1/credit 查询 信用积分
    @apiName GetCredit
    @apiGroup 项目
    @apiDescription 查询 信用积分
    @apiParam {int} [page_size] 分页-页面大小
    @apiParam {int} [page_index] 分页-页数
    @apiParamExample {json} Request-Example:
    ?page_size=1&page_index=5
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "id": 6,
                "score": 48,
                "status": 0,
                "user_id": 95
            },
            {
                "id": 7,
                "score": 101,
                "status": 0,
                "user_id": 1
            },
            {
                "id": 8,
                "score": 110,
                "status": 0,
                "user_id": 26
            }
        ],
        "message": "ok",
        "page_index": 1,
        "page_size": 3,
        "total": 8
    }
    """
    page_size, page_index = parse_list_args2()
    page_size = page_size or 10
    page_index = page_index or 1
    data, total = CreditBusiness.paginate_data(page_size, page_index)
    return json_list_render2(0, data, page_size, page_index, total)


@credit.route('/', methods=['POST'])
def credit_create_handler():
    """
    @api {post} /v1/credit 初始化 信用积分
    @apiName CreateCredit
    @apiGroup 项目
    @apiDescription 初始化 信用积分
    @apiParamExample {json} Request-Example:
    {
        "user_id": 4
    }
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": 8,
    }
    """
    user_id = parse_json_form('credit_create')
    ret, msg = CreditBusiness.create(user_id=user_id, score=100, status=0)
    return json_detail_render(ret, [], msg)


@credit.route('/record/<int:user_id>', methods=['GET'])
def credit_record_index_handler(user_id):
    """
    @api {post} /v1/credit/record/{int:user_id} 查询 信用积分记录
    @apiName GetCreditRecordByUserId
    @apiGroup 项目
    @apiDescription 查询 信用积分记录
    @apiParam {int} user_id 根据 用户 ID 查询积分记录
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [
            {
                "modified_time": "2019-06-14 22:17:59",
                "operation": "初始化 孟伟 信用分为 100"
            }
        ],
        "message": "ok"
    }
    """
    data = CreditRecordBusiness.query_record_detail(user_id)
    return json_detail_render(0, data)
