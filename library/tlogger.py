import logging
import os
import traceback
from logging.handlers import RotatingFileHandler
from os.path import abspath, dirname

from flask import request, g
from flask.logging import default_handler


def logger_create(service_name, app):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_path = os.path.join(dirname(dirname(abspath(__file__))), 'apps', service_name, 'log')

    if not os.path.exists(log_path):
        os.mkdir(log_path)
    formatter = TloggerFormatter(
        f"[%(asctime)s][%(process)d][{service_name}][%(filename)s %(lineno)d %(levelname)s]: %(message)s")

    logfile = f'{log_path}/{service_name}.log'
    fh = RotatingFileHandler(logfile, maxBytes=10 * 1024 * 1024, backupCount=5)
    fh.setLevel(logging.INFO)
    info_filter = InfoFilter()
    fh.addFilter(info_filter)
    fh.setFormatter(formatter)

    error_logfile = f'{log_path}/{service_name}_error.log'
    fh_error = RotatingFileHandler(error_logfile, maxBytes=10 * 1024 * 1024, backupCount=5)
    fh_error.setLevel(logging.ERROR)
    fh_error.setFormatter(formatter)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)

    app.logger.removeHandler(default_handler)
    app.logger.addHandler(sh)
    app.logger.addHandler(fh)
    app.logger.addHandler(fh_error)


class InfoFilter(logging.Filter):
    def filter(self, record):
        """only use INFO
        筛选, 只需要 INFO 级别的log
        :param record:
        :return:
        """
        if logging.INFO <= record.levelno < logging.ERROR:
            # 已经是INFO级别了
            # 然后利用父类, 返回 1
            return 1
        else:
            return 0


class TloggerFormatter(logging.Formatter):

    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        if record.levelno == logging.ERROR or record.levelno == logging.WARNING:
            if self.usesTime():
                record.asctime = self.formatTime(record, self.datefmt)
            msg = f"""{record.getMessage()}
request  : {request.path}  {request.method} [handler: {g.userid}]
token    : {request.headers.get('Authorization', 'notoken')}
projectid: {request.headers.get('projectid', 'noprojectid')}
query    : {request.args.to_dict()}
{f"body  : {request.json}" if request.method == 'POST' else ''}
{traceback.format_exc()}"""
            record.message = msg
            return self.formatMessage(record)
        else:
            return logging.Formatter.format(self, record)

