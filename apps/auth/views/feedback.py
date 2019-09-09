from apps.auth.business.feedback import FeedbackBusiness
from apps.auth.extentions import validation, parse_json_form
from library.api.render import json_detail_render
from library.api.tBlueprint import tblueprint

bpname = 'feedback'
bpname_relate = 'projectconfig'
feedback = tblueprint(bpname, __name__, bpname=bpname_relate, has_view=False)


# 用户反馈新增
@feedback.route('/', methods=['POST'])
@validation('POST:feedback_create')
def feedback_add_handler():
    """
    @api {post} /v1/feedback 新增 反馈
    @apiName CreateFeedback
    @apiGroup 用户
    @apiDescription 提交一个反馈
    @apiParam {string} [contact] 联系方式
    @apiParam {string} comment 反馈内容
    @apiParamExample {json} Request-Example:
    {
       "contact": "xxx@xxx.com",
       "comment": "xx模块有问题"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
       "code": 0,
       "data": [],
       "message": ""
     }
    """
    contact, comment = parse_json_form('feedback_create')
    ret = FeedbackBusiness.feedback_create(contact, comment)
    return json_detail_render(ret)


# 用户反馈单个删除
@feedback.route('/<int:feedback_id>', methods=['DELETE'])
def feedback_modify_handler(feedback_id):
    ret = FeedbackBusiness.feedback_delete(feedback_id)
    return json_detail_render(ret)


# 用户反馈查询-userID
@feedback.route('/', methods=['GET'])
def feedback_query_all_handler():
    """
    @api {get} /v1/feedback 获取 反馈
    @apiName GetFeedback
    @apiGroup 用户
    @apiDescription 根据创建者id或者获取全部反馈
    @apiParam {int} userid 创建者id
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
    "code": 0,
    "data": [
        {
            "comment": "1",
            "contact": "1",
            "creation_time": "2019-07-22",
            "creator_id": 20,
            "creator_name": "刘德华",
            "id": 17
        }
    ],
    "message": "ok"
    }
    """
    data = FeedbackBusiness.query_all_json()
    return json_detail_render(0, data)


# 用户反馈单个查询
@feedback.route('/<int:feedback_id>', methods=['GET'])
def feedback_query_handler(feedback_id):
    data = FeedbackBusiness.query_by_id(feedback_id)
    return json_detail_render(0, data)
