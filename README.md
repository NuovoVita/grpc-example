gen code
```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. hello_bilibili.proto
```

use
```
python service.py
python client.py
```
