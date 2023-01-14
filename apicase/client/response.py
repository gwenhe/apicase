from typing import Union

import jmespath


class APIResponse(object):
    response_json: Union[dict, list] = None

    def __init__(self, response):
        self.request = response.request
        self.status_code = response.status_code
        self.headers = response.headers
        self.json = response.json
        self.text = response.text

    def _init_json(self):
        if self.response_json is None:
            self.response_json = self.json()

    def jmespath(self, expression):
        self._init_json()
        return jmespath.search(expression=expression, data=self.response_json)
