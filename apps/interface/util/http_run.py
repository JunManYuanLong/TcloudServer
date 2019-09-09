# coding=utf-8
import copy
import datetime
import importlib
import json

# from app import scheduler
from flask.json import JSONEncoder
from httprunner import HttpRunner, loader, parser, utils

# import httprunner
from apps.interface.business.interfacereport import InterfaceReportBusiness
from apps.interface.models.interfaceapimsg import InterfaceApiMsg
from apps.interface.models.interfacecase import InterfaceCase
from apps.interface.models.interfacecasedata import InterfaceCaseData
from apps.interface.models.interfaceconfig import InterfaceConfig
from apps.interface.models.interfaceproject import InterfaceProject
from apps.interface.util.global_variable import *
from apps.interface.util.utils import merge_config, encode_object


class MyHttpRunner(HttpRunner):
    """
    修改HttpRunner，用例初始化时导入函数
    """

    def __init__(self):
        super(MyHttpRunner, self).__init__()

    def parse_tests(self, testcases, variables_mapping=None):
        """ parse testcases configs, including variables/parameters/name/request.

        Args:
            testcases (list): testcase list, with config unparsed.
            variables_mapping (dict): if variables_mapping is specified, it will override variables in config block.

        Returns:
            list: parsed testcases list, with config variables/parameters/name/request parsed.

        """
        self.exception_stage = "parse tests"
        variables_mapping = variables_mapping or {}

        parsed_testcases_list = []
        for testcase in testcases:
            # parse config parameters
            config_parameters = testcase.setdefault("config", {}).pop("parameters", [])

            cartesian_product_parameters_list = parser.parse_parameters(
                config_parameters,
                self.project_mapping["debugtalk"]["variables"],
                self.project_mapping["debugtalk"]["functions"]
            ) or [{}]

            for parameter_mapping in cartesian_product_parameters_list:
                testcase_dict = testcase
                config = testcase_dict.setdefault("config", {})

                testcase_dict["config"]["functions"] = {}

                # imported_module = importlib.reload(importlib.import_module('func_list.build_in'))
                # testcase_dict["config"]["functions"].update(loader.load_python_module(imported_module)["functions"])

                if config.get('import_module_functions'):
                    for f in config.get('import_module_functions'):
                        imported_module = importlib.reload(importlib.import_module(f))
                        debugtalk_module = loader.load_python_module(imported_module)
                        testcase_dict["config"]["functions"].update(debugtalk_module["functions"])
                testcase_dict["config"]["functions"].update(self.project_mapping["debugtalk"]["functions"])
                # self.project_mapping["debugtalk"]["functions"].update(debugtalk_module["functions"])
                raw_config_variables = config.get("variables", [])
                parsed_config_variables = parser.parse_data(
                    raw_config_variables,
                    self.project_mapping["debugtalk"]["variables"],
                    testcase_dict["config"]["functions"])

                # priority: passed in > debugtalk.py > parameters > variables
                # override variables mapping with parameters mapping
                config_variables = utils.override_mapping_list(
                    parsed_config_variables, parameter_mapping)
                # merge debugtalk.py module variables
                config_variables.update(self.project_mapping["debugtalk"]["variables"])
                # override variables mapping with passed in variables_mapping
                config_variables = utils.override_mapping_list(
                    config_variables, variables_mapping)

                testcase_dict["config"]["variables"] = config_variables

                # parse config name
                testcase_dict["config"]["name"] = parser.parse_data(
                    testcase_dict["config"].get("name", ""),
                    config_variables,
                    self.project_mapping["debugtalk"]["functions"]
                )

                # parse config request
                testcase_dict["config"]["request"] = parser.parse_data(
                    testcase_dict["config"].get("request", {}),
                    config_variables,
                    self.project_mapping["debugtalk"]["functions"]
                )
                # put loaded project functions to config
                # testcase_dict["config"]["functions"] = self.project_mapping["debugtalk"]["functions"]
                parsed_testcases_list.append(testcase_dict)
        return parsed_testcases_list


def main_ate(cases):
    runner = MyHttpRunner().run(cases)
    summary = runner.summary
    return summary


