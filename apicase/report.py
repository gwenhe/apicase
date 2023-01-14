import json
import allure


class AllureAttach(object):

    @classmethod
    def api_record(cls, response):
        name = "{0} {1}".format(response.request.method, response.request.url)
        req_headers = json.dumps(dict(response.request.headers), ensure_ascii=False)
        res_headers = json.dumps(dict(response.headers), ensure_ascii=False)
        req_body = response.request.body
        if type(req_body) == bytes:
            try:
                req_body = req_body.decode()
            except UnicodeDecodeError:
                req_body = 'form-data参数不做打印'
        data_template = {
            'request': {
                'body': req_body,
                'headers': req_headers,
            },
            'response': {
                'status_code': response.status_code or None,
                'body': response.text,
                'headers': res_headers,
                # 'cookies': response.cookies or None,
                'encoding': response.encoding,
                'reason': response.reason,
                'ok': response.ok,
                'response_time_s': response.elapsed.total_seconds(),
            }
        }
        data_template = json.dumps(data_template, indent=1, separators=(',          ', ': '), ensure_ascii=False)
        allure.attach(body=data_template, name=name, attachment_type=allure.attachment_type.JSON)

    @classmethod
    def sql_record(cls, sql_info: dict):
        crud = sql_info['crud']
        url = sql_info['url']
        name = None
        for i in crud:
            if crud[i]:
                name = str(i) + ' ' + str(url)
                break
        data = str(sql_info['sql']) + '\n' + str(sql_info['parameters'])
        allure.attach(body=data, name=name, attachment_type=allure.attachment_type.TEXT)

    @classmethod
    def schema_assert_record(cls, assert_json: dict, schema: dict) -> None:
        """
        TODO(GuoWenHe): 待扩展数组模式
        """
        assert_json = json.dumps(assert_json, ensure_ascii=False)
        schema = json.dumps(schema, ensure_ascii=False)
        name = 'Assert api_json->schema'
        data = 'assert_data:\n' + str(assert_json) + '\nassert_schema\n' + str(schema)
        allure.attach(body=data, name=name, attachment_type=allure.attachment_type.TEXT)

    @classmethod
    def diff_record(cls, json_data) -> None:
        name = 'Assert Diff'
        data_template = json.dumps(json_data, indent=1, separators=(',  ', ': '), ensure_ascii=False)
        allure.attach(body=data_template, name=name, attachment_type=allure.attachment_type.JSON)
