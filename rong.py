#! /usr/bin/env python
# coding=utf-8

import os
import re
import json
import time
import logging
import random
import hashlib

import datetime
import requests

Version = 'v1.0'

class ConnectionError(Exception):
    def __init__(self, response, content=None, message=None):
        self.response = response
        self.content = content
        self.message = message

    def __str__(self):
        message = "Failed."
        if hasattr(self.response, 'status_code'):
            message += " Response status: %s." % (self.response.status_code)
        if hasattr(self.response, 'reason'):
            message += " Response message: %s." % (self.response.reason)
        if self.content is not None:
            message += " Error message: " + str(self.content)
        return message


class Redirection(ConnectionError):
    """3xx Redirection
    """

    def __str__(self):
        message = super(Redirection, self).__str__()
        if self.response.get('Location'):
            message = "%s => %s" % (message, self.response.get('Location'))
        return message


class MissingParam(TypeError):
    pass


class MissingConfig(Exception):
    pass


class ClientError(ConnectionError):
    """4xx Client Error
    """
    pass


class BadRequest(ClientError):
    """400 Bad Request
    """
    pass


class UnauthorizedAccess(ClientError):
    """401 Unauthorized
    """
    pass


class ForbiddenAccess(ClientError):
    """403 Forbidden
    """
    pass


class ResourceNotFound(ClientError):
    """404 Not Found
    """
    pass


class ResourceConflict(ClientError):
    """409 Conflict
    """
    pass


class ResourceGone(ClientError):
    """410 Gone
    """
    pass


class ResourceInvalid(ClientError):
    """422 Invalid
    """
    pass


class ServerError(ConnectionError):
    """5xx Server Error
    """
    pass


class MethodNotAllowed(ClientError):
    """405 Method Not Allowed
    """

    def allowed_methods(self):
        return self.response['Allow']


