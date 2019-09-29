import os

import oss2

from public_config import (
    OSSAccessKeyId, OSSAccessKeySecret, OSS_ENDPOINT, OSS_BUCTET_NAME, OSSHost,
)


def oss_upload(path, project_name, file_name, user_id):
    auth = oss2.Auth(OSSAccessKeyId, OSSAccessKeySecret)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCTET_NAME)

    current_file_path = project_name + '/' + str(user_id) + '/' + file_name
    try:
        bucket.put_object_from_file(current_file_path, path)
    except oss2.exceptions:
        return ''
    url_string = OSSHost + '/' + current_file_path
    os.remove(path)
    return url_string


def oss_upload_monkey_package_picture(path, picture):
    auth = oss2.Auth(OSSAccessKeyId, OSSAccessKeySecret)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCTET_NAME)

    oss_path = f'monkey/package/{picture}'
    actual_path = f'{path}/{picture}'

    try:
        bucket.put_object_from_file(oss_path, actual_path)
    except oss2.exceptions:
        return ''
    url_string = OSSHost + '/' + oss_path
    os.remove(actual_path)
    return url_string


def oss_download(user_id, url):
    auth = oss2.Auth(OSSAccessKeyId, OSSAccessKeySecret)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCTET_NAME)

    path = os.getcwd()
    dir_path = path + '/excel'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    dir_path = dir_path + '/{}'.format(user_id)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_path = dir_path + '/case_import.xls'

    path_list = url.split('/')
    path_list = path_list[3:]
    path_string = '/'.join(path_list)
    try:
        bucket.get_object_to_file(path_string, file_path)
    except oss2.exceptions:
        return -1
    else:
        return file_path