class RunCase(object):
    def __init__(self, project_ids=None):
        self.project_ids = project_ids
        self.pro_config_data = None
        self.pro_base_url = None
        self.new_report_id = None
        self.init_project_data()

    def init_project_data(self):
        self.pro_config_data = self.pro_config(
            InterfaceProject.query.filter_by(id=self.project_ids, status=InterfaceProject.ACTIVE).first())
        pro_base_url = {}
        for pro_data in InterfaceProject.query.all():
            if pro_data.environment_choice == 'first':
                pro_base_url['{}'.format(pro_data.id)] = json.loads(pro_data.host)
            elif pro_data.environment_choice == 'second':
                pro_base_url['{}'.format(pro_data.id)] = json.loads(pro_data.host_two)
            if pro_data.environment_choice == 'third':
                pro_base_url['{}'.format(pro_data.id)] = json.loads(pro_data.host_three)
            if pro_data.environment_choice == 'fourth':
                pro_base_url['{}'.format(pro_data.id)] = json.loads(pro_data.host_four)
        self.pro_base_url = pro_base_url

    @staticmethod
    def pro_config(project_data):
        """
        把project的配置数据解析出来
        :param project_data:
        :return:
        """
        pro_cfg_data = {
            'config': {'name': 'config_name', 'request': {}, 'output': []},
            'teststeps': [],
            'name': 'config_name'
        }

        pro_cfg_data['config']['request']['headers'] = {h['key']: h['value'] for h in
                                                        json.loads(project_data.headers) if h.get('key')}
        # pro_cfg_data['config']['request']['headers'] = {h['key']: h['value'] for h in
        #                                                 json.loads([]) if h.get('key')}
        pro_cfg_data['config']['variables'] = json.loads(project_data.variables)
        return pro_cfg_data

    @staticmethod
    def assemble_step(api_id=None, step_data=None, pro_base_url=None, status=False):
        """
        :param api_id:
        :param step_data:
        :param pro_base_url:
        :param status: 判断是接口调试(false)or业务用例执行(true)
        :return:
        """
        if status:
            # 为true，获取api基础信息；case只包含可改变部分所以还需要api基础信息组合成全新的用例
            api_data = InterfaceApiMsg.query.filter_by(id=step_data.api_msg_id, status=InterfaceApiMsg.ACTIVE).first()
        else:
            # 为false，基础信息和参数信息都在api里面，所以api_case = case_data，直接赋值覆盖
            api_data = InterfaceApiMsg.query.filter_by(id=api_id, status=InterfaceApiMsg.ACTIVE).first()
            step_data = api_data
            # api_data = case_data

        _data = {
            'name': step_data.name,
            'request': {
                'method': api_data.method,
                'files': {},
                'data': {}
            }
        }

        _data['request']['headers'] = {h['key']: h['value'] for h in json.loads(api_data.header)
                                       if h['key']} if json.loads(api_data.header) else {}

        if api_data.status_url != '-1':

            _data['request']['url'] = pro_base_url['{}'.format(api_data.project_id)][
                                          int(api_data.status_url)] + api_data.url.split('?')[0]
        else:
            _data['request']['url'] = api_data.url

        if step_data.up_func:
            _data['setup_hooks'] = [step_data.up_func]

        if step_data.down_func:
            _data['teardown_hooks'] = [step_data.down_func]

        if status:
            _data['times'] = step_data.time
            if json.loads(step_data.status_param)[0]:
                if json.loads(step_data.status_param)[1]:
                    _param = json.loads(step_data.param)
                else:
                    _param = json.loads(api_data.param)
            else:
                _param = None

            if json.loads(step_data.status_variables)[0]:
                if json.loads(step_data.status_variables)[1]:
                    _json_variables = step_data.json_variable
                    _variables = json.loads(step_data.variable)
                else:
                    _json_variables = api_data.json_variable
                    _variables = json.loads(api_data.variable)
            else:
                _json_variables = None
                _variables = None

            if json.loads(step_data.status_extract)[0]:
                if json.loads(step_data.status_extract)[1]:
                    _extract = step_data.extract
                else:
                    _extract = api_data.extract
            else:
                _extract = None

            if json.loads(step_data.status_validate)[0]:
                if json.loads(step_data.status_validate)[1]:
                    _validate = step_data.validate
                else:
                    _validate = api_data.validate
            else:
                _validate = None

        else:
            _param = json.loads(api_data.param)
            _json_variables = api_data.json_variable
            _variables = json.loads(api_data.variable)
            _extract = api_data.extract
            _validate = api_data.validate

        _data['request']['params'] = {param['key']: param['value'].replace('%', '&') for param in
                                      _param if param.get('key')} if _param else {}

        _data['extract'] = [{ext['key']: ext['value']} for ext in json.loads(_extract) if
                            ext.get('key')] if _extract else []
        _data['validate'] = [{val['comparator']: [val['key'], val['value']]} for val in json.loads(_validate) if
                             val.get('key')] if _validate else []

        if api_data.method == 'GET':
            pass
        # elif _variables:
        #     print(_variables)
        #     print(111)
        elif api_data.variable_type == 'text' and _variables:
            for variable in _variables:
                if variable['param_type'] == 'string' and variable.get('key'):
                    _data['request']['files'].update({variable['key']: (None, variable['value'])})
                elif variable['param_type'] == 'file' and variable.get('key'):
                    _data['request']['files'].update({
                        variable['key']: (
                            variable['value'].split('/')[-1], open(variable['value'], 'rb'),
                            CONTENT_TYPE['.{}'.format(variable['value'].split('.')[-1])])
                    })

        elif api_data.variable_type == 'data' and _variables:
            for variable in _variables:
                if variable['param_type'] == 'string' and variable.get('key'):
                    _data['request']['data'].update({variable['key']: variable['value']})
                elif variable['param_type'] == 'file' and variable.get('key'):
                    _data['request']['files'].update({
                        variable['key']: (
                            variable['value'].split('/')[-1], open(variable['value'], 'rb'),
                            CONTENT_TYPE['.{}'.format(variable['value'].split('.')[-1])])
                    })

        elif api_data.variable_type == 'json':
            if _json_variables:
                _data['request']['json'] = json.loads(_json_variables)

        return _data

    def get_api_test(self, api_ids, config_id):
        # scheduler.app.logger.info('本次测试的接口id：{}'.format(api_ids))
        temp_case = []
        _temp_config = copy.deepcopy(self.pro_config_data)
        config_data = InterfaceConfig.query.filter_by(id=config_id, status=InterfaceConfig.ACTIVE).first()
        _config = json.loads(config_data.variables) if config_id else []
        if config_id:
            _temp_config['config']['import_module_functions'] = ['func_list.{}'.format(
                f.replace('.py', '')) for f in json.loads(config_data.func_address)]
        _temp_config = merge_config(_temp_config, _config)
        _temp_config['teststeps'] = [self.assemble_step(api_id=api_id, pro_base_url=self.pro_base_url) for api_id in
                                     api_ids]
        temp_case.append(_temp_config)
        return temp_case

    def get_case_test(self, case_ids):
        # scheduler.app.logger.info('本次测试的用例id：{}'.format(case_ids))
        temp_case = []
        for case_id in case_ids:
            case_data = InterfaceCase.query.filter_by(id=case_id, status=InterfaceCase.ACTIVE).first()
            case_times = case_data.times if case_data.times else 1
            for s in range(case_times):
                _temp_config = copy.deepcopy(self.pro_config_data)
                _temp_config['config']['name'] = case_data.name

                # 获取需要导入的函数
                _temp_config['config']['import_module_functions'] = ['func_list.{}'.format(
                    f.replace('.py', '')) for f in json.loads(case_data.func_address)]

                # 获取业务集合的配置数据
                scene_config = json.loads(case_data.variable) if case_data.variable else []

                # 合并公用项目配置和业务集合配置
                _temp_config = merge_config(_temp_config, scene_config)
                for _step in InterfaceCaseData.query.filter_by(
                        case_id=case_id, execute_status=InterfaceCaseData.ACTIVE).order_by(
                    InterfaceCaseData.num.asc()
                ).all():
                    if _step.status == 'true':  # 判断用例状态，是否执行
                        _temp_config['teststeps'].append(self.assemble_step(None, _step, self.pro_base_url, True))
                temp_case.append(_temp_config)
        return temp_case

    def build_report(self, jump_res, case_ids):

        case_names = ','.join(
            [InterfaceCase.query.filter_by(id=scene_id, status=InterfaceCase.ACTIVE).first().name for scene_id in
             case_ids]),
        read_status = '待阅'
        self.new_report_id = InterfaceReportBusiness.report_create(case_names, read_status, self.project_ids)

        with open('{}{}.txt'.format(REPORT_ADDRESS, self.new_report_id), 'w') as f:
            f.write(jump_res)

    @staticmethod
    def run_case(test_cases):
        now_time = datetime.datetime.now()
        # scheduler.app.logger.info('测试数据：{}'.format(test_cases))
        res = main_ate(test_cases)

        res['time']['duration'] = "%.2f" % res['time']['duration']
        res['stat']['successes_1'] = res['stat']['successes']
        res['stat']['failures_1'] = res['stat']['failures']
        res['stat']['errors_1'] = res['stat']['errors']
        res['stat']['successes'] = "{} ({}%)".format(res['stat']['successes'],
                                                     int(res['stat']['successes'] / res['stat'][
                                                         'testsRun'] * 100))
        res['stat']['failures'] = "{} ({}%)".format(res['stat']['failures'],
                                                    int(res['stat']['failures'] / res['stat'][
                                                        'testsRun'] * 100))
        res['stat']['errors'] = "{} ({}%)".format(res['stat']['errors'],
                                                  int(res['stat']['errors'] / res['stat'][
                                                      'testsRun'] * 100))
        res['stat']['successes_scene'] = 0
        res['stat']['failures_scene'] = 0
        for num_1, res_1 in enumerate(res['details']):
            if res_1['success']:
                res['stat']['successes_scene'] += 1
            else:
                res['stat']['failures_scene'] += 1
        res['stat']['all_scene'] = res['stat']['successes_scene'] + res['stat']['failures_scene']

        res['stat']['successes_scene1'] = "{} ({}%)".format(res['stat']['successes_scene'],
                                                            int(res['stat']['successes_scene'] / res['stat'][
                                                                'all_scene'] * 100))
        res['stat']['failures_scene1'] = "{} ({}%)".format(res['stat']['failures_scene'],
                                                           int(res['stat']['failures_scene'] / res['stat'][
                                                               'all_scene'] * 100))

        res['time']['start_at'] = now_time.strftime('%Y/%m/%d %H:%M:%S')
        jump_res = json.dumps(res, ensure_ascii=False, default=encode_object, cls=JSONEncoder)
        # scheduler.app.logger.info('返回数据：{}'.format(jump_res))
        return jump_res
