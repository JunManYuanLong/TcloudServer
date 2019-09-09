from flask import current_app
from sqlalchemy import desc

from apps.auth.models.ability import Ability
from apps.auth.models.roles import Role, RoleBindAbility
from library.api.db import db
from library.api.transfer import slicejson, transfer2json


class RoleBusiness(object):
    @classmethod
    def _query(cls):
        return Role.query.outerjoin(
            RoleBindAbility, RoleBindAbility.role_id == Role.id).outerjoin(
            Ability, Ability.id == RoleBindAbility.ability_id).add_columns(
            Role.id.label('id'),
            Role.name.label('name'),
            Role.comment.label('comment'),
            Role.status.label('status'),
            Role.weight.label('weight'),
            Ability.id.label('ability_id'),
            Ability.name.label('ability_name'),

        )

    @classmethod
    @slicejson(['ability|id|name|ability_id|ability_name'])
    @transfer2json('?id|!name|!comment|!status|!weight|@ability_id|@ability_name')
    def query_all_json(cls, limit, offset):
        return cls._query().filter(Role.status == Role.ACTIVE).order_by(desc(Role.id)).limit(limit).offset(
            offset).all()

    @classmethod
    @slicejson(['ability|id|name|ability_id|ability_name'])
    @transfer2json('?id|!name|!comment|!status|!weight|@ability_id|@ability_name')
    def query_some_json(cls, limit, offset):
        return cls._query().filter(Role.status == Role.ACTIVE, Role.id != 1).order_by(desc(Role.id)).limit(
            limit).offset(
            offset).all()

    @classmethod
    @transfer2json('?id|!name|!comment|!status|!weight')
    def query_by_id(cls, roleid):
        return cls._query().filter(Role.status == Role.ACTIVE,
                                   Role.id == roleid).order_by(
            desc(Role.weight)).all()

    @classmethod
    def create(cls, name, comment, ability_ids):
        try:
            ret = Role.query.filter(Role.name == name, Role.status != Role.DISABLE).first()
            if ret:
                return 103, None
            r = Role(name=name,
                     comment=comment)
            db.session.add(r)
            db.session.commit()
            if ability_ids:
                cls.bind_abilities(r.id, ability_ids)
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def delete(cls, roleid):
        try:
            r = Role.query.get(roleid)
            r.status = Role.DISABLE
            db.session.add(r)
            [db.session.delete(item) for item in RoleBindAbility.query.filter_by(role_id=roleid).all()]
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 105, str(e)

    @classmethod
    def modify(cls, _id, name, comment, ability_ids):
        try:
            ret = Role.query.filter(Role.name == name, Role.status != Role.DISABLE, Role.id != _id).first()
            if ret:
                return 103, None
            r = Role.query.get(_id)
            # 不能修改角色名称
            # r.name = name
            r.comment = comment
            cls.bind_abilities(_id, ability_ids)
            db.session.add(r)
            db.session.commit()
            return 0, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            return 102, str(e)

    @classmethod
    def bind_abilities(cls, _id, ability_ids):
        try:
            [db.session.delete(item) for item in RoleBindAbility.query.filter_by(role_id=_id).all()]
            if ability_ids:
                [db.session.add(RoleBindAbility(role_id=_id, ability_id=abilityid)) for abilityid in ability_ids]
            db.session.commit()
            return 0, None
        except Exception as e:
            current_app.logger.error(str(e))
            return 102, str(e)
