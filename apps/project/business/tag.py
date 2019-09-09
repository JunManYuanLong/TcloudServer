from flask import request, g, current_app
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from apps.project.business.tasks import TaskBusiness
from apps.project.models.tag import Tag
from library.api.db import db
from library.api.transfer import transfer2json


class TagBusiness(object):

    @classmethod
    def _query(cls):
        return Tag.query.add_columns(
            Tag.id.label('id'),
            Tag.status.label('status'),
            Tag.tag.label('tag'),
            Tag.project_id.label('project_id'),
            Tag.creator.label('creator'),
            Tag.description.label('description'),
            Tag.tag_type.label('tag_type')
        )

    @classmethod
    def create(cls, tag, project_id, description, tag_type):
        try:
            creator = g.userid if g.userid else None

            task = Tag(
                tag=tag,
                project_id=project_id,
                description=description,
                tag_type=tag_type,
                creator=creator,
            )
            db.session.add(task)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 102

    @classmethod
    @transfer2json('?id|!tag')
    def gain_tag(cls):
        project_id = request.args.get('project_id')
        tag_type = request.args.get('tag_type')
        ret = cls._query().filter(Tag.status != Tag.DISABLE)
        if project_id:
            ret = ret.filter(Tag.project_id == project_id)
        if tag_type:
            ret = ret.filter(Tag.tag_type == tag_type)

        ret = ret.order_by(desc(Tag.id)).all()
        return ret

    @classmethod
    @transfer2json('?id|!tag')
    def judage_tag(cls, project_id, tag_type):
        ret = cls._query().filter(Tag.status != Tag.DISABLE)
        if project_id:
            ret = ret.filter(Tag.project_id == project_id)
        if tag_type:
            ret = ret.filter(Tag.tag_type == tag_type)
        ret = ret.order_by(desc(Tag.id)).all()

        return ret

    @classmethod
    def delete(cls, id, project_id, tag_type):
        try:
            if tag_type:
                if int(tag_type) == 2 and TaskBusiness.judge_tag_include(str(id), project_id):
                    # 查询该字段是否在task存在，若存在则不能删除
                    return 106
            tag = Tag.query.get(id)
            tag.status = tag.DISABLE
            db.session.add(tag)
            db.session.commit()
            return 0
        except SQLAlchemyError:
            return 106
