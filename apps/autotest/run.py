from apps.autotest.settings import config

if config.SERVER_ENV != 'dev':
    from gevent import monkey

    monkey.patch_all()
else:
    pass

from apps.autotest.views.datashow import datashow
from apps.autotest.views.monkey import monkey
from library.api.tFlask import tflask


def create_app():
    app = tflask(config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(monkey, url_prefix='/v1/monkey')
    app.register_blueprint(datashow, url_prefix='/v1/datashow')


if __name__ == '__main__':
    create_app().run(port=config.PORT)
