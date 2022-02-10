import time
from concurrent import futures

import grpc

import hello_bilibili_pb2 as pb2
import hello_bilibili_pb2_grpc as pb2_grpc


class Bilibili(pb2_grpc.BibiliServicer):
    def HelloDewei(self, request, context):
        name = request.name
        age = request.age

        if not name or not age:
            context.set_details('fuck xxx')
            context.set_code(grpc.StatusCode.DATA_LOSS)
            raise context

        context.set_trailing_metadata((('name', 'pig'), ('key', 'value')))
        headers = context.invocation_metadata()
        print(headers[0].key, headers[0].value)
        result = 'my name is {}, i am {} years old'.format(name, age)
        context.set_compression(grpc.Compression.Gzip)
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
        futures.ThreadPoolExecutor(max_workers=4),
        compression=grpc.Compression.Gzip,
        options=[
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024)
        ]
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
