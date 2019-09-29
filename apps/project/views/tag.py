from flask import request

from apps.auth.auth_require import required
from apps.project.business.tag import TagBusiness
from apps.project.extentions import parse_json_form, validation
from library.api.tBlueprint import tblueprint

bpname = 'tag'
modify_permission = f'{bpname}_modify'
tag = tblueprint(bpname, __name__)


# 获取到的tag标签
@tag.route('/', methods=['GET'])
def gain_tag():
    """
    @api {get} /v1/tag/ 获取 标签
    @apiName GetTag
    @apiGroup 项目
    @apiDescription 根据当前project_id来获取所有标签
    @apiParam {int} project_id 项目ID
    @apiParam {string} tag tag名称模糊查询
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
      "code": 0,
      "data": [
        {
          "id": 16,
          "tag": "老功能新操作"
        },
        {
          "id": 15,
          "tag": "测试权限"
        },
        {
          "id": 14,
          "tag": "新增标签"
        }
      ],
      "message": "ok"
    }
    """
    page_size = request.args.get('page_size')
    page_index = request.args.get('page_index')
    data, count = TagBusiness.paginate_data(page_size, page_index)
    return {'code': 0, 'data': data, 'total': count, 'page_index': page_index, 'page_size': page_size}


@tag.route('/', methods=['POST'])
@required(modify_permission)
@validation('POST:createtag')
def create_tag():
    """
    @api {post} /v1/tag 新增 标签
    @apiName CreateTag
    @apiGroup 项目
    @apiDescription 新增 标签
    @apiParam {int} tag  标签名称
    @apiParam {int} project_id 项目ID
    @apiParam {int} description 描述
    @apiParamExample {json} Request-Example:
    {
        "tag": "标签a",
        "project_id": 4,
        "description": "这是一个标签a"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    tag_name, project_id, description = parse_json_form('createtag')
    code = TagBusiness.create(tag_name, project_id, description)
    return {'code': code}


@tag.route('/<int:tag_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:updatetag')
def update_tag(tag_id):
    """
    @api {post} /v1/tag/{tag_id} 修改 标签
    @apiName UpdateTag
    @apiGroup 项目
    @apiDescription 修改 标签
    @apiParam {int} tag  标签名称
    @apiParam {int} description 描述
    @apiParamExample {json} Request-Example:
    {
        "tag": "标签a",
        "description": "这是一个标签a"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    tag_name, description = parse_json_form('updatetag')
    code = TagBusiness.update(tag_id, tag_name, description)
    return {'code': code}


@tag.route('/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    """
    @api {delete} /v1/tag/{tag_id} 删除 标签
    @apiName DeleteTag
    @apiGroup 项目
    @apiDescription 删除标签, 当且仅当该标签被引用数为0才成功
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
    {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    code = TagBusiness.delete(tag_id)
    return {'code': code}
