import time
from concurrent import futures

import grpc

import hello_bilibili_pb2 as pb2
import hello_bilibili_pb2_grpc as pb2_grpc


class Bilibili(pb2_grpc.BibiliServicer):
    def HelloDewei(self, request, context):
        name = request.name
        age = request.age

        result = 'my name is {}, i am {} years old'.format(name, age)
        return pb2.HelloDeweiReply(result=result)

    def TestClientRecvStream(self, request, context):
        index = 0
        while context.is_active():
            data = request.data
            if data == 'close':
                print('data is close, request wil cancel')
                context.cancel()
            time.sleep(1)
            index += 1
            result = 'send {} {}'.format(index, data)
            print(result)
            yield pb2.TestClientRecvStreamResponse(
                result=result
            )

    def TestClientSendStream(self, request_iterator, context):
        index = 0
        for request in request_iterator:
            print(request.data, ':', index)
            if index == 10:
                break
            index += 1

        return pb2.TestClientSendStreamResponse(result='ok')

    def TestTwoWayStream(self, request_iterator, context):
        index = 0
        for request in request_iterator:
            data = request.data

            if index == 3:
                time.sleep(15)
            index += 1
            yield pb2.TestTwoWayStreamResponse(result='service send client {}'.format(data))


def run():
    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4)
    )
    pb2_grpc.add_BibiliServicer_to_server(Bilibili(), grpc_server)
    grpc_server.add_insecure_port('0.0.0.0:5000')
    print('server will start at 0.0.0.0:5000')
    grpc_server.start()

    try:
        while 1:
            time.sleep(3600)
    except KeyboardInterrupt:
        grpc_server.stop(0)


if __name__ == '__main__':
    run()
