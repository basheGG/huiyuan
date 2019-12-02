import consul
import grpc
import time

from app.grpc_server.protos import product_pb2
from app.grpc_server.protos import product_pb2_grpc
from app.common.con_port_consul import config

c = consul.Consul(host=config.consul.host, port=config.consul.port, scheme='http')


def test_demo():
    channel = grpc.insecure_channel(findSMSServiceAddress())
    stub = product_pb2_grpc.AServiceStub(channel)
    response = stub.TestVerificationCode(product_pb2.TestVerificationCodeRequest(phone="18132568795"))
    print("发送结果 {}".format(response.username))

def test_demo_integral():
    channel = grpc.insecure_channel(findSMSServiceAddress())
    stub = product_pb2_grpc.AServiceStub(channel)
    print('------------------------------------------------test_demo_integral----------------------------------------------------------')
    response = stub.IntegralChange(product_pb2.IntegralChangeRequest(order_number="123456789"))
    print('------------------------------------------------test_demo_integral----------------------------------------------------------')
    print("发送结果 {},返回信息 {}".format(response.success,response.message))



def findSMSServiceAddress():
    return findServiceByAddress('com.bbc')


def findServiceByAddress(service):
    global c
    data = c.catalog.service(service)
    for value in data[1]:
        return "{address}:{port}".format(address=value['ServiceAddress'], port=value['ServicePort'])


if __name__ == '__main__':
    test_demo()
    test_demo_integral()