from typing import NewType


class Case(object):
    pass


CaseType = NewType('CaseType', Case)


class Vars(object):
    __vars = {}

    def put(self, key, value) -> None:
        self.__vars[key] = value

    def get(self, key):
        return self.__vars.get(key)

    def delete_all(self):
        self.__vars = {}

    def get_all(self):
        return self.__vars

    # @staticmethod
    # def log(dict_path, value):
    #     data = '已经存入数据:' + 'dict_path【{}】'.format(str(dict_path)) + 'data【{}】'.format(str(value))
    #     # logger.debug(data)


VarsType = NewType('VarsType', Vars)