class ApiClient(object):
    api_host = "http://api.cn.ronghub.com"
    response_type = "json"

    ACTION_USER_TOKEN = "/user/getToken"
    ACTION_USER_REFRESH = "/user/refresh"
    ACTION_USER_CHECKONLINE = "/user/checkOnline"
    ACTION_USER_BLOCK = '/user/block'
    ACTION_USER_UNBLOCK = '/user/unblock'
    ACTION_USER_BLOCK_QUERY = '/user/block/query'

    ACTION_USER_BLACKLIST_ADD = "/user/blacklist/add"
    ACTION_USER_BLACKLIST_REMOVE = "/user/blacklist/remove"
    ACTION_USER_BLACKLIST_QUERY = "/user/blacklist/query"

    ACTION_MESSAGE_PUBLISH = "/message/private/publish"
    ACTION_MESSAGE_SYSTEM_PUBLISH = "/message/system/publish"
    ACTION_MESSAGE_GROUP_PUBLISH = "/message/group/publish"
    ACTION_MESSAGE_CHATROOM_PUBLISH = "/message/chatroom/publish"
    ACTION_MESSAGE_HISTORY = '/message/history'

    ACTION_GROUP_SYNC = "/group/sync"
    ACTION_GROUP_CREATE = "/group/create"
    ACTION_GROUP_JOIN = "/group/join"
    ACTION_GROUP_QUIT = "/group/quit"
    ACTION_GROUP_DISMISS = "/group/dismiss"
    ACTION_GROUP_REFRESH = "/group/refresh"

    ACTION_CHATROOM_CREATE = "/chatroom/create"
    ACTION_CHATROOM_DESTROY = "/chatroom/destroy"
    ACTION_CHATROOM_QUERY = "/chatroom/query"
    ACTION_CHATROOM_USER_QUERY = "/chatroom/user/query"

    def __init__(self, key=None, secret=None):
        self._app_key = key
        self._app_secret = secret

        if self._app_key is None:
            self._app_key = os.environ.get('rongcloud_app_key')
        if self._app_secret is None:
            self._app_secret = os.environ.get('rongcloud_app_secret')

    @staticmethod
    def _merge_dict(data, *override):
        result = {}
        for current_dict in (data,) + override:
            result.update(current_dict)
        return result

    @staticmethod
    def _join_url(url, *paths):
        for path in paths:
            url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
        return url

    @staticmethod
    def _handle_response(response, content):
        """Validate HTTP response
        """
        status = response.status_code
        if status in (301, 302, 303, 307):
            raise Redirection(response, content)
        elif 200 <= status <= 299:
            return json.loads(content) if content else {}
        elif status == 400:
            raise BadRequest(response, content)
        elif status == 401:
            raise UnauthorizedAccess(response, content)
        elif status == 403:
            raise ForbiddenAccess(response, content)
        elif status == 404:
            raise ResourceNotFound(response, content)
        elif status == 405:
            raise MethodNotAllowed(response, content)
        elif status == 409:
            raise ResourceConflict(response, content)
        elif status == 410:
            raise ResourceGone(response, content)
        elif status == 422:
            raise ResourceInvalid(response, content)
        elif 401 <= status <= 499:
            raise ClientError(response, content)
        elif 500 <= status <= 599:
            raise ServerError(response, content)
        else:
            raise ConnectionError(response, content, "Unknown response code: #{response.code}")

    def _make_common_signature(self):

        """生成通用签名
        一般情况下，您不需要调用该方法
        文档详见 http://docs.rongcloud.cn/server.html#_API_调用签名规则
        :return: {'app-key':'xxx','nonce':'xxx','timestamp':'xxx','signature':'xxx'}
        """

        nonce = str(random.random())
        timestamp = str(
            int(time.time()) * 1000
        )

        signature = hashlib.sha1(
            self._app_secret + nonce + timestamp
        ).hexdigest()

        return {
            "rc-app-key": self._app_key,
            "rc-nonce": nonce,
            "rc-timestamp": timestamp,
            "rc-signature": signature
        }

    def _headers(self):
        """Default HTTP headers
        """
        return self._merge_dict(
            self._make_common_signature(),
            {
                "content-type": "application/x-www-form-urlencoded",
            }
        )

    def _http_call(self, url, method, **kwargs):
        """Makes a http call. Logs response information.
        """
        logging.info("Request[%s]: %s" % (method, url))
        start_time = datetime.datetime.now()

        response = requests.request(method,
                                    url,
                                    verify=False,
                                    **kwargs)

        duration = datetime.datetime.now() - start_time
        logging.info("Response[%d]: %s, Duration: %s.%ss." %
                     (response.status_code, response.reason,
                      duration.seconds, duration.microseconds))

        return self._handle_response(response,
                                     response.content.decode("utf-8"))

    def _filter_params(self, params):
        _r = dict()
        for k, v in params.items():
            if v is not None:
                _r[k] = v
        return _r

    def call_api(self, action, params=None, **kwargs):
        """
        调用API的通用方法，有关SSL证书验证问题请参阅

        http://www.python-requests.org/en/latest/user/advanced/#ssl-cert-verification

        :param action: Method Name，
        :param params: Dictionary,form params for api.
        :param timeout: (optional) Float describing the timeout of the request.
        :return:
        """
        headers=self._headers()
        if action in ['/message/private/publish_template', '/message/system/publish_template']:
            headers["content-type"] = "application/json"
            params = json.dumps(params)
        return self._http_call(
            url=self._join_url(self.api_host, "%s.%s" % (action, self.response_type)),
            method="POST",
            data=params,
            headers=headers,
            **kwargs
        )

    def user_get_token(self, user_id, name, portrait_uri):

        """ 获取token
        http://docs.rongcloud.cn/server.html#_获取_Token_方法

        :param user_id:
        :param name:
        :param portrait_uri:
        :return: {"code":200, "userId":"jlk456j5", "token":"sfd9823ihufi"}

        """
        return self.call_api(
            action=self.ACTION_USER_TOKEN,
            params={
                "userId": user_id,
                "name": name,
                "portraitUri": portrait_uri
            }
        )

    def user_refresh(self, user_id, name, portrait_uri):
        return self.call_api(
            action=self.ACTION_USER_REFRESH,
            params={
                "userId": user_id,
                "name": name,
                "portraitUri": portrait_uri
            }
        )

    def user_check_online(self, user_id):
        return self.call_api(
            action=self.ACTION_USER_CHECKONLINE,
            params={
                "userId": user_id
            }
        )

    def user_block(self, user_id, minute):
        return self.call_api(
            action=self.ACTION_USER_BLOCK,
            params={
                "userId": user_id,
                "minute": minute
            }
        )

    def user_unblock(self, user_id):
        return self.call_api(
            action=self.ACTION_USER_UNBLOCK,
            params={
                "userId": user_id
            }
        )

    def user_block_query(self):
        return self.call_api(
            action=self.ACTION_USER_BLOCK_QUERY
        )

    def user_blocklist_add(self, user_id, black_user_id):
        return self.call_api(
            action=self.ACTION_USER_BLACKLIST_ADD,
            params={
                'userId': user_id,
                'blackUserId': black_user_id
            }
        )

    def user_blocklist_remove(self, user_id, black_user_id):
        return self.call_api(
            action=self.ACTION_USER_BLACKLIST_REMOVE,
            params={
                'userId': user_id,
                'blackUserId': black_user_id
            }
        )

    def user_blocklist_query(self, user_id):
        return self.call_api(
            action=self.ACTION_USER_BLACKLIST_QUERY,
            params={
                'userId': user_id,
            }
        )

    def message_publish(self, from_user_id, to_user_id,
                        object_name, content,
                        push_content=None, push_data=None):

        """ 发送会话消息
        http://docs.rongcloud.cn/server.html#_融云内置消息类型表
        http://docs.rongcloud.cn/server.html#_发送会话消息_方法

        :param from_user_id:发送人用户 Id
        :param to_user_id:接收用户 Id，提供多个本参数可以实现向多人发送消息。
        :param object_name:消息类型,目前包括如下类型 ["RC:TxtMsg","RC:ImgMsg","RC:VcMsg","RC:LocMsg"]
        :param content:发送消息内容，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        :param push_content:如果为自定义消息，定义显示的 Push 内容(可选)
        :param push_data:针对 iOS 平台，Push 通知附加的 payload 字段，字段名为 appData。(可选)
        :return:{"code":200}
        """
        params = [
            ("fromUserId", from_user_id),
            ("objectName", object_name),
            ("content", content),
            ("pushContent", push_content if push_content is not None else ""),
            ("pushData", push_data if push_data is not None else "")
        ]
        if not isinstance(to_user_id, list):
            to_user_id = [to_user_id]

        for user in to_user_id:
            params.append(("toUserId", user))
        return self.call_api(
            action=self.ACTION_MESSAGE_PUBLISH,
            params=params
        )

    def message_system_publish(self, from_user_id, to_user_id,
                               object_name, content,
                               push_content=None, push_data=None):
        """发送系统消息
        http://docs.rongcloud.cn/server.html#_发送系统消息_方法

        :param from_user_id:发送人用户 Id
        :param to_user_id:接收用户 Id，提供多个本参数可以实现向多人发送消息。
        :param object_name:消息类型,目前包括如下类型 ["RC:TxtMsg","RC:ImgMsg","RC:VcMsg","RC:LocMsg"]
        :param content:发送消息内容，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        :param push_content:如果为自定义消息，定义显示的 Push 内容(可选)
        :param push_data:针对 iOS 平台，Push 通知附加的 payload 字段，字段名为 appData。(可选)
        :return:{"code":200}
        """
        params = [
            ("fromUserId", from_user_id),
            ("objectName", object_name),
            ("content", content),
            ("pushContent", push_content if push_content is not None else ''),
            ("pushData", push_data if push_data is not None else '')
        ]
        if not isinstance(to_user_id, list):
            to_user_id = [to_user_id]
        for user in to_user_id:
            params.append(("toUserId", user))

        return self.call_api(action=self.ACTION_MESSAGE_SYSTEM_PUBLISH, params=params)

    def message_group_publish(self, from_user_id, to_group_id, object_name,
                              content, push_content=None, push_data=None):
        """以一个用户身份向群组发送消息
        http://docs.rongcloud.cn/server.html#_发送群组消息_方法

        :param from_user_id:发送人用户 Id
        :param to_group_id:接收群Id，提供多个本参数可以实现向多群发送消息。（必传）
        :param object_name:消息类型,目前包括如下类型 ["RC:TxtMsg","RC:ImgMsg","RC:VcMsg","RC:LocMsg"]
        :param content:发送消息内容，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        :param push_content:如果为自定义消息，定义显示的 Push 内容(可选)
        :param push_data:针对 iOS 平台，Push 通知附加的 payload 字段，字段名为 appData。(可选)
        :return:{"code":200}
        """
        params = [
            ("fromUserId", from_user_id),
            ("objectName", object_name),
            ("content", content),
            ("pushContent", push_content if push_content is not None else ''),
            ("pushData", push_data if push_data is not None else '')
        ]
        if not isinstance(to_group_id, list):
            to_group_id = [to_group_id]
        for group in to_group_id:
            params.append(("toGroupId", group))

        return self.call_api(
            action=self.ACTION_MESSAGE_GROUP_PUBLISH,
            params=params
        )

    def message_chatroom_publish(self, from_user_id,
                                 to_chatroom_id,
                                 object_name,
                                 content):
        return self.call_api(
            action=self.ACTION_MESSAGE_CHATROOM_PUBLISH,
            params={
                "fromUserId": from_user_id,
                "toChatroomId": to_chatroom_id,
                "objectName": object_name,
                "content": content
            }
        )

    def message_history(self, date):
        return self.call_api(
            action=self.ACTION_MESSAGE_HISTORY,
            params={
                "date": date,
            }
        )

    def group_sync(self, user_id, groups):
        group_mapping = {"group[%s]" % k: v for k, v in groups.items()}
        group_mapping.setdefault("userId", user_id)

        return self.call_api(action=self.ACTION_GROUP_SYNC, params=group_mapping)

    def group_create(self, user_id_list, group_id, group_name):
        return self.call_api(action=self.ACTION_GROUP_CREATE, params={
            "userId": user_id_list,
            "groupId": group_id,
            "groupName": group_name
        })

    def group_join(self, user_id_list, group_id, group_name):
        return self.call_api(action=self.ACTION_GROUP_JOIN, params={
            "userId": user_id_list,
            "groupId": group_id,
            "groupName": group_name
        })

    def group_quit(self, user_id_list, group_id):
        return self.call_api(action=self.ACTION_GROUP_QUIT, params={
            "userId": user_id_list,
            "groupId": group_id
        })

    def group_dismiss(self, user_id, group_id):
        """将该群解散，所有用户都无法再接收该群的消息。
        http://docs.rongcloud.cn/server.html#_解散群组_方法


        :param user_id: 操作解散群的用户 Id。
        :param group_id:要解散的群 Id。
        :return:{"code":200}
        """
        return self.call_api(action=self.ACTION_GROUP_DISMISS, params={
            "userId": user_id,
            "groupId": group_id,
        })

    def group_refresh(self, group_id, group_name):
        return self.call_api(action=self.ACTION_GROUP_REFRESH, params={
            "groupId": group_id,
            "groupName": group_name

        })

    def chatroom_create(self, chatrooms):
        """创建聊天室 方法
        http://docs.rongcloud.cn/server.html#_创建聊天室_方法
        :param chatrooms: {'r001':'room1'} id:要创建的聊天室的id；name:要创建的聊天室的name
        :return:{"code":200}
        """
        chatroom_mapping = {'chatroom[%s]' % k: v for k, v in chatrooms.items()}
        return self.call_api(action=self.ACTION_CHATROOM_CREATE, params=chatroom_mapping)

    def chatroom_destroy(self, chatroom_id_list=None):
        """销毁聊天室 方法
        当提交参数chatroomId多个时表示销毁多个聊天室

        http://docs.rongcloud.cn/server.html#_销毁聊天室_方法
        :param chatroom_id_list:要销毁的聊天室 Id。
        :return:{"code":200}

        """
        params = {
            "chatroomId": chatroom_id_list
        } if chatroom_id_list is not None else {}

        return self.call_api(action=self.ACTION_CHATROOM_DESTROY, params=params)

    def chatroom_query(self, chatroom_id_list=None):
        """查询聊天室信息 方法

        http://docs.rongcloud.cn/server.html#_查询聊天室信息_方法

        :param chatroom_id_list:当提交多个时表示查询多个聊天室， 如果为None ，则查询所有聊天室
        :return:{"code":200,"chatRooms":[{"chatroomId":"id1001","name":"name1","time":"2014-01-01 1:1:1"},{"chatroomId":"id1002","name":"name2","time":"2014-01-01 1:1:2"}]}
        """

        params = {
            "chatroomId": chatroom_id_list
        } if chatroom_id_list is not None else {}

        return self.call_api(action=self.ACTION_CHATROOM_QUERY, params=params)

    def chatroom_user_query(self, chatroom_id):
        """查询聊天室内用户 方法

        http://docs.rongcloud.cn/server.html#_查询聊天室内用户_方法

        :param chatroom_id:要查询的聊天室id
        :return:{"code":200,"users":[{"id":"uid1"},{"id":"uid2"}]}
        """
        return self.call_api(action=self.ACTION_CHATROOM_USER_QUERY, params={
            "chatroomId": chatroom_id
        })

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

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

        return self.call_api(action='/message/private/publish_template',
                          params=self._filter_params({"fromUserId": fromUserId,
                                  "toUserId": toUserId,
                                  "objectName": objectName,
                                  "values": values,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData,
                                  "verifyBlacklist": verifyBlacklist}))

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

        return self.call_api(action='/message/system/publish_template',
                          params=self._filter_params({"fromUserId": fromUserId,
                                  "toUserId": toUserId,
                                  "objectName": objectName,
                                  "values": values,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData}))

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
        return self.call_api(action='/message/discussion/publish',
                          params=self._filter_params({"fromUserId": fromUserId,
                                  "toDiscussionId": toDiscussionId,
                                  "objectName": objectName,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData,
                                  "isPersisted": isPersisted,
                                  "isCounted": isCounted}))

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

        return self.call_api(action='/message/broadcast',
                          params=self._filter_params({"fromUserId": fromUserId,
                                  "objectName": objectName,
                                  "content": content,
                                  "pushContent": pushContent,
                                  "pushData": pushData,
                                  "os": os}))

    def addWordFilter(self, word):
        """
        添加敏感词方法(设置敏感词后，App 中用户不会收到含有敏感词的消息内容，默认最多设置 50 个敏感词。) 方法
        @param  word:敏感词，最长不超过 32 个字符。（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/wordfilter/add', params={"word": word})

    def deleteWordfilter(self, word):
        """
        移除敏感词方法(从敏感词列表中，移除某一敏感词。) 方法
        @param  word:敏感词，最长不超过 32 个字符。（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/wordfilter/delete',
                          params={"word": word})

    def listWordfilter(self):
        """
        查询敏感词列表方法 方法

        @return code:返回码，200 为正常。
        @return word:敏感词内容。
	    """
        return self.call_api(action='/wordfilter/list', params={})

    def HistoryMessageDelete(self, date):
        """
        消息历史记录删除方法(删除 APP 内指定某天某小时内的所有会话消息记录。调用该接口返回成功后，date参数指定的某小时的消息记录文件将在随后的5-10分钟内被永久删除。) 方法
        @param  date:指定北京时间某天某小时，格式为2014010101,表示：2014年1月1日凌晨1点.（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/message/history/delete',
                          params={"date": date})

    def groupUserQuery(self, groupId):
        """
        查询群成员方法 方法
        @param  groupId:群组Id。（必传）

        @return code:返回码，200 为正常。
        @return id:群成员用户Id。
	    """

        return self.call_api(action='/group/user/query',
                          params={"groupId": groupId})

    def addGagGroupUser(self, userId, groupId, minute):
        """
        添加禁言群成员方法(在 App 中如果不想让某一用户在群中发言时，可将此用户在群组中禁言，被禁言用户可以接收查看群组中用户聊天信息，但不能发送消息。) 方法
        @param  minute:禁言时长，以分钟为单位，最大值为43200分钟.（必传）
        @param  groupId:群组 Id.（必传）
        @param  userId:用户 Id.（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/group/user/gag/add',
                          params={"userId": userId,
                                  "groupId": groupId,
                                  "minute": minute})

    def rooBackGagGroupUser(self, userId, groupId):
        """
        移除禁言群成员方法 方法
        @param  groupId:群组Id。（必传）
        @param  userId:用户Id。支持同时移除多个群成员（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/group/user/gag/rollback',
                          params={"userId": userId,
                                  "groupId": groupId})

    def listGagGroupUser(self, groupId):
        """
        查询被禁言群成员方法 方法
        @param  groupId:群组Id。（必传）

        @return code:返回码，200 为正常.
        @return users:群组成员列表
        @return time:解禁时间。（yyyy-mm-dd hh:mm:ss）
        @return users:群成员 Id。
	    """
        return self.call_api(action='/group/user/gag/list',
                          params={"groupId": groupId})

    def chatroomJoin(self, userId, chatroomId):
        """
        加入聊天室方法 方法
        @param  chatroomId:要加入的聊天室 Id。（必传）
        @param  userId:要加入聊天室的用户 Id，可提交多个，最多不超过 50 个。（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/chatroom/join',
                          params={"userId": userId,
                                  "chatroomId": chatroomId})

    def stopDistributionChatroomMessage(self, chatroomId):
        """
        聊天室消息停止分发方法(可实现控制对聊天室中消息是否进行分发，停止分发后聊天室中用户发送的消息，融云服务端不会再将消息发送给聊天室中其他用户。) 方法
        @param  chatroomId:聊天室 Id。（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/chatroom/message/stopDistribution',
                          params={"chatroomId": chatroomId})

    def resumeDistributionChatroomMessage(self, chatroomId):
        """
        聊天室消息恢复分发方法 方法
        @param  chatroomId:聊天室 Id。（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/chatroom/message/resumeDistribution',
                          params={"chatroomId": chatroomId})

    def addGagChatroomUser(self, userId, chatroomId, minute):
        """
        添加禁言聊天室成员方法（在 App 中如果不想让某一用户在聊天室中发言时，可将此用户在聊天室中禁言，被禁言用户可以接收查看聊天室中用户聊天信息，但不能发送消息.） 方法
        @param  minute:禁言时长，以分钟为单位，最大值为43200分钟。（必传）
        @param  chatroomId:聊天室 Id。（必传）
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/chatroom/user/gag/add',
                          params={"userId": userId,
                                  "chatroomId": chatroomId,
                                  "minute": minute})

    def rollbackGagChatroomUser(self, userId, chatroomId):
        """
        移除禁言聊天室成员方法 方法
        @param  chatroomId:聊天室Id。（必传）
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/chatroom/user/gag/rollback',
                          params={"userId": userId,
                                  "chatroomId": chatroomId})

    def listGagChatroomUser(self, chatroomId):
        """
        查询被禁言聊天室成员方法 方法
        @param  chatroomId:聊天室 Id。（必传）

        @return code:返回码，200 为正常。
        @return users:聊天室被禁言用户列表。
        @return time:解禁时间。
        @return userId:群成员Id。
	    """
        return self.call_api(action='/chatroom/user/gag/list',
                          params={"chatroomId": chatroomId})

    def addChatroomBlockUser(self, userId, chatroomId, minute):
        """
        添加封禁聊天室成员方法 方法
        @param  minute:封禁时长，以分钟为单位，最大值为43200分钟。（必传）
        @param  chatroomId:聊天室 Id。（必传）
        @param  userId:用户 Id。（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/chatroom/user/block/add',
                          params={"userId": userId,
                                  "chatroomId": chatroomId,
                                  "minute": minute})

    def rollbackBlockChatroomUser(self, userId, chatroomId):
        """
        移除封禁聊天室成员方法 方法
        @param  chatroomId:聊天室 Id.（必传）
        @param  userId:用户 Id.（必传）

        @return code:返回码，200 为正常。
	    """
        return self.call_api(action='/chatroom/user/block/rollback',
                          params={"userId": userId,
                                  "chatroomId": chatroomId})

    def listBlockChatroomUser(self, chatroomId):
        """
        查询被封禁聊天室成员方法 方法
        @param  chatroomId:聊天室 Id.（必传）

        @return code:返回码，200 为正常。
        @return users:聊天室成员数组。
        @return time:解禁时间。
        @return userId:群成员 Id。
	    """
        return self.call_api(action='/chatroom/user/block/list',
                          params={"chatroomId": chatroomId})
