from flask import Blueprint, request

from apps.auth.auth_require import required_no_dec, required_no_pid_no_dec
from library.api.exceptions import PermissionDeniedException, OperationPermissionDeniedException

try:
    from public_config import TCLOUD_ENV
except ImportError:
    TCLOUD_ENV = 'product'


def tblueprint(bp, name, bpname=None, with_pid=True, has_view=True, has_delete=True):
    if not bpname:
        bpname = bp
    view_permission = f'{bpname}_view'
    delete_permission = f'{bpname}_delete'
    if with_pid:
        required = required_no_dec
    else:
        required = required_no_pid_no_dec

    blueprint = Blueprint(bp, name)

    @blueprint.before_request
    def check_permission():

        if has_view and request.method == 'GET' and TCLOUD_ENV != 'dev':
            if not required(view_permission):
                raise PermissionDeniedException
        elif has_delete and request.method == 'DELETE':
            if not required(delete_permission):
                raise OperationPermissionDeniedException

    return blueprint
