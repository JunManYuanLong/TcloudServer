from apps.auth.auth_require import is_admin, required_without_projectid
from apps.project.business.assets import PhoneBusiness, PhoneRecordBusiness, VirtualAssetBusiness, PhoneBorrowBusiness
from apps.project.extentions import parse_list_args2, parse_json_form, validation
from library.api.render import json_list_render2, json_detail_render
from library.api.tBlueprint import tblueprint

bpname = 'asset'
modify_permission = f'{bpname}_modify'
phone = tblueprint('phone', __name__, bpname, with_pid=False, has_view=False)
virtualasset = tblueprint('virtual', __name__, bpname, with_pid=False, has_view=False)

"""
blueprint自带的before_request 做get和delete这些没有争议的请求方式权限控制
post可能包含查询、新增、修改等，所以单独加上装饰器管理
"""


@phone.route('/', methods=['GET'])
def phone_index_handler():
    """
    @api {get} /v1/asset/phone 查询 资产设备列表
    @apiName GetPhoneList
    @apiGroup 项目
    @apiDescription 查询 资产设备列表
    @apiParam {int} [page_size] 分页-单页大小
    @apiParam {int} [page_index] 分页-页数
    @apiParam {string} [name] 资产名称
    @apiParam {string} [vendor] 制造商
    @apiParam {string} [os] 操作系统
    @apiParam {string} [resolution] 分辨率
    @apiParam {int} [borrower_id] 持有人 ID
    @apiParam {string} [device_source] 设备来源
    @apiParam {string} [device_belong] 设备归属
    @apiParamExample {json} Request-Example:
    ?page_size=10&page_index=1&name=小米
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [
            {
              "asset_id": "1",
              "borrow_id": 5,
              "borrow_nickname": "周培丽hello",
              "borrow_status": "[周培丽hello] 持有",
              "buy_date": "2019-07-17T16:00:00.000Z",
              "confirm_status": 1,
              "core": "1",
              "cpu": "1",
              "creator_id": 5,
              "device_belong": "1",
              "device_number": "1",
              "device_source": "1",
              "id": 79,
              "move_status": 0,
              "name": "小米3",
              "os": "1",
              "ram": "1",
              "region": "1",
              "resolution": "1x1",
              "rom": "1",
              "status": 0,
              "vendor": "1",
              "device_belong": "1231",
              "device_source": "123123
            }
          ],
          "message": "ok",
          "page_index": 1,
          "page_size": 10,
          "total": 3
        }
    """
    page_size, page_index = parse_list_args2()

    data, count = PhoneBusiness.get_phone_all(page_size, page_index)

    return json_list_render2(0, data, page_size, page_index, count)


@phone.route('/', methods=['POST'])
@required_without_projectid(modify_permission)
@validation('POST:phone_create')
def phone_indexs_handler():
    """
    @api {post} /v1/asset/phone 新增 资产
    @apiName CreatePhone
    @apiGroup 项目
    @apiDescription 查询 资产设备列表
    @apiParam {string} name 资产名称
    @apiParam {string} vendor 制造商
    @apiParam {string} os 操作系统
    @apiParam {string} resolution 分辨率
    @apiParam {int} borrower_id 持有人 ID
    @apiParam {int} asset_id 资产编号
    @apiParam {string} cpu cpu 型号
    @apiParam {int} core cpu 核心数
    @apiParam {int} ram 内存大小
    @apiParam {int} rom 存储大小
    @apiParam {string} buy_date 购买日期
    @apiParam {string} region 地区
    @apiParam {string} device_source 设备来源
    @apiParam {string} device_belong 设备所属
    @apiParam {string} device_number 设备序列号
    @apiParamExample {json} Request-Example:
    {
        "name": "iphone xs 4",
        "asset_id": "XHAH600004",
        "vendor": "apple",
        "os": "ios 12.3",
        "cpu": "a13",
        "core": 8,
        "ram": 4,
        "rom": 64,
        "resolution": "2015x1080",
        "buy_date": "2019-06-11",
        "region": "ShangHai",
        "status": "0",
        "borrow_id": 93,
        "device_source": "JingDong",
        "device_belong": "Innotech",
        "device_number": "RTYUJBG678HH761D"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
    }
    """
    (name, asset_id, vendor, device_number, os, cpu, core, ram, rom, resolution, buy_date, region, borrow_id,
     device_source, device_belong, creator_id) = parse_json_form('phone_create')
    ret, msg = PhoneBusiness.create(name, asset_id, vendor, device_number, os, cpu, core, ram, rom, resolution,
                                    buy_date, region, borrow_id, device_source, device_belong, creator_id)

    return json_detail_render(ret, [], msg)


