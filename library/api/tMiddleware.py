import jwt
from flask import request, g
from werkzeug.exceptions import HTTPException

# from apps.public.daos.guest import record_guest
# from library.api.db import t_redis
from library.api.exceptions import Error, NotLoginException
from library.api.parse import format_response
# from library.serverchan import send2serverchan
from public_config import AUTH_KEY, TSECRET, ALGORITHM, SECRET, ROUTE_STATISTICS, USER_ONLINE


def jwt_b_decode(st):
    return jwt.decode(st, SECRET, algorithm=ALGORITHM)


# 记录接口调用情况
# 记录访客情况
def record_track(path, method):
    if path != '/favicon.ico':
        pl = path.rstrip('/').replace('/v1/', '').split('/', 1)
        t_redis.hincrby(ROUTE_STATISTICS + pl[0], f"[{method}]{pl[-1] if len(pl) > 1 else '/'}", 1)
        # ip = request.headers['Remoteip'] if 'Remoteip' in request.headers else request.remote_addr
        # if ip != '127.0.0.1':
            # user_agent = request.user_agent
            # record_guest(ip, user_agent)


# 记录十分钟内在线用户
def record_ol_user():
    t_redis.set(f'{USER_ONLINE}{g.userid}', 1, ex=10 * 60)


# 白名单无需login
def is_whitelist(path):
    return (
            'login' in path or
            'interface' in path or
            'jira' in path or
            'monkey' in path or
            'performance' in path
    )


WARN_CODE = (108, 109, 110, 412)


def t_middleware(app):
    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, HTTPException):
            code = e.code
            message = e.name
            # send2serverchan(code)
        elif issubclass(type(e), Error):
            code = e.code
            message = e.message
        else:
            code = 500
            message = "服务异常，请联系管理员"
            # send2serverchan(code)

        err_res = {
            "code": code,
            "message": message
        }
        # 操作限制以及未登录
        if code in WARN_CODE:
            app.logger.warn('')
        else:
            app.logger.error('')
        return format_response(err_res)

    @app.before_request
    def handle_before():
        g.userid = 0
        g.username = ''
        g.nickname = ''
        g.is_admin = 0
        g.istrpc = 0
        path = request.path
        if path:
            # record_track(path, request.method)
            pass
        if request.headers.get('projectid'):
            g.projectid = request.headers.get('projectid')
        auth_key = request.headers.get(AUTH_KEY)
        tsecret = request.headers.get('tsecret')

        if is_whitelist(request.path):
            pass
        # 内部trpc，也不需要登录
        elif tsecret and tsecret == TSECRET:
            g.istrpc = 1
        elif auth_key:
            try:
                info = jwt_b_decode(auth_key)
            # 超时自动包超时错误，返回未登录错误即可
            except jwt.exceptions.ExpiredSignatureError:
                raise NotLoginException
            except Exception:
                raise NotLoginException
            g.userid = info.get('userid', 0)
            g.username = info.get('username', '')
            g.nickname = info.get('nickname', '')
            # record_ol_user()
            # 偷懒，因为admin基本不会修改，所以在这直接分析token而不是查表
            if 'admin' in [r.get('name') for r in info.get('role', [])]:
                g.is_admin = 1
        else:
            raise NotLoginException
