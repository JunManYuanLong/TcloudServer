from apps.public.settings import config

if config.SERVER_ENV != 'dev':
    from gevent import monkey

    monkey.patch_all()
else:
    pass

# from apps.public.views.guest import guest
from apps.public.views.public import public
from library.api.tFlask import tflask


def create_app():
    app = tflask(config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(public, url_prefix="/v1/public")
    # app.register_blueprint(guest, url_prefix="/v1/guest")


if __name__ == '__main__':
    create_app().run(port=config.PORT)
