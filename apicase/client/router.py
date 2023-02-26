from typing import Any, List

from apicase.client.reuquest import APIRequest
from apicase.common.enumeration import BodyTypeEnum
from apicase.common.schema import JSONAssertSchema


class APIRouter:

    def __init__(self,
                 base_url: str,
                 intermediate_route: str = None,
                 pre: list = None,
                 after: list = None,
                 default_json_extraction: str = None,
                 default_json_asserter_list: List = None,
                 default_custom_asserter_list: List = None,
                 ):
        """
        APIRouter
        :param base_url: 基础路由
        :param intermediate_route: 服务路由
        :param pre: 全局前置处理器
        :param after: 全局后置处理器
        :param default_json_extraction: 公共JSON提取器
        :param default_json_asserter_list: 全局默认断言列表
        :param default_custom_asserter_list: 全局默认自定义处理器
        """
        self.base_url = base_url
        self.intermediate_route = intermediate_route
        if intermediate_route:
            self.base_url = self.base_url + self.intermediate_route
        self.pro = pre
        self.after = after
        self.default_json_extraction = default_json_extraction
        self.default_json_asserter_list = default_json_asserter_list
        self.default_custom_asserter_list = default_custom_asserter_list

    def api_route(self,
                  method: str,
                  path: str,
                  body_type: BodyTypeEnum,
                  pre: list = None,
                  after: list = None,
                  other: dict = None,
                  description: str = None,
                  default_json_asserter_list: list = None,
                  ) -> APIRequest:
        url = self.base_url + path
        if pre is None:
            pre = list()
        if after is None:
            after = list()
        if self.pro:
            pre = self.pro + pre
        if self.after:
            after = self.after + after
        json_asserter_list = self.default_json_asserter_list
        if default_json_asserter_list:
            json_asserter_list = default_json_asserter_list
        api = APIRequest(
            url=url,
            method=method,
            body_type=body_type,
            pre=pre,
            after=after,
            other=other,
            path=self.intermediate_route + path,
            description=description,
            default_json_extraction=self.default_json_extraction,
            default_json_asserter_list=json_asserter_list,
            default_custom_asserter_list=self.default_custom_asserter_list,
        )
        return api

    def post(self,
             path: str,
             request_model: Any = None,
             query_params_model: Any = None,
             body_type: BodyTypeEnum = BodyTypeEnum.NULL,
             pre: list = None,
             after: list = None,
             other: dict = None,
             description: str = None,
             default_json_asserter_list: list = None
             ) -> APIRequest:
        """
        request_model 因达不到类型提示的效果，仅做注释关联使用
        """
        if request_model:
            body_type = BodyTypeEnum.JSON
        return self.api_route(
            method='post',
            path=path,
            body_type=body_type,
            pre=pre,
            after=after,
            other=other,
            description=description,
            default_json_asserter_list=default_json_asserter_list,
        )

    def get(self,
            path: str,
            query_params_model: Any = None,
            pre: list = None,
            after: list = None,
            other: dict = None,
            description: str = None,
            default_json_asserter_list: list = None
            ) -> APIRequest:
        return self.api_route(
            method='get',
            path=path,
            body_type=BodyTypeEnum.NULL,
            pre=pre,
            after=after,
            other=other,
            description=description,
            default_json_asserter_list=default_json_asserter_list,
        )
