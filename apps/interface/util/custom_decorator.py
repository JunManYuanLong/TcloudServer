from functools import wraps

from flask import jsonify
from flask_login import current_user


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'msg': '登录超时,请重新登录', 'status': 0})
        return func(*args, **kwargs)

    return decorated_view


def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            # User.query.filter_by(id=current_app.id).first().role_id
            if not current_user.can(permission_name):
                return jsonify({'msg': '没有该权限', 'status': 0})
            return func(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(func):
    return permission_required('ADMINISTER')(func)
