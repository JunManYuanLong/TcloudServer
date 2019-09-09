#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
import json
import os
import re
import subprocess
import time
import traceback
import zipfile
from datetime import datetime

import requests
from flask import request, current_app

from library.oss import oss_upload_monkey_package_picture
from public_config import TCLOUD_FILE_TEMP_PATH


class ToolBusiness(object):

    @classmethod
    def get_tool_ip(cls):
        ip = request.args.get('ip')

        url = 'http://api.map.baidu.com/location/ip'
        params = {"ip": ip, "ak": 'kqCYLKt8Uz9VnvHBXA7uOI51FIrei0OM'}
        ret = requests.get(url=url, params=params)
        ret = json.loads(ret.content)

        if ret and 'status' in ret and ret['status'] == 0 and 'content' in ret and 'address' in ret:
            return ret['status'], ret['content'], ret['address'], 'ok'

        return 101, '', '', '获取失败'

    @classmethod
    def apk_analysis(cls, apk_download_url, type=1):
        try:
            # type 1 : not save , 2: save to db
            target_path = "/tmp/packages/"
            if not os.path.exists(target_path):
                os.mkdir(target_path)

            date_time_now = datetime.now().strftime('%Y%m%d-%H.%M.%S')
            target_name = '{}.apk'.format(date_time_now)

            download_apk_name = os.path.join(target_path, target_name)

            current_app.logger.info('开始从 {} 下载到 {}'.format(apk_download_url, download_apk_name))

            response = requests.get(url=apk_download_url, verify=False)

            with open(download_apk_name, 'wb') as f:
                f.write(response.content)

            time.sleep(0.5)
            # 下载失败
            if not os.path.exists(download_apk_name):
                current_app.logger.error('{} 下载失败!'.format(apk_download_url))
                return 102, "下载失败"

            current_app.logger.info('下载成功,保存地址 {}'.format(download_apk_name))
            current_app.logger.info('开始分析')

            package_info_re = re.compile(r"package: name='(.*)' versionCode='(.*)' versionName='(.*?)'.*", re.I)
            label_icon_re = re.compile(r"application: label='(.+)'.*icon='(.+)'", re.I)
            launchable_activity_re = re.compile(r"launchable-activity: name='(.+)'.*label.*", re.I)

            apk_info = {}

            cmd = '/usr/local/bin/aapt dump badging {}'.format(download_apk_name)

            command_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            infos = command_process.stdout.readlines()

            for info in infos:
                info = info.decode('utf-8')
                if info.startswith('package:'):
                    temp = package_info_re.search(info)
                    apk_info['package_name'] = temp.group(1)
                    apk_info['version_code'] = temp.group(2) or 0
                    apk_info['version_name'] = temp.group(3)
                elif info.startswith('application:'):
                    temp = label_icon_re.search(info)
                    apk_info['label'] = temp.group(1)
                    apk_info['icon'] = temp.group(2)
                elif info.startswith('launchable-activity:'):
                    temp = launchable_activity_re.search(info)
                    apk_info['default_activity'] = temp.group(1)

            try:
                size = round(os.path.getsize(download_apk_name) / float(1024 * 1024), 2)
                apk_info['size'] = str(size)
                zip = zipfile.ZipFile(download_apk_name)
                icon_binary = zip.read(apk_info['icon'])
                time_now = datetime.now().strftime('%Y%m%d.%H%M%S')
                picture = f'monkey-{time_now}.png'
                dir_path = f'{TCLOUD_FILE_TEMP_PATH}/monkey'

                if not os.path.exists(TCLOUD_FILE_TEMP_PATH):
                    os.mkdir(TCLOUD_FILE_TEMP_PATH)

                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
                with open(f'{dir_path}/{picture}', 'wb') as f:
                    f.write(icon_binary)

                apk_info['icon'] = oss_upload_monkey_package_picture(dir_path, picture)
            except Exception as e:
                current_app.logger.warning(e)
                current_app.logger.warning(traceback.format_exc())

            current_app.logger.info(apk_info)

            if type == 1:
                pass
            elif type == 2:
                pass

            return apk_info
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error(traceback.format_exc())
            return {}
