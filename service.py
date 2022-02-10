import time

import grpc
import hello_bilibili_pb2 as pb2
import hello_bilibili_pb2_grpc as pb2_grpc

from concurrent import futures


class Bilibili(pb2_grpc.BibiliServicer):
    def HelloDewei(self, request, context):
        name = request.name
        age = request.age

        result = 'my name is {}, i am {} years old'.format(name, age)
        return pb2.HelloDeweiReply(result=result)


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