@phone.route('/<int:pid>', methods=['GET'])
def phone_detail_handler(pid):
    """
    @api {get} /v1/asset/phone/{int:id} 查询 资产设备 （id)
    @apiName GetPhoneListById
    @apiGroup 项目
    @apiDescription 查询 资产设备 根据 ID
    @apiParam {int} [id] phone id
    @apiParamExample {json} Request-Example:
    ?id=100
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
        }
    """
    code, phones = PhoneBusiness.get_phone_by_id(pid)

    return json_detail_render(code, phones)


@phone.route('/<int:pid>', methods=['POST'])
@required_without_projectid(modify_permission)
@validation('POST:phone_update')
def phone_modify_details_handler(pid):
    """
    @api {post} /v1/asset/phone/{int:id} 更新 资产
    @apiName UpdatePhone
    @apiGroup 项目
    @apiDescription 更新 资产设备
    @apiParam {string} [name] 资产名称
    @apiParam {string} [vendor] 制造商
    @apiParam {string} [os] 操作系统
    @apiParam {string} [resolution] 分辨率
    @apiParam {int} [borrower_id] 持有人 ID
    @apiParam {int} [asset_id] 资产编号
    @apiParam {string} [cpu] cpu 型号
    @apiParam {int} [core] cpu 核心数
    @apiParam {int} [ram] 内存大小
    @apiParam {int} [rom] 存储大小
    @apiParam {string} [buy_date] 购买日期
    @apiParam {string} [region] 地区
    @apiParam {string} [device_source] 设备来源
    @apiParam {string} [device_belong] 设备所属
    @apiParam {string} [device_number] 设备序列号
    @apiParamExample {json} Request-Example:
    {
        "name": "iphone xs 4",
        "asset_id": "XHAH600004",
        "vendor": "apple",
        "os": "ios 12.3",
        "cpu": "a13",
        "core": 8,
        "ram": 4,
        "rom": 64,
        "resolution": "2015x1080",
        "buy_date": "2019-06-11",
        "region": "ShangHai",
        "status": "0",
        "borrow_id": 93,
        "device_source": "JingDong",
        "device_belong": "Innotech",
        "device_number": "RTYUJBG678HH761D"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
    }
    """
    (name, asset_id, vendor, device_number, os, cpu, core, ram, rom, resolution, buy_date, region, borrow_id,
     device_source, device_belong, creator_id) = parse_json_form(
        'phone_update')
    ret, msg = PhoneBusiness.update(pid, name, asset_id, vendor, device_number, os, cpu, core, ram, rom, resolution,
                                    buy_date, region, borrow_id, device_source, device_belong, creator_id)

    return json_detail_render(ret, [], msg)


@phone.route('/<int:pid>', methods=['DELETE'])
@validation('POST:phone_update')
def phone_details_handler(pid):
    """
    @api {delete} /v1/asset/phone/{int:id} 删除 资产设备 （id)
    @apiName DeletePhoneListById
    @apiGroup 项目
    @apiDescription 删除 资产设备 根据 ID
    @apiParam {int} [id] phone id
    @apiParamExample {json} Request-Example:
    ?id=100
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
    }
    """
    ret = PhoneBusiness.delete(pid)
    return json_detail_render(ret)


# 查询设备流转信息
@phone.route('/record/detail/<int:pid>', methods=['GET'])
def phone_record_detail_handler(pid):
    """
    @api {get} /v1/asset/phone/record/detail/{int:id} 查询 资产设备 记录
    @apiName GetPhoneRecordList
    @apiGroup 项目
    @apiDescription 查询 资产设备 记录
    @apiParam {int} [id]
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [
            {
              "modified_time": "2019-07-23 10:36:44",
              "operation": "[孟伟(mengwei@innotechx.com)] : 增加新的资产 11"
            }
          ],
          "message": "ok"
    }
    """
    data = PhoneRecordBusiness.query_record_detail(pid)
    return json_detail_render(0, data)


# 设备流转
@phone.route('/move/<int:pid>', methods=['POST'])
@required_without_projectid(modify_permission)
@validation('POST:phone_move')
def phone_move_handler(pid):
    """
    @api {post} /v1/asset/phone/move/{int:id} 流转 资产设备
    @apiName MovePhone
    @apiGroup 项目
    @apiDescription 流转 资产设备
    @apiParam {int} id
    @apiParam {int} borrow_id 流转人 ID
    @apiParamExample {json} Request-Example:
    {
        "borrow_id": 2
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
    }
    """
    if is_admin() or PhoneBusiness.can_move_status(pid):
        borrow_id = parse_json_form('phone_move')
        ret, msg = PhoneBusiness.move_to_user(pid, borrow_id)
        return json_detail_render(ret, [], msg)
    else:
        return json_detail_render(403)


