from typing import Union, Dict, List
import json

import requests
from pydantic import BaseModel

from apicase.client.response import APIResponse
from apicase.common.schema import RequestSchema
from apicase.common.enumeration import BodyTypeEnum

session = requests.Session()


class APIRequest(object):
    response = None

    def __init__(self, url: str, method: str, body_type: BodyTypeEnum, headers: dict = None, cookies: dict = None,
                 timeout: int = 30, pre: list = None, after: list = None, other: dict = None, description: str = None,
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

    def send(self,
             schema: BaseModel = None,
             data: Union[str, Dict, List, bytes] = None,
             query_params: dict = None,
             path_params: dict = None,
             files: dict = None
             ):
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

        if schema:
            self.request.data = schema.dict()

        self.set_content_type()
        if self.pre:
            self.request = self.execution_processor(self.pre, self.request)
        response = session.request(
            method=self.request.method,
            url=self.request.url,
            params=self.request.query_params,
            data=self.request.data,
            files=self.request.files,
            headers=self.request.headers,
            cookies=self.request.cookies,
            timeout=self.request.timeout,
            verify=False  # 不认证证书
        )
        self.response = response
        response.json()
        if self.after:
            self.response = self.execution_processor(self.after, self.response)
        return APIResponse(self.response)

    @staticmethod
    def execution_processor(exec_list: list, parameter):
        for i in exec_list:
            parameter = i(parameter)
        return parameter

    def set_content_type(self):
        body_type = self.request.body_type
        content_type = None
        if not body_type:
            if body_type == BodyTypeEnum.JSON:
                content_type = 'application/json'
                self.request.data = json.dumps(self.request.data, ensure_ascii=False)
                self.request.data = self.request.data.encode('utf-8')
            elif body_type == BodyTypeEnum.TEXT:
                content_type = 'text/plain'
            elif body_type == BodyTypeEnum.XML:
                content_type = 'application/xml'
            elif body_type == BodyTypeEnum.FORM_URLENCODED:
                content_type = 'application/x-www-form-urlencoded'
            self.request.headers['Content-Type'] = content_type

    def add_pro(self, pro_list: list):
        pass

    def add_after(self, after_list: list):
        pass
