"""
报警信息发送给server酱  转发到微信中
"""
import threading
import traceback

import requests
from flask import request, g

SCKEY = 'xxxxxxxx'
serverchan_url = f'https://sc.ftqq.com/{SCKEY}.send'


def _send(text):
    try:
        desp = f"""request  : {request.path}  {request.method} [handler: {g.userid}]  
token    : {request.headers.get('Authorization', 'notoken')}  
projectid: {request.headers.get('projectid', 'noprojectid')}  
query    : {request.args.to_dict()}  
{f"body  : {request.json}" if request.method == 'POST' else ''}  
{traceback.format_exc()}"""
        requests.get(serverchan_url, params={'text': text, 'desp': desp}, timeout=5)
    except requests.RequestException:
        pass


def send2serverchan(text):
    t = threading.Thread(target=_send, args=(text,))
    t.start()
