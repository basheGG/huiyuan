# -*- coding:utf-8 -*-

import time, uuid
from app.common.verify_csld import VerifyC
from app.common.verify_header import verify_header
from app.models.recharge_order_model import RechargeOrder
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import request


class RechargeOrderList(Resource):

    def get(self):
        parser = RequestParser(trim=True)
        parser.add_argument('page', type=int)
        parser.add_argument('page_size', type=int)
        parser.add_argument('shop_id', type=int)
        args = parser.parse_args(strict=True)
        verify_header(args, request)
        print(verify_header(args, request))
        row = RechargeOrder().get_data(args['page'], args['page_size'])
        result = []
        for r in row.items:
            create_time = r.create_time.strftime('%Y-%m-%d %H:%M:%S')
            result.append({
                "id": r.id,
                "give_amount": r.give_amount,
                "create_time": create_time
            })
        return {'message': '成功', 'success': True, 'code': 200, 'data': result}


class RechargeOrderInfo(Resource):

    def get(self, id):
        parser = RequestParser(trim=True)
        parser.add_argument('shop_id', type=int)
        args = parser.parse_args(strict=True)
        verify_header(args, request)
        print(verify_header(args, request))
        row = RechargeOrder().get_one(id)
        create_time = row.create_time.strftime('%Y-%m-%d %H:%M:%S')
        result = {'id': row.id, 'give_amount': row.give_amount, 'create_time': create_time}
        return {'message': '成功', 'success': True, 'code': 200, 'data': result}


class RechargeOrderCreate(Resource):

    def post(self):
        parser = RequestParser(trim=True)
        parser.add_argument('amount', type=float)
        parser.add_argument('give_amount', type=float)
        parser.add_argument('remark', type=str)
        parser.add_argument('shop_id', type=int)
        args = parser.parse_args(strict=True)
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        args['create_time'] = create_time
        args['update_time'] = update_time
        args['state'] = 0
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        args['order_number'] = suid
        args['shop_number'] = 1
        args['channel'] = '充值'
        args['integral'] = 1
        if args['amount'] is None or args['give_amount'] is None or args['remark'] is None or args['shop_id'] is None:
            return {'message': '参数错误', 'success': False, 'code': -10}
        verify_header(args, request)
        print(verify_header(args, request))
        res = RechargeOrder().insert_data(args)
        if res:
            return {'message': '成功', 'success': True, 'code': 200}
        else:
            return {'message': '失败', 'success': False, 'code': -1}


class RechargeOrderDelete(Resource):

    def delete(self, id):
        parser = RequestParser(trim=True)
        parser.add_argument('shop_id', type=int)
        args = parser.parse_args(strict=True)
        verify_header(args, request)
        print(verify_header(args, request))
        res = RechargeOrder().delete_data(id)
        if res:
            return {'message': '成功', 'success': True, 'code': 200}
        else:
            return {'message': '失败', 'success': False, 'code': -1}
