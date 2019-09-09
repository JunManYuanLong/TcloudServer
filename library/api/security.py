from copy import deepcopy
from functools import wraps

from flask import request

from library.api.exceptions import (
    FieldMissingException, InvalidDataException, FieldLengthErrorException,
    DataTypeErrorException,
)


class Validation(object):

    def __init__(self, yaml_json):
        self.yaml_json = yaml_json
        self.key_func_map = {
            'required': self.validate_required,
            'min_length': self.validate_min_length,
            'max_length': self.validate_max_length,
            'type': self.validate_type,
        }

    @staticmethod
    def validate_required(*args):
        key = args[0]
        try:
            request_value = request.json.get(key)
            if request_value is None:
                raise FieldMissingException("{} is required".format(key))
        except AttributeError:
            raise InvalidDataException()

    @staticmethod
    def validate_min_length(*args):
        key = args[0]
        expect_value = args[1]
        request_value = request.json.get(key)
        if request_value is not None and len(request_value) < expect_value:
            raise FieldLengthErrorException("{} min length is {}".format(key, expect_value))

    @staticmethod
    def validate_max_length(*args):
        key = args[0]
        expect_value = args[1]
        request_value = request.json.get(key)
        if request_value is not None and len(request_value) > expect_value:
            raise FieldLengthErrorException("{} max length is {}".format(key, expect_value))

    @staticmethod
    def validate_type(*args):
        ttype_dict = {
            'list': list,
            'basestring': str,
            'dict': dict,
            'int': int,
            'bool': bool,
        }
        key = args[0]
        value = args[1]
        request_value = request.json.get(key)
        if request_value is not None and not isinstance(request_value, ttype_dict.get(value)):
            raise DataTypeErrorException("{} should be a {}".format(key, value))

    def validation(self, validate_name=None):
        def wrapper(func):
            @wraps(func)
            def _(*args, **kwargs):
                protocol, vname = validate_name.split(':')
                if request.method == protocol:
                    all_json = self.yaml_json
                    validate_json = deepcopy(all_json.get(vname))
                    del validate_json['returnvalue']
                    for item, settings in validate_json.items():
                        for key, value in settings.items():
                            f = self.key_func_map.get(key)
                            f(item, value)
                return func(*args, **kwargs)

            return _

        return wrapper
