import json


class MyResponse:
    def __init__(self, msg, data=[], code=200):
        self.msg = msg
        self.data = data
        self.code = code

    @property
    def response_data(self):
        res = {'code': self.code, 'data': self.data, 'msg': self.msg}
        return json.dumps(res)
