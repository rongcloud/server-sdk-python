server-sdk-python
=================

Rong Cloud Server SDK in Python.

# 版本说明
本sdk分为两个版本：v1.0 和v2.0，不互相兼容；版本以分支名称区分，主分支指向v2.0版本

# python 版本
server-sdk-python supports Python 2.6, Python 2.7 and Python 3.3+

# 依赖说明
- 本sdk 依赖于requests

# API文档
- 官方文档(http://www.rongcloud.cn/docs/server.html)

# 使用教程

## 示例
```
>>> import os
>>> from rong import ApiClient
>>> app_key = os.environ['APP_KEY']
>>> app_secret = os.environ['APP_SECRET']
>>> api = ApiClient(app_key, app_secret)
>>>
>>> r = api.getToken(userId='userid1', name='username', portraitUri='http://www.rongcloud.cn/images/logo.png')
>>> print(r)
{'token': 'P9YNVZ2cMQwwaADiNDVrtRZKF+J2pVPOWSNlYMA1yA1g49pxjZs58n4FEufsH9XMCHTk6nHR6unQTuRgD8ZS/nlbkcv6ll4x', 'userId': 'userid1', 'code': 200}
>>> 
>>> r = api.publishMessage(
...     pushContent='userid1',
...     toUserId='userid1',
...     content=json.dumps({"content":"hello","extra":"helloExtra"}),
...     pushData='userid1',
...     fromUserId='userid1',
...     objectName='RC:TxtMsg')
>>> print(r)
{'code': 200}
```

## 更多示例
* 请参考单元测试test.py

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

## 高级API接口
- getToken        获取 Token 
- refreshUser        刷新用户信息
- checkOnlineUser        检查用户在线状态 
- blockUser        封禁用户
- unBlockUser        解除用户封禁
- queryBlockUser        获取被封禁用户
- addUserBlacklist        添加用户到黑名单
- removeBlacklistUser        从黑名单中移除用户
- queryBlacklistUser        获取某用户的黑名单列表
- publishMessage    发送单聊消息
- publishTemplateMessage    发送单聊模板消息
- systemPublishMessage  发送系统消息
- systemPublishTemplateMessage  发送系统模板消息
- publishGroupMessage   发送群组消息
- publishDiscussionMessage  发送讨论组消息
- publishChatroomMessage    发送聊天室消息
- broadcastMessage  发送广播消息
- addWordFilter        添加敏感词
- deleteWordfilter        移除敏感词
- listWordfilter        查询敏感词列表
- historyMessage        消息历史记录下载地址获取
- HistoryMessageDelete        消息历史记录删除
- groupSync        同步用户所属群组
- groupCreate        创建群组
- groupjoin        将用户加入指定群组
- groupQuit        退出群组
- groupDismiss        解散群组
- groupRefresh        刷新群组信息
- groupUserQuery        查询群成员
- addGagGroupUser        添加禁言群成员
- rooBackGagGroupUser        移除禁言群成员
- listGagGroupUser        查询被禁言群成员
- chatroomCreate        创建聊天室
- chatroomJoin        加入聊天室
- chatroomDestroy        销毁聊天室
- chatroomQuery        查询聊天室信息
- chatroomUserQuery        查询聊天室内用户
- stopDistributionChatroomMessage        聊天室消息停止分发
- resumeDistributionChatroomMessage        聊天室消息恢复分发
- addGagChatroomUser        添加禁言聊天室成员
- rollbackGagChatroomUser        移除禁言聊天室成员
- listGagChatroomUser        查询被禁言聊天室成员
- addChatroomBlockUser        添加封禁聊天室成员
- rollbackBlockChatroomUser        移除封禁聊天室成员
- listBlockChatroomUser        查询被封禁聊天室成员

# 更新说明
### 20160801
- 返回结果结构变更
- 按官方文档(http://www.rongcloud.cn/docs/server.html) 补全Server API接口
- 为每个接口添加参数及返回值说明信息

### 20150206
- 去掉可能会导致SSL验证失败的代码
- 更改环境变量名称，老的环境变量名称在某些操作系统中无法被识别
