import json

from rongcloud.module import Module, ParamException


class Sensitive(Module):
    """
    设置敏感词后，App 中用户不会收到含有敏感词的消息内容，默认最多设置 50 个敏感词，设置后 2 小时内生效，
    目前只支持融云内置消息类型文本消息的敏感词过滤、替换功能，通过 Server API 发送的消息默认不支持敏感词过滤、替换，
    如果需要过滤敏感词请提交工单申请开通。
    敏感词过滤方式有两种：屏蔽包含敏感词的消息和替换敏感词，详细请查看屏蔽包含敏感词的消息与替换敏感词功能说明
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, word, replace_word=None):
        """
        添加敏感词。
        :param word:                敏感词，最长不超过 32 个字符，格式为汉字、数字、字母。（必传）
        :param replace_word:        需要替换的敏感词，最长不超过 32 个字符，（非必传）。
                                    如未设置替换的敏感词，当消息中含有敏感词时，消息将被屏蔽，用户不会收到消息。
                                    如设置了替换敏感词，当消息中含有敏感词时，将被替换为指定的字符进行发送。
                                    敏感词替换目前只支持单聊、群聊、聊天室会话。
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/sensitiveword/add.json'
        format_str = 'word={{ word }}' \
                     '{% if replace_word is not none %}&replaceWord={{ replace_word }}{% endif %}'
        try:
            self._check_param(word, str, '1~32')
            self._check_param(replace_word, str, '1~32')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, words):
        """
        从敏感词列表中，移除某一敏感词，移除后 2 小时内生效。
        :param words:               敏感词或敏感词列表，敏感词最长不超过 32 个字符。（必传）
                                    一次最多移除敏感词不超过 50 个，移除后 2 小时内生效。
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        words = self._tran_list(words)
        param_dict = locals().copy()
        if len(words) == 1:
            url = '/sensitiveword/delete.json'
            format_str = 'word={{ words }}'
            try:
                self._check_param(words, list, '1~1')
                for user in words:
                    self._check_param(user, str, '1~32')
                return self._http_post(url, self._render(param_dict, format_str))
            except ParamException as e:
                return json.loads(str(e))
        else:
            url = '/sensitiveword/batch/delete.json'
            format_str = '{% for item in words %}words={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
            try:
                self._check_param(words, list, '1~50')
                for user in words:
                    self._check_param(user, str, '1~32')
                return self._http_post(url, self._render(param_dict, format_str))
            except ParamException as e:
                return json.loads(str(e))

    def query(self, word_type=1):
        """
        查询敏感词列表。
        :param word_type:           查询敏感词的类型，0 为查询替换敏感词，1 为查询屏蔽敏感词，2 为查询全部敏感词。默认为 1。（非必传）
        :return:                    请求返回结果，code 返回码，200 为正常；word 敏感词内容；
                                    replaceWord 替换敏感词的内容，为空时对应 Word 敏感词类型为屏蔽敏感词。
                                    如：{"code":200,"words":[{"type":"0","word":"黄赌毒","replaceWord":"***"},
                                    {"type":"1","word":"qqq","replaceWord":""}]}
        """
        param_dict = locals().copy()
        url = '/sensitiveword/list.json'
        format_str = 'type={{ word_type }}'
        try:
            self._check_param(word_type, int, '0~2')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
