from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request
from app.models.audit_model import AuditModel
from app.common.uils import make_response
from app.common.verify_csld import VerifyC

from app.models.member_model import *



class AllAuditApi(Resource):
    def __init__(self):
        self.auditdata = RequestParser(trim=True)
        self.auditdata.add_argument('page', type=int)
        self.auditdata.add_argument('page_size', type=int)
        self.auditdata.add_argument('username', type=str)
        self.auditdata.add_argument('state', type=int)
        self.auditdata.add_argument('audit_state', type=int)
        self.auditdata.add_argument('email', type=str)
        self.auditdata.add_argument('operaition', type=int)
        self.args = self.auditdata.parse_args(strict=True)
        print("body传递过来的数据：",self. args)

        self.arg_header_Ac_Code = request.headers.get("Ac_Code", type=int)
        self.arg_header_Sign = request.headers.get("sign", type=str)
        self.arg_header_token = request.headers.get("token", type=int)
        self.arg_header_shop_id = request.headers.get("shop_id",type=int)

        self.datas = {
            "Ac_Code": self.arg_header_Ac_Code,
            "Sign": self.arg_header_Sign,
            "token": self.arg_header_token,
            "shop_id":self.arg_header_shop_id
        }

    def is_connection(self):
        datas = self.datas
        print("验证的数据：",datas)
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

# 详情列表
class AuditApi(AllAuditApi):
    def get(self):
        res = self.is_connection()
        if res is None:
            critern = set()
            ress = AuditModel().get_data(*critern)
            result = []
            for r in ress:
                result.append({
                    "id": r.id,
                    "username": r.username,
                    "state": r.state,  # 开通类别
                    "audit_state": r.audit_state,  # 审核状态
                    "email": r.email,
                    "operaition": r.operaition,  # 操作
                })
            print("详情列表：", result)
            if result:
                return {'msg': '详情列表查询成功', 'success': True, 'code': 200, 'data': result}
            else:
                return {"errcode": 400, "success": False, "errormsg": "详情列表查询失败"}
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


#搜索查询
class SearchAudit(AllAuditApi):
    def get(self):
        res = self.is_connection()
        if res is None:
            critern = set()
            if "auditnames" in self.args:
                critern.add(AuditModel.username == self.args["auditnames"])
            ress = AuditModel().get_data_search(*critern,page = self.args["page"],page_size = self.args["page_size"])
            # 获取到分页的数据
            page = ress.page
            per_page = ress.per_page
            print(per_page)
            total = ress.total

            result = []
            for r in ress.items:
                result.append({
                    "id": r.id,
                    "username": r.username,
                    "state": r.state,  # 开通类别
                    "audit_state": r.audit_state,  # 审核状态
                    "email": r.email,
                    "operaition": r.operaition,  # 操作
                })
            print(result)
            return make_response(data=result,page=page,per_page=self.args["page_size"],total=total)
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])


# 添加审核用户
class IntoAudit(AllAuditApi):
    def post(self):
        res = self.is_connection()
        if res is None:
            insert_datas = {
                "username":self.args["username"],
                "state" : self.args["state"],
                "audit_state" :self.args["audit_state"],
                "email": self.args["email"],
                "operaition" : self.args["operaition"]
            }
            ress = AuditModel().insert_data(insert_datas)
            if ress is True:
                return {"code": 200, "success": True, "msg": "新增成功"}
            else:
                return {"errcode": 400, "success": False, "errormsg": "新增失败，请重新添加"}
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])

# 修改审核用户
class UpdataAudit(AllAuditApi):
    def put(self,id):
        res = self.is_connection()
        if res is None:
            auditdata = RequestParser(trim=True)
            auditdata.add_argument('username', type=str)
            auditdata.add_argument('state', type=int)
            auditdata.add_argument('audit_state', type=int)
            auditdata.add_argument('email', type=str)
            auditdata.add_argument('operaition', type=int)
            args = auditdata.parse_args(strict=True)
            res = AuditModel().update_data(args, id)
            if res is True:
                return {"code": 200, "success": True, "msg": "修改成功"}
            else:
                return {"errcode": 400, "success": False, "errormsg": "修改失败，请查询字段等信息，重新修改"}
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])

#删除审核用户
class DeleteAudit(AllAuditApi):
    def delete(self,id):
        res = self.is_connection()
        if res is None:
            ress = AuditModel().delete_data(id)
            if ress is True:
                return {"code": 200, "success": True, "msg": "删除成功"}
            else:
                return {"errcode": 400, "success": False, "errormsg": "删除失败"}
        else:
            return make_response(error_code=res["errcode"], error_message=res["message"])
