from contextlib import contextmanager
from datetime import datetime

# from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy
# from redis import StrictRedis

from library.api.exceptions import SaveObjectException
# from public_config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD


class SQLAlchemy(BaseSQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise SaveObjectException()


# mysql数据库
db = SQLAlchemy()

# redis
# t_redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)

# 缓存，依赖redis
# cache = Cache(
#     config={
#         'CACHE_TYPE': 'redis',
#         'CACHE_REDIS_HOST': REDIS_HOST,
#         'CACHE_REDIS_PORT': REDIS_PORT,
#         'CACHE_REDIS_PASSWORD': REDIS_PASSWORD,
#         'CACHE_REDIS_DB': REDIS_DB
#     })


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
