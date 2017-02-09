#!/usr/bin/env python
# encoding: utf-8
from .base import RongCloudBase, Response


class Wordfilter(RongCloudBase):
    """Server 开发指南, 请参阅 http://www.rongcloud.cn/docs/server.html"""

    def add(self, word):
        """
        添加敏感词方法（设置敏感词后，App 中用户不会收到含有敏感词的消息内容，默认最多设置 50 个敏感词。） 方法
        @param  word:敏感词，最长不超过 32 个字符。（必传）
	 
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
            action='/wordfilter/add.json',
            params={"word": word})
        return Response(r, desc)

    def getList(self):
        """
        查询敏感词列表方法 方法
	 
        @return code:返回码，200 为正常。
        @return word:敏感词内容。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "ListWordfilterReslut",
            "desc": "listWordfilter返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "word",
                "type": "String",
                "desc": "敏感词内容。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('API', 'POST', 'application/x-www-form-urlencoded'),
            action='/wordfilter/list.json',
            params={})
        return Response(r, desc)

    def delete(self, word):
        """
        移除敏感词方法（从敏感词列表中，移除某一敏感词。） 方法
        @param  word:敏感词，最长不超过 32 个字符。（必传）
	 
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
            action='/wordfilter/delete.json',
            params={"word": word})
        return Response(r, desc)
