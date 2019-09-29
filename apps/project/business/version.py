import time

from flask import request, g, current_app
from sqlalchemy import desc, func
from sqlalchemy.orm import aliased

from apps.auth.models.users import User
from apps.project.models.version import Version
from library.api.db import db
from library.api.exceptions import SaveObjectException
from library.api.transfer import transfer2json, slicejson
from library.trpc import Trpc


class VersionBusiness(object):
    user_trpc = Trpc('auth')

    @classmethod
    def project_permission(cls, pid=None, id=None):
        project_id = cls.user_trpc.requests('get', '/user/userbindproject', {'userid': g.userid})
        if g.is_admin:
            return 0
        if pid:
            return 0 if pid in project_id else 1
        else:
            ret = Version.query.add_columns(Version.project_id.label('projectid')).filter(Version.id == id).first()
            return 0 if ret.projectid in project_id else 1

    @classmethod
    def _query(cls):
        user_creator = aliased(User)

        return Version.query.outerjoin(
            user_creator, user_creator.id == Version.creator).add_columns(
            Version.id.label('id'),
            Version.title.label('title'),
            Version.project_id.label('project_id'),
            func.date_format(Version.creation_time, "%Y-%m-%d").label('creation_time'),
            func.date_format(Version.start_time, "%Y-%m-%d").label('start_time'),
            func.date_format(Version.end_time, "%Y-%m-%d").label('end_time'),
            func.date_format(Version.publish_time, "%Y-%m-%d").label('publish_time'),
            Version.creator.label('creator'),
            Version.publish_status.label('publish_status'),
            Version.status.label('status'),
            Version.description.label('description'),
            Version.comment.label('comment'),
            Version.weight.label('weight'),
            user_creator.id.label('creator_id'),
            user_creator.nickname.label('creator_name'),

        )

    @classmethod
    @slicejson([
        'creator|id|name|creator_id|creator_name'])
    @transfer2json(
        '?id|!title|!project_id|!creation_time|!start_time|!end_time|!publish_time|!publish_status|!status|'
        '!description|!comment|@creator_id|@creator_name')
    def query_all_json(cls):
        projectid = request.args.get('projectid')
        versionid = request.args.get('versionid')
        publish_status = request.args.get('publishstatus')
        ret = cls._query().filter(Version.status != Version.DISABLE)
        if projectid:
            ret = ret.filter(Version.project_id == projectid)
        if versionid:
            ret = ret.filter(Version.version == versionid)
        if publish_status:
            ret = ret.filter(Version.publish_status == publish_status)
        ret = ret.order_by(desc(Version.id)).all()
        return ret

    @classmethod
    @slicejson(['creator|id|name|creator_id|creator_name'])
    @transfer2json(
        '?id|!title|!project_id|!creation_time|!start_time|!end_time|!publish_time|!publish_status|!status|'
        '!description|!comment|@creator_id|@creator_name')
    def query_by_id(cls, versionid):
        ret = cls._query().filter(Version.status != Version.DISABLE,
                                  Version.id == versionid).all()
        return ret

    @classmethod
    def version_delete(cls, versionid):
        version = Version.query.get(versionid)
        version.status = Version.DISABLE
        db.session.add(version)
        db.session.commit()
        return 0

    @classmethod
    def version_publish(cls, versionid):
        version = Version.query.get(versionid)
        if version is None:
            return 101
        version.publish_status = Version.IS_PUBLISH
        version.publish_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(time.time()))
        db.session.add(version)
        db.session.commit()
        return 0

    @classmethod
    def version_create(cls, title, project_id, start_time, end_time, description, creator=None):
        ret = Version.query.filter_by(title=title, project_id=project_id, status=Version.ACTIVE).first()
        if ret:
            raise SaveObjectException('存在相同名称的版本')

        creator = g.userid if creator is None else creator
        current_app.logger.info("creator:" + str(creator))
        c = Version(
            title=title,
            project_id=project_id,
            start_time=start_time,
            end_time=end_time,
            creator=creator,
            description=description,
        )
        db.session.add(c)
        db.session.commit()
        mid = c.id
        c.version_number = 'TC' + str(mid)
        db.session.add(c)
        db.session.commit()
        return 0

    @classmethod
    def version_modify(cls, versionid, title, start_time, end_time, description):
        c = Version.query.get(versionid)

        ret = Version.query.filter_by(title=title,
                                      status=Version.ACTIVE,
                                      project_id=c.project_id).filter(Version.id != versionid).first()
        if ret:
            raise SaveObjectException('存在相同名称的版本')

        c.title = title,
        c.start_time = start_time,
        c.end_time = end_time,
        c.description = description,
        db.session.add(c)
        db.session.commit()
        return 0
