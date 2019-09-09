import json
import logging
import sys
from urllib.parse import urlparse


def convert_list_to_dict(origin_list):
    """ convert HAR data list to mapping
    @param (list) origin_list
        [
            {"name": "v", "value": "1"},
            {"name": "w", "value": "2"}
        ]
    @return (dict)
        {"v": "1", "w": "2"}
    """
    return {
        item["name"]: item["value"]
        for item in origin_list
    }


def load_api_log_entries(file_path, file_type):
    """
    """
    with open(file_path, "r+") as f:
        try:
            content_json = json.loads(f.read())
            if file_type == 'har':
                return content_json["log"]["entries"]
            elif file_type == 'json':
                return content_json['requests']
        except (KeyError, TypeError):
            logging.error("api_1_0 file content error: {}".format(file_path))
            sys.exit(1)


class HarParser(object):
    IGNORE_REQUEST_HEADERS = [
        "host",
        "accept",
        "content-length",
        "connection",
        "accept-encoding",
        "accept-language",
        "origin",
        "referer",
        "cache-control",
        "pragma",
        "cookie",
        "upgrade-insecure-requests",
        ":authority",
        ":method",
        ":scheme",
        ":path"
    ]

    def __init__(self, file_path, file_type='har'):
        self.log_entries = load_api_log_entries(file_path, file_type)
        self.user_agent = None
        self.file_type = file_type
        self.testset = self.make_testset()

    @staticmethod
    def _make_har_request_url(testcase_dict, entry_json):
        """ parse HAR entry request url and queryString, and make testcase url and params
        """
        request_params = convert_list_to_dict(entry_json["request"].get("queryString", []))

        url = entry_json["request"].get("url")
        if not url:
            logging.exception("url missed in request.")
            sys.exit(1)
        parsed_object = urlparse(url)
        if request_params:
            testcase_dict["param"] = json.dumps(
                [{'key': k, 'value': v, 'param_type': 'string'} for k, v in request_params.items()])

        testcase_dict["status_url"] = parsed_object.netloc
        testcase_dict["url"] = parsed_object.path
        testcase_dict["name"] = parsed_object.path

    @staticmethod
    def _make_json_data(testcase_dict, entry_json):
        testcase_dict['name'] = entry_json['name']
        testcase_dict['method'] = entry_json['method']
        if not entry_json['url'].startswith('http'):
            entry_json['url'] = 'http://' + entry_json['url']
        url = urlparse(entry_json['url'])
        testcase_dict['url'] = url.path
        if url.netloc:
            testcase_dict['status_url'] = url.netloc
        else:
            testcase_dict['status_url'] = url.scheme
        testcase_dict['header'] = json.dumps(
            [{'key': h['key'], 'value': h['value']} for h in entry_json['headerData'] if h])
        if entry_json['method'] == 'GET':
            testcase_dict['param'] = json.dumps(
                [{'key': h1['key'], 'value': h1['value'], 'param_type': 'string'} for h1 in entry_json['queryParams'] if
                 h1])
        if entry_json['method'] != 'GET':
            if entry_json['data']:
                testcase_dict['variable'] = json.dumps(
                    [{'key': h1['key'], 'value': h1['value'], 'param_type': 'string'} for h1 in
                     entry_json['data'] if h1])
            elif entry_json.get('rawModeData'):
                testcase_dict['variable_type'] = 'json'
                testcase_dict['json_variable'] = entry_json['rawModeData']

    def _make_har_request_headers(self, testcase_dict, entry_json):
        """ parse HAR entry request headers, and make testcase headers.
        """
        testcase_headers = []
        for header in entry_json["request"].get("header", []):
            if header["name"].lower() in self.IGNORE_REQUEST_HEADERS:
                continue
            if header["name"].lower() == "user-agent":
                if not self.user_agent:
                    self.user_agent = header["value"]
                continue
            testcase_headers.append({'key': header["name"], 'value': header["value"]})

        testcase_dict["header"] = json.dumps(testcase_headers)

    @staticmethod
    def _make_har_request_data(testcase_dict, entry_json):
        """ parse HAR entry request data, and make testcase request data
        """
        method = entry_json["request"].get("method")
        if not method:
            logging.exception("method missed in request.")
            sys.exit(1)

        testcase_dict["method"] = method
        if method in ["POST", "PUT"]:
            mime_type = entry_json["request"].get("postData", {}).get("mimeType")

            # Note that text and params fields are mutually exclusive.
            params = entry_json["request"].get("postData", {}).get("params", [])
            text = entry_json["request"].get("postData", {}).get("text")
            if text:
                post_data = text
            else:
                post_data = convert_list_to_dict(params)

            request_data_key = "data"
            if not mime_type:
                pass
            elif mime_type.startswith("application/json"):
                post_data = json.loads(post_data)
                request_data_key = "json"
            elif mime_type.startswith("application/x-www-form-urlencoded"):
                # post_data = utils.x_www_form_urlencoded(post_data)
                pass
            else:
                # TODO: make compatible with more mimeType
                pass
            testcase_dict["variable_type"] = request_data_key
            if request_data_key == 'json':
                testcase_dict["json_variable"] = json.dumps(post_data)
            else:
                testcase_dict["variable"] = json.dumps([
                    {'key': k, 'value': v, 'param_type': 'string'} for k, v in post_data.items()])

    def make_testcase(self, entry_json):
        """ extract info from entry dict and make testcase
        """
        testcase_dict = {
            "url": '',
            "name": "待定",
            "header": '[]',
            "method": 'POST',
            "variable_type": 'data',
            "variable": '[]',
            "extract": '[]',
            "validate": '[]',
            "param": '[]',
        }
        if self.file_type == 'har':
            self._make_har_request_url(testcase_dict, entry_json)
            self._make_har_request_headers(testcase_dict, entry_json)
            self._make_har_request_data(testcase_dict, entry_json)
        elif self.file_type == 'json':
            self._make_json_data(testcase_dict, entry_json)
        return testcase_dict

    def make_testcases(self):
        """ extract info from HAR log entries list and make testcase list
        """
        testcases = []
        for entry_json in self.log_entries:
            testcases.append(self.make_testcase(entry_json))
        return testcases

    def make_testset(self):
        """ Extract info from HAR file and prepare for testcase
        """
        logging.debug("Extract info from HAR file and prepare for testcase.")
        testset = self.make_testcases()
        # config = self.make_config()
        # testset.insert(0, config)
        return testset


if __name__ == '__main__':
    har_parser = HarParser('test.har')
