import logging
from typing import Union, List, Any
import jmespath
import loguru
from prettytable import PrettyTable

from apicase.common.schema import JSONAssertSchema
from apicase.assertion.assertion import (
    JSONAsserter, CustomAsserter
)
from apicase.report.attach import AllureAttach
from apicase.common.enumeration import CheckResultEnum
from apicase.common.exception import JsonAssertError


class APIResponse(object):
    """
    http响应数据
    """
    response_json: Union[dict, list] = None

    def __init__(self, response,
                 default_json_extraction: str = None,
                 default_json_asserter_list: List[JSONAssertSchema] = None,
                 json_asserter_list: List[JSONAssertSchema] = None,
                 default_custom_asserter_list: List = None,
                 custom_asserter_list: List = None,
                 description: str = None,
                 path: str = None
                 ):
        self.validators = None
        self.extraction_json = None
        self.request = response.request
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.json = response.json
        self.text = response.text
        self.default_json_extraction = default_json_extraction
        self.default_json_asserter_list = default_json_asserter_list
        self.json_asserter_list = json_asserter_list
        self.default_custom_asserter_list = default_custom_asserter_list
        self.custom_asserter_list = custom_asserter_list

        self.error = []

        self._api_assert()

        AllureAttach.record_http(
            response=self.response, validators=self.validators, description=description, path=path
        )
        self._raise_error()
        self.raise_failure()

    def _init_json(self):
        if not self.response_json:
            try:
                self.response_json = self.json()
            except Exception:
                self._set_error('JSONDecodeError', self.response.request.url + '\n' + self.text)
        if not self.default_json_extraction:
            self.extraction_json = self.response_json
        else:
            extraction_json = jmespath.search(expression=self.default_json_extraction, data=self.response_json)
            self.extraction_json = extraction_json

    def _api_assert(self):
        """
        :param self:
        """
        self._init_json()
        validators = []
        if self.default_json_asserter_list:
            validators += JSONAsserter(self.default_json_asserter_list, self.response_json).assert_results_list
        if self.json_asserter_list:
            validators += JSONAsserter(self.json_asserter_list, self.extraction_json).assert_results_list
        if self.default_custom_asserter_list:
            CustomAsserter(self.default_custom_asserter_list, self)
        if self.custom_asserter_list:
            CustomAsserter(self.custom_asserter_list, self)
        self.validators = validators

    def raise_failure(self):
        """
        抛出失败异常
        :return:
        """
        error_str = ''

        for i in self.validators:
            if i.check == CheckResultEnum.FAIL:
                error_str += '\n\t检查:{},比较器:{},期望:{},实际:{}'.format(i.jmespath, i.comparator, i.expectations, i.value)
        if error_str:
            raise JsonAssertError('JSON 断言失败' + error_str)

    def _set_error(self, error_type: str, error_msg: str):
        """
        设置异常信息
        :param error_type:
        :param error_msg:
        :return:
        """
        error = {
            'error_type': error_type,
            'error_msg': error_msg,
        }
        self.error.append(error)

    def _raise_error(self):
        """

        :return:
        """
        if self.error:
            table = PrettyTable(["error_type", "error_msg"])
            table.align["error_type"] = "l"
            for i in self.error:
                table.add_row(["error_type", i.get('error_type')])
                table.add_row(["error_msg", i.get('error_msg')])
                raise Exception(table)

    def get_extraction_json(self) -> dict:
        """
        获取提取后的json数据
        :return:
        """
        self._init_json()
        return self.extraction_json

    def jmespath(self, *expressions):
        """
        jsonpath提取器
        :param expressions: 单个或多个要提取的jsonpath字符串
        :return: 返回单个或多个提取的数据，可使用解包接收
                var1,var2,var3 = api.send().jmespath('data.id', 'data.name')
        """
        self._init_json()
        expressions = list(expressions)
        extraction_list = []
        for i in range(len(expressions)):
            expression = expressions[i]
            extraction_list.append(jmespath.search(expression=expression, data=self.extraction_json))
        if len(extraction_list) == 1:
            return extraction_list[0]
        return tuple(extraction_list)
