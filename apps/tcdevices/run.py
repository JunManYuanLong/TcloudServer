from apps.tcdevices.settings import config

if config.SERVER_ENV != 'dev':
    from gevent import monkey

    monkey.patch_all()
else:
    pass

from apps.tcdevices.views.tcDevices import tcdevices
from library.api.tFlask import tflask


def create_app():
    app = tflask(config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(tcdevices, url_prefix="/v1/tcdevices")


if __name__ == '__main__':
    create_app().run(port=config.PORT)
