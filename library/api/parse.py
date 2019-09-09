from hashlib import md5

from flask import request

from public_config import SALT, MSG_MAP


def format_response(res):
    if 'code' not in res.keys():
        res['code'] = 0
    if 'message' not in res.keys():
        res['message'] = MSG_MAP.get(res['code'], '')
    return res


class TParse(object):
    def __init__(self, yml_json):
        self.yml_json = yml_json

    @staticmethod
    def parse_pwd(pwd):
        return md5((SALT + pwd).encode('utf-8')).hexdigest()

    def parse_json_form(self, name):
        form_json = self.yml_json.get(name)
        returnvalue = form_json.get('returnvalue')
        return [request.json.get(x) for x in returnvalue]

    def parse_query_string(self, name):
        form_json = self.yml_json.get(name)
        returnvalue = form_json.get('returnvalue')
        return [request.args.get(x) for x in returnvalue]

    @staticmethod
    def parse_list_args():
        req_args = request.args
        limit = int(req_args.get('limit', 99999))
        offset = int(req_args.get('offset', 0))
        return limit, offset

    @staticmethod
    def parse_list_args2():
        req_args = request.args
        page_size = req_args.get('page_size', 10)
        if page_size:
            page_size = int(page_size)

        page_index = req_args.get('page_index', 1)
        if page_index:
            page_index = int(page_index)
        ispaginate = request.args.get('ispaginate', 0)
        if int(ispaginate) == 1:
            page_size, page_index = 0, 0
        return page_size, page_index

# def parse_pwd(pwd):
#     return md5((SALT + pwd).encode('utf-8')).hexdigest()


# def parse_list_args():
#     req_args = request.args
#     limit = int(req_args.get('limit', 99999))
#     offset = int(req_args.get('offset', 0))
#     # q = req_args.get('q', None)
#     return limit, offset
#
#
# def parse_list_args2():
#     req_args = request.args
#     page_size = req_args.get('page_size', 10)
#     if page_size:
#         page_size = int(page_size)
#
#     page_index = req_args.get('page_index', 1)
#     if page_index:
#         page_index = int(page_index)
#     return page_size, page_index
#
#
# def parse_json_form(name, yml_json, logger):
#     form_json = yml_json.get(name)
#     returnvalue = form_json.get('returnvalue')
#     logger.info(request.json)
#     return [request.json.get(x) for x in returnvalue]
#
#
# def parse_query_string(name, yml_json, logger):
#     form_json = yml_json.get(name)
#     returnvalue = form_json.get('returnvalue')
#     logger.info(request.args)
#     return [request.args.get(x) for x in returnvalue]
