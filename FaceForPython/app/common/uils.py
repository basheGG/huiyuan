

import hashlib
import base64


class DeviceSign:
    IMEI = ""
    MAC = ""
    Timestamp = ""

    def __init__(self, IMEI="", MAC="", Timestamp=""):
        self.IMEI = IMEI
        self.MAC = MAC
        self.Timestamp = Timestamp

    def Sign(self):
        body = self.IMEI + self.Timestamp + self.MAC
        return base64.b64encode(hashlib.sha256(body.encode('utf-8')).digest()).decode("utf-8")

class GetConsul():

    def get_data(self,AC_code):
        return {"IMEI":"aaa","MAC":"asdasd","Timestamp":"asdasdasda","shopID":123,"merchartId":123,}

class GetShebei():

    def get_data(self,id,shop_id):
        print(id,shop_id)
        return True


def make_response(data=None, page=None, pages=None, total=None, code=None, message=None,total_pages=None, **kwargs):
    result = {
        'success': data is not None,
        'data': data,
        'page': page,
        'pages': pages,
        'page_size': len(data) if data else None,
        'total': total,
        'total_pages':total_pages,
        'code': code,
        'message': message,
    }
    for key in kwargs.keys():
        if key not in result:
            result[key] = kwargs[key]
    return result

