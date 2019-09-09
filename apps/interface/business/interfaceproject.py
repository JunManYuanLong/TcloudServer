import json

from flask import current_app, jsonify
from sqlalchemy import asc, desc

from apps.auth.models.users import UserBindProject
from apps.interface.models.interfacecase import InterfaceCase
from apps.interface.models.interfacecaseset import InterfaceCaseSet
from apps.interface.models.interfaceconfig import InterfaceConfig
from apps.interface.models.interfacemodule import InterfaceModule
from apps.interface.models.interfaceproject import InterfaceProject
from library.api.db import db
from library.api.transfer import transfer2json
from library.trpc import Trpc

user_trpc = Trpc('auth')


class InterfaceProjectBusiness(object):

    @classmethod
    def _query(cls):
        return InterfaceProject.query.add_columns(
            InterfaceProject.id.label('id'),
            InterfaceProject.name.label('name'),
            InterfaceProject.description.label('description'),
            InterfaceProject.weight.label('weight'),
            InterfaceProject.status.label('status'),
            InterfaceProject.host.label('host'),
            InterfaceProject.host_two.label('host_two'),
            InterfaceProject.host_three.label('host_three'),
            InterfaceProject.host_four.label('host_four'),
            InterfaceProject.environment_choice.label('environment_choice'),
            InterfaceProject.principal.label('principal'),
            InterfaceProject.variables.label('variables'),
            InterfaceProject.headers.label('headers'),
            InterfaceProject.all_project_id.label('all_project_id'),
            InterfaceProject.user_id.label('user_id'),

        )

    @classmethod
    @transfer2json(
        '?id|!name|!description|!status|!weight|!host|!host_two|!host_three|!host_four|!environment_choice|'
        '!principal|!variables|!headers|!all_project_id|!user_id')
    def query_all_json(cls, limit, offset):
        ret = cls._query().filter(InterfaceProject.status == InterfaceProject.ACTIVE).order_by(
            desc(InterfaceProject.weight)).limit(limit).offset(offset).all()

        return ret

    @classmethod
    @transfer2json(
        '?id|!name|!description|!status|!weight|!host|!host_two|!host_three|!host_four|!environment_choice|'
        '!principal|!variables|!headers|!all_project_id|!user_id')
    def query_json_by_id(cls, id):
        return cls._query().filter(InterfaceProject.id == id,
                                   InterfaceProject.status == InterfaceProject.ACTIVE).all()

    @classmethod
    @transfer2json(
        '?id|!name|!description|!status|!weight|!host|!host_two|!host_three|!host_four|!environment_choice|'
        '!principal|!variables|!headers|!all_project_id|!user_id')
    def query_by_project_name(cls, name):
        ret = cls._query().filter(InterfaceProject.status == InterfaceProject.ACTIVE,
                                  InterfaceProject.name == name).order_by(desc(InterfaceProject.name)).all()
        return ret

    @classmethod
    def create_new_project(cls, name, host, host_two, host_three, host_four, environment_choice, variables, headers,
                           description, all_project_id, user_id):
        try:
            p = InterfaceProject(
                name=name,
                host=host,
                host_two=host_two,
                host_three=host_three,
                host_four=host_four,
                environment_choice=environment_choice,
                variables=variables,
                headers=headers,
                description=description,
                all_project_id=all_project_id,
                user_id=user_id,
            )
            db.session.add(p)
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def modify(cls, id, name, host, host_two, host_three, host_four, environment_choice, variables, headers,
               description, user_id):
        project = InterfaceProject.query.get(id)
        if project.status == InterfaceProject.ACTIVE:
            try:
                project.name = name
                project.host = host
                project.host_two = host_two
                project.host_three = host_three
                project.host_four = host_four
                project.environment_choice = environment_choice
                project.variables = variables
                project.headers = headers
                project.description = description
                project.user_id = user_id
                db.session.add(project)
                db.session.commit()
                return 0, None
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(str(e))
                return 102, str(e)
        else:
            return 101, "The InterfaceProject's Status is DISABLE!"

    @classmethod
    def close_project(cls, id):
        project = InterfaceProject.query.get(id)
        project.status = InterfaceProject.DISABLE
        db.session.add(project)
        db.session.commit()
        return 0

    @classmethod
    def bind_users(cls, pid, userids):
        try:
            [db.session.delete(item) for item in UserBindProject.query.filter_by(project_id=pid).all()]
            [db.session.add(UserBindProject(user_id=uid, project_id=pid)) for uid in userids]
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def get_pro_gather(cls, all_project_id):

        _pros = InterfaceProject.query.filter(InterfaceProject.status == InterfaceProject.ACTIVE,
                                              InterfaceProject.all_project_id == all_project_id).order_by(
            InterfaceProject.id).all()
        my_pros = InterfaceProject.query.filter_by(status=InterfaceProject.ACTIVE,
                                                   all_project_id=all_project_id).first()
        pro = {}
        pro_and_id = []
        pro_url = {}
        scene_config_lists = {}
        set_list = {}
        scene_list = {}
        for p in _pros:
            pro_and_id.append({'name': p.name, 'id': p.id})
            # 获取每个项目下的接口模块
            pro[p.name] = [{'name': m.name, 'moduleId': m.id} for m in
                           InterfaceModule.query.filter(InterfaceModule.status == InterfaceModule.ACTIVE,
                                                        InterfaceModule.project_id == p.id).order_by(
                               asc(InterfaceModule.num)).all()]
            # 获取每个项目下的配置信息
            scene_config_lists[p.name] = [{'name': c.name, 'configId': c.id} for c in
                                          InterfaceConfig.query.filter(InterfaceConfig.status == InterfaceConfig.ACTIVE,
                                                                       InterfaceConfig.project_id == p.id).order_by(
                                              asc(InterfaceConfig.num)).all()]
            # 获取每个项目下的用例集
            set_list[p.name] = [{'label': s.name, 'id': s.id} for s in
                                InterfaceCaseSet.query.filter(InterfaceCaseSet.status == InterfaceCaseSet.ACTIVE,
                                                              InterfaceCaseSet.project_id == p.id).order_by(
                                    asc(InterfaceCaseSet.num)).all()]
            # 获取每个用例集的用例
            for s in InterfaceCaseSet.query.filter(
                    InterfaceCaseSet.status == InterfaceCaseSet.ACTIVE,
                    InterfaceCaseSet.project_id == p.id
            ).order_by(asc(InterfaceCaseSet.num)).all():
                scene_list["{}".format(s.id)] = [{'label': scene.name, 'id': scene.id} for scene in
                                                 InterfaceCase.query.filter_by(case_set_id=s.id,
                                                                               status=InterfaceCase.ACTIVE,
                                                                               project_id=p.id).all()]

            # 获取每个项目下的url
            if p.environment_choice == 'first':
                pro_url[p.name] = json.loads(p.host)
            elif p.environment_choice == 'second':
                pro_url[p.name] = json.loads(p.host_two)
            elif p.environment_choice == 'third':
                pro_url[p.name] = json.loads(p.host_three)
            elif p.environment_choice == 'fourth':
                pro_url[p.name] = json.loads(p.host_four)

        if my_pros:
            my_pros = {'pro_name': my_pros.name, 'model_list': pro[my_pros.name]}
        else:
            my_pros = {}

        return (
            {
                'data': pro, 'urlData': pro_url, 'status': 1, 'user_pro': my_pros,
                'config_name_list': scene_config_lists,
                'set_list': set_list, 'scene_list': scene_list, 'pro_and_id': pro_and_id
            })

    @classmethod
    def project_index_handler(cls, project_name, host, host_two, host_three, host_four, environment_choice, ids,
                              headers,
                              variables, description, all_project_id, user_id):

        if not project_name:
            return jsonify({'msg': '项目名称不能为空', 'status': 0})
        if not user_id:
            return jsonify({'msg': '请选择负责人', 'status': 0})
        if ids:
            old_project_data = InterfaceProject.query.filter_by(id=ids, status=InterfaceProject.ACTIVE,
                                                                all_project_id=all_project_id).first()

            if InterfaceProject.query.filter_by(
                    name=project_name,
                    status=InterfaceProject.ACTIVE).first() and project_name != old_project_data.name:
                return jsonify({'msg': '项目名字重复', 'status': 0})
            else:
                ret, msg = InterfaceProjectBusiness.modify(ids, project_name, host, host_two, host_three, host_four,
                                                           environment_choice, variables, headers, description, user_id)
                return jsonify({'msg': '修改成功', 'status': 1})
        else:
            if InterfaceProject.query.filter_by(name=project_name, status=InterfaceProject.ACTIVE).first():
                return jsonify({'msg': '项目名字重复', 'status': 0})
            else:
                ret, msg = InterfaceProjectBusiness.create_new_project(project_name, host, host_two, host_three,
                                                                       host_four,
                                                                       environment_choice, variables, headers,
                                                                       description,
                                                                       all_project_id, user_id)
                return jsonify({'msg': '新建成功', 'status': 1})

    @classmethod
    def find_project(cls, project_name, page, per_page, all_project_id):

        users = user_trpc.requests('get', '/user')
        user_data = [{'user_id': u.get('userid'), 'user_name': u.get('username')} for u in users]

        if project_name:
            _data = InterfaceProject.query.filter(InterfaceProject.name.like('%{}%'.format(project_name)),
                                                  InterfaceProject.status == InterfaceProject.ACTIVE,
                                                  InterfaceProject.all_project_id == all_project_id).all()
            total = len(_data)
            if not _data:
                return jsonify({'msg': '没有该项目', 'status': 0})
        else:
            pagination = InterfaceProject.query.filter(InterfaceProject.status == InterfaceProject.ACTIVE,
                                                       InterfaceProject.all_project_id == all_project_id).order_by(
                InterfaceProject.id.asc()).paginate(page, per_page=per_page, error_out=False)
            _data = pagination.items
            total = pagination.total

        project = [
            {
                'id': c.id,
                'host': c.host,
                'name': c.name,
                'choice': c.environment_choice,
                'principal': user_trpc.requests('get', '/user', query={'userid': c.user_id})[0].get('name'),
                'host_two': c.host_two,
                'host_three': c.host_three,
                'host_four': c.host_four
            }
            for c in _data
        ]

        return jsonify({'data': project, 'total': total, 'status': 1, 'userData': user_data})

    @classmethod
    def edit_project(cls, pro_id, all_project_id):
        _edit = InterfaceProject.query.filter_by(id=pro_id, status=InterfaceProject.ACTIVE,
                                                 all_project_id=all_project_id).first()

        if not _edit.user_id:
            return jsonify({'msg': '请选择负责人', 'status': 0})

        _data = {
            'pro_name': _edit.name,
            'principal': _edit.principal,
            'host': json.loads(_edit.host),
            'host_two': json.loads(_edit.host_two),
            'host_three': json.loads(_edit.host_three),
            'host_four': json.loads(_edit.host_four),
            'headers': json.loads(_edit.headers),
            'environment_choice': _edit.environment_choice,
            'variables': json.loads(_edit.variables),
            'user_id': _edit.user_id,
        }

        return jsonify({'data': _data, 'status': 1})

    @classmethod
    def del_project(cls, ids, all_project_id):
        # pro_data = Project.query.filter_by(id=ids).first()
        # if current_user.id != pro_data.user_id:
        #     return jsonify({'msg': '不能删除别人创建的项目', 'status': 0})

        if InterfaceModule.query.filter(
                InterfaceModule.status == InterfaceModule.ACTIVE, InterfaceModule.project_id == ids,
                InterfaceProject.all_project_id == all_project_id
        ).order_by(asc(InterfaceModule.num)).all():
            return jsonify({'msg': '请先删除项目下的接口模块', 'status': 0})
        if InterfaceCaseSet.query.filter(InterfaceCaseSet.status == InterfaceCaseSet.ACTIVE,
                                         InterfaceCaseSet.project_id == ids).order_by(asc(InterfaceCaseSet.num)).all():
            return jsonify({'msg': '请先删除项目下的业务集', 'status': 0})
        if InterfaceConfig.query.filter(InterfaceConfig.status == InterfaceConfig.ACTIVE,
                                        InterfaceConfig.project_id == ids).order_by(asc(InterfaceConfig.num)).all():
            return jsonify({'msg': '请先删除项目下的业务配置', 'status': 0})

        InterfaceProjectBusiness.close_project(ids)
        return jsonify({'msg': '删除成功', 'status': 1})
