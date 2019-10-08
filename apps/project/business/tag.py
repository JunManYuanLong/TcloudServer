from flask import request, g, current_app
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from apps.project.models.tag import Tag
from library.api.db import db
from library.api.exceptions import SaveObjectException, RemoveObjectException, CannotFindObjectException
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
            Tag.reference_nums.label('reference_nums')
        )

    @classmethod
    def filter_query(cls):
        tag = request.args.get('tag')
        project_id = request.args.get('project_id')
        ret = cls._query().filter(Tag.status == Tag.ACTIVE)
        if project_id:
            ret = ret.filter(Tag.project_id == project_id)
        if tag:
            ret = ret.filter(Tag.tag.like(f'%{tag}%'))
        return ret

    @classmethod
    def create(cls, tag, project_id, description):
        try:
            creator = g.userid if g.userid else None
            ret = Tag.query.filter(Tag.tag == tag).first()
            if ret:
                if ret.status == Tag.DISABLE:
                    with db.auto_commit():
                        ret.status = Tag.ACTIVE
                        ret.creator = creator
                        db.session.add(ret)
                    return 0
                else:
                    raise SaveObjectException('存在相同名称的标签')
            else:
                task = Tag(
                    tag=tag,
                    project_id=project_id,
                    description=description,
                    creator=creator
                )
                db.session.add(task)
                db.session.commit()
                return 0
        except Exception as e:
            current_app.logger.error(str(e))
            raise SaveObjectException

    @classmethod
    def update(cls, tag_id, tag_name, description):
        tag = Tag.query.get(tag_id)
        if not tag:
            raise CannotFindObjectException
        ret = Tag.query.filter(Tag.tag == tag_name, Tag.project_id == g.projectid, Tag.id != tag_id).first()
        if ret:
            raise SaveObjectException('存在相同名称的标签')
        tag.tag = tag_name
        tag.description = description
        tag.modifier = g.userid
        with db.auto_commit():
            db.session.add(tag)
        return 0

    @classmethod
    @transfer2json('?id|!tag|!description|!reference_nums')
    def gain_tag(cls):
        project_id = request.args.get('project_id')
        ret = cls._query().filter(Tag.status != Tag.DISABLE)
        if project_id:
            ret = ret.filter(Tag.project_id == project_id)
        ret = ret.order_by(desc(Tag.id)).all()
        return ret

    @classmethod
    @transfer2json('?id|!tag|!description|!reference_nums', ispagination=True)
    def paginate_data(cls, page_size=None, page_index=None):
        query = cls.filter_query().order_by(desc(Tag.id))
        count = query.count()
        if page_size and page_index:
            query = query.limit(int(page_size)).offset((int(page_index) - 1) * int(page_size))
        data = query.all()
        return data, count

    @classmethod
    def delete(cls, tag_id):
        try:
            tag = Tag.query.get(tag_id)
            if tag is None:
                raise CannotFindObjectException
            if tag.reference_nums > 0:
                raise RemoveObjectException('有关联的项目，不可删除')
            tag.status = tag.DISABLE
            db.session.add(tag)
            db.session.commit()
            return 0
        except SQLAlchemyError:
            return 106

    @classmethod
    def less_reference(cls, tags):
        if tags:
            tag_list = tags.split(',')
            session_list = []
            for tagid in tag_list:
                tag = Tag.query.get(tagid)
                if tag is None:
                    continue
                if tag.reference_nums > 0:
                    tag.reference_nums -= 1
                    session_list.append(tag)
            if session_list:
                db.session.add_all(session_list)
                db.session.commit()

    @classmethod
    def add_reference(cls, tags):
        if tags:
            tag_list = tags.split(',')
            session_list = []
            for tagid in tag_list:
                tag = Tag.query.get(tagid)
                if tag is None:
                    continue
                tag.reference_nums += 1
                session_list.append(tag)
            if session_list:
                db.session.add_all(session_list)
                db.session.commit()

    @classmethod
    def change_reference(cls, old_tags, new_tags):
        cls.less_reference(old_tags)
        cls.add_reference(new_tags)
