server-sdk-python
=================

Rong Cloud Server SDK in Python.

# 版本说明
本 SDK 分为三个版本： V1.0、V2.0、V2.0.1, 不互相兼容；版本以分支名称区分，主分支指向 V2.0.1 版本

# python 版本
server-sdk-python supports Python 2.6, Python 2.7 and Python 3.3+

# 依赖说明
- 本 SDK 依赖于 requests

# API文档
- 官方文档(http://www.rongcloud.cn/docs/server.html)

# 使用教程

## 示例
```
>>> import os
>>> from rongcloud import RongCloud
>>> app_key = os.environ['APP_KEY']
>>> app_secret = os.environ['APP_SECRET']
>>> rcloud = RongCloud(app_key, app_secret)
>>>
>>> r = rcloud.User.getToken(userId='userid1', name='username', portraitUri='http://www.rongcloud.cn/images/logo.png')
>>> print(r)
{'token': 'P9YNVZ2cMQwwaADiNDVrtRZKF+J2pVPOWSNlYMA1yA1g49pxjZs58n4FEufsH9XMCHTk6nHR6unQTuRgD8ZS/nlbkcv6ll4x', 'userId': 'userid1', 'code': 200}
>>> 
>>> r = rcloud.Message.publishPrivate(
...     fromUserId='userId1',
...     toUserId={"userId2","userid3","userId4"},
...     objectName='RC:VcMsg',
...     content='{"content":"hello","extra":"helloExtra","duration":20}',
...     pushContent='thisisapush',
...     pushData='{"pushData":"hello"}',
...     count='4',
...     verifyBlacklist='0',
...     isPersisted='0',
...     isCounted='0')
>>> print(r)
{'code': 200}
```

## 更多示例
* 请参考单元测试 test.py, 单元测试为每个 API 提供了一个调用示例。

## 返回结果
```
Help on Response in module rong object:

class Response(builtins.object)
|  Methods defined here:
|  
|  __init__(self, response, desc)
|      Initialize self.  See help(type(self)) for accurate signature.
|  
|  __str__(self)
|      打印字符串
|  
|  get(self)
|      返回调用结果
|  
|  ----------------------------------------------------------------------
|  Data descriptors defined here:
|  
|  __dict__
|      dictionary for instance variables (if defined)
|  
|  __weakref__
|      list of weak references to the object (if defined)
|  
|  ok
|      调用成功返回True，其它返回False
|  
|  result
|      调用结果
|  
|  status
|      Http 返回码
```

# 实现功能

## 底层API调用方法
```
from rongcloud import base
rcloud = base.RongCloudBase(app_key, app_secret)
publish = rcloud.call_api(
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

## 高级API接口
### User
- getToken  获取 Token 
- refresh  刷新用户信息
- checkOnline  检查用户在线状态 
- block  封禁用户
- unBlock  解除用户封禁
- queryBlock  获取被封禁用户
- addBlacklist  添加用户到黑名单
- queryBlacklist  获取某用户的黑名单列表
- removeBlacklist  从黑名单中移除用户

### Message
- publishPrivate  发送单聊消息
- publishTemplate  发送单聊模板消息
- PublishSystem  发送系统消息
- publishSystemTemplate  发送系统模板消息
- publishGroup  发送群组消息
- publishDiscussion  发送讨论组消息
- publishChatroom  发送聊天室消息
- broadcast  发送广播消息
- getHistory  消息历史记录下载地址获取 消息历史记录下载地址获取。获取 APP 内指定某天某小时内的所有会话消息记录的下载地址
- deleteMessage  消息历史记录删除

### Wordfilter
- add  添加敏感词
- delete  移除敏感词
- getList  查询敏感词列表

### Group
- create  创建群组
- sync  同步用户所属群组
- refresh  刷新群组信息
- join  将用户加入指定群组，用户将可以收到该群的消息，同一用户最多可加入 500 个群，每个群最大至 3000 人
- queryUser  查询群成员
- quit  退出群组
- addGagUser  添加禁言群成员
- lisGagUser  查询被禁言群成员
- rollBackGagUser  移除禁言群成员
- dismiss  解散群组。

### Chatroom
- create  创建聊天室
- join  加入聊天室
- query  查询聊天室信息
- queryUser  查询聊天室内用户
- stopDistributionMessage  聊天室消息停止分发
- resumeDistributionMessage  聊天室消息恢复分发
- addGagUser  添加禁言聊天室成员
- ListGagUser  查询被禁言聊天室成员
- rollbackGagUser  移除禁言聊天室成员
- addBlockUser  添加封禁聊天室成员
- getListBlockUser  查询被封禁聊天室成员
- rollbackBlockUser  移除封禁聊天室成员
- destroy  销毁聊天室
- addWhiteListUser  添加聊天室白名单成员
- addPriority  添加聊天室消息优先级

### Push
- setUserPushTag  添加 Push 标签
- broadcastPush  广播消息

### SMS
- getImageCode  获取图片验证码
- sendCode  发送短信验证码
- verifyCode  验证码验证
