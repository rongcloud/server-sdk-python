#!/usr/bin/env python
# encoding: utf-8
from .base import RongCloudBase, Response


class Chatroom(RongCloudBase):
    """Server 开发指南, 请参阅 http://www.rongcloud.cn/docs/server.html"""

    def create(self, chatRoomInfo):
        """
        创建聊天室方法 方法
        @param  chatRoomInfo:id:要创建的聊天室的id；name:要创建的聊天室的name。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        params = {
            'chatroom[{0}]'.format(Id): name
            for Id, name in chatRoomInfo
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/create.json',
            params=params)
        return Response(r, desc)

    def join(self, userId, chatroomId):
        """
        加入聊天室方法 方法
        @param  userId:要加入聊天室的用户 Id，可提交多个，最多不超过 50 个。（必传）
        @param  chatroomId:要加入的聊天室 Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/join.json',
            params={"userId": userId,
                    "chatroomId": chatroomId})
        return Response(r, desc)

    def query(self, chatroomId):
        """
        查询聊天室信息方法 方法
        @param  chatroomId:要查询的聊天室id（必传）
	 
        @return code:返回码，200 为正常。
        @return chatRooms:聊天室信息数组。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "ChatroomQueryReslut",
            "desc": " chatroomQuery 返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "chatRooms",
                "type": "List<ChatRoom>",
                "desc": "聊天室信息数组。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/query.json',
            params={"chatroomId": chatroomId})
        return Response(r, desc)

    def queryUser(self, chatroomId, count, order):
        """
        查询聊天室内用户方法 方法
        @param  chatroomId:要查询的聊天室 ID。（必传）
        @param  count:要获取的聊天室成员数，上限为 500 ，超过 500 时最多返回 500 个成员。（必传）
        @param  order:加入聊天室的先后顺序， 1 为加入时间正序， 2 为加入时间倒序。（必传）
	 
        @return code:返回码，200 为正常。
        @return total:聊天室中用户数。
        @return users:聊天室成员列表。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "ChatroomUserQueryReslut",
            "desc": " chatroomUserQuery 返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "total",
                "type": "Integer",
                "desc": "聊天室中用户数。"
            }, {
                "name": "users",
                "type": "List<ChatRoomUser>",
                "desc": "聊天室成员列表。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/user/query.json',
            params={"chatroomId": chatroomId,
                    "count": count,
                    "order": order})
        return Response(r, desc)

    def stopDistributionMessage(self, chatroomId):
        """
        聊天室消息停止分发方法（可实现控制对聊天室中消息是否进行分发，停止分发后聊天室中用户发送的消息，融云服务端不会再将消息发送给聊天室中其他用户。） 方法
        @param  chatroomId:聊天室 Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/message/stopDistribution.json',
            params={"chatroomId": chatroomId})
        return Response(r, desc)

    def resumeDistributionMessage(self, chatroomId):
        """
        聊天室消息恢复分发方法 方法
        @param  chatroomId:聊天室 Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/message/resumeDistribution.json',
            params={"chatroomId": chatroomId})
        return Response(r, desc)

    def addGagUser(self, userId, chatroomId, minute):
        """
        添加禁言聊天室成员方法（在 App 中如果不想让某一用户在聊天室中发言时，可将此用户在聊天室中禁言，被禁言用户可以接收查看聊天室中用户聊天信息，但不能发送消息.） 方法
        @param  userId:用户 Id。（必传）
        @param  chatroomId:聊天室 Id。（必传）
        @param  minute:禁言时长，以分钟为单位，最大值为43200分钟。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/user/gag/add.json',
            params={
                "userId": userId,
                "chatroomId": chatroomId,
                "minute": minute
            })
        return Response(r, desc)

    def ListGagUser(self, chatroomId):
        """
        查询被禁言聊天室成员方法 方法
        @param  chatroomId:聊天室 Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return users:聊天室被禁言用户列表。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "ListGagChatroomUserReslut",
            "desc": "listGagChatroomUser返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "users",
                "type": "List<GagChatRoomUser>",
                "desc": "聊天室被禁言用户列表。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/user/gag/list.json',
            params={"chatroomId": chatroomId})
        return Response(r, desc)

    def rollbackGagUser(self, userId, chatroomId):
        """
        移除禁言聊天室成员方法 方法
        @param  userId:用户 Id。（必传）
        @param  chatroomId:聊天室Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/user/gag/rollback.json',
            params={"userId": userId,
                    "chatroomId": chatroomId})
        return Response(r, desc)

    def addBlockUser(self, userId, chatroomId, minute):
        """
        添加封禁聊天室成员方法 方法
        @param  userId:用户 Id。（必传）
        @param  chatroomId:聊天室 Id。（必传）
        @param  minute:封禁时长，以分钟为单位，最大值为43200分钟。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/user/block/add.json',
            params={
                "userId": userId,
                "chatroomId": chatroomId,
                "minute": minute
            })
        return Response(r, desc)

    def getListBlockUser(self, chatroomId):
        """
        查询被封禁聊天室成员方法 方法
        @param  chatroomId:聊天室 Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return users:被封禁用户列表。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "ListBlockChatroomUserReslut",
            "desc": "listBlockChatroomUser返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "users",
                "type": "List<BlockChatRoomUser>",
                "desc": "被封禁用户列表。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/user/block/list.json',
            params={"chatroomId": chatroomId})
        return Response(r, desc)

    def rollbackBlockUser(self, userId, chatroomId):
        """
        移除封禁聊天室成员方法 方法
        @param  userId:用户 Id。（必传）
        @param  chatroomId:聊天室 Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/user/block/rollback.json',
            params={"userId": userId,
                    "chatroomId": chatroomId})
        return Response(r, desc)

    def addPriority(self, objectName):
        """
        添加聊天室消息优先级方法 方法
        @param  objectName:低优先级的消息类型，每次最多提交 5 个，设置的消息类型最多不超过 20 个。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/message/priority/add.json',
            params={"objectName": objectName})
        return Response(r, desc)

    def destroy(self, chatroomId):
        """
        销毁聊天室方法 方法
        @param  chatroomId:要销毁的聊天室 Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/destroy.json',
            params={"chatroomId": chatroomId})
        return Response(r, desc)

    def addWhiteListUser(self, chatroomId, userId):
        """
        添加聊天室白名单成员方法 方法
        @param  chatroomId:聊天室中用户 Id，可提交多个，聊天室中白名单用户最多不超过 5 个。（必传）
        @param  userId:聊天室 Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CodeSuccessReslut",
            "desc": " http 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/chatroom/user/whitelist/add.json',
            params={"chatroomId": chatroomId,
                    "userId": userId})
        return Response(r, desc)
