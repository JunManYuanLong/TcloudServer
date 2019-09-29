import jwt
from flask import request, g
from werkzeug.exceptions import HTTPException

from library.api.exceptions import Error, NotLoginException
from library.api.parse import format_response
from library.serverchan import send2serverchan
from public_config import AUTH_KEY, TSECRET, ALGORITHM, SECRET


def jwt_b_decode(st):
    return jwt.decode(st, SECRET, algorithm=ALGORITHM)


def t_middleware(app):
    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, HTTPException):
            code = e.code
            message = e.name
            send2serverchan(code)
        elif issubclass(type(e), Error):
            code = e.code
            message = e.message
        else:
            code = 500
            message = "服务异常，请联系管理员"
            send2serverchan(code)

        err_res = {
            "code": code,
            "message": message
        }
        # 操作限制以及未登录
        if code in (108, 109, 110, 412):
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
        if request.headers.get('projectid'):
            g.projectid = request.headers.get('projectid')
        auth_key = request.headers.get(AUTH_KEY)
        tsecret = request.headers.get('tsecret')

        # 不需要登录就能通过
        if (
                'login' in request.path or
                'interface' in request.path or
                'jira' in request.path or
                'monkey' in request.path or
                'performance' in request.path
        ):
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
            # 偷懒，因为admin基本不会，所以在这直接分析token而不是查表
            if 'admin' in [r.get('name') for r in info.get('role', [])]:
                g.is_admin = 1
        else:
            raise NotLoginException
