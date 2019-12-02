import datetime
import random
import string

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request

from app.models.member_model import *
from app.common.verify_csld import VerifyC
from app.common.uils import make_response


class MemberApi(Resource):
    def __init__(self):
        self.memberparser = RequestParser(trim=True)
        self.memberparser.add_argument('shop_id', type=int)
        self.memberparser.add_argument("number", type=str)
        self.memberparser.add_argument('name', type=str)
        self.memberparser.add_argument('phone', type=str)
        self.memberparser.add_argument('gender', type=str)
        self.memberparser.add_argument('birthday', type=str)
        self.memberparser.add_argument('we_chat', type=str)
        self.memberparser.add_argument('page', type=int)
        self.memberparser.add_argument('size', type=int)
        self.memberparser.add_argument("money", type=float)
        self.args = self.memberparser.parse_args(strict=True)
        self.datas = {"token": request.headers.get('token'), "Sign": request.headers.get('sign'),
                      "Ac_Code": request.headers.get('Ac_Code'), "shop_id": self.args["shop_id"]}

    def is_connection(self):
        res = VerifyC().vericion(self.datas)
        if res is not None:
            if res["errcode"] == 4001:
                return {"message": "设备校验失败", "success": False, "errcode": -50}
            elif res["errcode"] == 4002:
                return {"message": "设备校验失败", "success": False, "errcode": -50}
            elif res["errcode"] == 4003:
                return {"message": "参数异常", "success": False, "errcode": -10}
            elif res["errcode"] == 4004:
                return {"message": " Token 无效", "success": False, "errcode": -20}
            elif res["errcode"] == 4005:
                return {"message": "shopID不能为空", "success": False, "errcode": -10}
            elif res["errcode"] == 4006:
                return {"message": " 通用错误", "success": False, "errcode": -1}
            elif res["errcode"] == 4007:
                return {"message": "设备校验失败", "success": False, "errcode": -50}
        return None


class FindMemberByPhone(MemberApi):

    def get(self):
        res = self.is_connection()
        if res is None:
            member = Members().findByPhone(self.args['shop_id'], self.args['phone'])
            if member.is_delete == 0:
                birthday = member.birthday.strftime('%Y-%m-%d')
                return ({
                    "shop_id": member.shop_id,
                    "number": member.number,
                    "name": member.name,
                    "phone": member.phone,
                    "gender": member.gender,
                    "birthday": birthday,
                    "we_chat": member.we_chat,
                    "integral": member.integral,
                    "consumption_time": member.consumption_time,
                    "create_time": member.create_time
                })
            else:
                return make_response(error_code=-1, error_message='ERROR The member may have been removed')
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


class CreateMember(MemberApi):

    def post(self):
        res = self.is_connection()
        if res is None:
            shop_id = self.args["shop_id"]
            name = self.args["name"]
            phone = self.args["phone"]
            gender = self.args["gender"]
            birthday = None if self.args["birthday"] is None else datetime.datetime.strptime(self.args["birthday"],
                                                                                             '%Y-%m-%d')
            we_chat = self.args["we_chat"]
            number = ''.join(random.sample(string.ascii_letters + string.digits, 9))
            create_time = datetime.datetime.now()
            if shop_id is not None:
                member = Members(shop_id=shop_id, number=number, name=name, phone=phone, gender=gender,
                                 birthday=birthday, we_chat=we_chat, create_time=create_time)
                flag = Members().createMember(member)
                return {"code": 200, "message": flag}
            else:
                return make_response(error_code=-2, error_message="shop_id cant't be None")
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


class DeleteMember(MemberApi):

    def delete(self):
        res = self.is_connection()
        if res is None:
            shop_id = int(self.args['shop_id'])
            number = self.args['number']
            flag = Members().deleteMember(shop_id, number)
            return {"code": 200, "message": flag}
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


class UpdateMember(MemberApi):

    def put(self):
        res = self.is_connection()
        if res is None:
            shop_id = self.args.pop('shop_id')
            number = self.args.pop("number")
            flag = Members().updateMember(shop_id, number, self.args)
            return {"code": 200, "message": flag}
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


class MemberInfo(MemberApi):

    def get(self):
        res = self.is_connection()
        if res is None:
            shop_id = self.args['shop_id']
            number = self.args['number']
            member = Members().itemMember(shop_id, number)
            if member.is_delete == 0:
                birthday = member.birthday.strftime('%Y-%m-%d')
                result = {
                    "shop_id": member.shop_id,
                    "number": member.number,
                    "name": member.name,
                    "phone": member.phone,
                    "gender": member.gender,
                    "birthday": birthday,
                    "we_chat": member.we_chat,
                    "integral": member.integral,
                    "consumption_time": member.consumption_time,
                    "create_time": member.create_time
                }
                return make_response(code=200, message='itemInfo already', data=result)
            else:
                return make_response(error_code=-1, error_message='ERROR The member may have been removed')
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


class MemberList(MemberApi):
    def get(self):
        res = self.is_connection()
        if res is None:
            shop_id = self.args['shop_id']
            page = self.args['page']
            page_size = self.args['size']
            m_args = Members().listMember(shop_id, page, page_size)
            print(m_args.__dict__)
            result = []
            total_pages = int(m_args.total / page_size) + 1
            for i in m_args.items:
                result.append({
                    "number": i.number,
                    "name": i.name,
                    "phone": i.phone,
                    "integral": i.integral
                })
            return make_response(code=200, message='list already', page=page, total_pages=total_pages, data=result)
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


