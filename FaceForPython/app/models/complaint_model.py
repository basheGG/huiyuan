# -*- coding:utf-8 -*-

from . import db


class Complaint(db.Model):
    __tablename__ = 'offline_complaint'  # 表格名字
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    info = db.Column(db.Text)
    state = db.Column(db.Integer)
    creat_time = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    operation = db.Column(db.Integer)
    admin_id = db.Column(db.Integer)

    def get_data(self, page, page_size):
        data = db.session.query(Complaint).paginate(page, page_size)
        db.session.close()
        return data

    def search_data(self, parm, page, page_size):
        data = db.session.query(Complaint).filter(Complaint.info.like('%' + parm + '%')).paginate(page, page_size)
        db.session.close()
        return data

    def get_one(self, parm):
        data = db.session.query(Complaint).filter(Complaint.id == parm).first()
        db.session.close()
        return data

    def insert_data(self, data):
        try:
            obj = Complaint(**data)
            db.session.add(obj)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            db.session.rollback()
            db.session.close()

    def update_data(self, data, obj_id):
        try:
            db.session.query(Complaint).filter(Complaint.id == obj_id).update(data)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            db.session.rollback()
            db.session.close()

    def delete_data(self, obj_id):
        try:
            row = db.session.query(Complaint).filter(Complaint.id == obj_id).first()
            db.session.delete(row)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            db.session.rollback()
            db.session.close()
