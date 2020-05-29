import datetime
import json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

class MyResponse:
    def __init__(self, msg='success', data=[], code=200):
        self.msg = msg
        self.data = data
        self.code = code

    @property
    def response_data(self):
        res = {'code': self.code, 'data': self.data, 'msg': self.msg}
        # print(res)
        return json.dumps(res, cls=DateEncoder)
