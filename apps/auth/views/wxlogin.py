from flask import Blueprint

from apps.auth.business.wxlogin import WxLoginBusiness
from apps.auth.extentions import validation, parse_json_form
from library.api.render import json_detail_render

wxlogin = Blueprint("wxlogin", __name__)


@wxlogin.route('/', methods=['POST'])
@validation('POST:wx_user_code')
def wxuser_index_handler():
    """
    @api {post} /v1/wxlogin/ 登录 微信
    @apiName WxLogin
    @apiGroup 用户
    @apiDescription 登录微信
    @apiParam {string} user_code 用户编码
    @apiParamExample {json} Request-Example:
    {
        "user_code":"j2qL3QjNXXwa_4A0WJFDNJyPEx88HTHytARgRbr176g"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
       "code": 0,
       "data": {
            "token": "asdasdasd"
        },
       "message": ""
     }
    """
    user_code = parse_json_form('wx_user_code')

    ret, data, msg = WxLoginBusiness.get_user(user_code[0])

    return json_detail_render(ret, data, msg)
