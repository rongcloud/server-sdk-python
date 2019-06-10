import json

from rongcloud.module import Module, ParamException


class Sensitive(Module):
    """
    默认最多设置 50 个敏感词， 设置 2 小时后生效，目前仅支持 文本消息(RC:TxtMsg) 的敏感词过滤、替换功能。
    默认不过滤、不替换 Server API 发送的消息，需要过滤敏、替换请 提交工单 申请开通。
    敏感词替换目前只支持单聊、群聊、聊天室会话类型消息
    """
    SENSITIVE_REPLACE = 0
    SENSITIVE_BLOCK = 1
    SENSITIVE_ALL = 2

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, keyword, replace=None):
        """
        添加敏感词。
        :param keyword: 需要被替换的敏感词，最长不超过 32 个字符，格式为汉字、数字、字母。
        :param replace: 替换后的敏感词，最长不超过 32 个字符。若为空则代表直接屏蔽。
        """
        param_dict = locals().copy()
        url = '/sensitiveword/add.json'
        format_str = 'word={{ keyword }}' \
                     '{% if replace is not none %}&replaceWord={{ replace }}{% endif %}'
        try:
            self._check_param(keyword, str, '1-32')
            self._check_param(replace, str, '1-32')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, keywords):
        """
        删除敏感词。
        :param keywords: 敏感词或敏感词列表，最多不超过 50 个敏感词。
        """
        keywords = self._tran_list(keywords)
        param_dict = locals().copy()
        url = '/sensitiveword/batch/delete.json'
        format_str = '{% for item in keywords %}words={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(keywords, list, '1-50')
            for user in keywords:
                self._check_param(user, str, '1-32')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, type=1):
        """
        获取敏感词列表。
        :param type: 查询敏感词的类型，0 为查询替换敏感词，1 为查询屏蔽敏感词，2 为查询全部敏感词。默认为 1。（非必传）
        """
        param_dict = locals().copy()
        url = '/sensitiveword/list.json'
        format_str = 'type={{ type }}'
        try:
            self._check_param(type, int, '0-2')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))