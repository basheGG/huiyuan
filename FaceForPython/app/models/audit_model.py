# -*- coding:utf-8 -*-
from . import db


class AuditModel(db.Model):
    __tablename__ = 'offline_member_audit'  # 商户审核表
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),default=None)
    state = db.Column(db.Integer,default=None)
    audit_state = db.Column(db.Integer,default=None)
    email = db.Column(db.String(255),default=None)
    operaition = db.Column(db.Integer,default=None)

    def get_data(self,*critern):
        args = db.session.query(AuditModel).filter(*critern).all()
        db.session.close()
        return args

    def get_data_search(self,*critern, page, page_size):
        args = db.session.query(AuditModel).filter(*critern).paginate(int(page), int(page_size), False)
        db.session.close()
        return args


    def insert_data(self,datas):
        try:
            dao = AuditModel(**datas)
            db.session.add(dao)
            db.session.commit()
            db.session.close()
            return True
        except:
            db.session.rollback()
            db.session.close()


    def update_data(self,datas,id):
        try:
            db.session.query(AuditModel).filter(AuditModel.id == id).update(datas)
            db.session.commit()
            db.session.close()
            return True
        except:
            db.session.rollback()
            db.session.close()


    def delete_data(self,id):
        try:
            rows = db.session.query(AuditModel).filter(AuditModel.id == id).first()
            db.session.delete(rows)
            db.session.commit()
            db.session.close()
            return True
        except:
            db.session.rollback()
            db.session.close()
