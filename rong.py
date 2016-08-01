#! /usr/bin/env python
# coding=utf-8

import os
import time
import json
import logging
import random
import hashlib
import datetime
import requests


class ApiClientBase(object):
    api_host = "http://api.cn.ronghub.com"

    def __init__(self, key=None, secret=None):
        self._app_key = key
        self._app_secret = secret

        if self._app_key is None:
            self._app_key = os.environ.get('rongcloud_app_key', '')
        if self._app_secret is None:
            self._app_secret = os.environ.get('rongcloud_app_secret', '')

    @staticmethod
    def _merge_dict(data, *override):
        result = {}
        for current_dict in (data, ) + override:
            result.update(current_dict)
        return result

    def _make_common_signature(self):
        """生成通用签名, 一般情况下，您不需要调用该方法 文档详见 http://docs.rongcloud.cn/server.html#_API_调用签名规则
        :return: {'app-key':'xxx','nonce':'xxx','timestamp':'xxx','signature':'xxx'}
        """
        nonce = str(random.random())
        timestamp = str(int(time.time()) * 1000)
        signature = hashlib.sha1((self._app_secret + nonce + timestamp).encode(
            'utf-8')).hexdigest()

        return {
            "rc-app-key": self._app_key,
            "rc-nonce": nonce,
            "rc-timestamp": timestamp,
            "rc-signature": signature
        }

    def _headers(self):
        """Default HTTP headers """
        return self._merge_dict(
            self._make_common_signature(),
            {"content-type": "application/x-www-form-urlencoded"})

    def _http_call(self, url, method, **kwargs):
        """Makes a http call. Logs response information."""
        logging.info("Request[{0}]: {1}".format(method, url))
        start_time = datetime.datetime.now()

        logging.debug("Header: {0}".format(kwargs['headers']))
        logging.debug("Params: {0}".format(kwargs['data']))
        response = requests.request(method, url, verify=False, **kwargs)

        duration = datetime.datetime.now() - start_time
        logging.info("Response[{0:d}]: {1}, Duration: {2}.{3}s.".format(
            response.status_code, response.reason, duration.seconds,
            duration.microseconds))
        return response

    def _filter_params(self, params):
        _r = dict()
        for k, v in params.items():
            if v is not None:
                _r[k] = v
        return _r

    def call_api(self, action, params=None, **kwargs):
        """
        :param action: Method Name，
        :param params: Dictionary,form params for api.
        :param timeout: (optional) Float describing the timeout of the request.
        :return:
        """
        headers = self._headers()
        data = self._filter_params(params)
        if action in ['/message/private/publish_template.json',
                      '/message/system/publish_template.json']:
            headers['content-type'] = "application/json"
            data = json.dumps(data)
        return self._http_call(url=self.api_host + action,
                               method="POST",
                               data=data,
                               headers=headers,
                               **kwargs)


class Response:
    def __init__(self, response, desc):
        self.desc = desc
        self.response = response

    @property
    def result(self):
        """调用结果"""
        return self.response.json()

    @property
    def status(self):
        """Http 返回码"""
        return self.response.status_code

    @property
    def ok(self):
        """调用成功返回True，其它返回False"""
        return self.response.ok

    def get(self):
        """返回调用结果"""
        return self.result

    def __str__(self):
        """打印字符串"""
        return str(self.result)


