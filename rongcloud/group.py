#!/usr/bin/env python
# encoding: utf-8
from .base import RongCloudBase, Response


class Group(RongCloudBase):
    """Server 开发指南, 请参阅 http://www.rongcloud.cn/docs/server.html"""

    def create(self, userId, groupId, groupName):
        """
        创建群组方法（创建群组，并将用户加入该群组，用户将可以收到该群的消息，同一用户最多可加入 500 个群，每个群最大至 3000 人，App 内的群组数量没有限制.注：其实本方法是加入群组方法 /group/join 的别名。） 方法
        @param  userId:要加入群的用户 Id。（必传）
        @param  groupId:创建群组 Id。（必传）
        @param  groupName:群组 Id 对应的名称。（必传）
	 
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
            action='/group/create.json',
            params={
                "userId": userId,
                "groupId": groupId,
                "groupName": groupName
            })
        return Response(r, desc)

    def sync(self, userId, groupInfo):
        """
        同步用户所属群组方法（当第一次连接融云服务器时，需要向融云服务器提交 userId 对应的用户当前所加入的所有群组，此接口主要为防止应用中用户群信息同融云已知的用户所属群信息不同步。） 方法
        @param  userId:被同步群信息的用户 Id。（必传）
        @param  groupInfo:该用户的群信息，如群 Id 已经存在，则不会刷新对应群组名称，如果想刷新群组名称请调用刷新群组信息方法。
	 
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
        params = {'group[{0}]'.format(Id): name for Id, name in groupInfo}
        params['userId'] = userId
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/group/sync.json',
            params=params)
        return Response(r, desc)

    def refresh(self, groupId, groupName):
        """
        刷新群组信息方法 方法
        @param  groupId:群组 Id。（必传）
        @param  groupName:群名称。（必传）
	 
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
            action='/group/refresh.json',
            params={"groupId": groupId,
                    "groupName": groupName})
        return Response(r, desc)

    def join(self, userId, groupId, groupName):
        """
        将用户加入指定群组，用户将可以收到该群的消息，同一用户最多可加入 500 个群，每个群最大至 3000 人。 方法
        @param  userId:要加入群的用户 Id，可提交多个，最多不超过 1000 个。（必传）
        @param  groupId:要加入的群 Id。（必传）
        @param  groupName:要加入的群 Id 对应的名称。（必传）
	 
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
            action='/group/join.json',
            params={
                "userId": userId,
                "groupId": groupId,
                "groupName": groupName
            })
        return Response(r, desc)

    def queryUser(self, groupId):
        """
        查询群成员方法 方法
        @param  groupId:群组Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return id:群成员用户Id。
        @return users:群成员列表。
	    """

        desc = {
            "name": "GroupUserQueryReslut",
            "desc": "groupUserQuery返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "id",
                "type": "String",
                "desc": "群成员用户Id。"
            }, {
                "name": "users",
                "type": "List<GroupUser>",
                "desc": "群成员列表。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/group/user/query.json',
            params={"groupId": groupId})
        return Response(r, desc)

    def quit(self, userId, groupId):
        """
        退出群组方法（将用户从群中移除，不再接收该群组的消息.） 方法
        @param  userId:要退出群的用户 Id.（必传）
        @param  groupId:要退出的群 Id.（必传）
	 
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
            action='/group/quit.json',
            params={"userId": userId,
                    "groupId": groupId})
        return Response(r, desc)

    def addGagUser(self, userId, groupId, minute):
        """
        添加禁言群成员方法（在 App 中如果不想让某一用户在群中发言时，可将此用户在群组中禁言，被禁言用户可以接收查看群组中用户聊天信息，但不能发送消息。） 方法
        @param  userId:用户 Id。（必传）
        @param  groupId:群组 Id。（必传）
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
            action='/group/user/gag/add.json',
            params={"userId": userId,
                    "groupId": groupId,
                    "minute": minute})
        return Response(r, desc)

    def lisGagUser(self, groupId):
        """
        查询被禁言群成员方法 方法
        @param  groupId:群组Id。（必传）
	 
        @return code:返回码，200 为正常.
        @return users:群组被禁言用户列表。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "ListGagGroupUserReslut",
            "desc": " lisitGagGroupUser 返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常."
            }, {
                "name": "users",
                "type": "List<GagGroupUser>",
                "desc": "群组被禁言用户列表。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/group/user/gag/list.json',
            params={"groupId": groupId})
        return Response(r, desc)

    def rollBackGagUser(self, userId, groupId):
        """
        移除禁言群成员方法 方法
        @param  userId:用户Id。支持同时移除多个群成员（必传）
        @param  groupId:群组Id。（必传）
	 
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
            action='/group/user/gag/rollback.json',
            params={"userId": userId,
                    "groupId": groupId})
        return Response(r, desc)

    def dismiss(self, userId, groupId):
        """
        解散群组方法。（将该群解散，所有用户都无法再接收该群的消息。） 方法
        @param  userId:操作解散群的用户 Id。（必传）
        @param  groupId:要解散的群 Id。（必传）
	 
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
            action='/group/dismiss.json',
            params={"userId": userId,
                    "groupId": groupId})
        return Response(r, desc)
