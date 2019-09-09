from apps.jobs.settings import config

if config.SERVER_ENV != 'dev':
    from gevent import monkey

    monkey.patch_all()
else:
    pass

from apps.jobs.views.jobs import jobs
from library.api.tFlask import tflask


def create_app():
    app = tflask(config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(jobs, url_prefix="/v1/jobs")


if __name__ == '__main__':
    create_app().run(port=config.PORT, server_env=config.SERVER_ENV)
