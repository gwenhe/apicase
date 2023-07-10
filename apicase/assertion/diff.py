"""
@File    ：diff.py
@Author  ：guowenhe
@Date    ：2023/3/28 01:23 
"""

from deepdiff import DeepDiff
from typing import Optional, Union
import json


class DiffJson(object):
    """
    比对
    """
    diff_result: bool
    diff_tree: dict
    diff_record: dict

    def __init__(self, expected: Union[dict, list], actual: Union[dict, list], ignore_order: bool = False,
                 ignore_order_func=None, exclude_paths: list = None, **kwargs):
        """
        :param expected: 期望数据
        :param actual: 实际数据
        :param ignore_order: 忽略列表排序，True=是
        :param ignore_order_func: 忽略某些路径的循序:如下
                DeepDiff(t1, t2, ignore_order=True, ignore_order_func=lambda level: "root['data']['itim2']" in level.path())
                def ignore_order_func(level):
                    return 'a' in level.path()
                DeepDiff(t1, t2, ignore_order=True, ignore_order_func=ignore_order_func)
        :param exclude_paths:排除某些对象的比较
                DeepDiff(t1, t2, exclude_paths=[
                    "root['data']['itim2']"
                ])
        :param kwargs:
        """
        diff_res = DeepDiff(t1=expected, t2=actual, ignore_order=ignore_order,
                            ignore_order_func=ignore_order_func, exclude_paths=exclude_paths, **kwargs)
        diff_json = diff_res.to_json()
        self.diff_tree = json.loads(diff_json)
        if exclude_paths:
            exclude_paths = str(exclude_paths)
        self.diff_record = {
            'diff_result': None,
            'diff': None,
            'ignore_order': ignore_order,
            'ignore_order_func': ignore_order_func,
            'exclude_paths': exclude_paths,
            'expected': json.dumps(expected, ensure_ascii=False),
            'actual': json.dumps(actual, ensure_ascii=False),
        }

        self.modify_diff_tree()
        self.diff_assert()

    def modify_diff_tree(self):
        """
        修改差异树
        :return:
        """
        if self.diff_tree == {}:
            self.diff_record['diff_result'] = True
        else:
            self.diff_record['diff_result'] = False
            self.diff_record['diff'] = self.diff_tree

    def diff_assert(self):
        """
        比对断言
        :return:
        """
        print(self.diff_record['diff_result'])
        if self.diff_record['diff_result'] is False:
            diff_record = json.dumps(self.diff_record)
            raise AssertionError('数据对比失败,有差异: {diff_tree}'.format(diff_tree=diff_record))
