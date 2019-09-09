# encoding: utf-8

import io
import os
from base64 import b64encode
from collections import Iterable
from pathlib import Path

from httprunner import logger
from httprunner.compat import bytes, json, numeric_types
from jinja2 import Template, escape


def stringify_data(meta_data, request_or_response):
    """
    meta_data = {
        "request": {},
        "response": {}
    }
    """
    headers = meta_data[request_or_response]["headers"]
    request_or_response_dict = meta_data[request_or_response]

    for key, value in request_or_response_dict.items():

        if isinstance(value, list):
            value = json.dumps(value, indent=2, ensure_ascii=False)

        elif isinstance(value, bytes):
            try:
                encoding = meta_data["response"].get("encoding")
                if not encoding or encoding == "None":
                    encoding = "utf-8"

                if request_or_response == "response" and key == "content" \
                        and "image" in meta_data["response"]["content_type"]:
                    # display image
                    value = "data:{};base64,{}".format(
                        meta_data["response"]["content_type"],
                        b64encode(value).decode(encoding)
                    )
                else:
                    value = escape(value.decode(encoding))
            except UnicodeDecodeError:
                pass

        elif not isinstance(value, (str, numeric_types, Iterable)):
            # class instance, e.g. MultipartEncoder()
            value = repr(value)

        meta_data[request_or_response][key] = value


def render_html_report(summary, html_report_name=None, html_report_template=None, data_or_report=False):
    """ render html report with specified report name and template
        if html_report_name is not specified, use current datetime
        if html_report_template is not specified, use default report template
    """
    if not html_report_template:
        html_report_template = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            Path("templates"),
            Path("default_report_template.html")
        )
        logger.log_debug("No html report template specified, use default.")
    else:
        logger.log_info("render with html report template: {}".format(html_report_template))

    logger.log_info("Start to render Html report ...")
    logger.log_debug("render data: {}".format(summary))

    report_dir_path = os.path.join(os.path.abspath('.') + r'/reports')
    if html_report_name:
        summary["html_report_name"] = html_report_name
        # report_dir_path = os.path.join(report_dir_path, html_report_name)
        html_report_name += ".html"
    else:
        summary["html_report_name"] = ""

    if not os.path.isdir(report_dir_path):
        os.makedirs(report_dir_path)
    for index, suite_summary in enumerate(summary["details"]):
        if not suite_summary.get("name"):
            suite_summary["name"] = "test suite {}".format(index)
        for record in suite_summary.get("records"):
            meta_data = record['meta_data']
            stringify_data(meta_data, 'request')
            stringify_data(meta_data, 'response')
    with io.open(html_report_template, "r", ) as fp_r:
        template_content = fp_r.read()
        # rendered_content = Template(template_content).render(summary)
        report_path = os.path.join(report_dir_path, html_report_name)
        # report_path = r'E:\project\source/reports\aaa.html'
        rendered_content = Template(template_content, extensions=["jinja2.ext.loopcontrols"]).render(summary)
        if data_or_report:
            return rendered_content
        with io.open(report_path, 'w', ) as fp_w:
            fp_w.write(rendered_content)
        return report_path
