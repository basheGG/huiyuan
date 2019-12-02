from . import db
from flask_restful import abort

class ProductModel(db.Model):
    __tablename__ = 'offline_product'  # 表名字
    id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(20))
    version = db.Column(db.String(20),default=None)
    infos = db.Column(db.String(20),default=None)
    pro_sys = db.Column(db.String(20),default=None)
    channel = db.Column(db.String(20),default=None)
    opernation = db.Column(db.Integer,default=None)

    def get_data(self,*critern,page,page_size):
        args = db.session.query(ProductModel).filter(*critern).paginate(int(page), int(page_size),False)
        db.session.close()
        return args


    def get_data_info(self,*critern):
        args = db.session.query(ProductModel).filter(*critern).all()
        db.session.close()
        return args

    def insert_data(self,datas):

        try:
            dao = ProductModel(**datas)
            db.session.add(dao)
            db.session.commit()
            db.session.close()
            print('新增成功')
            return True
        except:
            db.session.rollback()
            db.session.close()
            abort(500)
            print('新增失败')


    def update_data(self,datas,id):
        try:
            db.session.query(ProductModel).filter(ProductModel.id == id).update(datas)
            db.session.commit()
            db.session.close()
            return True
        except:
            db.session.rollback()
            db.session.close()

    def delete_data(self,id):
        try:
            """删除数据，默认开始事务"""
            rows = db.session.query(ProductModel).filter(ProductModel.id == id).first()
            db.session.delete(rows)
            db.session.commit()
            db.session.close()
            return True
        except:
            db.session.rollback()
            db.session.close()
