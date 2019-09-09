from flask import Blueprint, request

from apps.autotest.business.datashow import (
    DataShowFieldsBusiness, DataShowResponseKernelRecordBusiness,
    DataShowFirstPageFirstWordCorrectRateBusiness, DataShowResponseLogBusiness,
)
from apps.autotest.extentions import parse_list_args2, validation, parse_json_form

datashow = Blueprint('datashow', __name__)


@datashow.route('/fields', methods=['GET'])
def fields_index_handler():
    """
    @api {get} /v1/datashow/fields 查询 测试数据属性 列表
    @apiName GetDataShowFields
    @apiGroup 自动化测试
    @apiDescription 查询 测试数据属性 列表
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "data": {
        "1": [
          {
            "id": 7,
            "value": "test"
          }
        ],
        "2": [
          {
            "id": 6,
            "value": "2"
          }
        ]
      },
      "message": "ok"
    }
    """
    data = DataShowFieldsBusiness.query_all_json()
    return {
        "data": data
    }


@datashow.route('/fields', methods=['POST'])
@validation('POST:data_show_filed_create')
def fields_create_handler():
    """
    @api {post} /v1/datashow/fields 新增 测试数据属性
    @apiName SetDataShowFields
    @apiGroup 自动化测试
    @apiDescription 新建 测试数据属性
    @apiParam {int} data_type 属性类型
    @apiParam {base_string} data_value 属性值
    @apiParamExample {json} Request-Example:
    {
        "data_type": 1,
        "data_value": "test"
    }
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "data": [],
      "message": "ok"
    }
    """
    data_type, data_value = parse_json_form("data_show_filed_create")
    code = DataShowFieldsBusiness.create(data_type, data_value)
    return {
        "code": code
    }


@datashow.route('/response/kernel', methods=['GET'])
def response_kernel_get_handler():
    """
    @api {get} /v1/datashow/response/kernel 查询 响应时间_内核录屏 列表
    @apiName GetDataShowResponseKernel
    @apiGroup 自动化测试
    @apiDescription 查询 响应时间_内核录屏 列表
    @apiParam {int} data_source 数据来源
    @apiParam {int} phone_model 手机类型
    @apiParam {int} apk_version apk 版本
    @apiParam {int} kernel_version 内核版本
    @apiParam {int} system_version 系统版本
    @apiParam {int} thesaurus_version 词库版本
    @apiParam {int} corpus_version 语料库版本
    @apiParam {int} show_in_chart 获取图信息 0:获取，1:不获取
    @apiParam {int} date_time 配合show_in_chart使用的时间段：0：默认，1：7天，2：1个月
    @apiParamExample {json} Request-Example:
    ?data_source=1
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "data": [
        {
          "apk_version": "3",
          "average": "9",
          "comment": "",
          "corpus_version": "test",
          "creation_time": "",
          "creator": "",
          "creator_nickname": "",
          "data_source": "1",
          "id": 1,
          "kernel_version": "4",
          "key_9_and_26": "8",
          "line_90_percent": "",
          "line_95_percent": "",
          "phone_model": "2",
          "system_version": "1",
          "thesaurus_version": "2",
          "show_in_chart": 0
        }
      ],
      "message": "ok",
      "page_index": 1,
      "page_size": 10,
      "total": 8
    }
    """
    show_in_chart = request.args.get('show_in_chart')
    date_time = str(request.args.get('date_time', '0'))
    if str(show_in_chart) == "0":
        data = DataShowResponseKernelRecordBusiness.query_chart_data(date_time)
        return {
            "data": data
        }
    else:
        page_size, page_index = parse_list_args2()
        data, count = DataShowResponseKernelRecordBusiness.query_all_data(page_size, page_index)
        return {
            "data": data,
            "total": count,
            "page_index": page_index,
            "page_size": page_size
        }


