import grpc

import hello_bilibili_pb2 as pb2
import hello_bilibili_pb2_grpc as pb2_grpc


def run():
    conn = grpc.insecure_channel('0.0.0.0:5000')
    client = pb2_grpc.BibiliStub(channel=conn)
    response = client.HelloDewei(
        pb2.HelloDeweiReq(
            name='dewei',
            age=33
        )
    )
    print(response.result)


if __name__ == '__main__':
    run()
