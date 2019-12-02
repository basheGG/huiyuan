# -*- coding:utf-8 -*-

from app.common.verify_csld import VerifyC
from flask_restful.reqparse import RequestParser


def verify_header(args, request):
    # 解析headers头中的数据，如果不传解析的对应的字段 则默认为None
    arg_header_Ac_Code = request.headers.get("Ac_Code", type=int)
    arg_header_Sign = request.headers.get("Sign", type=str)
    arg_header_token = request.headers.get("token", type=str)
    ver = {
        "Ac_Code": arg_header_Ac_Code,
        "Sign": arg_header_Sign,
        "token": arg_header_token,
        "shop_id": args["shop_id"],
    }
    return ver
    # 进行设备校验
    # res = VerifyC().vericion(ver)
    # if res:
    #     return res
