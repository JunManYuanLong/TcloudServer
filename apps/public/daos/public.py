import base64
import datetime
import hmac
import json
import time
from hashlib import sha1 as sha

import requests
from flask import current_app
from sqlalchemy import func

from apps.public.models.public import Config, RouteStatistics
from apps.public.settings.config import (
    OSSAccessKeySecret, OSSAccessKeyId, OSSHost, CMSHost, WX_MESSAGE_URL, USER_ONLINE,
    ROUTE_STATISTICS,
)
from library.api.db import db
# from library.api.db import t_redis
from library.api.exceptions import CannotFindObjectException
from library.trpc import Trpc

user_trpc = Trpc('auth')

expire_time = 30
upload_dir = 'static/'


def get_config(module, module_type, is_all, project_id=None):
    _query = Config.query.add_columns(Config.content.label('content'),
                                      func.date_format(Config.modified_time, "%Y-%m-%d %H:%i:%s").label(
                                          'modified_time'),
                                      Config.id.label('id')
                                      ).filter(Config.module == module)

    if module_type:
        _query = _query.filter(Config.module_type == int(module_type))

    query = _query.first()

    if project_id:
        query = _query.filter(Config.projectid == int(project_id)).first()

        if not query:
            query = _query.filter(Config.projectid == 0).first()

    if not query:
        raise CannotFindObjectException(f'config {module}-{module_type}-{project_id} not found in system!')

    data = query.content

    if not is_all:
        return 0, data
    else:
        return 0, {'content': data, 'modified_time': query.modified_time, 'id': query.id}


def update_config(config_id, module, module_type, content, description, project_id):
    config = Config.query.get(config_id)
    if not config:
        raise CannotFindObjectException(f'config {config_id} not found in system!')

    module = module if module else config.module
    module_type = module_type if module_type else config.module_type

    if config.projectid in ['0', 0, None, 'null']:
        config_check = Config.query.filter(Config.module == module,
                                           Config.module_type == module_type,
                                           Config.projectid == project_id).first()
        if not config_check:
            current_app.logger.info('should create a new config with this project!')
            return create_config(
                module=module if module is not None else config.module,
                module_type=module_type if module_type is not None else config.module_type,
                content=content if content is not None else config.content,
                description=description if description is not None else config.description,
                project_id=project_id)
        else:
            config = config_check

    with db.auto_commit():
        config.module = module if module is not None else config.module
        config.module_type = module_type if module_type is not None else config.module_type
        config.content = json.dumps(content) if content is not None else config.content
        config.description = description if description is not None else config.description
        db.session.add(config)
    return 0


def create_config(module, module_type, content, description, project_id):
    if isinstance(content, dict):
        content = json.dumps(content)
    config = Config(
        module=module,
        module_type=module_type,
        content=content,
        description=description,
        projectid=project_id
    )
    with db.auto_commit():
        db.session.add(config)
    return 0


def send_wxmessage(user_ids, text, user_emails, is_email):
    if not is_email:
        emails_list = user_trpc.requests('get', '/user/wxemail',
                                         {'userids': ','.join([str(user_id) for user_id in user_ids])})
        if emails_list:
            email = '|'.join(emails_list)
        else:
            return 0, '未获取企业邮箱'
    else:
        email = user_emails
    data = {'Email': email, 'WXText': text}
    req = requests.post(url=WX_MESSAGE_URL, json=data)
    if req.status_code == 200:
        return 0, 'success'
    else:
        return 104, ''


def get_iso_8601(expire):
    gmt = datetime.datetime.fromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt


def get_token():
    now = int(time.time())
    expire_syncpoint = now + expire_time
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {'expiration': expire}
    condition_array = []
    array_item = ['starts-with', '$key', upload_dir]
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    # policy_encode = base64.encodestring(policy)
    policy_encode = base64.b64encode(policy.encode('utf-8'))
    h = hmac.new(OSSAccessKeySecret.encode('utf-8'), policy_encode, sha)
    sign_result = base64.encodebytes(h.digest()).strip()

    token_dict = {
        'accessid': OSSAccessKeyId, 'host': OSSHost, 'policy': policy_encode.decode('utf-8'),
        'signature': sign_result.decode('utf-8'),
        'expire': expire_syncpoint, 'dir': upload_dir, 'cdn_host': CMSHost
    }
    # result = json.dumps(token_dict)
    return token_dict


def get_flow_config(project_id):
    _query = Config.query.add_columns(Config.content.label('content')).filter(Config.module == 'flow_config')

    query = _query.filter(Config.projectid == project_id).first()
    if not query:
        query = _query.filter(Config.projectid == 0).first()
    content = query.content
    config = ''
    try:
        config = json.loads(content)
        return 0, config
    except json.JSONDecodeError as e:
        current_app.logger.error(e)
        return 101, config


def get_count_online():
    # 最近十分钟在线用户
    ud_online = t_redis.keys(f'{USER_ONLINE}*')
    ul = [int(u.replace(USER_ONLINE, '')) for u in ud_online]
    users = user_trpc.requests(method='get', path='/user', query={'base_info': True})
    users_dict = {user.get('userid'): user.get('nickname') for user in users}
    ol_users = [users_dict.get(u) for u in ul]
    count = len(ul)
    return 0, {'count': count, 'users': ol_users}


def get_statistics_route():
    # 待修改成缓存类型接口
    # 接口调用次数
    routes = t_redis.keys(f'{ROUTE_STATISTICS}*')
    data = {}
    for r in routes:
        r_info = t_redis.hgetall(r)
        r_name = r.replace(ROUTE_STATISTICS, '')
        data[r_name] = r_info
        add_list = []
        for k, v in r_info.items():
            k_info = k.split(']')
            method = k_info[0].replace('[', '')
            route = k_info[1]
            ret = RouteStatistics.query.filter_by(service=r_name,
                                                  route=route,
                                                  method=method).first()
            if ret:
                ret.count = v
            else:
                ret = RouteStatistics(
                    service=r_name,
                    route=route,
                    method=method,
                    count=int(v)
                )
            add_list.append(ret)
        with db.auto_commit():
            db.session.add_all(add_list)
    return 0, data


def get_statistics_route_job():
    with db.app.app_context():
        db.app.logger.info('get_statistics_route_job start')
        get_statistics_route()
        db.app.logger.info('get_statistics_route_job stop')
