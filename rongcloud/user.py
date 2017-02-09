#!/usr/bin/env python
# encoding: utf-8
from .base import RongCloudBase, Response


class User(RongCloudBase):
    """Server 开发指南, 请参阅 http://www.rongcloud.cn/docs/server.html"""

    def getToken(self, userId, name, portraitUri):
        """
        获取 Token 方法 方法
        @param  userId:用户 Id，最大长度 64 字节.是用户在 App 中的唯一标识码，必须保证在同一个 App 内不重复，重复的用户 Id 将被当作是同一用户。（必传）
        @param  name:用户名称，最大长度 128 字节.用来在 Push 推送时显示用户的名称.用户名称，最大长度 128 字节.用来在 Push 推送时显示用户的名称。（必传）
        @param  portraitUri:用户头像 URI，最大长度 1024 字节.用来在 Push 推送时显示用户的头像。（必传）
	 
        @return code:返回码，200 为正常.如果您正在使用开发环境的 AppKey，您的应用只能注册 100 名用户，达到上限后，将返回错误码 2007.如果您需要更多的测试账户数量，您需要在应用配置中申请“增加测试人数”。
        @return token:用户 Token，可以保存应用内，长度在 256 字节以内.用户 Token，可以保存应用内，长度在 256 字节以内。
        @return userId:用户 Id，与输入的用户 Id 相同.用户 Id，与输入的用户 Id 相同。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "TokenReslut",
            "desc": "getToken 返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc":
                "返回码，200 为正常.如果您正在使用开发环境的 AppKey，您的应用只能注册 100 名用户，达到上限后，将返回错误码 2007.如果您需要更多的测试账户数量，您需要在应用配置中申请“增加测试人数”。"
            }, {
                "name": "token",
                "type": "String",
                "desc":
                "用户 Token，可以保存应用内，长度在 256 字节以内.用户 Token，可以保存应用内，长度在 256 字节以内。"
            }, {
                "name": "userId",
                "type": "String",
                "desc": "用户 Id，与输入的用户 Id 相同.用户 Id，与输入的用户 Id 相同。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/user/getToken.json',
            params={
                "userId": userId,
                "name": name,
                "portraitUri": portraitUri
            })
        return Response(r, desc)

    def refresh(self, userId, name=None, portraitUri=None):
        """
        刷新用户信息方法 方法
        @param  userId:用户 Id，最大长度 64 字节.是用户在 App 中的唯一标识码，必须保证在同一个 App 内不重复，重复的用户 Id 将被当作是同一用户。（必传）
        @param  name:用户名称，最大长度 128 字节。用来在 Push 推送时，显示用户的名称，刷新用户名称后 5 分钟内生效。（可选，提供即刷新，不提供忽略）
        @param  portraitUri:用户头像 URI，最大长度 1024 字节。用来在 Push 推送时显示。（可选，提供即刷新，不提供忽略）
	 
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
            action='/user/refresh.json',
            params={
                "userId": userId,
                "name": name,
                "portraitUri": portraitUri
            })
        return Response(r, desc)

    def checkOnline(self, userId):
        """
        检查用户在线状态 方法 方法
        @param  userId:用户 Id，最大长度 64 字节。是用户在 App 中的唯一标识码，必须保证在同一个 App 内不重复，重复的用户 Id 将被当作是同一用户。（必传）
	 
        @return code:返回码，200 为正常。
        @return status:在线状态，1为在线，0为不在线。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "CheckOnlineReslut",
            "desc": "checkOnlineUser返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "status",
                "type": "String",
                "desc": "在线状态，1为在线，0为不在线。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/user/checkOnline.json',
            params={"userId": userId})
        return Response(r, desc)

    def block(self, userId, minute):
        """
        封禁用户方法（每秒钟限 100 次） 方法
        @param  userId:用户 Id。（必传）
        @param  minute:封禁时长,单位为分钟，最大值为43200分钟。（必传）
	 
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
            action='/user/block.json',
            params={"userId": userId,
                    "minute": minute})
        return Response(r, desc)

    def unBlock(self, userId):
        """
        解除用户封禁方法（每秒钟限 100 次） 方法
        @param  userId:用户 Id。（必传）
	 
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
            action='/user/unblock.json',
            params={"userId": userId})
        return Response(r, desc)

    def queryBlock(self):
        """
        获取被封禁用户方法（每秒钟限 100 次） 方法
	 
        @return code:返回码，200 为正常。
        @return users:被封禁用户列表。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "QueryBlockUserReslut",
            "desc": "queryBlockUser返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "users",
                "type": "List<BlockUsers>",
                "desc": "被封禁用户列表。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/user/block/query.json',
            params={})
        return Response(r, desc)

    def addBlacklist(self, userId, blackUserId):
        """
        添加用户到黑名单方法（每秒钟限 100 次） 方法
        @param  userId:用户 Id。（必传）
        @param  blackUserId:被加到黑名单的用户Id。（必传）
	 
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
            action='/user/blacklist/add.json',
            params={"userId": userId,
                    "blackUserId": blackUserId})
        return Response(r, desc)

    def queryBlacklist(self, userId):
        """
        获取某用户的黑名单列表方法（每秒钟限 100 次） 方法
        @param  userId:用户 Id。（必传）
	 
        @return code:返回码，200 为正常。
        @return users:黑名单用户列表。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "QueryBlacklistUserReslut",
            "desc": "queryBlacklistUser返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "users",
                "type": "String[]",
                "desc": "黑名单用户列表。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/user/blacklist/query.json',
            params={"userId": userId})
        return Response(r, desc)

    def removeBlacklist(self, userId, blackUserId):
        """
        从黑名单中移除用户方法（每秒钟限 100 次） 方法
        @param  userId:用户 Id。（必传）
        @param  blackUserId:被移除的用户Id。（必传）
	 
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
            action='/user/blacklist/remove.json',
            params={"userId": userId,
                    "blackUserId": blackUserId})
        return Response(r, desc)
