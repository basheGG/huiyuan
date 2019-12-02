# -*- coding:utf-8 -*-

import time
from app.models.complaint_model import Complaint
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request
from app.common.uils import make_response


class ComplaintListHandler(Resource):

    def get(self):
        parser = RequestParser(trim=True)
        parser.add_argument('page', type=int)
        parser.add_argument('page_size', type=int)
        args = parser.parse_args(strict=True)
        row = Complaint().get_data(args['page'], args['page_size'])
        result = []
        for r in row.items:
            result.append({
                "id": r.id,
                "info": r.info,
                "phone": r.phone
            })
        return {'message': '成功', 'success': True, 'code': 200, 'data': result}


class ComplaintSearchHandler(Resource):

    def get(self):
        parser = RequestParser(trim=True)
        parser.add_argument('search', type=str)
        parser.add_argument('page', type=int)
        parser.add_argument('page_size', type=int)
        args = parser.parse_args(strict=True)
        row = Complaint().search_data(args['search'], args['page'], args['page_size'])
        result = []
        for r in row.items:
            result.append({
                "id": r.id,
                "info": r.info,
                "phone": r.phone
            })
        return {'message': '成功', 'success': True, 'code': 200, 'data': result}


class ComplaintInfoHandler(Resource):

    def get(self, id):
        rows = Complaint().get_one(id)
        result = {'id': rows.id, 'info': rows.info, 'phone': rows.phone}
        return {'message': '成功', 'success': True, 'code': 200, 'data': result}


class ComplaintCreateHandler(Resource):

    def post(self):
        parser = RequestParser(trim=True)
        parser.add_argument('info', type=str)
        parser.add_argument('phone', type=str)
        args = parser.parse_args(strict=True)
        creat_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        args['creat_time'] = creat_time
        args['state'] = 0
        args['operation'] = 0
        args['admin_id'] = 1
        if 'info' not in args.keys() or 'phone' not in args.keys():
            return {'message': '参数错误', 'success': False, 'code': -10}
        res = Complaint().insert_data(args)
        if res:
            return {'message': '成功', 'success': True, 'code': 200}
        else:
            return {'message': '失败', 'success': False, 'code': -1}


class ComplaintUpdateHandler(Resource):

    def put(self,id):
        parser = RequestParser(trim=True)
        parser.add_argument('info', type=str)
        parser.add_argument('phone', type=str)
        args = parser.parse_args(strict=True)
        args['state'] = 1
        args['operation'] = 1
        if 'info' not in args.keys() or 'phone' not in args.keys():
            return {'message': '参数错误', 'success': False, 'code': -10}
        res = Complaint().update_data(args, id)
        if res:
            return {'message': '成功', 'success': True, 'code': 200}
        else:
            return {'message': '失败', 'success': False, 'code': -1}


class ComplaintDeleteHandler(Resource):

    def delete(self, id):
        res = Complaint().delete_data(id)
        if res:
            return {'message': '成功', 'success': True, 'code': 200}
        else:
            return {'message': '失败', 'success': False, 'code': -1}