class IntegralApi(Resource):
    def __init__(self):
        self.memberparser = RequestParser(trim=True)
        self.memberparser.add_argument('shop_id', type=int)
        self.memberparser.add_argument("number", type=str)
        self.memberparser.add_argument('name', type=str)
        self.memberparser.add_argument('id', type=str)
        self.memberparser.add_argument('exchange_integral', type=int)
        self.memberparser.add_argument('exchange_good', type=str)
        self.memberparser.add_argument('remark', type=str)
        self.memberparser.add_argument('exchange_num', type=str)
        self.memberparser.add_argument('money', type=float)
        self.memberparser.add_argument('integral', type=int)
        self.memberparser.add_argument('member_points', type=float)
        self.memberparser.add_argument('page', type=int)
        self.memberparser.add_argument('size', type=int)

        self.args = self.memberparser.parse_args(strict=True)
        self.datas = {"token": request.headers.get('token'), "Sign": request.headers.get('sign'),
                      "Ac_Code": request.headers.get('Ac_Code'), "shop_id": self.args["shop_id"]}

    def is_connection(self):
        res = VerifyC().vericion(self.datas)
        if res is not None:
            if res["errcode"] == 4001:
                return {"message": "设备校验失败", "success": False, "errcode": -50}
            elif res["errcode"] == 4002:
                return {"message": "设备校验失败", "success": False, "errcode": -50}
            elif res["errcode"] == 4003:
                return {"message": "参数异常", "success": False, "errcode": -10}
            elif res["errcode"] == 4004:
                return {"message": " Token 无效", "success": False, "errcode": -20}
            elif res["errcode"] == 4005:
                return {"message": "shopID不能为空", "success": False, "errcode": -10}
            elif res["errcode"] == 4006:
                return {"message": " 通用错误", "success": False, "errcode": -1}
            elif res["errcode"] == 4007:
                return {"message": "设备校验失败", "success": False, "errcode": -50}
        return None


class IntegralExchangeInfo(IntegralApi):
    def get(self):
        res = self.is_connection()
        if res is None:
            shop_id = self.args['shop_id']
            exchange_num = self.args['exchange_num']
            integral = Integral().get_info(shop_id, exchange_num)
            if integral is not None:
                exchange_time = integral[0].exchange_time.strftime('%Y-%m-%d %H:%M:%S')
                result = {
                    "id": integral[0].id,
                    "shop_id": integral[0].shop_id,
                    "number": integral[0].number,
                    "name": integral[0].name,
                    "exchange_num": integral[0].exchange_num,
                    "exchange_integral": integral[0].exchange_integral,
                    "exchange_good": integral[0].exchange_goods,
                    "exchange_time": exchange_time,
                    "integral": integral[1],
                    "remark": integral[0].remark
                }
                return make_response(code=200, message='itemInfo already', data=result)
            else:
                return make_response(error_code=-3, error_message='ERROR The Integral may have been removed')
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


class IntegralExchangeList(IntegralApi):
    def get(self):
        res = self.is_connection()
        if res is None:
            shop_id = self.args['shop_id']
            page = self.args['page']
            page_size = self.args['size']
            I_args = Integral().get_list(shop_id, page, page_size)
            result = []
            total_pages = int(I_args.total / page_size) + 1
            for i in I_args.items:
                exchange_time = i.exchange_time.strftime('%Y-%m-%d %H:%M:%S')
                result.append({
                    "shop_id": i.shop_id,
                    "number": i.number,
                    "name": i.name,
                    "exchange_integral": i.exchange_integral,
                    "exchange_goods": i.exchange_goods,
                    "remark": i.remark,
                    "exchange_time": exchange_time
                })
            return make_response(code=200, message='list already', page=page, total_pages=total_pages, data=result)
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


class IntegralExchange(IntegralApi):
    def post(self):
        res = self.is_connection()
        if res is None:
            shop_id = self.args["shop_id"]
            number = self.args["number"]
            name = self.args["name"]
            exchange_integral = self.args["exchange_integral"]
            exchange_goods = self.args["exchange_good"]
            remark = self.args["remark"]
            exchange_num = ''.join(random.sample(string.ascii_letters + string.digits, 6))
            exchange_time = datetime.datetime.now()
            member = Members().itemMember(shop_id, number)
            if member:
                if member.is_delete == 0:
                    integral = Integral(shop_id=shop_id, number=number, name=name, exchange_goods=exchange_goods,
                                        remark=remark,
                                        exchange_integral=exchange_integral, exchange_num=exchange_num,
                                        exchange_time=exchange_time)

                    flag = Integral().Exchange(self.args, integral)
                    return {"code": 200, "message": flag}
                else:
                    message = "ERROR The member may have been removed"
                    return make_response(error_code=-4, error_message=message)
            else:
                return make_response(error_code=-5, error_message='ERROR wrong shop_id or number')
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


class SettingIntegral(IntegralApi):
    def post(self):
        shop_id = self.args["shop_id"]
        number = self.args["number"]
        money = self.args["money"]
        # integral = self.args["integral"]
        member_points = self.args["member_points"]
        member = Members().itemMember(shop_id, number)
        if member:
            if member.is_delete == 0:
                new_integral = money * member_points + member.integral
                new_balance = member.balance - money
                Members().updateMember(shop_id, number, {"integral": new_integral, "balance": new_balance})
                return {"code": 200, "message": 'successful setting!'}
            else:
                return make_response(error_code=-1, error_message='ERROR The member may have been removed')
        else:
            return make_response(error_code=-5, error_message='ERROR wrong shop_id or number')

        


