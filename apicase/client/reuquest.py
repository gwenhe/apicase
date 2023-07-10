import urllib3
from typing import Union, Dict, List
import json

import requests
from pydantic import BaseModel

from apicase.client.response import APIResponse
from apicase.common.schema import RequestSchema, JSONAssertSchema
from apicase.common.enumeration import BodyTypeEnum

session = requests.Session()
urllib3.disable_warnings()

from abc import ABC, abstractmethod
import requests

from typing import Callable, List, Dict, Any

from enum import Enum


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value


class HttpSession(requests.Session):
    """
    HttpSession
    """
    http_timeout: int = 60,
    http_allow_redirects = False,
    http_proxies = None,
    http_stream = None,
    http_verify = False,
    http_cert = None,

    def __init__(self) -> None:
        super().__init__()
        self.pre: Dict[str, List[Callable]] = {'pre_request': []}
        self.hooks: Dict[str, List[Callable]] = {'response': []}

    def request(self, **kwargs):
        """
        重新request
        :param kwargs:
        :return:
        """
        kwargs['verify'] = self.http_verify[0]
        kwargs['timeout'] = self.http_timeout[0]
        kwargs['allow_redirects'] = self.http_allow_redirects[0]
        kwargs['proxies'] = self.http_proxies[0]
        kwargs['verify'] = self.http_verify[0]
        kwargs['cert'] = self.http_cert[0]
        for call in self.pre.get('pre_request'):
            call(kwargs)
        return super(HttpSession, self).request(**kwargs)