@datashow.route('/response/kernel', methods=['POST'])
@validation('POST:data_show_response_kernel_record_create')
def response_kernel_create_handler():
    """
    @api {post} /v1/datashow/response/kernel 新增 响应时间_内核录屏
    @apiName CreateDataShowResponseKernel
    @apiGroup 自动化测试
    @apiDescription 创建 响应时间_内核录屏
    @apiParam {int} data_source 数据来源
    @apiParam {int} phone_model 手机类型
    @apiParam {int} apk_version apk 版本
    @apiParam {int} kernel_version 内核版本
    @apiParam {int} system_version 系统版本
    @apiParam {int} thesaurus_version 词库版本
    @apiParam {int} corpus_version 语料库版本
    @apiParam {string} key_9_and_26 9键26键
    @apiParam {string} average 平均值
    @apiParam {string} line_90_percent 90% Line
    @apiParam {string} line_95_percent 95% Line
    @apiParam {string} comment 备注
    @apiParam {int} show_in_chart 是否显示在图表中,0:保存，1:不保存
    @apiParamExample {json} Request-Example:
    {
        "data_source": 1,
        "phone_model": 2,
        "apk_version": 3,
        "kernel_version": 4,
        "system_version": 5,
        "thesaurus_version": 6,
        "corpus_version": 7,
        "key_9_and_26": "1231.123123",
        "average": "12.13",
        "line_90_percent": "12.23",
        "line_95_percent": "12.23",
        "comment": "asdfasdfasdf",
        "show_in_chart": 0
    }
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "message": "ok"
    }
    """
    params = parse_json_form('data_show_response_kernel_record_create')
    data = DataShowResponseKernelRecordBusiness.create(params)
    return {
        "message": "创建成功",
        "code": data
    }


@datashow.route('/response/kernel/<int:id>', methods=['POST'])
@validation('POST:data_show_response_kernel_record_create')
def response_kernel_update_handler(id):
    """
    @api {post} /v1/datashow/response/kernel/{id:int} 修改 响应时间_内核录屏
    @apiName ModifyDataShowResponseKernel
    @apiGroup 自动化测试
    @apiDescription 修改 响应时间_内核录屏
    @apiParam {int} data_source 数据来源
    @apiParam {int} phone_model 手机类型
    @apiParam {int} apk_version apk 版本
    @apiParam {int} kernel_version 内核版本
    @apiParam {int} system_version 系统版本
    @apiParam {int} thesaurus_version 词库版本
    @apiParam {int} corpus_version 语料库版本
    @apiParam {string} key_9_and_26 9键26键
    @apiParam {string} average 平均值
    @apiParam {string} line_90_percent 90% Line
    @apiParam {string} line_95_percent 95% Line
    @apiParam {string} comment 备注
    @apiParam {int} show_in_chart 是否显示在图表中,0:保存，1:不保存
    @apiParamExample {json} Request-Example:
    {
        "data_source": 1,
        "phone_model": 2,
        "apk_version": 3,
        "kernel_version": 4,
        "system_version": 5,
        "thesaurus_version": 6,
        "corpus_version": 7,
        "key_9_and_26": "1231.123123",
        "average": "12.13",
        "line_90_percent": "12.23",
        "line_95_percent": "12.23",
        "comment": "asdfasdfasdf",
        "show_in_chart": 0
    }
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "message": "ok"
    }
    """
    params = parse_json_form('data_show_response_kernel_record_create')
    data = DataShowResponseKernelRecordBusiness.update(id, params)
    return {
        "message": "更新成功",
        "code": data
    }


@datashow.route('/response/kernel/<int:id>', methods=['DELETE'])
def response_kernel_delete_handler(id):
    """
    @api {delete} /v1/datashow/response/kernel/{id:int} 删除 响应时间_内核录屏
    @apiName DeleteDataShowResponseKernel
    @apiGroup 自动化测试
    @apiDescription 删除 响应时间_内核录屏
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "message": "ok"
    }
    """
    data = DataShowResponseKernelRecordBusiness.delete(id)
    return {
        "message": "删除成功",
        "code": data
    }


