from flask import Blueprint

member_blueprint = Blueprint('member', __name__)


@member_blueprint.before_request
def before_request():
    pass

@member_blueprint.after_request
def after_request(response):
    return response


from flask_restful import Api
api = Api(member_blueprint)


# 移动应用管理接口
from app.api_csld.product_csld import (
    ProductApiGet,
    ProductApiGetInfo,
    ProductApiPost,
    ProductApiPut,
    ProductApiDel
)
api.add_resource(ProductApiGet, '/product/get')
api.add_resource(ProductApiGetInfo, '/product/info/<int:id>')
api.add_resource(ProductApiPost, '/product/post')
api.add_resource(ProductApiPut, '/product/put/<int:id>')
api.add_resource(ProductApiDel, '/product/del/<int:id>')

from app.api_csld.member_csld import *
api.add_resource(FindMemberByPhone, '/merchants/member/findByPhone')        # 根据手机号查找会员
api.add_resource(CreateMember, '/merchants/member/createMember')        # 添加会员
api.add_resource(DeleteMember, '/merchants/member/deleteMember')        # 删除会员
api.add_resource(UpdateMember, '/merchants/member/updateMember')        # 修改会员资料
api.add_resource(MemberInfo, '/merchants/member/item')      # 会员详情（单条）
api.add_resource(MemberList, '/merchants/member/list')      # 会员列表
api.add_resource(IntegralExchangeList, '/merchants/integral/list')      # 积分兑换记录列表
api.add_resource(IntegralExchangeInfo, '/merchants/integral/item')      # 积分兑换记录详情
api.add_resource(IntegralExchange, '/merchants/integral/exchange')       # 积分兑换
api.add_resource(SettingIntegral, '/merchants/integral/setting')        # 积分设置

from app.api_csld.complaint_csld import *

api.add_resource(ComplaintListHandler, '/complaint/list/')      # 获取所有投诉内容
api.add_resource(ComplaintSearchHandler, '/complaint/search/')    # 按投诉内容搜索投诉内容
api.add_resource(ComplaintInfoHandler, '/complaint/info/<int:id>')      # 获取单条投诉内容详细信息
api.add_resource(ComplaintCreateHandler, '/complaint/create/')    # 创建投诉内容
api.add_resource(ComplaintUpdateHandler, '/complaint/update/<int:id>')    # 修改投诉内容
api.add_resource(ComplaintDeleteHandler, '/complaint/delete/<int:id>')    # 删除投诉内容

#用户审核
from app.api_csld.audit_csld import *

api.add_resource(AuditApi, '/auditlist') #用户审核详情列表
api.add_resource(SearchAudit, '/searchaudit') #搜索查询
api.add_resource(IntoAudit, '/intoaudit') # 添加审核用户*
api.add_resource(UpdataAudit, '/updataaudit/<int:id>') # 修改审核用户
api.add_resource(DeleteAudit, '/deleteaudit/<int:id>') #删除审核用户


from app.api_csld.recharge_order_csld import *

# 充值订单
api.add_resource(RechargeOrderList, '/recharge_order/list/')                # 订单详情列表
api.add_resource(RechargeOrderInfo, '/recharge_order/info/<int:id>')        # 获取订单详情
api.add_resource(RechargeOrderCreate, '/recharge_order/create/')            # 创建订单
api.add_resource(RechargeOrderDelete, '/recharge_order/delete/<int:id>')    # 删除订单
