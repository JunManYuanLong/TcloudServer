from flask import Blueprint

from apps.public.daos.guest import get_guest_info

guest = Blueprint('guest', __name__)


@guest.route('/', methods=['GET'])
def get():
    code, data, total = get_guest_info()
    return {'code': code, 'data': data, 'total': total}
