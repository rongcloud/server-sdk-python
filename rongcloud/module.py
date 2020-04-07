import hashlib
import json
import random
import socket
import time
from urllib import request
from urllib.error import HTTPError, URLError

from jinja2 import Template

HEADER_APP_KEY = 'App-Key'
HEADER_NONCE = 'Nonce'
HEADER_TIMESTAMP = 'Timestamp'
HEADER_SIGNATURE = 'Signature'
HEADER_USER_AGENT = 'User-Agent'
HEADER_CONTENT_TYPE = 'Content-Type'


class ParamException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info


class Module:
    def __init__(self, rc):
        self._rc = rc
        socket.setdefaulttimeout(10)

    def _signature(self):
        nonce = str(random.randint(0, 1000000000))
        timestamp = str(int(time.time()))
        sha1 = (self._rc.app_secret + nonce + timestamp).encode('utf8')
        signature = hashlib.sha1(sha1).hexdigest()
        return {HEADER_APP_KEY: self._rc.app_key,
                HEADER_NONCE: nonce,
                HEADER_TIMESTAMP: timestamp,
                HEADER_SIGNATURE: signature,
                HEADER_USER_AGENT: 'rc-python-sdk/3.1.1'}

    def _http_post(self, url, data=''):
        data = '{}'.encode('utf-8') if data is None else data.encode('utf-8')
        headers = self._signature()
        try:
            json.loads(data)
            headers[HEADER_CONTENT_TYPE] = 'application/json'
        except ValueError:
            pass
        try:
            req = request.Request(self._rc.host_url.get_url() + url, headers=headers, data=data)
            rep = request.urlopen(req).read()
        except HTTPError as e:
            rep = e.read()
        except URLError:
            self._rc.host_url.switch_url()
            rep = json.loads('{"code":-1, "reason":"URL error."}')
        except socket.timeout:
            self._rc.host_url.switch_url()
            rep = json.loads('{"code":-1, "reason":"Socket timeout."}')
        else:
            rep = json.loads(rep.decode('utf8'))
        return rep

    @staticmethod
    def _check_param(obj, obj_type, obj_range=None):
        if obj is None:
            return
        if type(obj) != obj_type:
            raise ParamException('{{"code":1002, "msg":"{} 参数类型错误！"}}'.format(obj))

        if type(obj) == int:
            obj_len = obj
        elif type(obj) == str or type(obj) == list:
            obj_len = len(obj)
        else:
            return
        if obj_range is not None:
            r_min, r_max = obj_range.split('~')
            if obj_len < int(r_min) or obj_len > int(r_max):
                raise ParamException('{{"code":1002, "msg":"{} 长度超限，应 >= {} 且 <= {}"}}'.format(obj, r_min, r_max))

    @staticmethod
    def _render(params, format_str):
        template = Template(format_str)
        data = template.render(params)
        return data

    @staticmethod
    def _tran_list(param):
        if type(param) is str:
            return [param]
        return param
