from apps.project.settings import config

if config.SERVER_ENV != 'dev':
    from gevent import monkey

    monkey.patch_all()
else:
    pass

from apps.project.views.assets import phone, virtualasset
from apps.project.views.board import board
from apps.project.views.boardconfig import board_config
from apps.project.views.cases import case
from apps.project.views.credit import credit
from apps.project.views.dashboard import dashboard
from apps.project.views.issue import issue
# from apps.project.views.jira import jira
from apps.project.views.modules import module
from apps.project.views.project import project
from apps.project.views.requirement import requirement
from apps.project.views.tag import tag
from apps.project.views.taskcase import taskcase
from apps.project.views.tasks import task
from apps.project.views.version import version
from library.api.tFlask import tflask


def create_app():
    app = tflask(config)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(project, url_prefix="/v1/project")
    app.register_blueprint(phone, url_prefix="/v1/asset/phone")
    app.register_blueprint(virtualasset, url_prefix="/v1/asset/virtual")
    app.register_blueprint(case, url_prefix="/v1/case")
    app.register_blueprint(credit, url_prefix="/v1/credit")
    # app.register_blueprint(jira, url_prefix="/v1/jira")
    app.register_blueprint(issue, url_prefix="/v1/issue")
    app.register_blueprint(module, url_prefix="/v1/module")
    app.register_blueprint(requirement, url_prefix="/v1/requirement")
    app.register_blueprint(taskcase, url_prefix="/v1/taskcase")
    app.register_blueprint(task, url_prefix="/v1/task")
    app.register_blueprint(version, url_prefix="/v1/version")
    app.register_blueprint(board_config, url_prefix="/v1/boardconfig")
    app.register_blueprint(tag, url_prefix="/v1/tag")
    app.register_blueprint(board, url_prefix="/v1/board")
    app.register_blueprint(dashboard, url_prefix="/v1/dashboard")


if __name__ == '__main__':
    create_app().run(port=config.PORT)