@datashow.route('/correction/first', methods=['GET'])
def response_first_get_handler():
    """
    @api {get} /v1/datashow/correction/first 查询 首页响应准确率 列表
    @apiName GetDataShowFirstPageWord
    @apiGroup 自动化测试
    @apiDescription 查询 首页响应准确率 列表
    @apiParam {int} data_source 数据来源
    @apiParam {int} phone_model 手机类型
    @apiParam {int} apk_version apk 版本
    @apiParam {int} kernel_version 内核版本
    @apiParam {int} system_version 系统版本
    @apiParam {int} thesaurus_version 词库版本
    @apiParam {int} corpus_version 语料库版本
    @apiParam {int} show_in_chart 获取图信息 0:获取，1:不获取
    @apiParam {int} date_time 配合show_in_chart使用的时间段：0：默认，1：7天，2：1个月
    @apiParamExample {json} Request-Example:
    ?data_source=1
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "data": [
        {
          "apk_version": "3",
          "comment": "",
          "corpus_version": "test",
          "creation_time": "",
          "creator": "",
          "creator_nickname": "",
          "data_source": "1",
          "first_page_correct_rate": "",
          "first_word_correct_rate": "9",
          "id": 1,
          "kernel_version": "4",
          "key_9_and_26": "8",
          "phone_model": "2",
          "system_version": "1",
          "thesaurus_version": "2",
          "show_in_chart": 0
        }
      ],
      "message": "ok",
      "page_index": 1,
      "page_size": 10,
      "total": 1
    }
    """
    show_in_chart = request.args.get('show_in_chart')
    date_time = str(request.args.get('date_time', '0'))
    if str(show_in_chart) == "0":
        data = DataShowFirstPageFirstWordCorrectRateBusiness.query_chart_data(date_time)
        return {
            "data": data
        }
    else:
        page_size, page_index = parse_list_args2()
        data, count = DataShowFirstPageFirstWordCorrectRateBusiness.query_all_data(page_size, page_index)
    return {
        "data": data,
        "total": count,
        "page_index": page_index,
        "page_size": page_size
    }


@datashow.route('/correction/first', methods=['POST'])
@validation('POST:data_show_first_page_first_word_correct_rate_create')
def response_first_create_handler():
    """
    @api {post} /v1/datashow/correction/first 新增 首页响应准确率
    @apiName CreateDataShowFirstPageWord
    @apiGroup 自动化测试
    @apiDescription 新增 首页响应准确率
    @apiParam {int} data_source 数据来源
    @apiParam {int} phone_model 手机类型
    @apiParam {int} apk_version apk 版本
    @apiParam {int} kernel_version 内核版本
    @apiParam {int} system_version 系统版本
    @apiParam {int} thesaurus_version 词库版本
    @apiParam {int} corpus_version 语料库版本
    @apiParam {string} key_9_and_26 9键26键
    @apiParam {string} first_word_correct_rate 首词准确率
    @apiParam {string} first_page_correct_rate 首页准确率
    @apiParam {string} comment 备注
    @apiParam {int} show_in_chart 是否显示在图表中,0:保存，1:不保存
    @apiParamExample {json} Request-Example:
    {
        "data_source": 1,
        "phone_model": 4,
        "apk_version": 3,
        "kernel_version": 4,
        "system_version": 5,
        "thesaurus_version": 6,
        "corpus_version": 7,
        "key_9_and_26": "1231.123123",
        "first_word_correct_rate": "12.13",
        "first_page_correct_rate": "12.23",
        "comment": "testsdfasdfdafdafdasf asdfas f",
        "show_in_chart": 0
    }
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "message": "ok"
    }
    """
    params = parse_json_form('data_show_first_page_first_word_correct_rate_create')
    data = DataShowFirstPageFirstWordCorrectRateBusiness.create(params)
    return {
        "message": "创建成功",
        "code": data
    }


@datashow.route('/correction/first/<int:id>', methods=['POST'])
@validation('POST:data_show_first_page_first_word_correct_rate_create')
def response_first_update_handler(id):
    """
    @api {post} /v1/datashow/correction/first/{id:int} 修改 首页响应准确率
    @apiName ModifyDataShowFirstPageWord
    @apiGroup 自动化测试
    @apiDescription 修改 首页响应准确率
    @apiParam {int} data_source 数据来源
    @apiParam {int} phone_model 手机类型
    @apiParam {int} apk_version apk 版本
    @apiParam {int} kernel_version 内核版本
    @apiParam {int} system_version 系统版本
    @apiParam {int} thesaurus_version 词库版本
    @apiParam {int} corpus_version 语料库版本
    @apiParam {string} key_9_and_26 9键26键
    @apiParam {string} first_word_correct_rate 首词准确率
    @apiParam {string} first_page_correct_rate 首页准确率
    @apiParam {string} comment 备注
    @apiParam {int} show_in_chart 是否显示在图表中,0:保存，1:不保存
    @apiParamExample {json} Request-Example:
    {
        "data_source": 1,
        "phone_model": 4,
        "apk_version": 3,
        "kernel_version": 4,
        "system_version": 5,
        "thesaurus_version": 6,
        "corpus_version": 7,
        "key_9_and_26": "1231.123123",
        "first_word_correct_rate": "12.13",
        "first_page_correct_rate": "12.23",
        "comment": "testsdfasdfdafdafdasf asdfas f",
        "show_in_chart": 0
    }
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "message": "ok"
    }
    """
    params = parse_json_form('data_show_first_page_first_word_correct_rate_create')
    data = DataShowFirstPageFirstWordCorrectRateBusiness.update(id, params)
    return {
        "message": "更新成功",
        "code": data
    }


