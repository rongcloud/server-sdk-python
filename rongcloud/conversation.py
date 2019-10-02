import json

from rongcloud.module import Module, ParamException


class Conversation(Module):

    def __init__(self, rc):
        super().__init__(rc)

    def get_notification(self):
        return Notification(self._rc)


class Notification(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def set(self, conversation_type, user_id, target_id, is_muted):
        """
        设置用户某会话接收新消息时是否进行消息提醒。
        :param conversation_type:   会话类型，二人会话是 1，讨论组会话是 2，群组会话是 3，客服会话是 5，系统通知是 6，
                                    应用公众服务是 7，公众服务是 8 。（必传）
        :param user_id:             设置消息免打扰的用户 Id。（必传）
        :param target_id:           目标 Id，根据不同的 ConversationType，
                                    可能是用户 Id，讨论组 Id，群组 Id，客服 Id，公众号 Id。（必传）
        :param is_muted:            消息免打扰设置状态，0 表示为关闭，1 表示为开启。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/conversation/notification/set.json'
        format_str = 'conversationType={{ conversation_type }}' \
                     '&requestId={{ user_id }}' \
                     '&targetId={{ target_id }}' \
                     '&isMuted={{ is_muted }}'
        try:
            self._check_param(conversation_type, int, '1~8')
            self._check_param(user_id, str, '1~64')
            self._check_param(target_id, str, '1~64')
            self._check_param(is_muted, int, '0~1')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def get(self, conversation_type, user_id, target_id):
        """
        查询用户某一会话消息免打扰的设置状态。。
        :param conversation_type:   会话类型，二人会话是 1，讨论组会话是 2，群组会话是 3，客服会话是 5，系统通知是 6，
                                    应用公众服务是 7，公众服务是 8 。（必传）
        :param user_id:             设置消息免打扰的用户 Id。（必传）
        :param target_id:           目标 Id，根据不同的 ConversationType，
                                    可能是用户 Id，讨论组 Id，群组 Id，客服 Id，公众号 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；
                                    isMuted 消息免打扰设置状态，0 表示为关闭，1 表示为开启。
                                    如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/conversation/notification/get.json'
        format_str = 'conversationType={{ conversation_type }}' \
                     '&requestId={{ user_id }}' \
                     '&targetId={{ target_id }}'
        try:
            self._check_param(conversation_type, int, '1~8')
            self._check_param(user_id, str, '1~64')
            self._check_param(target_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
