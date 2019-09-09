from flask import Blueprint

from apps.extention.business.tool import ToolBusiness
from apps.extention.extentions import validation, parse_json_form
from library.api.render import json_detail_render

tool = Blueprint('tool', __name__)


@tool.route('/ip', methods=['GET'])
def tool_ip():
    """
    @api {get} /v1/tool/ip 查询 ip 地址信息
    @apiName GetIpAddress
    @apiGroup 拓展
    @apiDescription 查询 ip 地址信息
    @apiParam {string} ip 合法的 ip 地址
    @apiParamExample {json} Request-Example:
    {
     "ip": "110.110.110.12"
    }
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
      "code": 0,
      "data": {
        "address": "\u4e0a\u6d77\u5e02",
        "address_detail": {
          "city": "\u4e0a\u6d77\u5e02",
          "city_code": 289,
          "district": "",
          "province": "\u4e0a\u6d77\u5e02",
          "street": "",
          "street_number": ""
        },
        "point": {
          "x": "13524118.26",
          "y":"3642780.37"
        }
      },
      "message":"ok"
    }
    """
    code, data, address, message = ToolBusiness.get_tool_ip()

    return json_detail_render(code, data, message)


@tool.route('/apk/analysis', methods=['POST'])
@validation('POST:tool_apk_analysis_upload')
def apk_analysis_handler():
    """
    @api {post} /v1/tool/apk/analysis 分析 apk 包信息
    @apiName AnalysisApkInformation
    @apiGroup 拓展
    @apiDescription 分析 apk 包信息
    @apiParam {apk_download_url} apk 包的下载地址
    @apiParamExample {json} Request-Example:
    {
      "apk_download_url": "http://tcloud-static.ywopt.com/static/3787c7f2-5caa-434a-9a47-3e6122807ada.apk"
    }
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "data": {
            "default_activity": "com.earn.freemoney.cashapp.activity.SplashActivity",
            "icon": "iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAVr0lEQVR42u2debAdVZ3HP6f79N3ekuQlJOQlARICBCGs",
            "label": "Dosh Winner",
            "package_name": "com.earn.freemoney.cashapp",
            "size": "13.97",
            "version_code": "86",
            "version_name": "2.0.36"
        },
        "message": "ok"
    }
    """
    apk_download_url, type = parse_json_form('tool_apk_analysis_upload')
    if apk_download_url:
        data = ToolBusiness.apk_analysis(apk_download_url, type)
        return json_detail_render(0, data)
    else:
        return json_detail_render(101, 'apk_download_url is required!')
