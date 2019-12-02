import json
from app.models.product_model import ProductModel
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request
from app.common.uils import make_response
from app.common.verify_csld import VerifyC




class ProductApiGet(Resource):
    def get(self):
        # RequestParser使用它来对传递的参数进行解析，解析出来的数据会自动生成一个dict
        productparser = RequestParser(trim=True)
        productparser.add_argument('page', type=int)
        productparser.add_argument('page_size', type=int)
        productparser.add_argument('shop_id', type=int)
        args = productparser.parse_args(strict=True)
        #解析headers头中的数据，如果不传解析的对应的字段 则默认为None
        arg_header_Ac_Code = request.headers.get("Ac_Code",type=int)
        arg_header_Sign = request.headers.get("Sign", type=str)
        arg_header_token = request.headers.get("token", type=str)

        ver = {
            "Ac_Code":arg_header_Ac_Code,
            "Sign": arg_header_Sign,
            "token": arg_header_token,
            "shop_id": args["shop_id"],
        }
        # 进行设备校验
        res = VerifyC().vericion(ver)
        if res:
            return res
        # 这个集合用于添加查询条件
        critern = set()
        if "productnames" in args:
            critern.add(ProductModel.product_name == args["productnames"])
        res = ProductModel().get_data(*critern,page = args["page"],page_size = args["page_size"])

        # 获取到分页的数据
        page = res.page
        per_page = res.per_page
        total = res.total

        result = []
        for r in res.items:
            result.append({
                "id": r.id,
                "version": r.version,
                "pro_sys": r.pro_sys,
                "opernation": r.opernation,
                "infos": r.infos,
                "product_name": r.product_name,
                "channel": r.channel,
            })
        return make_response(data=result,page=page,per_page=args["page_size"],total=total)


class ProductApiGetInfo(Resource):
    def get(self,id):
        productparser = RequestParser(trim=True)
        productparser.add_argument('shop_id', type=int)
        args = productparser.parse_args(strict=True)
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
        # 进行设备校验
        res = VerifyC().vericion(ver)
        if res:
            return res
        critern = set()
        if id is not None:
            critern.add(ProductModel.id == id)
        res = ProductModel().get_data_info(*critern)
        result = []
        for r in res:
            result.append({
                "id": r.id,
                "version": r.version,
                "pro_sys": r.pro_sys,
                "opernation": r.opernation,
                "infos": r.infos,
                "product_name": r.product_name,
                "channel": r.channel,
            })
        return result

class ProductApiPost(Resource):
    def post(self):
        # RequestParser使用它来对传递的参数进行解析，解析出来的数据会自动生成一个dict
        productparser = RequestParser(trim=True)
        productparser.add_argument('shop_id', type=int)
        productparser.add_argument('product_name', type=str)
        productparser.add_argument('version', type=str)
        productparser.add_argument('infos', type=str)
        productparser.add_argument('pro_sys', type=str)
        productparser.add_argument('channel', type=str)
        args = productparser.parse_args(strict=True)
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
        # 进行设备校验
        res = VerifyC().vericion(ver)
        if res:
            return res
        res = ProductModel().insert_data(args)
        if res is True:
            return {"code": 200, "success": True,"errormsg":"新增成功"}
        else:
            return {"errcode": 400, "success": False,"errormsg":"新增失败，请重新添加"}


class ProductApiPut(Resource):
    def put(self,id):
        # RequestParser使用它来对传递的参数进行解析，解析出来的数据会自动生成一个dict
        productparser = RequestParser(trim=True)
        productparser.add_argument('shop_id', type=int)
        productparser.add_argument('product_name', type=str)
        args = productparser.parse_args(strict=True)
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
        # 进行设备校验
        res = VerifyC().vericion(ver)
        if res:
            return res
        res = ProductModel().update_data(args,id)
        if res is True:
            return {"code": 200, "success": True,"errormsg":"修改成功"}
        else:
            return {"errcode": 400, "success": False, "errormsg": "修改失败，请查询字段等信息，重新修改"}


class ProductApiDel(Resource):
    def delete(self,id):
        # RequestParser使用它来对传递的参数进行解析，解析出来的数据会自动生成一个dict
        productparser = RequestParser(trim=True)
        productparser.add_argument('shop_id', type=int)
        args = productparser.parse_args(strict=True)
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
        # 进行设备校验
        res = VerifyC().vericion(ver)
        if res:
            return res

        res = ProductModel().delete_data(id)
        if res is True:
            return {"code": 200, "success": True,"errormsg":"删除成功"}
        else:
            return {"errcode": 400, "success": False, "errormsg": "删除失败"}