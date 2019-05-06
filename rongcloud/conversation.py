import json

from rongcloud.module import Module, ParamException


class Conversation(Module):
    CONVERSATION_PRIVATE = 1
    CONVERSATION_DISCUSSION = 2
    CONVERSATION_GROUP = 3
    CONVERSATION_CUSTOMER_SERVICE = 5
    CONVERSATION_SYSTEM = 6
    CONVERSATION_APP_PUBLIC = 7
    CONVERSATION_PUBLIC = 8

    def __init__(self, rc):
        super().__init__(rc)

    def mute(self, type, user_id, target_id):
        """
        设置用户某个会话屏蔽 Push。
        """
        param_dict = locals().copy()
        url = '/conversation/notification/set.json'
        format_str = 'conversationType={{ type }}' \
                     '&requestId={{ user_id }}' \
                     '&targetId={{ target_id }}' \
                     '&isMuted=1'
        try:
            self._check_param(type, int)
            self._check_param(user_id, str, '1-64')
            self._check_param(target_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def unmute(self, type, user_id, target_id):
        """
        设置用户某个会话接收 Push。
        """
        param_dict = locals().copy()
        url = '/conversation/notification/set.json'
        format_str = 'conversationType={{ type }}' \
                     '&requestId={{ user_id }}' \
                     '&targetId={{ target_id }}' \
                     '&isMuted=0'
        try:
            self._check_param(type, int)
            self._check_param(user_id, str, '1-64')
            self._check_param(target_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
