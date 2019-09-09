from flask import request, g, current_app
from sqlalchemy import desc, func

from apps.auth.models.feedback import Feedback
from apps.auth.models.users import User
from library.api.db import db
from library.api.transfer import transfer2json


class FeedbackBusiness(object):

    @classmethod
    def _query(cls):
        return Feedback.query.outerjoin(User, User.id == Feedback.creator).add_columns(
            Feedback.id.label('id'),
            Feedback.contact.label('contact'),
            Feedback.comment.label('comment'),
            func.date_format(Feedback.creation_time, "%Y-%m-%d").label('creation_time'),
            User.id.label('creator_id'),
            User.nickname.label('creator_name'),
        )

    @classmethod
    @transfer2json('?id|!contact|!comment|!creation_time|!creator_id|!creator_name')
    def query_all_json(cls):
        userid = request.args.get('userid')
        ret = cls._query().filter(Feedback.status != Feedback.DISABLE)
        if userid:
            ret = ret.filter(Feedback.creator == userid)
        ret = ret.order_by(desc(Feedback.id)).all()
        return ret

    @classmethod
    @transfer2json('?id|!contact|!comment|!creation_time|!creator_id|!creator_name')
    def query_by_id(cls, feedback_id):
        ret = cls._query().filter(Feedback.status != Feedback.DISABLE, Feedback.id == feedback_id).all()
        return ret

    @classmethod
    def feedback_delete(cls, feedback_id):
        version = Feedback.query.get(feedback_id)
        version.status = Feedback.DISABLE
        db.session.add(version)
        db.session.commit()
        return 0

    @classmethod
    def feedback_create(cls, contact, comment):
        try:
            creator = g.userid if g.userid else None
            c = Feedback(
                contact=contact,
                comment=comment,
                creator=creator,
            )
            db.session.add(c)
            db.session.commit()
            return 0
        except Exception as e:
            current_app.logger.error(str(e))
            return 102
