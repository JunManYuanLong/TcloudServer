from flask import Blueprint, request, g

from apps.auth.business.track import TrackBusiness, TrackUploadBusiness
from apps.auth.extentions import validation, parse_json_form
from library.api.render import json_list_render2, json_detail_render

track = Blueprint('track', __name__)


@track.route('/sdk', methods=['GET'])
def track_sdk_list():
    page = request.args.get('page_index')
    size = request.args.get('page_size')

    code, data, total, message = TrackBusiness.get_sdk_list()

    return json_list_render2(code, data, size, page, total)


@track.route('/device', methods=['GET'])
def track_device_list():
    code, data, message = TrackBusiness.get_device_type_list()
    return json_detail_render(code, data, message)


@track.route('/event', methods=['GET'])
def track_event_list():
    page = request.args.get('page_index')
    size = request.args.get('page_size')
    code, data, total, message = TrackBusiness.get_event_list()
    return json_list_render2(code, data, size, page, total)


@track.route('/add/event', methods=['POST'])
@validation('POST:track_evnet_create')
def track_event_create():
    project_id, version, update_comment, platform_list, param_list, name, description = parse_json_form(
        "track_evnet_create")
    code, data, message = TrackBusiness.create_event(
        project_id, version, update_comment, platform_list, param_list, name, description)
    return json_detail_render(code, data, message)


@track.route('/<int:event_id>', methods=['POST', 'DELETE'])
@validation('POST:track_modify')
def track_event_modify(event_id):
    if request.method == 'DELETE':
        delete_comment = request.json.get('deleteComment')

        code, data, message = TrackBusiness.track_delete(event_id, delete_comment)

        return json_detail_render(code, data, message)

    (create_at, creator, delete_comment, description, _id, name, paramList, platform, platformList, projectId,
     project_id, status, updateComment, update_at, update_comment, updator, version) = parse_json_form("track_modify")

    code, data, message = TrackBusiness.track_modify(event_id, create_at, creator, delete_comment, description, _id,
                                                     name, paramList, platform, platformList, projectId, project_id,
                                                     status, updateComment, update_at,
                                                     update_comment, updator, version)

    return json_detail_render(code, data, message)


@track.route('/add/param', methods=['POST'])
def track_add_param():
    code, data, message = TrackBusiness.track_add_param()
    return json_detail_render(code, data, message)


@track.route('/delete/param', methods=['DELETE'])
def track_delete_param():
    code, data, message = TrackBusiness.track_delete_param()
    return json_detail_render(code, data, message)


@track.route('/info', methods=['GET'])
def track_info():
    project_id = request.args.get('project_id')

    really_project_id = TrackBusiness.get_project_id(project_id)

    ip = TrackBusiness.get_websocket()

    token = TrackBusiness.get_token(g.userid, g.username, g.nickname)

    data = {"project_id": really_project_id, "ip": ip, "token": token}

    return json_detail_render(0, data, 'ok')


@track.route('/create/history/device', methods=['POST'])
@validation('POST:track_device_create')
def track_create_history_device():
    project_id, user_id, device_typename, device_number = parse_json_form("track_device_create")

    data = TrackUploadBusiness.check_device_exist(project_id, user_id, device_number)

    if len(data) > 0:
        return json_detail_render(0, [], 'ok')

    code, message = TrackUploadBusiness.create(project_id, user_id, 0, device_typename, device_number)

    return json_detail_render(code, [], message)


@track.route('/gain/history/device', methods=['GET'])
def track_gain_history_device():
    data = TrackUploadBusiness.gain_history_data()

    return json_detail_render(0, data, 'ok')

# @track.route('/device/url', methods=['GET'])
# def track_device_list_url():
#     aa = TrackBusiness.get_url()
#     print(aa)
#     print(type(str(aa)))

#     return json_detail_render(0,[],'ok')
