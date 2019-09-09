from apps.auth.models.ability import Ability
from library.api.transfer import transfer2json


class AbilityBusiness(object):
    @classmethod
    def _query(cls):
        return Ability.query

    @classmethod
    @transfer2json('?id|!name|!handler')
    def query_all_json(cls, limit, offset):
        return cls._query().limit(limit).offset(offset).all()

    @classmethod
    def get_ability_class(cls, limit, offset):
        # 以_来间隔  动作  和  权限
        list_data = cls.query_all_json(limit, offset)
        dict_data = {}
        dict_permission = {'view': 1, 'modify': 2, 'delete': 3}
        index = 4
        for data in list_data:
            key = data['handler'].split('_')[0]
            permission = data['handler'].split('_')[-1]
            if key not in dict_data:
                dict_data.update({key: {'data': []}})
            data['order'] = dict_permission.get(permission, index)
            if permission not in dict_permission:
                index += 1
            dict_data[key]['data'].append(data)
            dict_data[key]['label'] = data['name'].split('_')[-1]
            data['name'] = data['name'].replace('_', '')
        return [v for k, v in dict_data.items()]
