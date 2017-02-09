#!/usr/bin/env python
# encoding: utf-8
from .base import RongCloudBase, Response


class Push(RongCloudBase):
    """Server 开发指南, 请参阅 http://www.rongcloud.cn/docs/server.html"""

    def setUserPushTag(self, userTag):
        """
        添加 Push 标签方法 方法
        @param  userTag:用户标签。
	 
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
            method=('API', 'POST', 'application/json'),
            action='/user/tag/set.json',
            params=userTag)
        return Response(r, desc)

    def broadcastPush(self, pushMessage):
        """
        广播消息方法（fromuserid 和 message为null即为不落地的push） 方法
        @param  pushMessage:json数据
	 
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
            method=('API', 'POST', 'application/json'),
            action='/push.json',
            params=pushMessage)
        return Response(r, desc)
