# -*- coding:utf-8 -*-

from . import db


class RechargeOrder(db.Model):
    __tablename__ = 'offline_recharge_order'  # 表格名字
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    shop_id = db.Column(db.Integer)
    amount = db.Column(db.FLOAT, default=0.0, comment='充值金额')
    give_amount = db.Column(db.FLOAT, default=0.0, comment='赠送金额')
    create_time = db.Column(db.DateTime, default=None, comment='创建时间')
    update_time = db.Column(db.DateTime, default=None, comment='更新时间')
    state = db.Column(db.INTEGER,default=0, comment='订单状态')
    order_number = db.Column(db.String(255), default=None, comment='订单编号')
    shop_number = db.Column(db.String(255), default=None, comment='商铺编号')
    channel = db.Column(db.String(255), default=None, comment='渠道')
    remark = db.Column(db.String(255), default=None, comment='备注')
    integral = db.Column(db.String(255), default=None, comment='赠送积分')

    def get_data(self, page, page_size):
        data = db.session.query(RechargeOrder).paginate(page, page_size)
        db.session.close()
        return data

    def get_one(self, obj_id):
        data = db.session.query(RechargeOrder).filter(RechargeOrder.id == obj_id).first()
        db.session.close()
        return data

    def insert_data(self, data):
        try:
            obj = RechargeOrder(**data)
            db.session.add(obj)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.close()

    def delete_data(self, obj_id):
        try:
            row = db.session.query(RechargeOrder).filter(RechargeOrder.id == obj_id).first()
            db.session.delete(row)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            db.session.rollback()
            db.session.close()