@datashow.route('/correction/first/<int:id>', methods=['DELETE'])
def response_first_delete_handler(id):
    """
    @api {delete} /v1/datashow/correction/first/{id:int} 删除 首页响应准确率
    @apiName DeleteDataShowFirstPageWord
    @apiGroup 自动化测试
    @apiDescription 删除 首页响应准确率
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "message": "ok"
    }
    """
    data = DataShowFirstPageFirstWordCorrectRateBusiness.delete(id)
    return {
        "message": "删除成功",
        "code": data
    }


@datashow.route('/response/log', methods=['GET'])
def response_log_get_handler():
    """
    @api {get} /v1/datashow/response/log 查询 响应时间_Log 列表
    @apiName GetDataShowResponseLog
    @apiGroup 自动化测试
    @apiDescription 查询 响应时间_Log 列表
    @apiParam {int} data_source 数据来源
    @apiParam {int} phone_model 手机类型
    @apiParam {int} apk_version apk 版本
    @apiParam {int} kernel_version 内核版本
    @apiParam {int} system_version 系统版本
    @apiParam {int} thesaurus_version 词库版本
    @apiParam {int} corpus_version 语料库版本
    @apiParam {int} show_in_chart 获取图信息 0:获取，1:不获取
    @apiParam {int} date_time 配合show_in_chart使用的时间段：0：默认，1：7天，2：1个月
    @apiParamExample {json} Request-Example:
    ?data_source=1
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "data": [
        {
          "apk_version": "3",
          "battery_use": "12.23",
          "comment": "testsdfasdfdafdafdasf asdfas f",
          "corpus_version": "test",
          "cpu_average": "12.13",
          "creation_time": "2019-08-27 19:07:20",
          "creator": "0",
          "creator_nickname": null,
          "data_source": "1",
          "id": 2,
          "kernel_version": "4",
          "key_26_kernel_click_time_average": "12.13",
          "key_26_kernel_response_time": "1231.123123",
          "key_9_kernel_click_time_average": "1231.123123",
          "key_9_kernel_response_time": "12.23",
          "phone_model": "4",
          "ram_average": "12.23",
          "system_version": "1",
          "thesaurus_version": "2",
          "show_in_chart": 0
        }
      ],
      "message": "ok",
      "page_index": 1,
      "page_size": 10,
      "total": 2
    }
    """
    show_in_chart = request.args.get('show_in_chart')
    date_time = str(request.args.get('date_time', '0'))
    if str(show_in_chart) == "0":
        data = DataShowResponseLogBusiness.query_chart_data(date_time)
        return {
            "data": data
        }
    else:
        page_size, page_index = parse_list_args2()

        data, count = DataShowResponseLogBusiness.query_all_data(page_size, page_index)
    return {
        "data": data,
        "total": count,
        "page_index": page_index,
        "page_size": page_size
    }


