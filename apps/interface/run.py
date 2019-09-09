from apps.interface.settings import config

if config.SERVER_ENV != 'dev':
    from gevent import monkey

    monkey.patch_all()
else:
    pass

from apps.interface.views.interfaceapimsg import interfaceapimsg
from apps.interface.views.interfacecase import interfacecase
from apps.interface.views.interfacecaseset import interfacecaseset
from apps.interface.views.interfaceconfig import interfaceconfig
from apps.interface.views.interfacefunc import interfacefunc
from apps.interface.views.interfacemodule import interfacemodule
from apps.interface.views.interfaceproject import interfaceproject
from apps.interface.views.interfacereport import interfacereport
from apps.interface.views.interfacetask import interfacetask
from library.api.tFlask import tflask


def create_app():
    app = tflask(config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(interfaceproject, url_prefix='/v1/interfaceproject'),
    app.register_blueprint(interfacemodule, url_prefix='/v1/interfacemodule'),
    app.register_blueprint(interfaceconfig, url_prefix='/v1/interfaceconfig'),
    app.register_blueprint(interfacefunc, url_prefix='/v1/interfacefunc'),
    app.register_blueprint(interfaceapimsg, url_prefix='/v1/interfaceapimsg'),
    app.register_blueprint(interfacecaseset, url_prefix='/v1/interfacecaseset'),
    app.register_blueprint(interfacecase, url_prefix='/v1/interfacecase'),
    app.register_blueprint(interfacereport, url_prefix='/v1/interfacereport'),
    app.register_blueprint(interfacetask, url_prefix='/v1/interfacetask'),


if __name__ == '__main__':
    create_app().run(port=config.PORT)
