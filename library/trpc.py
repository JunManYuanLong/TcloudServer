#   ____  __    __     __
#    /   /__)  /__)  /
#   /   / (   /      \__
#
"""
Trpc
~~~~~~~~~~~~~~~~~~~~~
Tprc是当前阶段用来进行服务间相互调用的简易版rpc

Request: 请求方法、请求路径(自带一个v1，可通过参数去除)、url参数(可不带)、body(默认是json格式)
Response: 当服务500，返回None，当出现超时会重复三次，其他错误None
          服务200时，返回序列化的json对象(字典)  其中一种格式为：{'code': 0, 'data': [], 'message': 'ok'}

"""
import logging
import os
import os.path
import time
from os.path import dirname

import requests

from public_config import TSECRET

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logfile = "trpc_" + time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + ".log"
fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class Trpc:
    def __init__(self, service, no_v1=None):
        port = ''
        current_path = dirname(dirname(__file__))
        with open(os.path.join(current_path, f'apps/{service}/settings/config.py'), 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'PORT' in line:
                    port = line.split('=')[-1].strip()
                    port = ':' + port
                    break
        self.base_url = f'http://localhost{port}/v1' if not no_v1 else f'http://localhost{port}'

    def requests(self, method, path=None, query=None, body=None):
        for i in range(3):
            try:
                session = getattr(requests, method)
                if session:
                    r = session(self.base_url + path, json=body, params=query, timeout=8, headers={"tsecret": TSECRET})
                else:
                    return None
                if r.status_code == 200:
                    result = r.json()
                    logger.info(result)
                    if result['code'] == 0:
                        return result['data']
                    else:
                        return None
                elif r.status_code == 500:
                    return None
            except requests.Timeout:
                logger.error(f"{self.base_url} {path} 服务出现超时，"
                             f"method:{method}, query:{query}, body:{body}\n")
            except Exception as e:
                logger.error(f'{self.base_url} {path} 服务出现异常, '
                             f'method:{method}, query:{query}, body:{body}, 错误：{e}\n')
                return None
        return None