@datashow.route('/response/log', methods=['POST'])
@validation('POST:data_show_response_log')
def response_log_create_handler():
    """
    @api {post} /v1/datashow/response/log 新增 响应时间_Log
    @apiName CreateDataShowResponseLog
    @apiGroup 自动化测试
    @apiDescription 新增 响应时间_Log
    @apiParam {int} data_source 数据来源
    @apiParam {int} phone_model 手机类型
    @apiParam {int} apk_version apk 版本
    @apiParam {int} kernel_version 内核版本
    @apiParam {int} system_version 系统版本
    @apiParam {int} thesaurus_version 词库版本
    @apiParam {int} corpus_version 语料库版本
    @apiParam {string} key_9_kernel_click_time_average 9键点击请求内核响应平均时间
    @apiParam {string} key_26_kernel_click_time_average 26 键点击请求内核响应平均时间
    @apiParam {string} key_9_kernel_response_time  9 键点击请求内核响应时间
    @apiParam {string} key_26_kernel_response_time 26 键点击请求内核响应时间
    @apiParam {string} cpu_average cpu 平均值
    @apiParam {string} ram_average 内存 平均值
    @apiParam {string} battery_use 耗电量
    @apiParam {string} comment 备注
    @apiParam {int} show_in_chart 是否显示在图表中,0:保存，1:不保存
    @apiParamExample {json} Request-Example:
    {
        "data_source": 1,
        "phone_model": 4,
        "apk_version": 3,
        "kernel_version": 4,
        "system_version": 5,
        "thesaurus_version": 6,
        "corpus_version": 7,
        "key_9_kernel_click_time_average": "1231.123123",
        "key_26_kernel_click_time_average": "12.13",
        "key_9_kernel_response_time": "12.23",
        "key_26_kernel_response_time": "1231.123123",
        "cpu_average": "12.13",
        "ram_average": "12.23",
        "battery_use": "12.23",
        "comment": "testsdfasdfdafdafdasf asdfas f",
        "show_in_chart": 0
    }
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "message": "ok"
    }
    """
    params = parse_json_form('data_show_response_log')
    data = DataShowResponseLogBusiness.create(params)
    return {
        "message": "创建成功",
        "code": data
    }


@datashow.route('/response/log/<int:id>', methods=['POST'])
@validation('POST:data_show_response_log')
def response_log_update_handler(id):
    """
    @api {post} /v1/datashow/response/log/{id:int} 修改 响应时间_Log
    @apiName ModifyDataShowResponseLog
    @apiGroup 自动化测试
    @apiDescription 修改 响应时间_Log
    @apiParam {int} data_source 数据来源
    @apiParam {int} phone_model 手机类型
    @apiParam {int} apk_version apk 版本
    @apiParam {int} kernel_version 内核版本
    @apiParam {int} system_version 系统版本
    @apiParam {int} thesaurus_version 词库版本
    @apiParam {int} corpus_version 语料库版本
    @apiParam {string} key_9_kernel_click_time_average 9键点击请求内核响应平均时间
    @apiParam {string} key_26_kernel_click_time_average 26 键点击请求内核响应平均时间
    @apiParam {string} key_9_kernel_response_time  9 键点击请求内核响应时间
    @apiParam {string} key_26_kernel_response_time 26 键点击请求内核响应时间
    @apiParam {string} cpu_average cpu 平均值
    @apiParam {string} ram_average 内存 平均值
    @apiParam {string} battery_use 耗电量
    @apiParam {string} comment 备注
    @apiParam {int} show_in_chart 是否显示在图表中,0:保存，1:不保存
    @apiParamExample {json} Request-Example:
    {
        "data_source": 1,
        "phone_model": 4,
        "apk_version": 3,
        "kernel_version": 4,
        "system_version": 5,
        "thesaurus_version": 6,
        "corpus_version": 7,
        "key_9_kernel_click_time_average": "1231.123123",
        "key_26_kernel_click_time_average": "12.13",
        "key_9_kernel_response_time": "12.23",
        "key_26_kernel_response_time": "1231.123123",
        "cpu_average": "12.13",
        "ram_average": "12.23",
        "battery_use": "12.23",
        "comment": "testsdfasdfdafdafdasf asdfas f",
        "show_in_chart": 0
    }
    @apiSuccessExample {json} Success-Response:
    {
      "code": 0,
      "message": "ok"
    }
    """
    params = parse_json_form('data_show_response_log')
    data = DataShowResponseLogBusiness.update(id, params)
    return {
        "message": "更新成功",
        "code": data
    }


@datashow.route('/response/log/<int:id>', methods=['DELETE'])
def response_log_delete_handler(id):
    """
    @api {delete} /v1/datashow/response/log/{id:int} 删除 响应时间_Log
    @apiName DeleteDataShowResponseLog
    @apiGroup 自动化测试
    @apiDescription 删除 响应时间_Log
    @apiSuccessExample {json} Success-Response:
    {
    "code": 0,
    "message": "ok"
    }
    """
    data = DataShowResponseLogBusiness.delete(id)
    return {
        "message": "删除成功",
        "code": data
    }
