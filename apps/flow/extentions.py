import os
from os.path import join, abspath, dirname, splitext

import yaml

from library.api.parse import TParse
from library.api.security import Validation

current_path = dirname(abspath(__file__))

yml_json = {}

try:
    validate_yml_path = join(current_path, 'validations')
    for fi in os.listdir(validate_yml_path):
        if splitext(fi)[-1] != '.yml':
            continue
        with open(join(validate_yml_path, fi), 'rb') as f:
            yml_json.update(yaml.safe_load(f.read()))
except yaml.YAMLError as e:
    print(e)

v = Validation(yml_json)
validation = v.validation

p = TParse(yml_json)
parse_list_args = p.parse_list_args
parse_list_args2 = p.parse_list_args2
parse_json_form = p.parse_json_form
parse_pwd = p.parse_pwd