class ApiClient(ApiClientBase):
    """Server 开发指南, 请参阅 http://www.rongcloud.cn/docs/server.html"""

    def getToken(self, userId, name, portraitUri):
        """
        获取 Token 方法 方法
        @param  portraitUri:用户头像 URI，最大长度 1024 字节.用来在 Push 推送时显示用户的头像。（必传）
        @param  name:用户名称，最大长度 128 字节.用来在 Push 推送时显示用户的名称.用户名称，最大长度 128 字节.用来在 Push 推送时显示用户的名称。（必传）
        @param  userId:用户 Id，最大长度 64 字节.是用户在 App 中的唯一标识码，必须保证在同一个 App 内不重复，重复的用户 Id 将被当作是同一用户。（必传）

        @return code:返回码，200 为正常.如果您正在使用开发环境的 AppKey，您的应用只能注册 100 名用户，达到上限后，将返回错误码 2007.如果您需要更多的测试账户数量，您需要在应用配置中申请“增加测试人数”。
        @return token:用户 Token，可以保存应用内，长度在 256 字节以内.用户 Token，可以保存应用内，长度在 256 字节以内。
        @return userId:用户 Id，与输入的用户 Id 相同.用户 Id，与输入的用户 Id 相同。
	    """

        desc = {
            "name": "TokenReslut",
            "desc": "getToken返回结果",
            "fields":
            [{"name": "code",
              "type": "Integer",
              "desc":
              "返回码，200 为正常.如果您正在使用开发环境的 AppKey，您的应用只能注册 100 名用户，达到上限后，将返回错误码 2007.如果您需要更多的测试账户数量，您需要在应用配置中申请“增加测试人数”。"
              },
             {"name": "token",
              "type": "String",
              "desc":
              "用户 Token，可以保存应用内，长度在 256 字节以内.用户 Token，可以保存应用内，长度在 256 字节以内。"},
             {"name": "userId",
              "type": "String",
              "desc": "用户 Id，与输入的用户 Id 相同.用户 Id，与输入的用户 Id 相同。"}]
        }
        r = self.call_api(action='/user/getToken.json',
                          params={"userId": userId,
                                  "name": name,
                                  "portraitUri": portraitUri})
        return Response(r, desc)

    def refreshUser(self, userId, name=None, portraitUri=None):
        """
        刷新用户信息方法 方法
        @param  userId:用户 Id，最大长度 64 字节.是用户在 App 中的唯一标识码，必须保证在同一个 App 内不重复，重复的用户 Id 将被当作是同一用户。（必传）
        @param  name:用户名称，最大长度 128 字节。用来在 Push 推送时，显示用户的名称，刷新用户名称后 5 分钟内生效。（可选，提供即刷新，不提供忽略）
        @param  portraitUri:用户头像 URI，最大长度 1024 字节。用来在 Push 推送时显示。（可选，提供即刷新，不提供忽略）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/user/refresh.json',
                          params={"userId": userId,
                                  "name": name,
                                  "portraitUri": portraitUri})
        return Response(r, desc)

    def checkOnlineUser(self, userId):
        """
        检查用户在线状态 方法 方法
        @param  userId:用户 Id，最大长度 64 字节。是用户在 App 中的唯一标识码，必须保证在同一个 App 内不重复，重复的用户 Id 将被当作是同一用户。（必传）

        @return code:返回码，200 为正常。
        @return status:在线状态，1为在线，0为不在线。
	    """

        desc = {"name": "CheckOnlineReslut",
                "desc": "checkOnlineUser返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}, {"name": "status",
                                                      "type": "String",
                                                      "desc":
                                                      "在线状态，1为在线，0为不在线。"}]}
        r = self.call_api(action='/user/checkOnline.json',
                          params={"userId": userId})
        return Response(r, desc)

    def blockUser(self, userId, minute):
        """
        封禁用户方法 方法
        @param  minute:封禁时长,单位为分钟，最大值为43200分钟。（必传）
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/user/block.json',
                          params={"userId": userId,
                                  "minute": minute})
        return Response(r, desc)

    def unBlockUser(self, userId):
        """
        解除用户封禁方法 方法
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/user/unblock.json',
                          params={"userId": userId})
        return Response(r, desc)

    def queryBlockUser(self):
        """
        获取被封禁用户方法 方法

        @return code:返回码，200 为正常。
        @return users:被封禁用户列表。
        @return userId:被封禁用户 ID。
        @return blockEndTime:封禁结束时间。(yyyy-mm-dd hh:mm:ss)
	    """

        desc = {"name": "QueryBlockUserReslut",
                "desc": "queryBlockUser返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}, {"name": "users",
                                                      "type": "List<String>",
                                                      "desc": "被封禁用户列表。"},
                           {"name": "userId",
                            "type": "String",
                            "desc": "被封禁用户 ID。"},
                           {"name": "blockEndTime",
                            "type": "String",
                            "desc": "封禁结束时间。(yyyy-mm-dd hh:mm:ss)"}]}
        r = self.call_api(action='/user/block/query.json', params={})
        return Response(r, desc)

    def addUserBlacklist(self, userId, blackUserId):
        """
        添加用户到黑名单方法 方法
        @param  blackUserId:被加到黑名单的用户Id。(必传)
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/user/blacklist/add.json',
                          params={"userId": userId,
                                  "blackUserId": blackUserId})
        return Response(r, desc)

    def removeBlacklistUser(self, userId, blackUserId):
        """
        从黑名单中移除用户方法 方法
        @param  blackUserId:被移除的用户Id。(必传)
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/user/blacklist/remove.json',
                          params={"userId": userId,
                                  "blackUserId": blackUserId})
        return Response(r, desc)

    def queryBlacklistUser(self, userId):
        """
        获取某用户的黑名单列表方法 方法
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
        @return users:黑名单用户数组。
	    """

        desc = {"name": "QueryBlacklistUserReslut",
                "desc": "queryBlacklistUser返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}, {"name": "users",
                                                      "type": "List<String>",
                                                      "desc": "黑名单用户数组。"}]}
        r = self.call_api(action='/user/blacklist/query.json',
                          params={"userId": userId})
        return Response(r, desc)

    def publishMessage(self,
                       fromUserId,
                       toUserId,
                       objectName,
                       content,
                       pushContent=None,
                       pushData=None,
                       count=None,
                       verifyBlacklist=None,
                       isPersisted=None,
                       isCounted=None):
        """
        发送单聊消息方法（一个用户向另外一个用户发送消息，单条消息最大 128k。每分钟最多发送 6000 条信息，每次发送用户上限为 1000 人，如：一次发送 1000 人时，示为 1000 条消息。） 方法
        @param  toUserId:接收用户 Id，可以实现向多人发送消息，每次上限为 1000 人。（必传）
        @param  fromUserId:发送人用户 Id。（必传）
        @param  content:发送消息内容，参考融云消息类型表。示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        @param  objectName:消息类型，参考融云消息类型表.消息标志；可自定义消息类型。（必传）
        @param  pushContent:定义显示的 Push 内容，如果 objectName 为融云内置消息类型时，则发送后用户一定会收到 Push 信息。如果为自定义消息，则 pushContent 为自定义消息显示的 Push 内容，如果不传则用户不会收到 Push 通知。(可选)
        @param  pushData:针对 iOS 平台为 Push 通知时附加到 payload 中，Android 客户端收到推送消息时对应字段名为 pushData。(可选)
        @param  count:针对 iOS 平台，Push 时用来控制未读消息显示数，只有在 toUserId 为一个用户 Id 的时候有效。(可选)
        @param  verifyBlacklist:是否过滤发送人黑名单列表，0 表示为不过滤、 1 表示为过滤，默认为 0 不过滤。(可选)
        @param  isPersisted:当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行存储，0 表示为不存储、 1 表示为存储，默认为 1 存储消息。(可选)
        @param  isCounted:当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行未读消息计数，0 表示为不计数、 1 表示为计数，默认为 1 计数，未读消息数增加 1。(可选)

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/message/private/publish.json',
                          params={"fromUserId": fromUserId,
                                  "toUserId": toUserId,
                                  "objectName": objectName,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData,
                                  "count": count,
                                  "verifyBlacklist": verifyBlacklist,
                                  "isPersisted": isPersisted,
                                  "isCounted": isCounted})
        return Response(r, desc)

    def publishTemplateMessage(self,
                               fromUserId,
                               toUserId,
                               objectName,
                               values,
                               content,
                               pushContent=None,
                               pushData=None,
                               verifyBlacklist=None):
        """
        发送单聊模板消息方法(一个用户向多个用户发送不同消息内容，单条消息最大 128k.每分钟最多发送 6000 条信息，每次发送用户上限为 1000 人。) 方法
        @param  objectName:消息类型，参考融云消息类型表.消息标志；可自定义消息类型。（必传）
        @param  toUserId:接收用户 Id，提供多个本参数可以实现向多人发送消息，上限为 1000 人。（必传）
        @param  fromUserId:发送人用户 Id。（必传）
        @param  content:发送消息内容，内容中定义标识通过 values 中设置的标识位内容进行替换，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        @param  values:消息内容中，标识位对应内容。（必传）
        @param  pushContent:如果为自定义消息，定义显示的 Push 内容，内容中定义标识通过 values 中设置的标识位内容进行替换.如消息类型为自定义不需要 Push 通知，则对应数组传空值即可。（可选）
        @param  pushData:针对 iOS 平台为 Push 通知时附加到 payload 中，Android 客户端收到推送消息时对应字段名为 pushData。如不需要 Push 功能对应数组传空值即可。（可选）
        @param  verifyBlacklist:是否过滤发送人黑名单列表，0 为不过滤、 1 为过滤，默认为 0 不过滤.(可选)是否过滤发送人黑名单列表，0 为不过滤、 1 为过滤，默认为 0 不过滤.(可选)

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/message/private/publish_template.json',
                          params={"fromUserId": fromUserId,
                                  "toUserId": toUserId,
                                  "objectName": objectName,
                                  "values": values,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData,
                                  "verifyBlacklist": verifyBlacklist})
        return Response(r, desc)

    def systemPublishMessage(self,
                             fromUserId,
                             toUserId,
                             objectName,
                             content,
                             pushContent=None,
                             pushData=None,
                             isPersisted=None,
                             isCounted=None):
        """
        发送系统消息方法(一个用户向一个或多个用户发送系统消息，单条消息最大 128k，会话类型为 SYSTEM。每秒钟最多发送 100 条消息，每次最多同时向 100 人发送，如：一次发送 100 人时，示为 100 条消息。) 方法
        @param  content:发送消息内容，内容中定义标识通过 values 中设置的标识位内容进行替换，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        @param  objectName:消息类型，参考融云消息类型表.消息标志；可自定义消息类型。（必传）
        @param  toUserId:接收用户 Id，提供多个本参数可以实现向多人发送消息，上限为 1000 人。（必传）
        @param  fromUserId:发送人用户 Id。（必传）
        @param  pushContent:如果为自定义消息，定义显示的 Push 内容，内容中定义标识通过 values 中设置的标识位内容进行替换.如消息类型为自定义不需要 Push 通知，则对应数组传空值即可。（可选）
        @param  pushData:针对 iOS 平台为 Push 通知时附加到 payload 中，Android 客户端收到推送消息时对应字段名为 pushData。如不需要 Push 功能对应数组传空值即可。（可选）
        @param  isPersisted:当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行存储，0 表示为不存储、 1 表示为存储，默认为 1 存储消息。(可选)
        @param  isCounted:当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行未读消息计数，0 表示为不计数、 1 表示为计数，默认为 1 计数，未读消息数增加 1。(可选)

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/message/system/publish.json',
                          params={"fromUserId": fromUserId,
                                  "toUserId": toUserId,
                                  "objectName": objectName,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData,
                                  "isPersisted": isPersisted,
                                  "isCounted": isCounted})
        return Response(r, desc)

    def systemPublishTemplateMessage(self,
                                     fromUserId,
                                     toUserId,
                                     objectName,
                                     values,
                                     content,
                                     pushContent=None,
                                     pushData=None):
        """
        发送系统模板消息方法(一个用户向一个或多个用户发送系统消息，单条消息最大 128k，会话类型为 SYSTEM.每秒钟最多发送 100 条消息，每次最多同时向 100 人发送，如：一次发送 100 人时，示为 100 条消息。) 方法
        @param  toUserId:接收用户 Id，提供多个本参数可以实现向多人发送消息，上限为 100 人。（必传）
        @param  fromUserId:发送人用户 Id。（必传）
        @param  content:发送消息内容，内容中定义标识通过 values 中设置的标识位内容进行替换，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        @param  values:消息内容中，标识位对应内容。（必传）
        @param  objectName:消息类型，参考融云消息类型表.消息标志；可自定义消息类型。（必传）
        @param  pushContent:定义显示的 Push 内容，如果 objectName 为融云内置消息类型时，则发送后用户一定会收到 Push 信息. 如果为自定义消息，则 pushContent 为自定义消息显示的 Push 内容，如果不传则用户不会收到 Push 通知。(可选)
        @param  pushData:针对 iOS 平台为 Push 通知时附加到 payload 中，Android 客户端收到推送消息时对应字段名为 pushData.如不需要 Push 功能对应数组传空值即可。（可选）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/message/system/publish_template.json',
                          params={"fromUserId": fromUserId,
                                  "toUserId": toUserId,
                                  "objectName": objectName,
                                  "values": values,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData})
        return Response(r, desc)

    def publishGroupMessage(self,
                            fromUserId,
                            toGroupId,
                            objectName,
                            content,
                            pushContent=None,
                            pushData=None,
                            isPersisted=None,
                            isCounted=None):
        """
        发送群组消息方法(以一个用户身份向群组发送消息，单条消息最大 128k.每秒钟最多发送 20 条消息，每次最多向 3 个群组发送，如：一次向 3 个群组发送消息，示为 3 条消息.) 方法
        @param  content:发送消息内容，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        @param  objectName:消息类型，参考融云消息类型表.消息标志；可自定义消息类型。（必传）
        @param  toGroupId:接收群Id，提供多个本参数可以实现向多群发送消息，最多不超过 3 个群组。（必传）
        @param  fromUserId:发送人用户 Id 。（必传）
        @param  pushContent:定义显示的 Push 内容，如果 objectName 为融云内置消息类型时，则发送后用户一定会收到 Push 信息. 如果为自定义消息，则 pushContent 为自定义消息显示的 Push 内容，如果不传则用户不会收到 Push 通知。(可选)
        @param  pushData:针对 iOS 平台为 Push 通知时附加到 payload 中，Android 客户端收到推送消息时对应字段名为 pushData。(可选)
        @param  isPersisted:当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行存储，0 表示为不存储、 1 表示为存储，默认为 1 存储消息。(可选)
        @param  isCounted:当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行未读消息计数，0 表示为不计数、 1 表示为计数，默认为 1 计数，未读消息数增加 1。(可选)

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/message/group/publish.json',
                          params={"fromUserId": fromUserId,
                                  "toGroupId": toGroupId,
                                  "objectName": objectName,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData,
                                  "isPersisted": isPersisted,
                                  "isCounted": isCounted})
        return Response(r, desc)

    def publishDiscussionMessage(self,
                                 fromUserId,
                                 toDiscussionId,
                                 objectName,
                                 content,
                                 pushContent=None,
                                 pushData=None,
                                 isPersisted=None,
                                 isCounted=None):
        """
        发送讨论组消息方法(以一个用户身份向讨论组发送消息，单条消息最大 128k，每秒钟最多发送 20 条消息.) 方法
        @param  content:发送消息内容，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        @param  objectName:消息类型，参考融云消息类型表.消息标志；可自定义消息类型。（必传）
        @param  toDiscussionId:接收讨论组 Id。（必传）
        @param  fromUserId:发送人用户 Id。（必传）
        @param  pushContent:定义显示的 Push 内容，如果 objectName 为融云内置消息类型时，则发送后用户一定会收到 Push 信息. 如果为自定义消息，则 pushContent 为自定义消息显示的 Push 内容，如果不传则用户不会收到 Push 通知。(可选)
        @param  pushData:针对 iOS 平台为 Push 通知时附加到 payload 中，Android 客户端收到推送消息时对应字段名为 pushData.(可选)
        @param  isPersisted:当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行存储，0 表示为不存储、 1 表示为存储，默认为 1 存储消息.(可选)
        @param  isCounted:当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行未读消息计数，0 表示为不计数、 1 表示为计数，默认为 1 计数，未读消息数增加 1。(可选)

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/message/discussion/publish.json',
                          params={"fromUserId": fromUserId,
                                  "toDiscussionId": toDiscussionId,
                                  "objectName": objectName,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData,
                                  "isPersisted": isPersisted,
                                  "isCounted": isCounted})
        return Response(r, desc)

    def publishChatroomMessage(self, fromUserId, toChatroomId, objectName,
                               content):
        """
        发送聊天室消息方法(一个用户向聊天室发送消息，单条消息最大 128k。每秒钟限 100 次。) 方法
        @param  content:发送消息内容，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式.（必传）
        @param  objectName:消息类型，参考融云消息类型表.消息标志；可自定义消息类型.（必传）
        @param  toChatroomId:接收聊天室Id，提供多个本参数可以实现向多个聊天室发送消息.（必传）
        @param  fromUserId:发送人用户 Id.（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/message/chatroom/publish.json',
                          params={"fromUserId": fromUserId,
                                  "toChatroomId": toChatroomId,
                                  "objectName": objectName,
                                  "content": content})
        return Response(r, desc)

    def broadcastMessage(self,
                         fromUserId,
                         objectName,
                         content,
                         pushContent=None,
                         pushData=None,
                         os=None):
        """
        发送广播消息方法(发送消息给一个应用下的所有注册用户，如用户未在线会对满足条件（绑定手机终端）的用户发送 Push 信息，单条消息最大 128k，会话类型为 SYSTEM.每小时只能发送 1 次，每天最多发送 3 次。) 方法
        @param  content:发送消息内容，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        @param  objectName:消息类型，参考融云消息类型表.消息标志；可自定义消息类型。（必传）
        @param  fromUserId:发送人用户 Id。（必传）
        @param  pushContent:定义显示的 Push 内容，如果 objectName 为融云内置消息类型时，则发送后用户一定会收到 Push 信息. 如果为自定义消息，则 pushContent 为自定义消息显示的 Push 内容，如果不传则用户不会收到 Push 通知.(可选)
        @param  pushData:针对 iOS 平台为 Push 通知时附加到 payload 中，Android 客户端收到推送消息时对应字段名为 pushData。(可选)
        @param  os:针对操作系统发送 Push，值为 iOS 表示对 iOS 手机用户发送 Push ,为 Android 时表示对 Android 手机用户发送 Push ，如对所有用户发送 Push 信息，则不需要传 os 参数。(可选)

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/message/broadcast.json',
                          params={"fromUserId": fromUserId,
                                  "objectName": objectName,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData,
                                  "os": os})
        return Response(r, desc)

    def addWordFilter(self, word):
        """
        添加敏感词方法(设置敏感词后，App 中用户不会收到含有敏感词的消息内容，默认最多设置 50 个敏感词。) 方法
        @param  word:敏感词，最长不超过 32 个字符。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/wordfilter/add.json', params={"word": word})
        return Response(r, desc)

    def deleteWordfilter(self, word):
        """
        移除敏感词方法(从敏感词列表中，移除某一敏感词。) 方法
        @param  word:敏感词，最长不超过 32 个字符。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/wordfilter/delete.json',
                          params={"word": word})
        return Response(r, desc)

    def listWordfilter(self):
        """
        查询敏感词列表方法 方法

        @return code:返回码，200 为正常。
        @return word:敏感词内容。
	    """

        desc = {"name": "ListWordfilterReslut",
                "desc": "listWordfilterReslut返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}, {"name": "word",
                                                      "type": "String",
                                                      "desc": "敏感词内容。"}]}
        r = self.call_api(action='/wordfilter/list.json', params={})
        return Response(r, desc)

    def historyMessage(self, date):
        """
        消息历史记录下载地址获取 方法消息历史记录下载地址获取方法。获取 APP 内指定某天某小时内的所有会话消息记录的下载地址。（目前支持二人会话、讨论组、群组、聊天室、客服、系统通知消息历史记录下载） 方法
        @param  date:指定北京时间某天某小时，格式为2014010101,表示：2014年1月1日凌晨1点。（必传）

        @return code:返回码，200 为正常。
        @return url:历史消息下载地址。
        @return date:历史记录时间。
	    """

        desc = {"name": "HistoryMessageReslut",
                "desc": "historyMessage返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}, {"name": "url",
                                                      "type": "String",
                                                      "desc": "历史消息下载地址。"},
                           {"name": "date",
                            "type": "String",
                            "desc": "历史记录时间。"}]}
        r = self.call_api(action='/message/history.json',
                          params={"date": date})
        return Response(r, desc)

    def HistoryMessageDelete(self, date):
        """
        消息历史记录删除方法(删除 APP 内指定某天某小时内的所有会话消息记录。调用该接口返回成功后，date参数指定的某小时的消息记录文件将在随后的5-10分钟内被永久删除。) 方法
        @param  date:指定北京时间某天某小时，格式为2014010101,表示：2014年1月1日凌晨1点.（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/message/history/delete.json',
                          params={"date": date})
        return Response(r, desc)

    def groupSync(self, userId, group_id_name):
        """
        同步用户所属群组方法(当第一次连接融云服务器时，需要向融云服务器提交 userId 对应的用户当前所加入的所有群组，此接口主要为防止应用中用户群信息同融云已知的用户所属群信息不同步。) 方法
        @param  group_id_name:该用户的群信息，如群 Id 已经存在，则不会刷新对应群组名称，如果想刷新群组名称请调用刷新群组信息方法。
        @param  userId:被同步群信息的用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/group/sync.json',
                          params={"userId": userId,
                                  "group_id_name": group_id_name})
        return Response(r, desc)

    def groupCreate(self, userId, groupId, groupName):
        """
        创建群组方法(创建群组，并将用户加入该群组，用户将可以收到该群的消息，同一用户最多可加入 500 个群，每个群最大至 3000 人，App 内的群组数量没有限制.注：其实本方法是加入群组方法 /group/join 的别名。) 方法
        @param  groupName:群组 Id 对应的名称。（必传）
        @param  groupId:创建群组 Id。（必传）
        @param  userId:要加入群的用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/group/create.json',
                          params={"userId": userId,
                                  "groupId": groupId,
                                  "groupName": groupName})
        return Response(r, desc)

    def groupjoin(self, userId, groupId, groupName):
        """
        将用户加入指定群组，用户将可以收到该群的消息，同一用户最多可加入 500 个群，每个群最大至 3000 人。 方法
        @param  groupName:要加入的群 Id 对应的名称。（必传）
        @param  groupId:要加入的群 Id。（必传）
        @param  userId:要加入群的用户 Id，可提交多个，最多不超过 1000 个。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/group/join.json',
                          params={"userId": userId,
                                  "groupId": groupId,
                                  "groupName": groupName})
        return Response(r, desc)

    def groupQuit(self, userId, groupId):
        """
        退出群组方法(将用户从群中移除，不再接收该群组的消息.) 方法
        @param  groupId:要退出的群 Id.（必传）
        @param  userId:要退出群的用户 Id.（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/group/quit.json',
                          params={"userId": userId,
                                  "groupId": groupId})
        return Response(r, desc)

    def groupDismiss(self, userId, groupId):
        """
        解散群组方法。(将该群解散，所有用户都无法再接收该群的消息。) 方法
        @param  groupId:要解散的群 Id。（必传）
        @param  userId:操作解散群的用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/group/dismiss.json',
                          params={"userId": userId,
                                  "groupId": groupId})
        return Response(r, desc)

    def groupRefresh(self, groupId, groupName):
        """
        刷新群组信息方法 方法
        @param  groupName:群名称。（必传）
        @param  groupId:群组 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/group/refresh.json',
                          params={"groupId": groupId,
                                  "groupName": groupName})
        return Response(r, desc)

    def groupUserQuery(self, groupId):
        """
        查询群成员方法 方法
        @param  groupId:群组Id。（必传）

        @return code:返回码，200 为正常。
        @return id:群成员用户Id。
	    """

        desc = {"name": "GroupUserQueryReslut",
                "desc": "groupUserQuery返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}, {"name": "id",
                                                      "type": "String",
                                                      "desc": "群成员用户Id。"}]}
        r = self.call_api(action='/group/user/query.json',
                          params={"groupId": groupId})
        return Response(r, desc)

    def addGagGroupUser(self, userId, groupId, minute):
        """
        添加禁言群成员方法(在 App 中如果不想让某一用户在群中发言时，可将此用户在群组中禁言，被禁言用户可以接收查看群组中用户聊天信息，但不能发送消息。) 方法
        @param  minute:禁言时长，以分钟为单位，最大值为43200分钟.（必传）
        @param  groupId:群组 Id.（必传）
        @param  userId:用户 Id.（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/group/user/gag/add.json',
                          params={"userId": userId,
                                  "groupId": groupId,
                                  "minute": minute})
        return Response(r, desc)

    def rooBackGagGroupUser(self, userId, groupId):
        """
        移除禁言群成员方法 方法
        @param  groupId:群组Id。（必传）
        @param  userId:用户Id。支持同时移除多个群成员（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/group/user/gag/rollback.json',
                          params={"userId": userId,
                                  "groupId": groupId})
        return Response(r, desc)

    def listGagGroupUser(self, groupId):
        """
        查询被禁言群成员方法 方法
        @param  groupId:群组Id。（必传）

        @return code:返回码，200 为正常.
        @return users:群组成员列表
        @return time:解禁时间。（yyyy-mm-dd hh:mm:ss）
        @return users:群成员 Id。
	    """

        desc = {"name": "ListGagGroupUserReslut",
                "desc": "lisitGagGroupUser返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常."}, {"name": "users",
                                                      "type": "List<String>",
                                                      "desc": "群组成员列表"},
                           {"name": "time",
                            "type": "String",
                            "desc": "解禁时间。（yyyy-mm-dd hh:mm:ss）"},
                           {"name": "users",
                            "type": "String",
                            "desc": "群成员 Id。"}]}
        r = self.call_api(action='/group/user/gag/list.json',
                          params={"groupId": groupId})
        return Response(r, desc)

    def chatroomCreate(self, chatroom_id_name):
        """
        创建聊天室方法 方法
        @param  chatroom_id_name:id:要创建的聊天室的id；name:要创建的聊天室的name。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/chatroom/create.json',
                          params={"chatroom_id_name": chatroom_id_name})
        return Response(r, desc)

    def chatroomJoin(self, userId, chatroomId):
        """
        加入聊天室方法 方法
        @param  chatroomId:要加入的聊天室 Id。（必传）
        @param  userId:要加入聊天室的用户 Id，可提交多个，最多不超过 50 个。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/chatroom/join.json',
                          params={"userId": userId,
                                  "chatroomId": chatroomId})
        return Response(r, desc)

    def chatroomDestroy(self, chatroomId):
        """
        销毁聊天室方法 方法
        @param  chatroomId:要销毁的聊天室 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/chatroom/destroy.json',
                          params={"chatroomId": chatroomId})
        return Response(r, desc)

    def chatroomQuery(self, chatroomId):
        """
        查询聊天室信息方法 方法
        @param  chatroomId:要查询的聊天室id（必传）

        @return code:返回码，200 为正常。
        @return chatRooms:聊天室信息数组。
        @return chrmId:聊天室 ID。
        @return name:聊天室名称。
        @return chrmId:聊天室创建时间。
	    """

        desc = {"name": "ChatroomQueryReslut",
                "desc": "chatroomQuery返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}, {"name": "chatRooms",
                                                      "type": "String",
                                                      "desc": "聊天室信息数组。"},
                           {"name": "chrmId",
                            "type": "String",
                            "desc": "聊天室 ID。"}, {"name": "name",
                                                 "type": "String",
                                                 "desc": "聊天室名称。"},
                           {"name": "chrmId",
                            "type": "String",
                            "desc": "聊天室创建时间。"}]}
        r = self.call_api(action='/chatroom/query.json',
                          params={"chatroomId": chatroomId})
        return Response(r, desc)

    def chatroomUserQuery(self, chatroomId, count, order):
        """
        查询聊天室内用户方法 方法
        @param  order:加入聊天室的先后顺序， 1 为加入时间正序， 2 为加入时间倒序。（必传）
        @param  count:要获取的聊天室成员数，上限为 500 ，超过 500 时最多返回 500 个成员。（必传）
        @param  chatroomId:要查询的聊天室 ID（必传）

        @return code:返回码，200 为正常。
        @return total:聊天室中用户数。
        @return users:聊天室成员数组。
        @return id:聊天室用户Id。
        @return time:加入聊天室时间。
	    """

        desc = {"name": "ChatroomUserQueryReslut",
                "desc": "chatroomUserQuery返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}, {"name": "total",
                                                      "type": "Integer",
                                                      "desc": "聊天室中用户数。"},
                           {"name": "users",
                            "type": "List<String>",
                            "desc": "聊天室成员数组。"}, {"name": "id",
                                                  "type": "String",
                                                  "desc": "聊天室用户Id。"},
                           {"name": "time",
                            "type": "String",
                            "desc": "加入聊天室时间。"}]}
        r = self.call_api(action='/chatroom/user/query.json',
                          params={"chatroomId": chatroomId,
                                  "count": count,
                                  "order": order})
        return Response(r, desc)

    def stopDistributionChatroomMessage(self, chatroomId):
        """
        聊天室消息停止分发方法(可实现控制对聊天室中消息是否进行分发，停止分发后聊天室中用户发送的消息，融云服务端不会再将消息发送给聊天室中其他用户。) 方法
        @param  chatroomId:聊天室 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/chatroom/message/stopDistribution.json',
                          params={"chatroomId": chatroomId})
        return Response(r, desc)

    def resumeDistributionChatroomMessage(self, chatroomId):
        """
        聊天室消息恢复分发方法 方法
        @param  chatroomId:聊天室 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/chatroom/message/resumeDistribution.json',
                          params={"chatroomId": chatroomId})
        return Response(r, desc)

    def addGagChatroomUser(self, userId, chatroomId, minute):
        """
        添加禁言聊天室成员方法（在 App 中如果不想让某一用户在聊天室中发言时，可将此用户在聊天室中禁言，被禁言用户可以接收查看聊天室中用户聊天信息，但不能发送消息.） 方法
        @param  minute:禁言时长，以分钟为单位，最大值为43200分钟。（必传）
        @param  chatroomId:聊天室 Id。（必传）
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/chatroom/user/gag/add.json',
                          params={"userId": userId,
                                  "chatroomId": chatroomId,
                                  "minute": minute})
        return Response(r, desc)

    def rollbackGagChatroomUser(self, userId, chatroomId):
        """
        移除禁言聊天室成员方法 方法
        @param  chatroomId:聊天室Id。（必传）
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/chatroom/user/gag/rollback.json',
                          params={"userId": userId,
                                  "chatroomId": chatroomId})
        return Response(r, desc)

    def listGagChatroomUser(self, chatroomId):
        """
        查询被禁言聊天室成员方法 方法
        @param  chatroomId:聊天室 Id。（必传）

        @return code:返回码，200 为正常。
        @return users:聊天室被禁言用户列表。
        @return time:解禁时间。
        @return userId:群成员Id。
	    """

        desc = {"name": "ListGagChatroomUserReslut",
                "desc": "listGagChatroomUser返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}, {"name": "users",
                                                      "type": "List<String>",
                                                      "desc": "聊天室被禁言用户列表。"},
                           {"name": "time",
                            "type": "String",
                            "desc": "解禁时间。"}, {"name": "userId",
                                               "type": "String",
                                               "desc": "群成员Id。"}]}
        r = self.call_api(action='/chatroom/user/gag/list.json',
                          params={"chatroomId": chatroomId})
        return Response(r, desc)

    def addChatroomBlockUser(self, userId, chatroomId, minute):
        """
        添加封禁聊天室成员方法 方法
        @param  minute:封禁时长，以分钟为单位，最大值为43200分钟。（必传）
        @param  chatroomId:聊天室 Id。（必传）
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/chatroom/user/block/add.json',
                          params={"userId": userId,
                                  "chatroomId": chatroomId,
                                  "minute": minute})
        return Response(r, desc)

    def rollbackBlockChatroomUser(self, userId, chatroomId):
        """
        移除封禁聊天室成员方法 方法
        @param  chatroomId:聊天室 Id.（必传）
        @param  userId:用户 Id.（必传）

        @return code:返回码，200 为正常。
	    """

        desc = {"name": "CodeSuccessReslut",
                "desc": "http 返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}]}
        r = self.call_api(action='/chatroom/user/block/rollback.json',
                          params={"userId": userId,
                                  "chatroomId": chatroomId})
        return Response(r, desc)

    def listBlockChatroomUser(self, chatroomId):
        """
        查询被封禁聊天室成员方法 方法
        @param  chatroomId:聊天室 Id.（必传）

        @return code:返回码，200 为正常。
        @return users:聊天室成员数组。
        @return time:解禁时间。
        @return userId:群成员 Id。
	    """

        desc = {"name": "ListBlockChatroomUserReslut",
                "desc": "listBlockChatroomUser返回结果",
                "fields": [{"name": "code",
                            "type": "Integer",
                            "desc": "返回码，200 为正常。"}, {"name": "users",
                                                      "type": "List<String>",
                                                      "desc": "聊天室成员数组。"},
                           {"name": "time",
                            "type": "String",
                            "desc": "解禁时间。"}, {"name": "userId",
                                               "type": "String",
                                               "desc": "群成员 Id。"}]}
        r = self.call_api(action='/chatroom/user/block/list.json',
                          params={"chatroomId": chatroomId})
        return Response(r, desc)
