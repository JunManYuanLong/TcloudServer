from apps.extention.settings import config

if config.SERVER_ENV != 'dev':
    from gevent import monkey

    monkey.patch_all()
else:
    pass

from apps.extention.views.cidata import cidata
from apps.extention.views.tool import tool
from library.api.tFlask import tflask


def create_app():
    app = tflask(config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(tool, url_prefix='/v1/tool')
    app.register_blueprint(cidata, url_prefix='/v1/cidata')


if __name__ == '__main__':
    create_app().run(port=config.PORT)
