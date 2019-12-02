import time
import grpc
import consul
from concurrent import futures

from app.grpc_server.protos import product_pb2
from app.grpc_server.protos import product_pb2_grpc
import json
import MySQLdb
from app.grpc_server.config_cur import curs_db




class AService(product_pb2_grpc.AServiceServicer):
    def __init__(self):
        self.db_args = curs_db()
    def TestVerificationCode(self, request, context):
        print("成功进入TestVerificationCode")
        result = []
        # 建立与数据库的连接
        print('*************************************建立与数据库的连接*************************************************')
        conn = MySQLdb.connect(host=self.db_args['DBHOST'], user=self.db_args['DBUSER'], passwd=self.db_args['DBPASSWD'], db=self.db_args['DB'], port=self.db_args['PORT'], charset=self.db_args['CHARSET'])
        cur = conn.cursor()  # 建立游标，Python是通过游标执行SQL语句
        cur.execute("""select * from offline_product;""")
        args = cur.fetchall()
        # 语句结束关闭游标
        for r in args:
            result.append({
                "id": r[0],
                "version": r[1],
                "pro_sys": r[2],
                "opernation":r[3],
                "infos": r[4],
                "product_name": r[5],
                "channel": r[6],
            })
        result = json.dumps(result)
        return product_pb2.TestVerificationCodeResponse(
            username = result,
            phone ="1",
            email ="2"
        )

    def IntegralChange(self, request, context):
        print('---------------------------------------------------------------------------------------------------------')
        print("IntegralChange")
        order_number = request.order_number
        result = []
        # 建立与数据库的连接
        conn = MySQLdb.connect(host=self.db_args['DBHOST'], user=self.db_args['DBUSER'],
                               passwd=self.db_args['DBPASSWD'], db=self.db_args['DB'], port=self.db_args['PORT'],
                               charset=self.db_args['CHARSET'])
        cur = conn.cursor()  # 建立游标，Python是通过游标执行SQL语句
        str_cur_get = """SELECT state,amount,member_number,shop_id FROM offline_recharge_order WHERE merchant_number = %s;"""%order_number

        cur.execute(str_cur_get)
        args = cur.fetchall()
        # 语句结束关闭游标
        if bool(args):
            state = args[0][0]
            amount = args[0][1]
            member_number = args[0][2]
            shop_id = args[0][3]
            if state != 1:
                return product_pb2.IntegralChangeResponse(
                    success=False,
                    message="该订单状态错误，请检查订单状态在重新执行"
                )
        else:
            return product_pb2.IntegralChangeResponse(
                success=False,
                message="该订单号错误，请检查后在执行"
            )
        return self.IntegralUpdate(order_number,amount,member_number,shop_id)



    def IntegralUpdate(self,order_number,amount,member_number,shop_id):
        conn = MySQLdb.connect(host=self.db_args['DBHOST'], user=self.db_args['DBUSER'],
                               passwd=self.db_args['DBPASSWD'], db=self.db_args['DB'], port=self.db_args['PORT'],
                               charset=self.db_args['CHARSET'])
        cur = conn.cursor()  # 建立游标，Python是通过游标执行SQL语句
        try:
            str_cur_update = """update offline_recharge_order SET state = 2 , update_time = current_timestamp() WHERE merchant_number = %s;""" % order_number
            cur.execute(str_cur_update)
            print('**********************************开始执行更新语句***************************************************')
            str_cur_get_amount = """select balance  from offline_members  WHERE number = %s and shop_id = %s;""" % (member_number, shop_id)
            print('**********************************开始执行查询语句***************************************************')
            cur.execute(str_cur_get_amount)
            a_mem_amount = cur.fetchall()
            balance = a_mem_amount[0][0]
            balance_sum = balance + amount
            print('**********************************开始执会员余额更新语句***************************************************')
            str_cur_udt_amount = """update offline_members SET balance = %s WHERE number = %s and shop_id = %s;"""%(balance_sum,member_number, shop_id)
            cur.execute(str_cur_udt_amount)
            conn.commit()
        except:
            conn.rollback()
        # 语句结束关闭游标
        conn.close()
        print('---------------------------------------------------------------------------------------------------------')
        return product_pb2.IntegralChangeResponse(
            success=True,
            message="成功更新"
        )




def register(server_name, ip, port):
    c = consul.Consul()  # 连接consul 服务器，默认是127.0.0.1，可用host参数指定host
    print(f"开始注册服务{server_name}")
    check = consul.Check.tcp(ip, port, "10s")  # 健康检查的ip，端口，检查时间
    c.agent.service.register(server_name, f"{server_name}-{ip}-{port}", address=ip, port=port, check=check)  # 注册服务部分
    print(f"注册服务{server_name}成功")


def unregister(server_name, ip, port):
    c = consul.Consul()
    print(f"开始退出服务{server_name}")
    c.agent.service.deregister(f'{server_name}-{ip}-{port}')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_AServiceServicer_to_server(AService(), server)
    server.add_insecure_port('[::]:{}'.format(8967))
    register("com.bbc", "127.0.0.1", 8967)
    server.start()
    try:
        while True:
            time.sleep(186400)
    except KeyboardInterrupt:
        unregister("order_server", "127.0.0.1", 8967)
        server.stop(0)

if __name__ == '__main__':
    serve()