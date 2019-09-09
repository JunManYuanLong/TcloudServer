import json

import requests
from flask import request, g, current_app
from sqlalchemy import desc, func

from apps.auth.models.users import User
from apps.flow.models.deploy import Deploy, DeployRecord, DeployLog
from apps.flow.models.flow import FlowInfo, FlowBase
from library.api.db import db
from library.api.exceptions import FieldMissingException
from library.api.transfer import transfer2json
from library.trpc import Trpc


class DeployBusiness(object):
    public_trpc = Trpc('public')
    extention_trpc = Trpc('extention')

    @classmethod
    def _query(cls):
        return Deploy.query.add_columns(
            Deploy.id.label('id'),
            Deploy.project_id.label('project_id'),
            Deploy.server_list.label('server_list'),
            Deploy.node_list.label('node_list'),
            Deploy.status.label('status'),
            Deploy.branch.label('branch'),
            Deploy.flow_id.label('flow_id'),
            Deploy.user_id.label('user_id'),
        )

    # 获取url
    @classmethod
    def get_url(cls):
        project_config = cls.public_trpc.requests('get', '/public/config', {'module': 'deploy', 'module_type': 2})
        if project_config:
            run_dict = json.loads(project_config)
        else:
            return None
        track_url = run_dict['URL']

        return track_url

    # 获取url
    @classmethod
    def get_token(cls):
        project_config = cls.public_trpc.requests('get', '/public/config', {'module': 'deploy', 'module_type': 3})
        if project_config:
            run_dict = json.loads(project_config)
        else:
            return None
        track_url = run_dict['api']

        return track_url

    # 获取项目id
    @classmethod
    def get_project_id(cls, project_id):

        project_config = cls.public_trpc.requests('get', '/public/config', {'module': 'deploy', 'module_type': 1})
        if project_config:
            run_dict = json.loads(project_config)
        else:
            return None
        track_project_id = None
        operation_dict = run_dict['operation_dict']
        for i in range(0, len(operation_dict)):
            track_dict = operation_dict[i]
            for k, v in track_dict.items():
                if int(k) == int(project_id):
                    track_project_id = int(v)

        return track_project_id

    @classmethod
    def get_server(cls):
        project_id = request.args.get('project_id')

        deploy_project_id = DeployBusiness.get_project_id(project_id)

        if deploy_project_id:
            url = str(DeployBusiness.get_url()) + '/api/v1/service/tcloud/list'
            params = {"project_id": deploy_project_id, "page_size": 100, "page": 1}
            header = {"api": DeployBusiness.get_token()}
            ret = requests.get(url=url, params=params, headers=header)
            ret = json.loads(ret.content)
            if ret and 'result' in ret and 'data' in ret['result']:
                return ret['code'], ret['result']['data'], ret['message']

        return 101, [], 'can not find object'

    @classmethod
    def get_node(cls):
        project_id = request.args.get('project_id')
        if project_id:
            url = str(DeployBusiness.get_url()) + '/api/v1/node/tcloud/list'
            params = {"project_id": project_id, "page_size": 100, "page": 1}
            ret = requests.get(url=url, params=params)
            ret = json.loads(ret.content)
            if ret and 'result' in ret:
                return ret['code'], ret['result'], ret['message']

        return 101, [], 'can not find object'

    @classmethod
    def get_branch(cls):
        service_id = request.args.get('server_id')
        if service_id:
            url = str(DeployBusiness.get_url()) + '/api/v1/service/branches'
            params = {"service_id": service_id}
            header = {"api": DeployBusiness.get_token()}
            ret = requests.get(url=url, params=params, headers=header)
            ret = json.loads(ret.content)
            if ret and 'data' in ret:
                data_list = ret['data']
                branch_list = []
                for i in range(0, len(data_list)):
                    if 'displayId' in data_list[i]:
                        branch_list.append(data_list[i]['displayId'])

                return ret['code'], branch_list, ret['message']

        return 101, [], 'can not find object'

    @classmethod
    def deploy(cls, node_list, service_list, deploy_id, branch, project_id):

        deploy_project_id = DeployBusiness.get_project_id(project_id)

        if deploy_project_id is None:
            return {'code': 101}

        # 一键部署
        service_list_all = []
        for i in range(0, len(service_list)):
            service_dict = {'service_id': service_list[i], 'branch': branch, 'commit': 'tcloud'}
            service_list_all.append(service_dict)

        url = str(DeployBusiness.get_url()) + '/api/v1/deploy/tcloud/one-key'
        data = {
            "node_id_list": node_list, "service_list": service_list_all, "deploy_id": deploy_id,
            "project_id": deploy_project_id
        }
        data = json.dumps(data)
        header = {"Content-Type": "application/json", "api": DeployBusiness.get_token()}
        ret = requests.post(url=url, data=data, headers=header)
        ret = json.loads(ret.content)

        return ret

    @classmethod
    def create(cls, project_id, server_list_all, node_list_all, branch, flow_id):
        try:

            server_name = []
            server_list = []
            node_list = []
            node_name = []

            for i in range(0, len(server_list_all)):
                server_name.append(server_list_all[i]['server_name'])
                server_list.append(server_list_all[i]['server_id'])

            for i in range(0, len(node_list_all)):
                node_name.append(node_list_all[i]['node_name'])
                node_list.append(node_list_all[i]['node_id'])

            if len(server_list) == 0 or len(node_list) == 0:
                return 101, None

            server_list_string = ','.join(str(i) for i in server_list)
            node_list_string = ','.join(str(i) for i in node_list)

            c = Deploy(
                project_id=project_id,
                server_list=server_list_string,
                node_list=node_list_string,
                branch=branch,
                flow_id=flow_id,
                user_id=g.userid,
            )
            db.session.add(c)
            db.session.flush()

            ret = DeployBusiness.deploy(node_list, server_list, c.id, branch, project_id)

            # 判断是否正在执行

            if ret['code'] != 0 and 'result' in ret and 'code' in ret:
                return 101, None

            for i in range(0, len(server_list)):
                for j in range(0, len(node_list)):
                    DeployRecordBusiness.create(c.id, c.project_id, server_list[i], node_list[j], branch, flow_id,
                                                server_name[i], node_name[j], ret['result'])

            db.session.commit()
            return 0, c.id
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)


