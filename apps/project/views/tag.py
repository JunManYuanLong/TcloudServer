from apps.auth.auth_require import required
from apps.project.business.tag import TagBusiness
from apps.project.extentions import parse_json_form, validation
from library.api.render import json_detail_render
from library.api.tBlueprint import tblueprint

bpname = 'tag'
bpname_relate = 'task'
modify_permission = f'{bpname_relate}_modify'
tag = tblueprint(bpname, __name__, bpname=bpname_relate)


# 获取到的tag标签
@tag.route('/', methods=['GET'])
def gain_tag():
    data = TagBusiness.gain_tag()
    return json_detail_render(0, data)


# 更新的tag标签
@tag.route('/create', methods=['POST'])
@required(modify_permission)
@validation('POST:updatetag')
def update_tag():
    tag_id, project_id, description, tag_type = parse_json_form('updatetag')
    data = TagBusiness.judage_tag(project_id, tag_type)
    content_list = []

    for i in range(0, len(data)):
        content_list.append(data[i]['tag'])

    if tag_id in content_list:
        return json_detail_render(102, [], '增加的tag已经存在')
    ret = TagBusiness.create(tag_id, project_id, description, tag_type)
    return json_detail_render(ret)