class APIRequest(object):
    """
    APIRequest
    """
    response = None

    def __init__(self, url: str, method: str, body_type: BodyTypeEnum, headers: dict = None, cookies: dict = None,
                 timeout: int = 30, pre: list = None, after: list = None, other: dict = None, description: str = None,
                 default_json_extraction: str = None,
                 default_json_asserter_list: List[JSONAssertSchema] = None,
                 default_custom_asserter_list: List = None,
                 # -------------------------   参数分割   --------------------------------
                 path: str = None):
        self.path = path  # 提供该类属性，将接口路由展示报告上
        if pre is None:
            pre = list()
        if after is None:
            after = list()
        if headers is None:
            headers = list()
        if cookies is None:
            cookies = list()
        self.pre = pre
        self.after = after
        self.request = RequestSchema(
            url=url,
            method=method,
            body_type=body_type,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            other=other,
            description=description,

        )
        self.default_json_extraction = default_json_extraction
        self.default_json_asserter_list = default_json_asserter_list
        self.default_custom_asserter_list = default_custom_asserter_list

    def send(self,
             schema: BaseModel = None,
             data: Union[str, Dict, List, bytes] = None,
             query_params: dict = None,
             path_params: dict = None,
             files: dict = None,
             json_asserter_list: List[JSONAssertSchema] = None,
             custom_asserter_list: List = None,

             is_default_json_extraction: bool = True,
             is_default_json_asserter: bool = True,
             default_json_asserter_list: List[JSONAssertSchema] = None,
             default_custom_asserter_list: List = None,
             http_session: HttpSession = None
             ):
        """
        http请求、执行器、断言、记录
        :param http_session:
        :param is_default_json_extraction:
        :param is_default_json_asserter:
        :param schema:
        :param data:
        :param query_params:
        :param path_params:
        :param files:
        :param json_asserter_list:
        :param custom_asserter_list:
        :param default_custom_asserter_list:
        :param default_json_asserter_list:
        :return:
        """
        if not query_params:
            query_params = {}
        if not path_params:
            path_params = {}
        if not files:
            files = {}
        self.request.query_params = query_params
        self.request.path_params = path_params
        self.request.files = files
        self.request.data = data

        # 本次执行数据
        execution_default_json_asserter_list = self.default_json_asserter_list
        execution_default_json_extraction = self.default_json_extraction
        execution_default_custom_asserter_list = []

        if not is_default_json_extraction:
            # 不执行默认json提取
            execution_default_json_extraction = ''
        if default_json_asserter_list:
            # 替换默认断言列表
            execution_default_json_asserter_list = default_json_asserter_list
        if not is_default_json_asserter:
            # 不执行默认断言，断言列表
            # self.default_json_asserter_list = []
            execution_default_json_asserter_list = []
        if default_custom_asserter_list:
            # 替换断言器列表
            # self.default_custom_asserter_list = default_custom_asserter_list
            execution_default_custom_asserter_list = default_custom_asserter_list

        if schema:
            self.request.data = schema.dict()

        self.set_content_type()

        request_session = session
        if http_session:
            """
            使用自定义http_session
            """
            request_session = http_session

        if self.pre:
            self.request = self.execution_processor(self.pre, self.request, request_session)

        response = request_session.request(
            method=self.request.method,
            url=self.request.url,
            params=self.request.query_params,
            data=self.request.data,
            files=self.request.files,
            headers=self.request.headers,
            cookies=self.request.cookies,
            # timeout=self.request.timeout,
            # verify=False,  # 不认证证书
        )
        self.response = response
        if self.after:
            self.response = self.execution_processor(self.after, self.response, request_session)

        return APIResponse(self.response,
                           default_json_extraction=execution_default_json_extraction,
                           default_json_asserter_list=execution_default_json_asserter_list,
                           json_asserter_list=json_asserter_list,
                           default_custom_asserter_list=execution_default_custom_asserter_list,
                           custom_asserter_list=custom_asserter_list,
                           description=self.request.description,
                           path=self.path
                           )

    @staticmethod
    def execution_processor(exec_list: list, parameter, request_session):
        """
        前后置处理器，函数列表
        :param request_session:
        :param exec_list:
        :param parameter:
        :return:
        """
        for i in exec_list:
            parameter = i(parameter, request_session)
        return parameter

    def set_content_type(self):
        """
        根据不同的请求体类型设置请求头，
        json进行编码处理，request中文编码有问题
        :return:
        """
        body_type = self.request.body_type
        content_type = None
        if body_type:
            if body_type == BodyTypeEnum.JSON:
                content_type = 'application/json'
                print(self.request.data)
                self.request.data = json.dumps(self.request.data, ensure_ascii=False, cls=EnumEncoder)
                self.request.data = self.request.data.encode('utf-8')
            elif body_type == BodyTypeEnum.TEXT:
                content_type = 'text/plain'
            elif body_type == BodyTypeEnum.XML:
                content_type = 'application/xml'
            elif body_type == BodyTypeEnum.FORM_URLENCODED:
                content_type = 'application/x-www-form-urlencoded'
            self.request.headers['Content-Type'] = content_type