class DeployRecordBusiness(object):

    @classmethod
    def _query(cls):
        return DeployRecord.query.add_columns(
            DeployRecord.id.label('id'),
            DeployRecord.project_id.label('project_id'),
            DeployRecord.server_id.label('server_id'),
            DeployRecord.node_id.label('node_id'),
            DeployRecord.status.label('status'),
            DeployRecord.version.label('version'),
            DeployRecord.branch.label('branch'),
            DeployRecord.result.label('result'),
            DeployRecord.deploy_id.label('deploy_id'),
            DeployRecord.flow_id.label('flow_id'),
            DeployRecord.server_name.label('server_name'),
            DeployRecord.node_name.label('node_name'),
        )

    @classmethod
    @transfer2json('?id|!project_id|!server_id|!node_id|!status|!version|!branch|!result|'
                   '!deploy_id|!flow_id|!server_name|!node_name')
    def query_deploy_id_json(cls):

        project_id = request.args.get('project_id')
        flow_id = request.args.get('flow_id')
        deploy_id = request.args.get('deploy_id')

        ret = cls._query().filter(DeployRecord.status == DeployRecord.ACTIVE, DeployRecord.project_id == project_id,
                                  DeployRecord.flow_id == flow_id,
                                  DeployRecord.deploy_id == deploy_id).order_by(desc(DeployRecord.id)).all()
        return ret

    @classmethod
    @transfer2json('?id|!project_id|!server_id|!node_id|!status|!version|!branch|!result|'
                   '!deploy_id|!flow_id|!server_name|!node_name')
    def query_all_json(cls, page_size=10, page_index=1):

        project_id = request.args.get('project_id')
        flow_id = request.args.get('flow_id')

        ret = cls._query().filter(DeployRecord.status == DeployRecord.ACTIVE, DeployRecord.project_id == project_id,
                                  DeployRecord.flow_id == flow_id)

        if page_size and page_index:
            ret = ret.order_by(desc(DeployRecord.id)).limit(int(page_size)).offset(
                (int(page_index) - 1) * int(page_size)).all()
        else:
            ret = ret.order_by(desc(DeployRecord.id)).all()
        return ret

    @classmethod
    @transfer2json('?id|!version|!branch|!result|!server_name|!node_name')
    def query_record_deploy(cls, deploy_id):

        ret = cls._query().filter(DeployRecord.status == DeployRecord.ACTIVE, DeployRecord.deploy_id == deploy_id)

        ret = ret.order_by(desc(DeployRecord.id)).all()
        return ret

    @classmethod
    def query_all_count(cls, project_id, flow_id):
        ret = cls._query().filter(DeployRecord.status == DeployRecord.ACTIVE, DeployRecord.project_id == project_id,
                                  DeployRecord.flow_id == flow_id)
        return ret.count()

    @classmethod
    def create(cls, deploy_id, project_id, server_id, node_id, branch, flow_id, server_name, node_name, ret):
        try:
            version = None
            for i in range(0, len(ret)):
                if ret[i]['service_id'] == server_id and node_id == ret[i]['node_id']:
                    version = ret[i]['version']
                    break

            c = DeployRecord(
                deploy_id=deploy_id,
                project_id=project_id,
                server_id=server_id,
                node_id=node_id,
                branch=branch,
                flow_id=flow_id,
                version=version,
                server_name=server_name,
                node_name=node_name,

            )
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def modify_result(cls, ret, deploy_id):

        if len(ret) == 0:
            return 0

        for i in range(0, len(ret)):
            try:
                deploy = DeployRecord.query.filter(DeployRecord.status == DeployRecord.ACTIVE,
                                                   DeployRecord.server_id == ret[i]['service_id'],
                                                   DeployRecord.deploy_id == deploy_id,
                                                   DeployRecord.node_id == ret[i]['node_id']).first().id
                req = DeployRecord.query.get(deploy)
                req.result = ret[i]['result']
                db.session.add(req)
                db.session.commit()
            except Exception as e:
                current_app.logger.info(e)

        return 0

    # @classmethod
    # def run_automan(cls, deploy_id):
    #
    #     project_id = DeployRecord.query.filter(DeployRecord.status == DeployRecord.ACTIVE,
    #                                            DeployRecord.deploy_id == deploy_id).first().project_id
    #     run_list = [1]
    #     # TODO CiJobBusiness
    #     # run_dict, run_name_dict = CiJobBusiness.gain_run_dict(project_id)
    #     result = cls.extention_rpc.requests('get', '/rundict', {'projectid': project_id})
    #     run_dict = result['run_dict']
    #     run_name_dict = result['run_name_dict']
    #     if project_id and len(run_dict) == 0 and len(run_dict) < len(run_list):
    #         return 102, [], 'empty'
    #     run_name_list = []
    #     for i in range(0, len(run_list)):
    #         run_name_list.append(run_dict[str(run_list[i])])
    #     if len(run_name_list) == 0:
    #         return 102, [], 'empty'
    #
    #     # TODO 我修改的时候发现传入的参数并不对
    #     data = CiJobBusiness.run(run_name_list, run_dict, run_name_dict)
    #
    #     return data

    @classmethod
    def check_log_data(cls):

        record_id = request.args.get('record_id')
        if not record_id:
            raise FieldMissingException('miss record_id')
        deploy_record = DeployRecord.query.filter(DeployRecord.status == DeployRecord.ACTIVE,
                                                  DeployRecord.id == record_id).first()
        service_id = deploy_record.server_id
        node_id = deploy_record.node_id
        version = deploy_record.version

        if service_id and node_id and version:

            url = str(DeployBusiness.get_url()) + '/api/v1/deploy/all-result'

            header = {"api": DeployBusiness.get_token()}
            params = {"service_id": service_id, "node_id": node_id, "version": version}
            ret = requests.get(url=url, params=params, headers=header)
            ret = json.loads(ret.content)

            if ret and 'result' in ret:
                return ret['code'], ret['result'], ret['message']

        return 101, [], 'can not find object'

    @classmethod
    @transfer2json('?id')
    def is_one_key(cls):
        deploy_id = request.args.get('deploy_id')
        project_id = request.args.get('project_id')
        flow_id = request.args.get('flow_id')

        ret = cls._query().filter(DeployRecord.status == DeployRecord.ACTIVE, DeployRecord.project_id == project_id,
                                  DeployRecord.flow_id == flow_id,
                                  DeployRecord.deploy_id == deploy_id, DeployRecord.result == 0).order_by(
            desc(DeployRecord.id)).all()

        return ret

    @classmethod
    @transfer2json('?id')
    def not_init_data(cls, deploy_id):

        ret = cls._query().filter(DeployRecord.status == DeployRecord.ACTIVE, DeployRecord.deploy_id == deploy_id,
                                  DeployRecord.result == 0).order_by(desc(DeployRecord.id)).all()

        return ret