# 对设备发起借用
@phone.route('/borrow/<int:pid>', methods=['GET'])
def phone_borrow_handler_get(pid):
    """
    @api {post} /v1/asset/phone/borrow/{int:id} 借用 设备
    @apiName BorrowPhone
    @apiGroup 项目
    @apiDescription 借用 资产设备
    @apiParam {int} id
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
    }
    """
    ret, msg = PhoneBorrowBusiness.borrow(pid)
    return json_detail_render(ret, [], msg)


@phone.route('/borrow/<int:pid>', methods=['POST'])
def phone_borrow_handler_post(pid):
    """
    @api {post} /v1/asset/phone/borrow/{int:id} 借用 设备
    @apiName BorrowPhone
    @apiGroup 项目
    @apiDescription 借用 资产设备
    @apiParam {int} id
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
    }
    """
    ret, msg = PhoneBorrowBusiness.borrow(pid)
    return json_detail_render(ret, [], msg)


# 确认设备
@phone.route('/borrow/confirm/<int:pid>', methods=['GET'])
def phone_borrow_confirm_handler_get(pid):
    """
    @api {post} /v1/asset/borrow/confirm/{int:id} 接收 设备
    @apiName ConfirmPhone
    @apiGroup 项目
    @apiDescription 接收 资产设备
    @apiParam {int} id
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
    }
    """
    ret, msg = PhoneBorrowBusiness.confirm_borrow(pid)
    return json_detail_render(ret, [], msg)


# 确认设备
@phone.route('/borrow/confirm/<int:pid>', methods=['POST'])
def phone_borrow_confirm_handler_post(pid):
    """
    @api {post} /v1/asset/borrow/confirm/{int:id} 接收 设备
    @apiName ConfirmPhone
    @apiGroup 项目
    @apiDescription 接收 资产设备
    @apiParam {int} id
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
    }
    """
    ret, msg = PhoneBorrowBusiness.confirm_borrow(pid)
    return json_detail_render(ret, [], msg)


# 归还设备
@phone.route('/return/<int:pid>', methods=['POST'])
@required_without_projectid(modify_permission)
def phone_return_handler(pid):
    """
    @api {post} /v1/asset/borrow/confirm/{int:id} 归还 设备
    @apiName Phone
    @apiGroup 项目
    @apiDescription 归还 资产设备
    @apiParam {int} id
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
    }
    """
    if is_admin() or PhoneBusiness.can_move_status(pid):
        ret, msg = PhoneBusiness.return_to_admin(pid)

        return json_detail_render(ret, [], msg)
    else:
        return json_detail_render(403)


# 通过 phone_id 获取申请人员列表
@phone.route('/borrow/users/<int:pid>', methods=['GET'])
def phone_borrow_users_handler(pid):
    """
    @api {get} /v1/asset/phone/borrow/users/{int:id} 查询 申请人员列表
    @apiName GetPhoneBorrowerList
    @apiGroup 项目
    @apiDescription 查询 申请人员列表
    @apiParam {int} phone_id
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [
        {
          "id": 93,
          "nickname": "孟伟"
        },
        {
          "id": 96,
          "nickname": "张宇"
        }
      ],
      "message": "ok"
    }
    """
    users = PhoneBorrowBusiness.get_user_list_by_phone_id(pid)
    return json_detail_render(0, users)


# 获取所有持有人的列表
@phone.route('/holder', methods=['GET'])
def phone_holder_index_handler():
    """
    @api {get} /v1/asset/phone/holder 查询 所有持有人的列表
    @apiName GetPhoneHolderList
    @apiGroup 项目
    @apiDescription 查询 所有持有人的列表
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [
        {
          "id": 5,
          "nickname": "周培丽hello"
        },
        {
          "id": 110,
          "nickname": "吴茂澍"
        },
        {
          "id": 93,
          "nickname": "孟伟"
        }
      ],
      "message": "ok"
    }
    """
    data = PhoneBusiness.get_holder_json()
    return json_detail_render(0, data)


@virtualasset.route('/', methods=['GET'])
def virtual_asset_index_handler():
    """
    @api {get} /v1/asset/virtual 查询 虚拟资产列表
    @apiName GetVirtualList
    @apiGroup 项目
    @apiDescription 查询 虚拟资产列表
    @apiParam {int} [page_size] 分页-单页大小
    @apiParam {int} [page_index] 分页-页数
    @apiParamExample {json} Request-Example:
    ?page_size=1&page_index=1
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
   {
      "code": 0,
      "data": [
        {
          "administrator": "",
          "asset_id": "9",
          "asset_type": 1,
          "bind_tel": "",
          "id": 18,
          "idcard": "",
          "operator": "",
          "passwd": "",
          "status": 0
        }
      ],
      "message": "ok",
      "page_index": 1,
      "page_size": 10,
      "total": 27
    }
    """
    page_size, page_index = parse_list_args2()
    data, count = VirtualAssetBusiness.paginate_data(page_size, page_index)
    return json_list_render2(0, data, page_size, page_index, count)


