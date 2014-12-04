#! /usr/bin/env python
# coding=utf-8

import os
import json
import logging
import random
import datetime
import hashlib
import platform

import requests

import util
import exceptions
from version import __version__


class ApiClient(object):
    api_host = "https://api.cn.rong.io"
    response_type = "json"
    library_details = "python %s" % platform.python_version()
    user_agent = "RongCloudSdk/RongCloud-Python-Sdk %s (%s)" % \
                 (library_details, __version__)

    ACTION_USER_TOKEN = "/user/getToken"
    ACTION_MESSAGE_PUBLISH = "/message/publish"
    ACTION_MESSAGE_SYSTEM_PUBLISH = "/message/system/publish"
    ACTION_MESSAGE_GROUP_PUBLISH = "/message/group/publish"
    ACTION_MESSAGE_CHATROOM_PUBLISH = "/message/chatroom/publish"
    ACTION_GROUP_SYNC = "/group/sync"
    ACTION_GROUP_CREATE = "/group/create"
    ACTION_GROUP_JOIN = "/group/join"
    ACTION_GROUP_QUIT = "/group/quit"
    ACTION_GROUP_DISMISS = "/group/dismiss"
    ACTION_CHATROOM_CREATE = "/chatroom/create"
    ACTION_CHATROOM_DESTROY = "/chatroom/destroy"
    ACTION_CHATROOM_QUERY = "/chatroom/query"


    def __init__(self, app_key=None, app_secret=None, verify=True):

        """ API 客户端
        Usage::
            >>> from rongcloud.api import ApiClient
            >>> client = ApiClient('xxxxx', 'xxxx')

            建议您将APPKEY, APPSECRET 保存在系统的环境变量中
            环境变量的键值分别为：rongcloud-app-key， rongcloud-app-secret

            >>> from rongcloud.api import ApiClient
            >>> client = ApiClient()

        :param app_key: 开发者平台分配的 App Key
        :param app_secret: 开发者平台分配的 App Secret。
        :param verify: 发送请求时是否验证SSL证书的有效性
        """

        self.app_key = app_key or os.environ.get('rongcloud-app-key')
        self.app_secret = app_secret or os.environ.get('rongcloud-app-secret')
        self.verify = verify

    def make_common_signature(self):

        """生成通用签名
        一般情况下，您不需要调用该方法
        文档详见 http://docs.rongcloud.cn/server.html#_API_调用签名规则
        :return: {'app-key':'xxx','nonce':'xxx','timestamp':'xxx','signature':'xxx'}
        """

        nonce = str(random.random())
        timestamp = str(
            int(datetime.datetime.now().strftime("%s")) * 1000
        )

        signature = hashlib.sha1(
            self.app_secret + nonce + timestamp
        ).hexdigest()

        return {
            "app-key": self.app_key,
            "nonce": nonce,
            "timestamp": timestamp,
            "signature": signature
        }

    def headers(self):
        """Default HTTP headers
        """
        return util.merge_dict(
            self.make_common_signature(),
            {
                "content-type": "application/x-www-form-urlencoded",
                "user-agent": self.user_agent
            }
        )

    def http_call(self, url, method, **kwargs):
        """Makes a http call. Logs response information.
        """
        logging.info("Request[%s]: %s" % (method, url))
        start_time = datetime.datetime.now()

        response = requests.request(method,
                                    url,
                                    verify=self.verify,
                                    **kwargs)

        duration = datetime.datetime.now() - start_time
        logging.info("Response[%d]: %s, Duration: %s.%ss." %
                     (response.status_code, response.reason,
                      duration.seconds, duration.microseconds))

        return self.handle_response(response,
                                    response.content.decode("utf-8"))

    def handle_response(self, response, content):
        """Validate HTTP response
        """
        status = response.status_code
        if status in (301, 302, 303, 307):
            raise exceptions.Redirection(response, content)
        elif 200 <= status <= 299:
            return json.loads(content) if content else {}
        elif status == 400:
            raise exceptions.BadRequest(response, content)
        elif status == 401:
            raise exceptions.UnauthorizedAccess(response, content)
        elif status == 403:
            raise exceptions.ForbiddenAccess(response, content)
        elif status == 404:
            raise exceptions.ResourceNotFound(response, content)
        elif status == 405:
            raise exceptions.MethodNotAllowed(response, content)
        elif status == 409:
            raise exceptions.ResourceConflict(response, content)
        elif status == 410:
            raise exceptions.ResourceGone(response, content)
        elif status == 422:
            raise exceptions.ResourceInvalid(response, content)
        elif 401 <= status <= 499:
            raise exceptions.ClientError(response, content)
        elif 500 <= status <= 599:
            raise exceptions.ServerError(response, content)
        else:
            raise exceptions.ConnectionError(response, content, "Unknown response code: #{response.code}")

    def post(self, action, params=None):

        """POST 应用参数到接口地址
        所有http请求由此处理，方法内部封装统一的签名规则及 API URL
        当有新的接口推出，而SDK未更新时，您可用该方法

        Usage::
            >>> from rongcloud.api import ApiClient
            >>> client = ApiClient()
            >>> client.post('/user/getToken', {})

        :param action: 接口地址，例如：/message/chatroom/publish
        :param params: 应用级别参数，{"fromUserId":"xxxx", "content":"xxxxx"}
        :return: {"code":200, "userId":"jlk456j5", "token":"sfd9823ihufi"}

        """
        return self.http_call(
            url=util.join_url(self.api_host, "%s.%s" % (action, self.response_type)),
            method="POST",
            data=params,
            headers=self.headers()
        )

    def user_get_token(self, user_id, name, portrait_uri):

        """ 获取token
        http://docs.rongcloud.cn/server.html#_获取_Token_方法

        :param user_id:
        :param name:
        :param portrait_uri:
        :return: {"code":200, "userId":"jlk456j5", "token":"sfd9823ihufi"}

        """
        return self.post(
            action=self.ACTION_USER_TOKEN,
            params={
                "userId": user_id,
                "name": name,
                "portraitUri": portrait_uri
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

        return self.post(
            action=self.ACTION_MESSAGE_SYSTEM_PUBLISH,
            params={
                "fromUserId": from_user_id,
                "toUserId": to_user_id,
                "objectName": object_name,
                "content": content,
                "pushContent": push_content if push_content is not None else "",
                "pushData": push_data if push_data is not None else ""
            }
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
        return self.post(
            action=self.ACTION_MESSAGE_SYSTEM_PUBLISH,
            params={
                "fromUserId": from_user_id,
                "toUserId": to_user_id,
                "objectName": object_name,
                "content": content,
                "pushContent": push_content if push_content is not None else '',
                "pushData": push_data if push_data is not None else ''
            }
        )

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
        return self.post(
            action=self.ACTION_MESSAGE_GROUP_PUBLISH,
            params={
                "fromUserId": from_user_id,
                "toGroupId": to_group_id,
                "objectName": object_name,
                "content": content,
                "pushContent": push_content if push_content is not None else '',
                "pushData": push_data if push_data is not None else ''
            }
        )

    def message_chatroom_publish(self, from_user_id,
                                 to_chatroom_id,
                                 object_name,
                                 content):

        """一个用户向聊天室发送消息
        http://docs.rongcloud.cn/server.html#_发送聊天室消息_方法

        :param from_user_id:发送人用户 Id。（必传）
        :param to_chatroom_id:接收聊天室Id，提供多个本参数可以实现向多个聊天室发送消息。（必传）
        :param object_name:消息类型，参考融云消息类型表.消息标志；可自定义消息类型。（必传）
        :param content:发送消息内容，参考融云消息类型表.示例说明；如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        :return:{"code":200}
        """

        return self.post(
            action=self.ACTION_MESSAGE_GROUP_PUBLISH,
            params={
                "fromUserId": from_user_id,
                "toGroupId": to_chatroom_id,
                "objectName": object_name,
                "content": content
            }
        )

    def group_sync(self, user_id, groups):

        """同步用户所属群组
        融云当前群组的架构设计决定，您不需要调用融云服务器去“创建”群组
        也就是告诉融云服务器哪些群组有哪些用户。
        您只需要同步当前用户所属的群组信息给融云服务器
        即相当于“订阅”或者“取消订阅”了所属群组的消息。
        融云会根据用户同步的群组数据，计算群组的成员信息并群发消息。

        :param user_id:用户Id
        :param groups: groupId 和 groupName 的对应关系.例如：{10001:'group1',10002:'group2'}
        :return:{"code":200}
        """

        group_mapping = {"group[%s]" % k:v for k, v in groups.items()}
        group_mapping.setdefault("userId", user_id)

        return self.post(action=self.ACTION_GROUP_SYNC, params=group_mapping)

    def group_create(self, user_id_list, group_id, group_name):

        """创建群组，并将用户加入该群组，用户将可以收到该群的消息。
        注：其实本方法是加入群组方法 /group/join 的别名。
        http://docs.rongcloud.cn/server.html#_创建群组_方法

        :param user_id_list:要加入群的用户 Id ，可以传递多个值:[userid1,userid2]
        :param group_id:要加入的群 Id。
        :param group_name:要加入的群 Id 对应的名称。
        :return:{"code":200}
        """
        return self.post(action=self.ACTION_GROUP_CREATE, params={
            "userId":user_id_list,
            "groupId":group_id,
            "groupName":group_name
        })

    def group_join(self, user_id_list, group_id, group_name):

        """将用户加入指定群组，用户将可以收到该群的消息
        http://docs.rongcloud.cn/server.html#_加入群组_方法


        :param user_id_list:要加入群的用户 [userid1,userid2 ...]
        :param group_id:要加入的群 Id。
        :param group_name:要加入的群 Id 对应的名称。
        :return:{"code":200}
        """
        return self.post(action=self.ACTION_GROUP_JOIN, params={
            "userId":user_id_list,
            "groupId":group_id,
            "groupName":group_name
        })

    def group_dismiss(self, user_id, group_id):

        """将该群解散，所有用户都无法再接收该群的消息。
        http://docs.rongcloud.cn/server.html#_解散群组_方法


        :param user_id: 操作解散群的用户 Id。
        :param group_id:要解散的群 Id。
        :return:{"code":200}
        """
        return self.post(action=self.ACTION_GROUP_DISMISS, params={
            "userId":user_id,
            "groupId":group_id,
        })

    def chatroom_create(self, chatrooms):

        """创建聊天室 方法
        http://docs.rongcloud.cn/server.html#_创建聊天室_方法
        :param chatrooms: {'r001':'room1'} id:要创建的聊天室的id；name:要创建的聊天室的name
        :return:{"code":200}
        """
        chatroom_mapping = {'chatroom[%s]' % k:v for k, v in chatrooms.items()}
        return self.post(action=self.ACTION_CHATROOM_CREATE, params=chatroom_mapping)

    def chatroom_destroy(self, chatroom_id_list=None):

        """销毁聊天室 方法
        当提交参数chatroomId多个时表示销毁多个聊天室

        http://docs.rongcloud.cn/server.html#_销毁聊天室_方法
        :param chatroom_id_list:要销毁的聊天室 Id。
        :return:{"code":200}

        """
        params={
            "chatroomId":chatroom_id_list
        } if chatroom_id_list is not None else {}

        return self.post(action=self.ACTION_CHATROOM_DESTROY, params=params)

    def chatroom_query(self, chatroom_id_list=None):

        """查询聊天室信息 方法

        http://docs.rongcloud.cn/server.html#_查询聊天室信息_方法

        :param chatroom_id_list:当提交多个时表示查询多个聊天室， 如果为None ，则查询所有聊天室
        :return:{"code":200,"chatRooms":[{"chatroomId":"id1001","name":"name1","time":"2014-01-01 1:1:1"},{"chatroomId":"id1002","name":"name2","time":"2014-01-01 1:1:2"}]}
        """

        params={
            "chatroomId":chatroom_id_list
        } if chatroom_id_list is not None else {}

        return self.post(action=self.ACTION_CHATROOM_QUERY, params=params)