server-sdk-python
=================

Rong Cloud Server SDK in Python.

# 更新说明

* 20150206
* 去掉可能会导致SSL验证失败的代码
* 更改环境变量名称，老的环境变量名称在某些操作系统中无法被识别


# 依赖说明
* 本sdk 依赖于requests

# 使用说明

```
import os
import json
import unittest
import logging

from rong import ApiClient

app_key = ""
app_secret = ""

#您应该将key 和 secret 保存在服务器的环境变量中    
os.environ.setdefault('rongcloud_app_key', app_key)
os.environ.setdefault('rongcloud_app_secret', app_secret)
    
logging.basicConfig(level=logging.INFO)
    
api = ApiClient()
```

##通用方法

* 对于单值参数调用

```
token = api.call_api(
	action="/user/getToken",
    params={
    	"userId": "user-id1",
    	"name":"username1",
   		"portraitUri":"p1"
   	}
)
```

* 对于多值参数调用

```
addblack = api.call_api(
    action="/user/blacklist/add",
    params={
        "userId": "user-id1",
        "blackUserId":["user-id1","user-id2","user-id3"]
    }
)
```
如果一个参数需要传递多个值， 可以直接传递list 类型


* 对于json类型参数

```
publish = api.call_api(
    action="/message/private/publish",
    params={
        "fromUserId": "user-id1",
        "toUserId": "user-id8",
        "objectName": "RC:ContactNtf",
        "content": json.dumps(
            {
                "content":"this is content",
                "targetUserId":"user-id8",
                "sourceUserId":"user-id1",
                "message": "fydtest",
                "operation": "Request",
                "extra":json.dumps(
                    {
                        "title":"this is title",
                        "name":"this is name"
                    }
                )
            }),

            "pushContent": "this is push content",
            "pushData": "this is push data"
        }
)
```

## 封装方法

如果您觉得通过 call_api 方法调用不够方便，可参阅 test.py 中的单元测试代码。

我们对 call_api 进行了更进一步的封装，但是不建议您在生产环境中使用。