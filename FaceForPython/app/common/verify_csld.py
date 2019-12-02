import json
from app.common.uils import DeviceSign,GetConsul,GetShebei
from app.common.redis_token import Token

class VerifyC():

    def vericion(self,data_dict):
        Sign = data_dict["Sign"]
        if data_dict["Ac_Code"] is not None:

            # 开始验证AC_CODE
            AC_CODE = data_dict["Ac_Code"]
            args = GetConsul().get_data(AC_CODE)
            res = DeviceSign(IMEI=args["IMEI"], MAC=args["MAC"], Timestamp=args["Timestamp"]).Sign()
            if Sign == res:
                shop_id = args["shopID"]
                merchart_Id = args["merchartId"]
                if shop_id == 0:
                    return {"message": "该设备未绑定", "success": False, "errcode": 4001}
                if merchart_Id == 0:
                    return {"message": "该设备未注册", "success": False, "errcode": 4002}
            else:
                return {"message": "sign错误", "success": False, "errcode": 4003}
        else:
            if "token" in data_dict and "shop_id" in data_dict:
                token = data_dict["token"]
                shop_id = data_dict["shop_id"]
                if token is None:
                    return {"message": "token不能为空", "success": False, "errcode": 4004}
                elif shop_id is None:
                    return {"message": "shopID不能为空", "success": False, "errcode": 4005}
                else:
                    res_token = Token().LoadToken(token)
                    # 开始进行设备验证
                    sbid = GetShebei().get_data(res_token.Id, shop_id)
                    if sbid != True:
                        return {"message": "该设备不存在", "success": False, "errcode": 4007}
            else:
                return {"message": "不能为空", "success": False, "errcode": 4006}