@virtualasset.route('/', methods=['POST'])
@validation('POST:virtual_asset_create')
@required_without_projectid(modify_permission)
def virtual_assets_index_handler():
    """
    @api {post} /v1/asset/virtual 新增 虚拟资产
    @apiName CreateVirtualList
    @apiGroup 项目
    @apiDescription 新增 虚拟资产
    @apiParam {int} asset_id 资产编号
    @apiParam {int} [passwd] 密码
    @apiParam {int} [administrator] 管理员
    @apiParam {int} [idcard] id 卡
    @apiParam {int} [asset_type] 资产类型
    @apiParam {int} [operator] 操作者
    @apiParamExample {json} Request-Example:
    {
        "asset_id": "123",
        "passwd": "123",
        "administrator": "123",
        "bind_tel": "123",
        "idcard": "123",
        "operator": "123",
        "asset_type": 2,
        "borrow_id": 93
    }
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
     "code": 0,
     "data": [],
     "message": "ok"
    }
    """
    asset_id, passwd, administrator, bind_tel, idcard, asset_type, operator = parse_json_form('virtual_asset_create')
    ret, msg = VirtualAssetBusiness.create(asset_id, passwd, administrator, bind_tel, idcard, asset_type, operator)

    return json_detail_render(ret, [], msg)


@virtualasset.route('/<int:pid>', methods=['GET'])
def virtual_asset_detail_handler(pid):
    """
    @api {get} /v1/asset/virtual/{int:id} 查询 虚拟资产信息 （id)
    @apiName GetVirtualById
    @apiGroup 项目
    @apiDescription 查询 虚拟资产信息 根据 ID
    @apiParam {int} [id] phone id
    @apiParamExample {json} Request-Example:
    -
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
          "code": 0,
          "data": [],
          "message": "ok"
    }
    """
    data = VirtualAssetBusiness.query_json_by_id(pid)
    if len(data) == 0:
        return json_detail_render(101, data)

    return json_detail_render(0, data)


@virtualasset.route('/<int:pid>', methods=['POST'])
@validation('POST:virtual_asset_update')
@required_without_projectid(modify_permission)
def virtual_assets_detail_handler(pid):
    """
    @api {post/delete} /v1/asset/virtual 更新/删除 虚拟资产
    @apiName UpdateDeleteVirtualList
    @apiGroup 项目
    @apiDescription 更新 虚拟资产
    @apiParam {int} asset_id 资产编号
    @apiParam {int} [passwd] 密码
    @apiParam {int} [administrator] 管理员
    @apiParam {int} [idcard] id 卡
    @apiParam {int} [asset_type] 资产类型
    @apiParam {int} [operator] 操作者
    @apiParamExample {json} Request-Example:
    {
        "asset_id": "123",
        "passwd": "123",
        "administrator": "123",
        "bind_tel": "123",
        "idcard": "123",
        "operator": "123",
        "asset_type": 2,
        "borrow_id": 93
    }
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
     "code": 0,
     "data": [],
     "message": "ok"
    }
    """
    asset_id, passwd, administrator, bind_tel, idcard, asset_type, operator = parse_json_form('virtual_asset_update')
    ret, msg = VirtualAssetBusiness.update(pid, asset_id, passwd, administrator, bind_tel, idcard, asset_type, operator)

    return json_detail_render(ret, [], msg)


@virtualasset.route('/<int:pid>', methods=['DELETE'])
def virtual_assets_delete_handler(pid):
    """
    @api {post/delete} /v1/asset/virtual 更新/删除 虚拟资产
    @apiName UpdateDeleteVirtualList
    @apiGroup 项目
    @apiDescription 更新 虚拟资产
    @apiParam {int} asset_id 资产编号
    @apiParam {int} [passwd] 密码
    @apiParam {int} [administrator] 管理员
    @apiParam {int} [idcard] id 卡
    @apiParam {int} [asset_type] 资产类型
    @apiParam {int} [operator] 操作者
    @apiParamExample {json} Request-Example:
    {
        "asset_id": "123",
        "passwd": "123",
        "administrator": "123",
        "bind_tel": "123",
        "idcard": "123",
        "operator": "123",
        "asset_type": 2,
        "borrow_id": 93
    }
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
     "code": 0,
     "data": [],
     "message": "ok"
    }
    """
    ret = VirtualAssetBusiness.delete(pid)
    return json_detail_render(ret)
