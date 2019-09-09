from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy

from library.api.exceptions import SaveObjectException


class SQLAlchemy(BaseSQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise SaveObjectException()


db = SQLAlchemy()


# t_redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)


class EntityModel(db.Model):
    __abstract__ = True

    __table_args__ = (
        dict(
            mysql_engine='InnoDB',
            mysql_charset='utf8',
        )
    )

    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime, default=datetime.now)
    modified_time = db.Column(db.TIMESTAMP,
                              nullable=False,
                              default=db.func.current_timestamp())

    @classmethod
    def gets(cls, ids):
        return cls.query.filter(cls.id.in_(ids)).all()


class EntityWithNameModel(EntityModel):
    __abstract__ = True

    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.name.encode('utf-8')

    def __unicode__(self):
        return self.name
