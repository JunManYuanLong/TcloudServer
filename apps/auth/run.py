from apps.auth.settings import config

if config.SERVER_ENV != 'dev':
    from gevent import monkey

    monkey.patch_all()
else:
    pass

from apps.auth.views.ability import ability
from apps.auth.views.feedback import feedback
from apps.auth.views.roles import role
from apps.auth.views.track import track
from apps.auth.views.users import user
from apps.auth.views.wxlogin import wxlogin
from library.api.tFlask import tflask


def create_app():
    app = tflask(config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(user, url_prefix="/v1/user")
    app.register_blueprint(track, url_prefix="/v1/track")
    app.register_blueprint(role, url_prefix="/v1/role")
    app.register_blueprint(ability, url_prefix="/v1/ability")
    app.register_blueprint(feedback, url_prefix="/v1/feedback")
    app.register_blueprint(wxlogin, url_prefix="/v1/wxlogin")


if __name__ == '__main__':
    create_app().run(port=config.PORT)
