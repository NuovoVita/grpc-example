import random
import time

import grpc

import hello_bilibili_pb2 as pb2
import hello_bilibili_pb2_grpc as pb2_grpc


def test():
    index = 0
    while 1:
        time.sleep(1)
        data = str(random.random())
        if index == 5:
            break
        print(index)
        index += 1
        yield pb2.TestClientSendStreamRequest(data=data)


def run():
    conn = grpc.insecure_channel('0.0.0.0:5000')
    client = pb2_grpc.BibiliStub(channel=conn)
    # response = client.HelloDewei(
    #     pb2.HelloDeweiReq(
    #         name='dewei',
    #         age=33
    #     )
    # )
    # print(response.result)

    # response = client.TestClientRecvStream(pb2.TestClientRecvStreamReq(data='dewei'))
    # for item in response:
    #     print item.result

    response = client.TestClientSendStream(test())
    print(response.result)


if __name__ == '__main__':
    run()
