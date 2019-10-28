from flask import Blueprint

from apps.public.daos.guest import get_guest_info
from apps.public.extentions import parse_list_args2

guest = Blueprint('guest', __name__)


@guest.route('/', methods=['GET'])
def get():
    page_size, page_index = parse_list_args2()
    code, data, total = get_guest_info(page_size, page_index)
    return {'code': code, 'data': data, 'total': total, 'page_size': page_size, 'page_index': page_index}

