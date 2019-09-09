from apps.flow.settings import config

if config.SERVER_ENV != 'dev':
    from gevent import monkey

    monkey.patch_all()
else:
    pass

from apps.flow.views.deploy import deploy
from apps.flow.views.flow import flow
from library.api.tFlask import tflask


def create_app():
    app = tflask(config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(flow, url_prefix="/v1/flow")
    app.register_blueprint(deploy, url_prefix="/v1/deploy")


if __name__ == '__main__':
    create_app().run(port=config.PORT)
