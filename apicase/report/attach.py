import json
import allure
from apicase.report.html.gen_report import gen_html_report
import requests
from typing import List
from apicase.common.logger import log
from apicase.common.schema import JSONAssertSchema
from apicase.common.exception import JsonAssertError


class AllureAttach(object):

    @classmethod
    def record_http(cls, response, validators: List[JSONAssertSchema]
                    , description: str = None, path: str = None):
        """

        :param path:
        :param description:
        :param response:
        :param validators:
        :return:
        """

        validate_extractor = []

        for i in validators:
            k = i.copy()
            k.comparator = k.comparator.__name__
            k = k.dict()
            k['check'] = k['check'].value
            validate_extractor.append(k)
        title_name = "Request.{0}: {1} {2}".format(response.request.method, path, description)
        content_size = int(dict(response.headers).get("content-length") or 0)
        if isinstance(response.request.body, bytes):
            try:
                response.request.body = str(response.request.body, 'utf-8')
            except UnicodeDecodeError as e:
                response.request.body = str(e)
        summary = {
            'name': description,
            'path': response.request.url,
            'request': {
                'url': response.request.url,
                'headers': cls.headers_format(response.request.headers),
                'body': response.request.body
            },
            'response': {
                'status_code': response.status_code,
                'headers': cls.headers_format(response.headers),
                'body': response.text
            },
            'validators': {
                'validate_extractor': validate_extractor,
                'validate_script': [

                ],
            },
            'time': {

            },
            'stat': {
                'content_size': content_size
            }
        }
        body = gen_html_report(summary=summary)
        # log.debug(summary)
        allure.attach(body=body, name=title_name, attachment_type=allure.attachment_type.HTML)

    @staticmethod
    def headers_format(headers: dict):
        """
        headers字典转为文本并进行编码处理
        :param headers:
        :return:
        """
        header_str = ''
        for i, k in headers.items():
            header_str += i + ': ' + k + '\n'
        return requests.utils.unquote(header_str)

    # @classmethod
    # def api_record(cls, response):
    #     name = "{0} {1}".format(response.request.method, response.request.url)
    #     req_headers = json.dumps(dict(response.request.headers), ensure_ascii=False)
    #     res_headers = json.dumps(dict(response.headers), ensure_ascii=False)
    #     req_body = response.request.body
    #     if type(req_body) == bytes:
    #         try:
    #             req_body = req_body.decode()
    #         except UnicodeDecodeError:
    #             req_body = 'form-data参数不做打印'
    #     data_template = {
    #         'request': {
    #             'body': req_body,
    #             'headers': req_headers,
    #         },
    #         'response': {
    #             'status_code': response.status_code or None,
    #             'body': response.text,
    #             'headers': res_headers,
    #             # 'cookies': response.cookies or None,
    #             'encoding': response.encoding,
    #             'reason': response.reason,
    #             'ok': response.ok,
    #             'response_time_s': response.elapsed.total_seconds(),
    #         }
    #     }
    #     data_template = json.dumps(data_template, indent=1, separators=(',          ', ': '), ensure_ascii=False)
    #     allure.attach(body=data_template, name=name, attachment_type=allure.attachment_type.JSON)
    #
    # @classmethod
    # def sql_record(cls, sql_info: dict):
    #     crud = sql_info['crud']
    #     url = sql_info['   url']
    #     name = None
    #     for i in crud:
    #         if crud[i]:
    #             name = str(i) + ' ' + str(url)
    #             break
    #     data = str(sql_info['sql']) + '\n' + str(sql_info['parameters'])
    #     allure.attach(body=data, name=name, attachment_type=allure.attachment_type.TEXT)

    # @classmethod
    # def schema_assert_record(cls, assert_json: dict, schema: dict) -> None:
    #     """
    #     TODO(GuoWenHe): 待扩展数组模式
    #     """
    #     assert_json = json.dumps(assert_json, ensure_ascii=False)
    #     schema = json.dumps(schema, ensure_ascii=False)
    #     name = 'Assert api_json->schema'
    #     data = 'assert_data:\n' + str(assert_json) + '\nassert_schema\n' + str(schema)
    #     allure.attach(body=data, name=name, attachment_type=allure.attachment_type.TEXT)

    # @classmethod
    # def diff_record(cls, json_data) -> None:
    #     name = 'Assert Diff'
    #     data_template = json.dumps(json_data, indent=1, separators=(',  ', ': '), ensure_ascii=False)
    #     allure.attach(body=data_template, name=name, attachment_type=allure.attachment_type.JSON)
