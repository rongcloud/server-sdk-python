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

    def call_api(self, action, params=None, **kwargs):
        """
        调用API的通用方法，有关SSL证书验证问题请参阅

        http://www.python-requests.org/en/latest/user/advanced/#ssl-cert-verification

        :param action: Method Name，
        :param params: Dictionary,form params for api.
        :param timeout: (optional) Float describing the timeout of the request.
        :return:
        """
        return self._http_call(
            url=self._join_url(self.api_host, "%s.%s" % (action, self.response_type)),
            method="POST",
            data=params,
            headers=self._headers(),
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

