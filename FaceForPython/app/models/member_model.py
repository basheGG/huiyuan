from . import db

class Members(db.Model):
    __tablename__ = 'offline_members'  # 表格名字
    # shop_id 和 number为复合主键
    shop_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    number = db.Column(db.String(255), nullable=False, primary_key=True)
    name = db.Column(db.String(255), default=None)
    phone = db.Column(db.String(255), default=None)
    gender = db.Column(db.String(255), default=None)
    birthday = db.Column(db.TIMESTAMP, default=None)
    we_chat = db.Column(db.String(255),default=None)
    integral = db.Column(db.BigInteger, default=0)
    consumption_time = db.Column(db.BigInteger, default=0)
    create_time = db.Column(db.TIMESTAMP, default=None)
    is_delete = db.Column(db.Integer, default=0)
    member_points = db.Column(db.FLOAT, default=0.0)
    balance = db.Column(db.FLOAT, default=0.0)



    def findByPhone(self, shop_id, phone):
        # 手机号是唯一值
        member = db.session.query(Members).filter_by(shop_id=shop_id, phone=phone).first()
        return member


    def createMember(self, member):
        try:
            db.session.add(member)
            db.session.commit()
            return 'Create OK'
        except:
            db.session.rollback()
            return 'Create False'


    def deleteMember(self, shop_id, number):
        # 删除为逻辑删除
        try:
            db.session.query(Members).filter(db.and_(Members.shop_id == shop_id, Members.number == number)).update({'is_delete': 1})
            db.session.commit()
            return 'Delete OK'
        except:
            db.session.rollback()
            return 'Delete FALSE'

    def updateMember(self, shop_id, number, member):
        try:
            db.session.query(Members).filter(db.and_(Members.shop_id == shop_id, Members.number == number)).update(member)
            db.session.commit()
            return 'Update OK'
        except:
            db.session.rollback()
            return 'Update False'

    def itemMember(self, shop_id, number):
        # 单条查询
        member = db.session.query(Members).filter_by(shop_id=shop_id, number=number).first()
        return member

    def listMember(self, shop_id, page, page_size):
        # 查询全部，不包括逻辑删除数据
        members = db.session.query(Members).filter_by(shop_id=shop_id, is_delete=0).paginate(int(page), int(page_size), False)

        return members


class Integral(db.Model):
    __tablename__ = 'integral_exchange_records'  # 积分表名
    id = db.Column(db.BigInteger, nullable=False, primary_key=True, autoincrement=True)     # 订单的ID
    created_at = db.Column(db.TIMESTAMP, default=None)
    updated_at = db.Column(db.TIMESTAMP, default=None)
    deleted_at = db.Column(db.TIMESTAMP, default=None)
    shop_id = db.Column(db.BigInteger, default=0)        # 对应商铺id
    number = db.Column(db.String(255), default=None)        # 对应会员的编码
    name = db.Column(db.String(255), default=None)          # 会员名称
    exchange_integral = db.Column(db.BigInteger, default=0)      # 兑换积分的值
    exchange_goods = db.Column(db.String(255), default=None)        # 积分兑换的商品
    remark = db.Column(db.String(255), default=None)   # 订单的备注
    exchange_time = db.Column(db.TIMESTAMP, default=None)  # 积分兑换时间
    phone = db.Column(db.String(255), default=None)
    exchange_num = db.Column(db.String(255), default=None)  # 积分兑换单号


    def get_list(self, shop_id, page, page_size):
        # 查询全部,并且实现分页
        integrals = db.session.query(Integral).filter_by(shop_id=shop_id).paginate(int(page), int(page_size), False)

        return integrals

    def get_info(self, shop_id, exchange_num):
        res = db.session.query(
            Integral,
            Members.integral
        ).filter(Integral.shop_id==shop_id, Integral.exchange_num==exchange_num)
        integral_query = res.outerjoin(Members,Integral.shop_id == Members.shop_id)
        integral = integral_query.first()
        return integral

    def Exchange(self, datas, integral_data):
        try:
            db.session.add(integral_data)
            db.session.commit()
            integral = datas["integral"]-datas["exchange_integral"]
            Members().updateMember(datas["shop_id"],datas["number"],{"integral":integral})
            return 'Exchange OK'
        except:
            db.session.rollback()
            return 'Exchange False'


    # def updateIntegral(self):
    #     pass
    #
    #
    # def deleteIntegral(self):
    #     pass

