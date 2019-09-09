from apps.auth.business.ability import AbilityBusiness
from apps.auth.extentions import parse_list_args
from library.api.render import json_list_render
from library.api.tBlueprint import tblueprint

bpname = 'ability'
ability = tblueprint(bpname, __name__)


@ability.route('/', methods=['GET'])
def ability_index_handler():
    """
    @api {get} /v1/ability 查询 Ability列表
    @apiName GetAbility
    @apiGroup 用户
    @apiDescription 查询Ability列表
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "handler": "user",
                "id": 1,
                "name": "用户模块"
            }
        ],
        "limit": 99999,
        "message": "ok",
        "offset": 0
    }
    """
    limit, offset = parse_list_args()
    ret = AbilityBusiness.get_ability_class(limit, offset)

    return json_list_render(0, ret, limit, offset)
