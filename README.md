### gen code

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. hello_bilibili.proto
```

### use

```bash
python service.py
python client.py
```

### support

  grpcio-tools==1.41.1 这个版本对应的 protobuf-3.17.3，最后的一个支持 Python2 的库。


### Reference
- [常用 Git 场景命令](/notes/git.md)
