from apps.auth.auth_require import required
from apps.project.business.boardconfig import BoardConfigBusiness
from apps.project.extentions import validation, parse_json_form
from library.api.render import json_detail_render
from library.api.tBlueprint import tblueprint

bpname = 'boardconfig'
bpname_relate = 'projectconfig'
modify_permission = f'{bpname}_modify'
board_config = tblueprint(bpname, __name__, bpname=bpname_relate, has_view=False)


@board_config.route('/<int:project_id>', methods=['GET'])
def get_project_config(project_id):
    """
    @api {get} /v1/boardconfig/{project_id} 获取 项目看板配置
    @apiName GetBoardConfig
    @apiGroup 项目
    @apiDescription 获取当前项目的看板配置情况，包括requirement和issue
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [
            {
                "issue": {
                    "1": "代办",
                    "2": "修复中",
                    "3": "测试中",
                    "4": "已关闭",
                    "5": "已拒绝",
                    "6": "延时处理"
                },
                "issue_sort": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "6",
                    "5"
                ],
                "requirement": {
                    "0": "规划中",
                    "1": "实现中",
                    "2": "测试中",
                    "3": "已拒绝",
                    "4": "待验收",
                    "5": "待发布",
                    "6": "完成"
                },
                "requirement_sort": [
                    "0",
                    "1",
                    "2",
                    "4",
                    "5",
                    "6",
                    "3"
                ]
            }
        ],
        "message": "ok"
    }
    """
    code, config = BoardConfigBusiness.get(project_id)
    return json_detail_render(code, config)


@board_config.route('/<int:project_id>', methods=['POST'])
@required(modify_permission)
@validation('POST:boardconfig')
def post_project_config(project_id):
    """
    @api {post} /v1/boardconfig/{project_id} 修改 项目看板配置
    @apiName ModifyBoardConfig
    @apiGroup 项目
    @apiDescription 修改项目看板配置
    @apiParam {string} issue 缺陷
    @apiParam {string} requirement 需求
    @apiParamExample {json} Request-Example:
    {
        "issue":"1,2,3",
        "requirement":"2,4,6"
    }
    @apiSuccessExample {json} Success-Response:
     HTTP/1.1 200 OK
     {
        "code": 0,
        "data": [],
        "message": "ok"
    }
    """
    issue, requirement = parse_json_form('boardconfig')
    ret = BoardConfigBusiness.update(project_id, issue, requirement)

    return json_detail_render(ret)
