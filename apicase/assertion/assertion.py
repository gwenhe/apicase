from typing import Union, List, Any
import jmespath
from apicase.common.exception import JsonAssertError
from apicase.common.enumeration import ComparatorEnum, CheckResultEnum
from apicase.common.schema import JSONAssertSchema


class Asserter(object):

    def _assert(self):
        pass


class JSONAsserter(Asserter):
    """
    json 断言器
    """
    assert_list = List[JSONAssertSchema]
    assert_results_list = List

    def __init__(self, assert_list: List[JSONAssertSchema], response_json: Union[dict, list],
                 equal_type: bool = True, ):
        self.assert_list = assert_list
        self.equal_type = equal_type
        self.json_assert(response_json)

    def json_assert(self, response_json: Union[dict, list]):
        """
        json断言
        :param response_json: 请求响应json
        :return:
        """
        assert_results_list = []
        for i in self.assert_list:
            i.value = jmespath.search(i.jmespath, response_json)
            try:
                i.comparator(i.value, i.expectations)
            except AssertionError:
                i.check = CheckResultEnum.FAIL
            else:
                i.check = CheckResultEnum.PASS
            assert_results_list.append(i)
        self.assert_results_list = assert_results_list


class ResponseAsserter(Asserter):
    pass


class CustomAsserter(Asserter):

    def __init__(self, a_list, response):
        self.a_list = a_list
        self.response = response

    def _assert(self):
        for i in self.a_list:
            i(self.response)