# class APIRequest(object):
#     response = None
#
#     def __init__(self, url: str, method: str, body_type: BodyTypeEnum, headers: dict = None, cookies: dict = None,
#                  timeout: int = 30, pre: list = None, after: list = None, other: dict = None, description: str = None,
#                  default_json_extraction: str = None,
#                  default_json_asserter_list: List[JSONAssertSchema] = None,
#                  default_custom_asserter_list: List = None,
#                  # -------------------------   参数分割   --------------------------------
#                  path: str = None):
#         self.path = path  # 提供该类属性，将接口路由展示报告上
#         if pre is None:
#             pre = list()
#         if after is None:
#             after = list()
#         if headers is None:
#             headers = list()
#         if cookies is None:
#             cookies = list()
#         self.pre = pre
#         self.after = after
#         self.request = RequestSchema(
#             url=url,
#             method=method,
#             body_type=body_type,
#             headers=headers,
#             cookies=cookies,
#             timeout=timeout,
#             other=other,
#             description=description,
#         )
#         self.default_json_extraction = default_json_extraction
#         self.default_json_asserter_list = default_json_asserter_list
#         self.default_custom_asserter_list = default_custom_asserter_list
#
#     def send(self,
#              schema: BaseModel = None,
#              data: Union[str, Dict, List, bytes] = None,
#              query_params: dict = None,
#              path_params: dict = None,
#              files: dict = None,
#              json_asserter_list: List[JSONAssertSchema] = None,
#              custom_asserter_list: List = None,
#
#              is_default_json_extraction: bool = True,
#              is_default_json_asserter: bool = True,
#              default_json_asserter_list: List[JSONAssertSchema] = None,
#              default_custom_asserter_list: List = None,
#              ):
#         """
#         http请求、执行器、断言、记录
#         :param is_default_json_extraction:
#         :param is_default_json_asserter:
#         :param schema:
#         :param data:
#         :param query_params:
#         :param path_params:
#         :param files:
#         :param json_asserter_list:
#         :param custom_asserter_list:
#         :param default_custom_asserter_list:
#         :param default_json_asserter_list:
#         :return:
#         """
#         if not query_params:
#             query_params = {}
#         if not path_params:
#             path_params = {}
#         if not files:
#             files = {}
#         self.request.query_params = query_params
#         self.request.path_params = path_params
#         self.request.files = files
#         self.request.data = data
#
#         if not is_default_json_extraction:
#             # 不执行默认json提取
#             self.default_json_extraction = ''
#         if default_json_asserter_list:
#             # 替换默认断言列表
#             self.default_json_asserter_list = default_json_asserter_list
#         if not is_default_json_asserter:
#             # 不执行默认断言，情况列表
#             self.default_json_asserter_list = []
#         if default_custom_asserter_list:
#             # 替换断言器列表
#             self.default_custom_asserter_list = default_custom_asserter_list
#
#         if schema:
#             self.request.data = schema.dict()
#
#         self.set_content_type()
#         if self.pre:
#             self.request = self.execution_processor(self.pre, self.request)
#
#         response = session.request(
#             method=self.request.method,
#             url=self.request.url,
#             params=self.request.query_params,
#             data=self.request.data,
#             files=self.request.files,
#             headers=self.request.headers,
#             cookies=self.request.cookies,
#             timeout=self.request.timeout,
#             verify=False  # 不认证证书
#         )
#         self.response = response
#         if self.after:
#             self.response = self.execution_processor(self.after, self.response)
#
#         return APIResponse(self.response,
#                            default_json_extraction=self.default_json_extraction,
#                            default_json_asserter_list=self.default_json_asserter_list,
#                            json_asserter_list=json_asserter_list,
#                            default_custom_asserter_list=self.default_custom_asserter_list,
#                            custom_asserter_list=custom_asserter_list,
#                            description=self.request.description,
#                            path=self.path
#                            )
#
#     @staticmethod
#     def execution_processor(exec_list: list, parameter):
#         """
#         前后置处理器，函数列表
#         :param exec_list:
#         :param parameter:
#         :return:
#         """
#         for i in exec_list:
#             parameter = i(parameter)
#         return parameter
#
#     def set_content_type(self):
#         """
#         根据不同的请求体类型设置请求头，
#         json进行编码处理，request中文编码有问题
#         :return:
#         """
#         body_type = self.request.body_type
#         content_type = None
#         if body_type:
#             if body_type == BodyTypeEnum.JSON:
#                 content_type = 'application/json'
#                 self.request.data = json.dumps(self.request.data, ensure_ascii=False)
#                 self.request.data = self.request.data.encode('utf-8')
#             elif body_type == BodyTypeEnum.TEXT:
#                 content_type = 'text/plain'
#             elif body_type == BodyTypeEnum.XML:
#                 content_type = 'application/xml'
#             elif body_type == BodyTypeEnum.FORM_URLENCODED:
#                 content_type = 'application/x-www-form-urlencoded'
#             self.request.headers['Content-Type'] = content_type