class DeployLogBusiness(object):

    @classmethod
    def _query(cls):
        return DeployLog.query.add_columns(
            DeployLog.id.label('id'),
            func.date_format(DeployLog.creation_time, "%Y-%m-%d %H:%i:%s").label('creation_time'),
            DeployLog.project_id.label('project_id'),
            DeployLog.comment.label('comment'),
            DeployLog.name.label('name'),
            DeployLog.use_id.label('use_id'),
            DeployLog.deploy_id.label('deploy_id'),
            DeployLog.user_name.label('user_name'),
            DeployLog.result_id.label('result_id'),
            DeployLog.status.label('status'),
            DeployLog.flow_id.label('flow_id'),
            DeployLog.log_type.label('log_type'),
            DeployLog.result.label('result'),
        )

    @classmethod
    @transfer2json('?id|!comment|!name|!use_id|!user_name|!result_id|!result|!creation_time')
    def query_all_json(cls, flow_id):

        ret = cls._query().filter(DeployLog.status == DeployLog.ACTIVE, DeployLog.flow_id == flow_id)

        ret = ret.order_by(desc(DeployLog.id)).all()
        return ret

    @classmethod
    def automan_data(cls, data, deploy_id):

        if len(data) > 0 and not data[0]['isexcuting']:
            comment = '<ul><li>名称:' + data[0]['name'] + '</li><li>报告链接:<a href=' + data[0]['url'] + '>' + data[0][
                'url'] + '</a></li></ul>'

            deploy_record_id = DeployRecord.query.filter(DeployRecord.status == DeployRecord.ACTIVE,
                                                         DeployRecord.deploy_id == deploy_id).first().id
            c = DeployRecord.query.get(deploy_record_id)

            flow_info = FlowInfo.query.get(c.flow_id)

            user_id = User.query.filter(User.status == User.ACTIVE, User.nickname == 'automan').first().id

            cls.create(c.project_id, comment, flow_info.name, user_id, deploy_id, 'automan', 4, c.flow_id, 1, '5')

        return 0, [], 'ok'

    @classmethod
    def deploy_data(cls, data, deploy_id):

        if len(data) > 0:
            data_dict = {"0": "编译中", "1": "打包失败", "2": "发布失败", "3": "重启失败", "4": "成功"}
            comment = ''

            for i in range(0, len(data)):
                comment = comment + '<p>ID:' + str(data[i]['id']) + '&nbsp;服务名:' + data[i][
                    'server_name'] + '&nbsp;节点名:' + data[i]['node_name'] + '&nbsp;分支:' + data[i][
                              'branch'] + '&nbsp;版本:' + data[i]['version'] + '&nbsp;部署状态:' + data_dict[
                              str(data[i]['result'])] + '</p>'

            deploy_record_id = DeployRecord.query.filter(DeployRecord.status == DeployRecord.ACTIVE,
                                                         DeployRecord.deploy_id == deploy_id).first().id
            c = DeployRecord.query.get(deploy_record_id)

            flow_info = FlowInfo.query.get(c.flow_id)

            user_id = Deploy.query.filter(Deploy.status == Deploy.ACTIVE, Deploy.id == deploy_id).first().user_id

            user_nickname = User.query.filter(User.status == User.ACTIVE, User.id == user_id).first().nickname

            # 获取result_id
            flow_base_id = FlowBase.query.filter(FlowBase.name == '提测').first().id
            result_id = flow_base_id

            # 获取result
            base_step = FlowBase.query.filter(FlowBase.name == '提测').first().step
            base_step_list = json.loads(base_step)
            result = "6"
            for i in range(0, len(base_step_list)):
                data_dict = base_step_list[i]
                for k, v in data_dict.items():
                    if v == '备注':
                        result = k

            cls.create(c.project_id, comment, flow_info.name, user_id, deploy_id,
                       user_nickname, result_id, c.flow_id, 2, result)

        return 0, [], 'ok'

    @classmethod
    def create(cls, project_id, comment, name, use_id, deploy_id, user_name, result_id, flow_id, log_type, result):
        try:

            c = DeployLog(
                project_id=project_id,
                comment=comment,
                name=name,
                use_id=use_id,
                deploy_id=deploy_id,
                user_name=user_name,
                result_id=result_id,
                flow_id=flow_id,
                log_type=log_type,
                result=result

            )
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)
