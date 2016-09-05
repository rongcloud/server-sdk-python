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


class RongCloudBase(object):
    api_host = "http://api.cn.ronghub.com"
    sms_host = "http://api.sms.ronghub.com"

    def __init__(self, key='', secret=''):
        self._app_key = key
        self._app_secret = secret

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

    def _headers(self, content_type):
        """Default HTTP headers """
        return self._merge_dict(self._make_common_signature(),
                                {"content-type": content_type})

    def _http_call(self, url, method, **kwargs):
        """Makes a http call. Logs response information."""
        logging.debug("Request[{0}]: {1}".format(method, url))
        start_time = datetime.datetime.now()

        logging.debug("Header: {0}".format(kwargs['headers']))
        logging.debug("Params: {0}".format(kwargs['data']))
        response = requests.request(method, url, verify=False, **kwargs)

        duration = datetime.datetime.now() - start_time
        logging.debug("Response[{0:d}]: {1}, Duration: {2}.{3}s.".format(
            response.status_code, response.reason, duration.seconds,
            duration.microseconds))
        return response

    def _filter_params(self, params):
        return {k: v for k, v in params.items() if v is not None}

    def call_api(self,
                 action,
                 params=None,
                 method=('API', 'POST', 'application/x-www-form-urlencoded'),
                 **kwargs):
        """
        :param method: methodName
        :param action: MethodUrl，
        :param params: Dictionary,form params for api.
        :param timeout: (optional) Float describing the timeout of the request.
        :return:
        """
        urltype, methodname, content_type = method
        if urltype == 'SMS':
            url = self.sms_host
        else:
            url = self.api_host
        if content_type == 'application/json':
            data = json.dumps(params)
        else:
            data = self._filter_params(params)
        return self._http_call(
            url=url + action,
            method=methodname,
            data=data,
            headers=self._headers(content_type),
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
