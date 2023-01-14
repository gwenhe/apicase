from typing import Any

from apicase.client.reuquest import APIRequest
from apicase.common.enumeration import BodyTypeEnum


class APIRouter:

    def __init__(self, base_url: str, intermediate_route: str = None, pre: list = None, after: list = None,
                 json_extraction: str = None, asser_list: list = None
                 ):
        self.base_url = base_url
        self.intermediate_route = intermediate_route
        if intermediate_route:
            self.base_url = self.base_url + self.intermediate_route
        self.pro = pre
        self.after = after
        self.json_extraction = json_extraction
        self.asser_list = asser_list

    def api_route(self,
                  method: str,
                  path: str,
                  body_type: BodyTypeEnum,
                  pre: list = None,
                  after: list = None,
                  other: dict = None,
                  description: str = None,
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
        api = APIRequest(
            url=url,
            method=method,
            body_type=body_type,
            pre=pre,
            after=after,
            other=other,
            path=self.intermediate_route + path,
            description=description,
        )
        return api

    def post(self,
             path: str,
             request_model: Any = None,
             body_type: BodyTypeEnum = BodyTypeEnum.NULL,
             pre: list = None,
             after: list = None,
             other: dict = None,
             description: str = None
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
        )

    def get(self,
            path: str,
            pre: list = None,
            after: list = None,
            other: dict = None,
            description: str = None,
            ) -> APIRequest:
        return self.api_route(
            method='get',
            path=path,
            body_type=BodyTypeEnum.NULL,
            pre=pre,
            after=after,
            other=other,
            description=description,
        )
