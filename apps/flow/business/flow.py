import datetime
import json
import os
import time

import pandas as pd
import xlwt
from flask import request, g, current_app
from sqlalchemy import desc, or_, func
from sqlalchemy.orm import aliased
from xlwt import Font

from apps.auth.business.users import UserBusiness
from apps.auth.models.users import User
from apps.flow.models.flow import FlowInfo, FlowAssemble, FlowBase, FlowRecord, FlowSource
from apps.project.models.project import Project
from apps.project.models.requirement import Requirement
from library.api.db import db
from library.api.exceptions import CannotFindObjectException, OperationPermissionDeniedException
from library.api.transfer import transfer2json
from library.notification import notification
from library.oss import oss_upload
from library.trpc import Trpc
from public_config import TCLOUD_FILE_TEMP_PATH


class FlowBusiness(object):
    user_trpc = Trpc('auth')
    public_trpc = Trpc('public')

    @classmethod
    def _query(cls):
        user_creator = aliased(User)
        # User_dev = aliased(User)
        # User_prod = aliased(User)
        # User_test = aliased(User)
        # User_owner = aliased(User)

        return FlowInfo.query.outerjoin(
            user_creator, user_creator.id == FlowInfo.creator).outerjoin(
            FlowAssemble, FlowAssemble.id == FlowInfo.flow_assemble_id).add_columns(
            FlowInfo.id.label('id'),
            FlowInfo.name.label('name'),
            FlowInfo.flow_type.label('flow_type'),
            FlowInfo.requirement_list.label('requirement_list'),
            FlowInfo.flow_assemble_id.label('flow_assemble_id'),
            FlowInfo.priority.label('priority'),
            FlowInfo.project_id.label('project_id'),
            FlowInfo.version_id.label('version_id'),
            FlowAssemble.name.label('flow_assemble_name'),
            FlowAssemble.flow_asstype.label('flow_assemble_type'),
            FlowAssemble.flow_base_list.label('flow_base_list'),
            func.date_format(FlowInfo.creation_time, "%Y-%m-%d %H:%i:%s").label('start_time'),
            # func.date_format(FlowInfo.start_time, "%Y-%m-%d %H:%M:%S").label('start_time'),
            func.date_format(FlowInfo.end_time, "%Y-%m-%d %H:%i:%s").label('end_time'),
            FlowInfo.action.label('action'),
            FlowInfo.status.label('status'),
            FlowInfo.comment.label('comment'),
            FlowInfo.weight.label('weight'),
            FlowInfo.user_owner.label('user_owner'),
            FlowInfo.user_prod.label('user_prod'),
            FlowInfo.user_test.label('user_test'),
            FlowInfo.user_dev.label('user_dev'),
            FlowInfo.platform.label('platform'),
            FlowInfo.dependence.label('dependence'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),
            user_creator.picture.label('picture'),

        )

    @classmethod
    def _query_all_jsons(cls, page_size, page_index):
        # 大量匹配like查询，数据量大了会慢，待改
        projectid = request.args.get('projectid')
        versionid = request.args.get('versionid')
        flow_status = request.args.get('status')
        name = request.args.get('name')
        user_id = request.args.get('userid')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        flow_assemble_id = request.args.get('flow_assemble_id')
        flow_types = request.args.get('flow_type')
        flow_id = request.args.get('flow_id')
        platform = request.args.get('platform')
        ret = cls._query().filter(FlowInfo.status != FlowInfo.DISABLE)
        if projectid:
            ret = ret.filter(FlowInfo.project_id == projectid)
        if versionid:
            ret = ret.filter(FlowInfo.version_id == versionid)
        if flow_assemble_id:
            flow_assemble_id = flow_assemble_id.split(',')
            ret = ret.filter(FlowInfo.flow_assemble_id.in_(flow_assemble_id))
            current_app.logger.info('flow_assemble_id:' + str(flow_assemble_id))
        if flow_types:
            flow_types = flow_types.split(',')
            ret = ret.filter(FlowInfo.flow_type.in_(flow_types))
            current_app.logger.info('flow_types:' + str(flow_types))
        if flow_id:
            ret = ret.filter(FlowInfo.id.like('%{}%'.format(flow_id)))
        if start_time and end_time:
            ret = ret.filter(FlowInfo.creation_time.between(start_time, end_time + " 23:59:59"))
        if user_id:
            ret = ret.filter(
                or_(FlowInfo.user_dev.like('[{},%'.format(user_id)), FlowInfo.user_dev.like('%, {}]'.format(user_id)),
                    FlowInfo.user_dev.like('%, {},%'.format(user_id)), FlowInfo.user_dev.like('%[{}]%'.format(user_id)),
                    FlowInfo.user_owner.like('[{},%'.format(user_id)),
                    FlowInfo.user_owner.like('%, {}]'.format(user_id)),
                    FlowInfo.user_owner.like('%, {},%'.format(user_id)),
                    FlowInfo.user_owner.like('%[{}]%'.format(user_id)),
                    FlowInfo.user_prod.like('[{},%'.format(user_id)), FlowInfo.user_prod.like('%, {}]'.format(user_id)),
                    FlowInfo.user_prod.like('%, {},%'.format(user_id)),
                    FlowInfo.user_prod.like('%[{}]%'.format(user_id)),
                    FlowInfo.user_test.like('[{},%'.format(user_id)), FlowInfo.user_test.like('%, {}]'.format(user_id)),
                    FlowInfo.user_test.like('%, {},%'.format(user_id)),
                    FlowInfo.user_test.like('%[{}]%'.format(user_id))))
        if flow_status:
            ret = ret.filter(FlowInfo.status == flow_status)
        if name:
            ret = ret.filter(or_(FlowInfo.name.like('%{}%'.format(name)),
                                 FlowInfo.name.like('%{}%'.format(name.lower())),
                                 FlowInfo.name.like('%{}%'.format(name.upper())),
                                 FlowInfo.id.startswith(f'{name}%')))

        if platform:
            ret = ret.filter(
                or_(FlowInfo.platform.like('[{},%'.format(platform)),
                    FlowInfo.platform.like('%, {}]'.format(platform)),
                    FlowInfo.platform.like('%, {},%'.format(platform)),
                    FlowInfo.platform.like('%[{}]%'.format(platform))))
        if page_size and page_index:
            ret = ret.order_by(desc(FlowInfo.id)).limit(int(page_size)).offset(
                (int(page_index) - 1) * int(page_size))
        else:
            ret = ret.order_by(desc(FlowInfo.id))
        return ret

    @classmethod
    def _query_all_jsons_kwargs(cls, **kwargs):
        project_id = kwargs.get('project_id')
        version_id = kwargs.get('version_id')
        flow_status = kwargs.get('status')
        name = kwargs.get('name')
        user_id = kwargs.get('user_id')
        start_time = kwargs.get('start_time')
        end_time = kwargs.get('end_time')
        flow_assemble_id = kwargs.get('flow_assemble_id')
        flow_types = kwargs.get('flow_type')
        flow_id = kwargs.get('flow_id')
        page_size = kwargs.get('page_size')
        page_index = kwargs.get('page_index')
        end_day = kwargs.get('end_day')
        ret = cls._query().filter(FlowInfo.status != FlowInfo.DISABLE)
        if project_id:
            ret = ret.filter(FlowInfo.project_id == project_id)
        if version_id:
            ret = ret.filter(FlowInfo.version_id == version_id)
        if flow_assemble_id:
            flow_assemble_id = flow_assemble_id.split(',')
            ret = ret.filter(FlowInfo.flow_assemble_id.in_(flow_assemble_id))
            current_app.logger.info('flow_assemble_id:' + str(flow_assemble_id))
        if flow_types:
            flow_types = flow_types.split(',')
            ret = ret.filter(FlowInfo.flow_type.in_(flow_types))
            current_app.logger.info('flow_types:' + str(flow_types))
        if flow_id:
            ret = ret.filter(FlowInfo.id.like('%{}%'.format(flow_id)))
        if start_time and end_time:
            ret = ret.filter(FlowInfo.creation_time.between(start_time, end_time))
        if end_day:
            ret = ret.filter(FlowInfo.end_time.startswith(end_day))
        if user_id:
            ret = ret.filter(
                or_(FlowInfo.user_dev.like('[{},%'.format(user_id)), FlowInfo.user_dev.like('%, {}]'.format(user_id)),
                    FlowInfo.user_dev.like('%, {},%'.format(user_id)), FlowInfo.user_dev.like('%[{}]%'.format(user_id)),
                    FlowInfo.user_owner.like('[{},%'.format(user_id)),
                    FlowInfo.user_owner.like('%, {}]'.format(user_id)),
                    FlowInfo.user_owner.like('%, {},%'.format(user_id)),
                    FlowInfo.user_owner.like('%[{}]%'.format(user_id)),
                    FlowInfo.user_prod.like('[{},%'.format(user_id)), FlowInfo.user_prod.like('%, {}]'.format(user_id)),
                    FlowInfo.user_prod.like('%, {},%'.format(user_id)),
                    FlowInfo.user_prod.like('%[{}]%'.format(user_id)),
                    FlowInfo.user_test.like('[{},%'.format(user_id)), FlowInfo.user_test.like('%, {}]'.format(user_id)),
                    FlowInfo.user_test.like('%, {},%'.format(user_id)),
                    FlowInfo.user_test.like('%[{}]%'.format(user_id))))
        if flow_status != '':
            ret = ret.filter(FlowInfo.status == flow_status)
        if name:
            ret = ret.filter(
                or_(FlowInfo.name.like('%{}%'.format(name)), FlowInfo.name.like('%{}%'.format(name.lower())),
                    FlowInfo.name.like('%{}%'.format(name.upper()))))
        if page_size and page_index:
            ret = ret.order_by(desc(FlowInfo.id)).limit(int(page_size)).offset(
                (int(page_index) - 1) * int(page_size))
        else:
            ret = ret.order_by(desc(FlowInfo.id))
        return ret

    @classmethod
    @transfer2json('?id|!name|!flow_type|!requirement_list|!flow_assemble_id|!flow_assemble_name|'
                   '!flow_assemble_type|!status|!flow_base_list|!priority|!start_time|!end_time|'
                   '!project_id|!version_id|!creator_id|!creator_name|!user_dev|!user_prod|'
                   '!user_test|!user_owner|~action|!weight|!comment')
    def query_all_jsons_kwargs(cls, **kwargs):
        return cls._query_all_jsons_kwargs(**kwargs).all()

    @classmethod
    @transfer2json('?id|!name|!flow_type|!requirement_list|!flow_assemble_id|!flow_assemble_name|'
                   '!flow_assemble_type|!status|!flow_base_list|!priority|!start_time|!end_time|'
                   '!picture|!project_id|!version_id|!creator_id|!creator_name|!user_dev|'
                   '!user_prod|!user_test|!user_owner|~action|!weight|!comment|!platform|!dependence')
    def query_all_jsons(cls, page_size, page_index):
        return cls._query_all_jsons(page_size, page_index).all()

    @classmethod
    def query_all_json_count(cls, page_size, page_index):
        return cls._query_all_jsons(page_size, page_index).count()

    @classmethod
    @transfer2json('?id|!name|!flow_type|!requirement_list|!flow_assemble_id|!flow_assemble_name|'
                   '!flow_assemble_type|!status|!flow_base_list|!priority|!start_time|!end_time|'
                   '!picture|!project_id|!version_id|!creator_id|!creator_name|!user_dev|'
                   '!user_prod|!user_test|!user_owner|~action|!weight|!comment|!platform|!dependence')
    def query_by_ids(cls, flow_id):
        ret = cls._query().filter(FlowInfo.status != FlowInfo.DISABLE, FlowInfo.id == flow_id).all()
        return ret

    @classmethod
    def query_by_id(cls, flow_id):
        ret = cls.query_by_ids(flow_id)
        user_list = ['user_dev_id', 'user_prod_id', 'user_test_id', 'user_owner_id']
        for re in ret:
            all_user_list = []
            for li in user_list:
                temp = []
                re[li] = json.loads(re[li[:-3]])
                for us in re[li]:
                    temp.append({'user_id': us, 'user_name': User.query.get(us).nickname})
                    all_user_list.append(us)
                re[li[:-3]] = temp
            re['all_user_list'] = list(set(all_user_list))
        return ret

    @classmethod
    def query_all_json(cls, page_size, page_index):
        ret = cls.query_all_jsons(page_size, page_index)
        ret_count = cls.query_all_json_count('', '')
        user_list = ['user_dev_id', 'user_prod_id', 'user_test_id', 'user_owner_id']
        # ret_user = UserBusiness.query_flow_all_json()
        ret_user = cls.user_trpc.requests('get', '/user/allflow')
        if not ret_user:
            current_app.logger.error("Error:cls.user_trpc.requests('get', '/user/allflow')")
            return [], 0, 101
        ret_user_list = {}
        for ru in ret_user:
            ret_user_list[str(ru['userid'])] = ru['nickname']
        for re in ret:
            all_user_list = []
            for li in user_list:
                temp = []
                re[li] = json.loads(re[li[:-3]])
                for us in re[li]:
                    temp.append({'user_id': us, 'user_name': ret_user_list[str(us)]})
                    all_user_list.append(us)
                re[li[:-3]] = temp
            re['all_user_list'] = list(set(all_user_list))

            if re['platform'] == '[]' or re['platform'] == '' or re['platform'] is None:
                re['platform'] = []
            else:
                platform_list = re['platform'].replace('[', '').replace(']', '').replace(' ', '').split(',')
                re['platform'] = platform_list
        return ret, ret_count, 0

    @classmethod
    def flow_get_rows(cls):
        """
        数据库中获取全部数据(条件筛选写在了query内，从request获取，所以不需要传入参数)，然后格式化数据
        :return: result:格式化数据, tab_dict:列名
        """
        all_result = cls.query_all_json(None, None)[0]

        result, tab_dict = cls.format_xls(all_result)
        return result, tab_dict

    @classmethod
    def flow_delete(cls, flow_id):
        flow_info = FlowInfo.query.get(flow_id)
        project_id = flow_info.project_id
        roles_row = UserBusiness.query_json_by_id_and_project(g.userid, project_id)
        roles_list = roles_row[0]['role'] if roles_row else []
        roles = [role['name'] for role in roles_list]
        user_owner = flow_info.user_owner[1:-1].replace(' ', '').split(',')
        if str(g.userid) not in user_owner and not g.is_admin and 'owner' not in roles:
            raise OperationPermissionDeniedException
        flow_info.status = FlowInfo.DISABLE
        db.session.add(flow_info)
        db.session.commit()
        return 0, ''

    @classmethod
    def flow_stop(cls, flow_id):
        flow_info = FlowInfo.query.get(flow_id)
        project_id = flow_info.project_id
        roles_row = UserBusiness.query_json_by_id_and_project(g.userid, project_id)
        roles_list = roles_row[0]['role'] if roles_row else []
        roles = [role['name'] for role in roles_list]
        user_owner = flow_info.user_owner[1:-1].replace(' ', '').split(',')
        if str(g.userid) not in user_owner and not g.is_admin and 'owner' not in roles:
            raise OperationPermissionDeniedException
        flow_info.status = FlowInfo.STOP
        action = json.loads(flow_info.action)
        action['current_step_name'] = "已终止"
        flow_info.action = json.dumps(action)
        db.session.add(flow_info)
        db.session.commit()
        return 0, ''

    @classmethod
    def flow_permission(cls, flow_info, flow_user_list, result, flow_step_id, modifier):
        # 检查每一步的对应权限：由 permission_check: True 控制
        flow_config = cls.public_trpc.requests('get', '/public/config',
                                               {'module': 'flow_config', 'project_id': flow_info.project_id})

        flow_config = json.loads(flow_config)
        if flow_config and isinstance(flow_config, list) and isinstance(flow_config[0], dict):
            flow_config = flow_config[0]
        elif isinstance(flow_config, dict):
            pass
        else:
            raise CannotFindObjectException(f'flow config error with project id {flow_info.project_id}')

        if not flow_config.get('permission_check', False):
            return True

        users_all = dict(
            user_dev=flow_user_list[0],
            user_prod=flow_user_list[1],
            user_test=flow_user_list[2],
            user_owner=flow_user_list[3]
        )
        flow_step_base = FlowBase.query.get(flow_step_id)
        _flow_comment = json.loads(flow_step_base.comment)

        # 有权限的 group
        user_groups = _flow_comment.get(str(result))
        # 所有有权限的用户
        users_who_have_permissions = []
        for group in user_groups:
            users_who_have_permissions.extend(users_all.get(group, []))

        if modifier not in users_who_have_permissions:
            raise OperationPermissionDeniedException(f'当前用户没有此步骤的操作权限!')

    @classmethod
    def flow_next(cls, flow_id, _id, name, result, comment):
        modifier = g.userid if g.userid else None
        flow_info = FlowInfo.query.get(flow_id)
        if flow_info is None:
            return 101, '获取流程数据异常!'
        user_list = [flow_info.user_dev, flow_info.user_prod, flow_info.user_test, flow_info.user_owner]
        flag = True
        for us in range(len(user_list)):
            us = json.loads(user_list[us])
            if modifier in us:
                flag = False
        if flag:
            return 106, '非流程参与者，无法执行!'

        flow_base_list = flow_info.flow_base_list
        flow_base_list = flow_base_list.split(',')
        # list去掉非数字字符
        # [flow_base_list.remove(i) for i in flow_base_list if not isinstance(i, int)]
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        temp_flow_info = {
            'id': _id, 'name': name, 'result': result, 'comment': comment, 'user_id': g.userid,
            'user_name': g.nickname, 'creation_time': now_time
        }
        action = json.loads(flow_info.action)
        if str(_id) != action['current_step']:
            return 106, '流程异常！'
        current_step = action['current_step']
        if action['current_step'] not in flow_base_list:
            return 106, '当前流程不包含此步骤！'
        user_dev = json.loads(flow_info.user_dev)
        user_prod = json.loads(flow_info.user_prod)
        user_test = json.loads(flow_info.user_test)
        user_owner = json.loads(flow_info.user_owner)
        # board_config = Config.query.add_columns(Config.content.label('content')).filter(
        #     Config.module == 'tcloud',
        #     Config.module_type == 1).first()
        board_config = cls.public_trpc.requests('get', '/public/config', {'module': 'tcloud', 'module_type': 1})
        if not board_config:
            return 102, '获取配置失败'

        cls.flow_permission(flow_info, [user_dev, user_prod, user_test, user_owner], result, _id, modifier)

        if _id != int(flow_base_list[-1]):
            if result == '2':
                if flow_base_list.index(action['current_step']) >= 1:
                    if 3 in flow_base_list or '3' in flow_base_list:
                        current_step = '3'
                    else:
                        current_step = flow_base_list[0]
                else:
                    return 403, '第一步不可执行不通过操作!'
                    # current_step = flow_base_list[flow_base_list.index(action['current_step']) - 1]
            elif result == '1' or result == '3':
                current_step = flow_base_list[flow_base_list.index(action['current_step']) + 1]
                fbase = FlowBase.query.get(int(current_step))
                if fbase.is_send == 1:
                    text = '''[Tcloud - {}]流程已流转，请相关人员跟进
当前步骤：{}
URL：{}/project/{}/flow/detail/{}'''.format(flow_info.name, fbase.name, board_config,
                                           flow_info.project_id, flow_info.id)
                    flow_base_comment = json.loads(fbase.comment)
                    us = flow_base_comment['1']
                    us_li = []
                    if 'user_prod' in us:
                        us_li.extend(user_prod)
                    if 'user_test' in us:
                        us_li.extend(user_test)
                    if 'user_dev' in us:
                        us_li.extend(user_dev)
                    us_li = list(set(us_li))
                    notification.send_notification(us_li, text)
            else:
                current_app.logger.info("停留在当前步骤")
            action['process'] = int(
                str(int(flow_base_list.index(current_step) * 100) / float(len(flow_base_list))).split(".")[0][:2])
            fbase = FlowBase.query.get(int(current_step))
            action['current_step_name'] = fbase.name

        else:
            if result == '1' or result == '3':
                action['process'] = 100
                current_step = '0'
                action['current_step_name'] = '完成'
                flow_info.status = FlowInfo.FINISHED
                flow_info.end_time = now_time

                user_dev.extend(user_prod)
                user_dev.extend(user_test)
                user_dev.extend(user_owner)
                user_list = list(set(user_dev))
                user_nickname = User.query.add_columns(
                    User.nickname.label('nickname')).filter(User.id.in_(user_list)).all()
                user_list.append(modifier)

                temp = ''

                for ni in user_nickname:
                    temp = temp + ni.nickname + ','
                text = '''[Tcloud - {}]流程已完成
参与者: {}
创建者: {}
URL：{}/project/{}/flow/detail/{}'''.format(flow_info.name, temp[:-1], g.nickname, board_config,
                                           flow_info.project_id, flow_info.id)
                notification.send_notification(user_list, text)

        if current_step == '0':
            current_step = flow_base_list[-1]
        flow_base_st = FlowBase.query.get(current_step)
        flow_base_step = json.loads(flow_base_st.step)
        flow_base_comment = json.loads(flow_base_st.comment)
        flow_base_step_list = []
        if isinstance(flow_base_step, dict):
            for key, value in flow_base_step.items():
                temp_dict = {'step_tab_id': key, 'step_tab_name': value}
                if key in ['1', '3']:
                    temp_dict['step_tab_result'] = '会跳转到下一步'
                elif key in ['2']:
                    temp_dict['step_tab_result'] = '会跳转到流程第一步'
                else:
                    temp_dict['step_tab_result'] = '会停留在当前步骤'
                flist = flow_base_comment[key]
                flist_user = ["user_dev", "user_test", "user_prod", "user_owner"]
                flist_str = []
                if flist_user[0] in flist:
                    flist_str.extend(user_dev)
                if flist_user[1] in flist:
                    flist_str.extend(user_test)
                if flist_user[2] in flist:
                    flist_str.extend(user_prod)
                if flist_user[3] in flist:
                    flist_str.extend(user_owner)
                temp_user_owner = ''
                user_owner_nickname = User.query.add_columns(
                    User.nickname.label('nickname')).filter(User.id.in_(flist_str)).all()
                for ni in user_owner_nickname:
                    temp_user_owner = temp_user_owner + ni.nickname + ','
                temp_dict['step_tab_user'] = temp_user_owner[:-1]
                flow_base_step_list.append(temp_dict)
        else:
            for st in range(len(flow_base_step)):
                temp_dict = {}
                key = list(flow_base_step[st].keys())[0]
                value = list(flow_base_step[st].values())[0]
                temp_dict['step_tab_id'] = key
                temp_dict['step_tab_name'] = value
                if key in ['1', '3']:
                    temp_dict['step_tab_result'] = '会跳转到下一步'
                elif key in ['2']:
                    temp_dict['step_tab_result'] = '会跳转到流程第一步'
                else:
                    temp_dict['step_tab_result'] = '会停留在当前步骤'
                flist = flow_base_comment[key]
                flist_user = ["user_dev", "user_test", "user_prod", "user_owner"]
                flist_str = []
                if flist_user[0] in flist:
                    flist_str.extend(user_dev)
                if flist_user[1] in flist:
                    flist_str.extend(user_test)
                if flist_user[2] in flist:
                    flist_str.extend(user_prod)
                if flist_user[3] in flist:
                    flist_str.extend(user_owner)
                temp_user_owner = ''
                user_owner_nickname = User.query.add_columns(
                    User.nickname.label('nickname')).filter(User.id.in_(flist_str)).all()
                for ni in user_owner_nickname:
                    temp_user_owner = temp_user_owner + ni.nickname + ','
                temp_dict['step_tab_user'] = temp_user_owner[:-1]
                flow_base_step_list.append(temp_dict)

        action['step_tab'] = flow_base_step_list

        cls.flow_record_create(flow_id, _id, name, result, comment, flow_info.project_id, flow_info.version_id,
                               current_step)
        action['steps'].append(temp_flow_info)
        action['current_step'] = current_step
        flow_info.action = json.dumps(action)
        current_app.logger.info(flow_info.action)
        db.session.add(flow_info)
        db.session.commit()
        return 0, None

    @classmethod
    def flow_record_create(cls, flow_id, _id, name, result, comment, project_id, version_id, current_step):
        try:
            creator = g.userid if g.userid else None
            c = FlowRecord(
                flow_info_id=flow_id,
                creator=creator,
                step_id=_id,
                next_step_id=current_step,
                result=result,
                description=name,
                project_id=project_id,
                version_id=version_id,
                comment=comment,
            )
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 102

    @classmethod
    def flow_create(cls, name, flow_type, requirement_list, flow_assemble_id, priority, project_id, version_id, creator,
                    user_dev, user_prod, user_test, user_owner, action, weight, comment, platform, dependence):
        try:
            if flow_type == 1 and requirement_list == '':
                return 101, '数据填写有误！'
            is_repeat = FlowInfo.query.filter(FlowInfo.name == name, FlowInfo.status != FlowInfo.DISABLE).first()
            if is_repeat:
                return 103, '标题或名称重复'
            creator = g.userid if g.userid else creator
            flow_asse = FlowAssemble.query.get(flow_assemble_id)
            if flow_asse is None:
                return 101, []
            flow_base_list = flow_asse.flow_base_list
            flow_base_lists = flow_asse.flow_base_list.split(',')
            process = 0
            # list去掉非数字字符
            [flow_base_lists.remove(i) for i in flow_base_lists if not isinstance(int(i), int)]
            current_step_name = FlowBase.query.get(flow_base_lists[0]).name
            action = {
                'process': process, 'current_step': flow_base_lists[0],
                'current_step_name': current_step_name, 'steps': []
            }

            flow_base_st = FlowBase.query.get(flow_base_lists[0])
            flow_base_step = json.loads(flow_base_st.step)
            flow_base_comment = json.loads(flow_base_st.comment)
            flow_base_step_list = []
            for st in range(len(flow_base_step)):
                temp_dict = {}
                key = list(flow_base_step[st].keys())[0]
                value = list(flow_base_step[st].values())[0]
                temp_dict['step_tab_id'] = key
                temp_dict['step_tab_name'] = value
                if key in ['1', '3']:
                    temp_dict['step_tab_result'] = '会跳转到下一步'
                elif key in ['2']:
                    temp_dict['step_tab_result'] = '会跳转到流程第一步'
                else:
                    temp_dict['step_tab_result'] = '会停留在当前步骤'
                flist = flow_base_comment[key]
                flist_user = ["user_dev", "user_test", "user_prod", "user_owner"]
                flist_str = []
                if flist_user[0] in flist:
                    flist_str.extend(user_dev)
                if flist_user[1] in flist:
                    flist_str.extend(user_test)
                if flist_user[2] in flist:
                    flist_str.extend(user_prod)
                if flist_user[3] in flist:
                    flist_str.extend(user_owner)
                temp_user_owner = ''
                user_owner_nickname = User.query.add_columns(
                    User.nickname.label('nickname')).filter(User.id.in_(flist_str)).all()
                for ni in user_owner_nickname:
                    temp_user_owner = temp_user_owner + ni.nickname + ','
                temp_dict['step_tab_user'] = temp_user_owner[:-1]
                flow_base_step_list.append(temp_dict)

            action['step_tab'] = flow_base_step_list
            action = json.dumps(action)
            current_app.logger.info("creator:" + str(creator))
            c = FlowInfo(
                name=name,
                flow_type=flow_type,
                requirement_list=requirement_list,
                flow_assemble_id=flow_assemble_id,
                flow_base_list=flow_base_list,
                priority=priority,
                project_id=project_id,
                version_id=version_id,
                creator=creator,
                user_dev=str(user_dev),
                user_prod=str(user_prod),
                user_test=str(user_test),
                user_owner=str(user_owner),
                action=action,
                weight=weight,
                comment=comment,
                platform=str(platform),
                dependence=dependence
            )
            db.session.add(c)
            db.session.commit()
            temp_user_dev = ''
            user_dev_nickname = User.query.add_columns(
                User.nickname.label('nickname')).filter(User.id.in_(user_dev)).all()
            for ni in user_dev_nickname:
                temp_user_dev = temp_user_dev + ni.nickname + ','

            user_dev.extend(user_prod)
            user_dev.extend(user_test)
            user_dev.extend(user_owner)
            user_list = list(set(user_dev))

            user_nickname = User.query.add_columns(
                User.nickname.label('nickname')).filter(User.id.in_(user_list)).all()
            user_list.append(creator)
            temp = ''
            board_config = cls.public_trpc.requests('get', '/public/config', {'module': 'tcloud', 'module_type': 1})
            if not board_config:
                return 102, '获取配置失败'
            current_app.logger.info('board_config:' + str(board_config))
            project = Project.query.add_columns(Project.name).filter(Project.id == project_id).first()
            project_name = ''
            if project:
                project_name = project.name
            for ni in user_nickname:
                temp = temp + ni.nickname + ','
            text = '''[Tcloud - {}]流程已创建,流程第一步由开发人员：{} 操作
项目: {}
参与者: {}
创建者: {}
当前步骤：{}
URL：{}/project/{}/flow/detail/{}'''.format(name, temp_user_dev[:-1], project_name, temp[:-1], g.nickname,
                                           current_step_name,
                                           board_config,
                                           project_id, c.id)
            notification.send_notification(user_list, text)
            return 0, [{"flow_id": c.id}]
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, []

    @classmethod
    def flow_modify(cls, flow_id, name, priority, user_dev, user_prod, user_test, user_owner, weight, comment,
                    dependence):
        try:
            c = FlowInfo.query.get(flow_id)
            if c.status != FlowInfo.ACTIVE:
                return 107, '流程已完成，无法调整人员！'
            action = json.loads(c.action)
            current_step = action['current_step']
            flow_base_st = FlowBase.query.get(current_step)
            flow_base_step = json.loads(flow_base_st.step)
            flow_base_comment = json.loads(flow_base_st.comment)
            flow_base_step_list = []

            for st in range(len(flow_base_step)):
                temp_dict = {}
                key = list(flow_base_step[st].keys())[0]
                value = list(flow_base_step[st].values())[0]
                temp_dict['step_tab_id'] = key
                temp_dict['step_tab_name'] = value
                if key in ['1', '3']:
                    temp_dict['step_tab_result'] = '会跳转到下一步'
                elif key in ['2']:
                    temp_dict['step_tab_result'] = '会跳转到流程第一步'
                else:
                    temp_dict['step_tab_result'] = '会停留在当前步骤'
                flist = flow_base_comment[key]
                flist_user = ["user_dev", "user_test", "user_prod", "user_owner"]
                flist_str = []
                if flist_user[0] in flist:
                    flist_str.extend(user_dev)
                if flist_user[1] in flist:
                    flist_str.extend(user_test)
                if flist_user[2] in flist:
                    flist_str.extend(user_prod)
                if flist_user[3] in flist:
                    flist_str.extend(user_owner)
                temp_user_owner = ''
                user_owner_nickname = User.query.add_columns(
                    User.nickname.label('nickname')).filter(User.id.in_(flist_str)).all()
                for ni in user_owner_nickname:
                    temp_user_owner = temp_user_owner + ni.nickname + ','
                temp_dict['step_tab_user'] = temp_user_owner[:-1]
                flow_base_step_list.append(temp_dict)

            action['step_tab'] = flow_base_step_list
            c.name = name
            c.priority = priority
            c.user_dev = str(user_dev)
            c.user_prod = str(user_prod)
            c.user_test = str(user_test)
            c.user_owner = str(user_owner)
            c.action = json.dumps(action)
            c.weight = weight
            c.dependence = dependence
            db.session.add(c)
            db.session.commit()
            user_dev.extend(user_prod)
            user_dev.extend(user_test)
            user_dev.extend(user_owner)
            user_list = list(set(user_dev))
            user_nickname = User.query.add_columns(
                User.nickname.label('nickname')).filter(User.id.in_(user_list)).all()
            user_list.append(g.userid)
            temp = ''
            board_config = cls.public_trpc.requests('get', '/public/config', {'module': 'tcloud', 'module_type': 1})
            if not board_config:
                return 102, '获取配置失败'

            for ni in user_nickname:
                temp = temp + ni.nickname + ','
            text = '''[Tcloud - {}]流程标题修改或人员调整
参与者: {}
修改者: {}
URL：{}/project/{}/flow/detail/{}'''.format(name, temp[:-1], g.nickname, board_config, c.project_id, c.id)
            notification.send_notification(user_list, text)
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 106, None

    @classmethod
    @transfer2json('?id|!name|~step|!comment')
    def query_base_all_json(cls):
        ret = FlowBase.query.add_columns(
            FlowBase.id.label('id'), FlowBase.name.label('name'), FlowBase.step.label('step'),
            FlowBase.comment.label('comment'))
        ret = ret.order_by(FlowBase.id).all()
        return ret

    @classmethod
    @transfer2json('?id|!name')
    def query_base_part_json(cls):
        ret = FlowBase.query.add_columns(
            FlowBase.id.label('id'), FlowBase.name.label('name'))
        ret = ret.order_by(FlowBase.id).all()
        return ret

    @classmethod
    @transfer2json('?id|!name|!flow_base_list|!project_id|!weight|!comment')
    def query_assemble_all_json(cls):
        projectid = request.args.get('projectid')
        ret = FlowAssemble.query.add_columns(
            FlowAssemble.id.label('id'),
            FlowAssemble.name.label('name'),
            FlowAssemble.flow_base_list.label('flow_base_list'),
            # FlowAssemble.flow_asstype.label('flow_asstype'),
            FlowAssemble.project_id.label('project_id'),
            FlowAssemble.weight.label('weight'),
            FlowAssemble.comment.label('comment')
        )
        ret = ret.filter(FlowAssemble.status != FlowAssemble.DISABLE)
        if projectid:
            ret = ret.filter(FlowAssemble.project_id == projectid)
        ret = ret.order_by(desc(FlowAssemble.id)).all()
        return ret

    @classmethod
    def flow_add_dashboard(cls, project_id, start_date, end_date):
        open_issue_dashboard_ret = FlowInfo.query.add_columns(
            func.date_format(FlowInfo.creation_time, "%Y-%m-%d").label('creation_time'),
            func.count('*').label('count')
        ).filter(
            FlowInfo.project_id == project_id, FlowInfo.status != FlowInfo.DISABLE,
            FlowInfo.creation_time.between(start_date, end_date + " 23:59:59")).group_by(
            func.date_format(FlowInfo.creation_time, "%Y-%m-%d")).all()
        # flow_average_ti = cls.flow_average_time(project_id, start_date, end_date)
        flow_assemble_sum_ret = FlowInfo.query.outerjoin(
            FlowAssemble, FlowAssemble.id == FlowInfo.flow_assemble_id).add_columns(
            FlowAssemble.name.label('flow_assemble_name'),
            func.count('*').label('count')
        ).filter(
            FlowInfo.project_id == project_id, FlowInfo.status != FlowInfo.DISABLE,
            FlowInfo.creation_time.between(start_date, end_date + " 23:59:59")).group_by(
            FlowInfo.flow_assemble_id).all()

        flow_type_sum_ret = FlowInfo.query.add_columns(
            FlowInfo.flow_type.label('flow_type'),
            func.count('*').label('count')
        ).filter(
            FlowInfo.project_id == project_id, FlowInfo.status != FlowInfo.DISABLE,
            FlowInfo.creation_time.between(start_date, end_date + " 23:59:59")).group_by(
            FlowInfo.flow_type).all()

        flow_assemble_sum_ret = [
            dict(i)
            for i in map(lambda x: zip(('flow_assemble', 'count'), x),
                         zip([i.flow_assemble_name for i in flow_assemble_sum_ret],
                             [i.count for i in flow_assemble_sum_ret]))
        ]
        flow_type_sum_ret = [
            dict(i)
            for i in map(lambda x: zip(('flow_type', 'count'), x),
                         zip([i.flow_type for i in flow_type_sum_ret],
                             [i.count for i in flow_type_sum_ret]))
        ]
        for i in range(len(flow_type_sum_ret)):
            if flow_type_sum_ret[i]['flow_type'] == 1:
                flow_type_sum_ret[i]['flow_type'] = '版本需求'
            if flow_type_sum_ret[i]['flow_type'] == 2:
                flow_type_sum_ret[i]['flow_type'] = '搜索推荐'
            if flow_type_sum_ret[i]['flow_type'] == 3:
                flow_type_sum_ret[i]['flow_type'] = '问题修复'
            if flow_type_sum_ret[i]['flow_type'] == 4:
                flow_type_sum_ret[i]['flow_type'] = '临时需求'
            if flow_type_sum_ret[i]['flow_type'] == 5:
                flow_type_sum_ret[i]['flow_type'] = '优化'
            if flow_type_sum_ret[i]['flow_type'] == 6:
                flow_type_sum_ret[i]['flow_type'] = '紧急需求'

        flow_type_detail = cls.flow_type_json(project_id, start_date, end_date)

        end_flow_count = cls.get_end_flow_data(project_id, start_date, end_date)

        detail = [
            dict(
                flow_add=[
                    dict(i)
                    for i in map(lambda x: zip(('date', 'count'), x),
                                 zip([i.creation_time for i in open_issue_dashboard_ret],
                                     [i.count for i in open_issue_dashboard_ret]))
                ],
                # flow_average=flow_average_ti,
                flow_type_sum=flow_type_sum_ret,
                flow_assemble_sum=flow_assemble_sum_ret,
                flow_type_detail=flow_type_detail,
                end_flow_count=end_flow_count)
        ]
        return detail[0]

    @classmethod
    @transfer2json(
        '?id|!start_time|!end_time|~action|!flow_assemble_id|!flow_assemble_name')
    def flow_average_time_json(cls, project_id, start_date, end_date):
        return cls._query().filter(FlowInfo.project_id == project_id, FlowInfo.status == 2,
                                   FlowInfo.creation_time.between(start_date, end_date + " 23:59:59")).all()

    @classmethod
    @transfer2json(
        '?id|!start_time|!end_time|~action|!flow_assemble_id|!flow_assemble_name|!flow_base_list')
    def flow_type_average_time_json(cls, project_id, start_date, end_date, flow_type):
        return cls._query().filter(FlowInfo.project_id == project_id, FlowInfo.status == 2,
                                   FlowInfo.flow_assemble_id == flow_type,
                                   FlowInfo.creation_time.between(start_date, end_date + " 23:59:59")).all()

    @classmethod
    def flow_type_json(cls, project_id, start_date, end_date):
        # base_dict = {'1':'client','2':'server','3':'skiptest','4':'hotfix'}
        temp_dict = {}
        flow_dict = {}
        flow_base = cls.query_base_part_json()
        for fl in flow_base:
            temp_dict[str(fl['id'])] = fl['name']
        for flow_type_id in range(1, 6):
            flow_type_ret = cls.flow_type_average_time_json(project_id, start_date, end_date, flow_type_id)
            if flow_type_ret:
                list_temp = []
                for flow_type_re in flow_type_ret:
                    flow_base_list = flow_type_re['flow_base_list']
                    flow_base_list = flow_base_list.split(',')[::-1]
                    actions = flow_type_re['action']
                    steps = actions['steps'][::-1]
                    for i in range(len(flow_base_list) - 1):
                        for j in range(len(steps) - 1):
                            if str(steps[j]['id']) == str(flow_base_list[i]):
                                total_d1 = datetime.datetime.strptime(steps[j + 1]['creation_time'],
                                                                      '%Y-%m-%d %H:%M:%S')
                                for k in range(len(steps)):
                                    if str(steps[k]['id']) == str(flow_base_list[i + 1]):
                                        total_d1 = datetime.datetime.strptime(steps[k]['creation_time'],
                                                                              '%Y-%m-%d %H:%M:%S')
                                        break
                                total_d2 = datetime.datetime.strptime(steps[j]['creation_time'], '%Y-%m-%d %H:%M:%S')
                                if (total_d2 - total_d1).days == 0:
                                    steps[j]['time_diff'] = (total_d2 - total_d1).seconds
                                else:
                                    steps[j]['time_diff'] = (total_d2 - total_d1).days * 60 * 60 * 24 + (
                                            total_d2 - total_d1).seconds
                                list_temp.append({
                                    'id': steps[j]['id'], 'name': temp_dict[str(steps[j]['id'])],
                                    "time": int(steps[j]['time_diff'])
                                })
                                break
                df = pd.DataFrame(list_temp)
                result = df.groupby(['id', 'name']).sum()
                current_app.logger.info(flow_type_ret[0]['flow_assemble_name'] + "的个数：" + str(len(flow_type_ret)))
                li_1 = result.index.to_list()
                li_2 = result.values.tolist()
                for y in range(len(li_1)):
                    li_1[y] = li_1[y][1]
                for e in range(len(li_2)):
                    li_2[e] = format(li_2[e][0] / float(3600 * len(flow_type_ret)), '.2f')
                current_app.logger.info(json.dumps(dict(zip(li_1, li_2)), ensure_ascii=False))
                for r in range(len(li_2)):
                    # tem_list.append(dict(zip([li_1[r]], [li_2[r]])))
                    temp = [li_2[r], li_1[r]]
                    li_2[r] = temp
                current_app.logger.info(json.dumps(li_2, ensure_ascii=False))
                # flow_dict['flow_' + str(flow_type_id)] = tem_list
                flow_dict['flow_' + str(flow_type_id)] = [
                    dict(i)
                    for i in map(lambda x: zip(('time', 'name'), x),
                                 zip([i[0] for i in li_2],
                                     [i[1] for i in li_2]))
                ]
            else:
                flow_dict['flow_' + str(flow_type_id)] = []
        current_app.logger.info(json.dumps(flow_dict, ensure_ascii=False))

        return flow_dict

    @classmethod
    def flow_average_time(cls, project_id, start_date, end_date):
        ret = cls.flow_average_time_json(project_id, start_date, end_date)
        temp_data = {}
        for re in range(len(ret)):
            temp_dict = {}
            total_d1 = datetime.datetime.strptime(ret[re]['start_time'], '%Y-%m-%d %H:%M:%S')
            total_d2 = datetime.datetime.strptime(ret[re]['end_time'], '%Y-%m-%d %H:%M:%S')
            if (total_d2 - total_d1).days == 0:
                ret[re]['total_time'] = (total_d2 - total_d1).seconds
            else:
                ret[re]['total_time'] = (total_d2 - total_d1).days * 60 * 60 * 24 + (total_d2 - total_d1).seconds
            action_step = ret[re]['action']['steps']
            a = 0
            test_d2 = None
            test_d1 = None
            for ac in action_step:
                if ac['id'] == 3 and ac['result'] == '1':
                    test_d1 = datetime.datetime.strptime(ac['creation_time'], '%Y-%m-%d %H:%M:%S')
                    a = a + 1
                if ac['id'] == 4:
                    test_d2 = datetime.datetime.strptime(ac['creation_time'], '%Y-%m-%d %H:%M:%S')
                    a = a + 1
            if a >= 2:
                if (test_d2 - test_d1).days == 0:
                    ret[re]['test_time'] = (test_d2 - test_d1).seconds
                else:
                    ret[re]['test_time'] = (test_d2 - test_d1).days * 60 * 60 * 24 + (test_d2 - test_d1).seconds
                    ret[re]['test_time'] = (test_d2 - test_d1).seconds
            else:
                ret[re]['test_time'] = 0
            temp_dict['id'] = str(ret[re]['flow_assemble_id'])
            temp_dict['name'] = str(ret[re]['flow_assemble_name'])
            temp_dict['test_time'] = ret[re]['test_time']
            temp_dict['total_time'] = ret[re]['total_time']
            if temp_dict['name'] in temp_data:
                temp_data[temp_dict['name']][0] = temp_data[temp_dict['name']][0] + temp_dict['total_time']
                temp_data[temp_dict['name']][1] = temp_data[temp_dict['name']][1] + temp_dict['test_time']
                temp_data[temp_dict['name']][2] = temp_data[temp_dict['name']][2] + 1
            else:
                temp_data[temp_dict['name']] = [temp_dict['total_time'], temp_dict['test_time'], 1]

        list_data = []
        for key, value in temp_data.items():
            temp = {
                'name': key, 'total_time': format(value[0] / float(3600 * value[2]), '.2f'),
                'test_time': format(value[1] / float(3600 * value[2]), '.2f')
            }
            list_data.append(temp)
        return list_data

    @classmethod
    def format_xls(cls, data):
        """
        筛选出三种flow_base：'提测', '预发布', '上线'，以及需要的数据连表获取信息，格式化成表格所需数据
        :param data: flow_info以及数个表
        :return: result:格式化数据, tab_dict:列名
        """
        all_result = []
        tab_list = ['任务列表', 'Jira编号', 'Tcloud编号', '类型', '流程类型', '涉及端', '测试人员', '开发人员',
                    '开发负责人', '产品经理', '当前阶段', '测试状态', '流程状态', '提测', '预发布', '上线', '上线依赖', '备注']
        flow_base_dict = {3: '提测', 6: '预发布', 11: '上线'}
        flow_base_list = [value for key, value in flow_base_dict.items()]
        flow_assemble_result = FlowAssemble.query.add_columns(
            FlowAssemble.id,
            FlowAssemble.name
        ).all()
        requirement_result = Requirement.query.add_columns(
            Requirement.id,
            Requirement.jira_id
        ).all()
        requirement_dict = {rm.id: rm.jira_id for rm in requirement_result}
        flow_assemble_dict = {far.id: far.name for far in flow_assemble_result}
        tab_dict = {v: k for k, v in enumerate(tab_list)}
        # 选择几个大段来显示流程状态
        for index in range(1, len(data) + 1):
            result = {}
            l_data = data[index - 1]
            current_step_name = ''
            current_step = l_data['action']['current_step'] if 'action' in l_data else ''
            current_step_status = l_data['action']['current_step_name'] if 'action' in l_data else ''
            if 1 <= int(current_step) <= 4:
                current_step_name = '测试中'
            elif 5 <= int(current_step) <= 6:
                current_step_name = '测试完成'
            elif 7 <= int(current_step) <= 9:
                current_step_name = '预发布'
            elif int(current_step) == 10:
                current_step_name = '灰度发包'
            elif int(current_step) == 11:
                current_step_name = '待上线'
            elif int(current_step) == 15:
                current_step_name = '全量发包'
            elif 12 <= int(current_step) <= 16 or int(current_step) == 0:
                current_step_name = '已上线'

            assemble_type = flow_assemble_dict[l_data['flow_assemble_id']]

            # 目前前端是写死的类型
            flow_type_id = l_data['flow_type']
            flow_type = ''
            if flow_type_id == 1:
                flow_type = '版本需求'
            elif flow_type_id == 2:
                flow_type = '搜索推荐'
            elif flow_type_id == 3:
                flow_type = '问题修复'
            elif flow_type_id == 4:
                flow_type = '临时需求'
            elif flow_type_id == 5:
                flow_type = '优化'
            elif flow_type_id == 6:
                flow_type = '紧急需求'

            platform = l_data['platform']

            projectid = request.args.get('projectid')
            flow_config = cls.public_trpc.requests('get', '/public/flow/', {'projectid': projectid})
            if flow_config:
                new_platform = []
                flow_platform = flow_config['platform']
                for platform_value in platform:
                    if platform_value in flow_platform:
                        new_platform.append(flow_platform.get(platform_value))
                platform = ', '.join(new_platform)

            jira_ids = []
            requirement_list = l_data['requirement_list'].split(',')
            for rl in requirement_list:
                if rl.isdigit() and requirement_dict.get(int(rl)):
                    jira_ids.append(requirement_dict.get(int(rl)))
            jira_id = ','.join(jira_ids)

            if l_data['action']['steps']:
                for step in l_data['action']['steps']:
                    # 步骤16完成结束后，当前步骤id会改为0
                    if step['id'] in flow_base_dict.keys() and (int(step['id']) <= int(current_step)
                                                                or int(current_step) == 0):
                        if step['result'] == '1' or step['result'] == '3':
                            result[tab_dict[flow_base_dict[step['id']]]] = step['creation_time']
                    # Hotfix(需QA验证) 的提测时间取步骤4：功能测试时间
                    elif l_data['flow_assemble_id'] == 5 and int(step['id']) == 4:
                        if step['result'] == '1' or step['result'] == '3':
                            result[tab_dict['提测']] = step['creation_time']

            # 当流程类型为SkipTest和HotFix时，提测时间改为项目的创建时间，之所以是start_time，是因为在搜索的时候把creation_time改成start_time的label
            if l_data['flow_assemble_id'] in (3, 4):
                result[tab_dict['提测']] = l_data['start_time']

            if l_data['status'] == 0:
                status_name = '进行中'
            elif l_data['status'] == 2:
                status_name = '已完成'
            elif l_data['status'] == 3:
                current_step_name = '已回退'
                status_name = '已终止'
            else:
                status_name = ''

            user_dev_list = [i['user_name'] for i in l_data['user_dev']] if 'user_dev' in l_data else []
            user_prod_list = [i['user_name'] for i in l_data['user_prod']] if 'user_prod' in l_data else []
            user_test_list = [i['user_name'] for i in l_data['user_test']] if 'user_test' in l_data else []
            user_owner_list = [i['user_name'] for i in l_data['user_owner']] if 'user_owner' in l_data else []
            result[tab_dict['任务列表']] = l_data['name']
            result[tab_dict['Jira编号']] = jira_id
            result[tab_dict['Tcloud编号']] = l_data['id']
            result[tab_dict['测试人员']] = ','.join(user_test_list)
            result[tab_dict['开发人员']] = ','.join(user_dev_list)
            result[tab_dict['开发负责人']] = ','.join(user_owner_list)
            result[tab_dict['产品经理']] = ','.join(user_prod_list)
            result[tab_dict['当前阶段']] = current_step_status
            result[tab_dict['测试状态']] = current_step_name
            result[tab_dict['流程状态']] = status_name
            result[tab_dict['类型']] = flow_type
            result[tab_dict['流程类型']] = assemble_type
            result[tab_dict['涉及端']] = platform
            result[tab_dict['上线依赖']] = l_data['dependence']

            all_result.append(result)
        tab_dict = {v: k + '时间' if k in flow_base_list else k for k, v in tab_dict.items()}
        return all_result, tab_dict

    @classmethod
    def gen_xls(cls, all_data, tab_dict):
        """
        写入到excel中  并上传到oss上
        :param all_data: 格式化数据
        :param tab_dict: 列名
        :return: oss的url
        """
        workbook = xlwt.Workbook()

        alignment = xlwt.Alignment()
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        alignment.horz = xlwt.Alignment.HORZ_LEFT
        alignment.vert = xlwt.Alignment.VERT_TOP

        style = xlwt.XFStyle()
        style.alignment = alignment
        sheet = workbook.add_sheet('流程列表', cell_overwrite_ok=True)

        fnt = Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
        fnt.name = u'宋体'
        style.font = fnt
        for key, value in tab_dict.items():
            sheet.write(0, key, value, style)
            if key == 0:
                sheet.col(key).width = 256 * 30
            if key == 5:
                sheet.col(key).width = 256 * 15
            elif key in (13, 14, 15):
                sheet.col(key).width = 256 * 20
            elif key == 16:
                sheet.col(key).width = 256 * 50
            else:
                sheet.col(key).width = 256 * 10

        for index, data in enumerate(all_data):
            for k, v in data.items():
                sheet.write(index + 1, k, v, style)

        path = os.getcwd()
        dir_path = path + '/excel'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        user_id = request.args.get('user_id')
        if not user_id:
            user_id = 'nobody'
        if user_id:
            dir_path = dir_path + '/{}'.format(user_id)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            file_path = dir_path + '/flow.xls'
            workbook.save(file_path)
            url = oss_upload(path=file_path, project_name='flow_export',
                             file_name=str(int(time.time())) + '.xls', user_id=user_id)
            return url
        else:
            return ''

    @classmethod
    def flow_export(cls):
        data, tab_dict = cls.flow_get_rows()
        url = cls.gen_xls(data, tab_dict)
        return {"url": url}

    @classmethod
    def flow_info_by_users(cls, users, project_id):
        """
        根据用户列表返回每个用户当前进行中的流程 和 今天结束的流程
        :return: data
        """
        if not users or not project_id:
            return []
        results = []
        user_list = users.split(',')
        user_result = User.query.add_columns(
            User.id,
            User.nickname
        ).all()
        user_dict = {ur.id: ur.nickname for ur in user_result}
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        for user in user_list:
            resource_dict = {
                'user_id': user, 'user_name': user_dict[int(user)],
                'flows': {'active': [], 'finished': []},
                'total_active': 0,
                'total_finished': 0
            }
            flow_info_active_results = cls.query_all_jsons_kwargs(user_id=user, project_id=project_id, status=0)
            for fiar in flow_info_active_results:
                if 'action' in fiar and 'current_step_name' in fiar['action']:
                    current_step_name = fiar['action']['current_step_name']
                else:
                    current_step_name = ''
                resource_dict['flows']['active'].append({
                    'id': fiar['id'], 'name': fiar['name'],
                    'step': current_step_name
                })
            flow_info_finished_results = cls.query_all_jsons_kwargs(user_id=user, project_id=project_id, status=2,
                                                                    end_day=today_date)
            for fifr in flow_info_finished_results:
                resource_dict['flows']['finished'].append({'id': fifr['id'], 'name': fifr['name']})
            resource_dict['total_active'] = len(resource_dict['flows']['active'])
            resource_dict['total_finished'] = len(resource_dict['flows']['finished'])
            results.append(resource_dict)

        return results

    @classmethod
    def export_flow_info_by_users(cls, users, project_id):
        if not users or not project_id:
            return []
        results = []
        user_list = users.split(',')
        user_result = User.query.add_columns(
            User.id,
            User.nickname
        ).all()
        user_dict = {ur.id: ur.nickname for ur in user_result}
        for user in user_list:
            resource_dict = {
                'user_name': user_dict[int(user)],
                'flows': {'active': []},
            }
            flow_info_active_results = cls.query_all_jsons_kwargs(user_id=user, project_id=project_id, status=0)
            for fiar in flow_info_active_results:
                if 'action' in fiar and 'current_step_name' in fiar['action']:
                    current_step_name = fiar['action']['current_step_name']
                else:
                    current_step_name = ''
                resource_dict['flows']['active'].append({
                    'id': fiar['id'], 'name': fiar['name'],
                    'step': current_step_name
                })
            results.append(resource_dict)

        return results

    @classmethod
    def export_resource(cls, users, project_id):
        result = cls.export_flow_info_by_users(users, project_id)

        rows = []
        for r in result:
            for flow in r['flows']['active']:
                if flow:
                    row = [r['user_name'], str(flow['id']), flow['step'], flow['name']]
                    rows.append(row)

        workbook = xlwt.Workbook()

        alignment = xlwt.Alignment()
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        alignment.horz = xlwt.Alignment.HORZ_LEFT
        alignment.vert = xlwt.Alignment.VERT_TOP

        style = xlwt.XFStyle()
        style.alignment = alignment
        sheet = workbook.add_sheet('流程资源', cell_overwrite_ok=True)

        fnt = Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
        fnt.name = u'宋体'
        style.font = fnt
        sheet.col(0).width = 256 * 10
        sheet.col(1).width = 256 * 10
        sheet.col(2).width = 256 * 15
        sheet.col(3).width = 256 * 40

        sheet.write(0, 0, '用户')
        sheet.write(0, 1, '流程ID')
        sheet.write(0, 2, '当前阶段')
        sheet.write(0, 3, '标题')

        for row_index, row in enumerate(rows):
            if row:
                for line_index, line in enumerate(row):
                    sheet.write(row_index + 1, line_index, line)

        if not os.path.exists(TCLOUD_FILE_TEMP_PATH):
            os.mkdir(TCLOUD_FILE_TEMP_PATH)

        dir_path = f'{TCLOUD_FILE_TEMP_PATH}/flow'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        user_id = request.args.get('user_id')
        if not user_id:
            user_id = 'nobody'
        if user_id:
            dir_path = dir_path + '/{}'.format(user_id)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            file_path = dir_path + '/resource.xls'
            workbook.save(file_path)
            url = oss_upload(path=file_path, project_name='resource_export',
                             file_name=str(int(time.time())) + '.xls', user_id=user_id)
            return 0, url
        else:
            return 101, ''

    @classmethod
    def flow_source_add(cls, project_id, user_ids):
        try:
            creator = g.userid if g.userid else None
            ret = FlowSource.query.filter(FlowSource.project_id == project_id, FlowSource.creator == creator).first()
            if ret:
                ret.user_ids = user_ids
                db.session.add(ret)
                db.session.commit()
            else:
                c = FlowSource(
                    project_id=project_id,
                    creator=creator,
                    user_ids=user_ids,
                    source_type=1,
                )
                db.session.add(c)
                db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 102

    @classmethod
    @transfer2json('?id|!project_id|!creator|!user_ids')
    def flow_source_get(cls, project_id, user_id):
        ret = FlowSource.query.add_columns(
            FlowSource.id.label('id'),
            FlowSource.project_id.label('project_id'),
            FlowSource.creator.label('creator'),
            FlowSource.user_ids.label('user_ids')).filter(FlowSource.project_id == project_id,
                                                          FlowSource.creator == user_id).all()

        return ret

    @classmethod
    def get_end_flow_data(cls, project_id, start_date, end_date):
        user_infos = cls.user_trpc.requests(method='get', path='/user/projectandrole',
                                            query={'project_id': project_id, 'role_id': 3})
        data_temp = {
            user.get('userid'): dict(
                nickname=user.get('nickname'),
                count=0
            ) for user in user_infos
        }
        end_flows = FlowInfo.query.add_columns(
            FlowInfo.user_test).filter(
            FlowInfo.status == FlowInfo.FINISHED, FlowInfo.end_time.between(start_date, end_date + " 23:59:59"),
            FlowInfo.project_id == project_id
        ).all()
        testers = list(data_temp.keys())
        for flow in end_flows:
            flow_testers = json.loads(flow.user_test) if flow.user_test is not None else []
            for tester in flow_testers:
                if tester in testers:
                    data_temp.get(tester)['count'] += 1

        return list(data_temp.values())
