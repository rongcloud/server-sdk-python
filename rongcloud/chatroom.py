import json

from rongcloud.module import Module, ParamException


class Chatroom(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def create(self, room_id, name):
        """
        创建聊天室。
        """
        param_dict = locals().copy()
        url = '/chatroom/create.json'
        format_str = 'chatroom[{{ room_id }}]={{ name }}'
        try:
            self._check_param(room_id, str, '1-64')
            self._check_param(name, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def destory(self, room_id):
        """
        销毁聊天室，禁言、封禁关系不销毁。
        """
        param_dict = locals().copy()
        url = '/chatroom/destroy.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, room_id):
        """
        获取聊天室信息，返回按时间排序后的最多 500 个成员信息。
        """
        param_dict = locals().copy()
        url = '/chatroom/user/query.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def is_exist(self, room_id, user_id):
        """
        检查用户是否在聊天室。
        """
        param_dict = locals().copy()
        url = '/chatroom/users/exist.json'
        format_str = 'chatroomId={{ room_id }}' \
                     '&userId={{ user_id }}'
        try:
            self._check_param(room_id, str, '1-64')
            self._check_param(user_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def get_block(self):
        return Block(self._rc)

    def get_ban(self):
        return Ban(self._rc)

    def get_gag(self):
        return Gag(self._rc)

    def get_demotion(self):
        return Demotion(self._rc)

    def get_distribute(self):
        return Distribute(self._rc)

    def get_keep_alive(self):
        return KeepAlive(self._rc)

    def get_message_while_list(self):
        return MessageWhileList(self._rc)

    def get_user_while_list(self):
        return UserWhileList(self._rc)


class Block(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, room_id, minute):
        """
        将用户踢出聊天室，并在设置禁言的时间范围内禁止加入指定聊天室，多次调用，以最后一次为准。
        :param user_ids: 封禁用户 ID 或 ID 列表，最多不超过 20 个用户。
        :param room_id: 聊天室 Id。
        :param minute: 封禁时长，以分钟为单位，最大值为43200分钟。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/block/add.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&chatroomId={{ room_id }}' \
                     '&minute={{ minute }}'
        try:
            self._check_param(user_ids, list, '1-20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1-64')
            self._check_param(room_id, str, '1-64')
            self._check_param(minute, int, '1-43200')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids, room_id):
        """
        解除封禁。
        :param user_ids: 解封用户 ID 或 ID 列表，最多不超过 20 个用户。
        :param room_id: 聊天室 Id。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/block/rollback.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&chatroomId={{ room_id }}'
        try:
            self._check_param(user_ids, list, '1-20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1-64')
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, room_id):
        """
        查询被封禁成员列表。
        :param room_id: 聊天室 Id。
        """
        param_dict = locals().copy()
        url = '/chatroom/user/block/list.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class Ban(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, minute):
        """
        禁止用户在应用内所有聊天室中发言，可将此用户添加到聊天室全局禁言中，被禁言用户可以接收聊天室中聊天信息，但不能发送消息
        多次调用，以最后一次为准。此功能需开通 专有云服务。
        :param user_ids: 封禁用户 ID 或 ID 列表，最多不超过 20 个用户。
        :param minute: 封禁时长，以分钟为单位，最大值为43200分钟。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/ban/add.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&minute={{ minute }}'
        try:
            self._check_param(user_ids, list, '1-20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1-64')
            self._check_param(minute, int, '1-43200')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids):
        """
        解除聊天室全局禁言。
        :param user_ids: 解禁用户 ID 或 ID 列表，最多不超过 20 个用户。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/ban/remove.json'
        format_str = '{% for item in user_ids %}userId={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(user_ids, list, '1-20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self):
        """
        获取聊天室全局禁言列表。
        """
        param_dict = locals().copy()
        url = '/chatroom/user/ban/query.json'
        return self._http_post(url)


class Gag(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, room_id, minute):
        """
        添加聊天室成员禁言，多次调用，以最后一次为准。
        :param user_ids: 封禁用户 ID 或 ID 列表，最多不超过 20 个用户。
        :param room_id: 聊天室 Id。
        :param minute: 封禁时长，以分钟为单位，最大值为43200分钟。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/gag/add.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&chatroomId={{ room_id }}' \
                     '&minute={{ minute }}'
        try:
            self._check_param(user_ids, list, '1-20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1-64')
            self._check_param(room_id, str, '1-64')
            self._check_param(minute, int, '1-43200')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids, room_id):
        """
        解除聊天室成员禁言。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/gag/rollback.json'
        format_str = '{% for item in user_ids %}userId={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}' \
                     '&chatroomId={{ room_id }}'
        try:
            self._check_param(user_ids, list, '1-20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1-64')
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, room_id):
        """
        获取聊天室成员禁言列表。
        :param room_id: 聊天室 Id。
        """
        param_dict = locals().copy()
        url = '/chatroom/user/gag/list.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class Demotion(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def add(self, obj_names):
        """
        添加应用内聊天室降级消息。
        :param obj_names: 低优先级的消息类型，每次最多提交 5 个。
        """
        obj_names = self._tran_list(obj_names)
        param_dict = locals().copy()
        url = '/chatroom/message/priority/add.json'
        format_str = '{% for item in obj_names %}objectName={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(obj_names, list, '1-5')
            for obj_name in obj_names:
                self._check_param(obj_name, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, obj_names):
        """
        移除应用内聊天室降级消息。
        :param obj_names: 低优先级的消息类型，每次最多提交 5 个。
        """
        obj_names = self._tran_list(obj_names)
        param_dict = locals().copy()
        url = '/chatroom/message/priority/remove.json'
        format_str = '{% for item in obj_names %}objectName={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(obj_names, list, '1-5')
            for obj_name in obj_names:
                self._check_param(obj_name, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self):
        """
        获取应用内聊天室降级消息。
        """
        url = '/chatroom/message/priority/query.json'
        return self._http_post(url)


class Distribute(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def stop(self, room_id):
        """
        停止聊天室消息分发。
        """
        param_dict = locals().copy()
        url = '/chatroom/message/stopDistribution.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def resume(self, room_id):
        """
        恢复聊天室消息分发。
        """
        param_dict = locals().copy()
        url = '/chatroom/message/resumeDistribution.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class KeepAlive(Module):
    """
    聊天室中 1 小时无人说话，同时没有人加入聊天室时，融云服务端会自动把聊天室内所有成员踢出并销毁聊天室。
    如果不希望聊天室自动销毁，可用此接口将指定聊天室做保活处理，聊天室不会自动销毁。
    此功能需开通专有云服务。
    """
    def __init__(self, rc):
        super().__init__(rc)

    def add(self, room_id):
        """
        添加保活聊天室。
        """
        param_dict = locals().copy()
        url = '/chatroom/keepalive/add.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, room_id):
        """
        删除保活聊天室。
        """
        param_dict = locals().copy()
        url = '/chatroom/keepalive/remove.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self):
        """
        获取保活聊天室。
        """
        param_dict = locals().copy()
        url = '/chatroom/keepalive/query.json'
        return self._http_post(url)


class MessageWhileList(Module):
    """
    设置消息白名单后，服务器负载高时聊天室中此类型消息不会被丢弃，设置 2 后小时生效。
    设置白名单后，消息优先级高于 High Level 消息。
    此功能需开通专有云服务。
    """
    def __init__(self, rc):
        super().__init__(rc)

    def add(self, obj_names):
        """
        添加聊天室消息白名单。
        :param obj_names: 消息标识，最多不超过 20 个。
        """
        obj_names = self._tran_list(obj_names)
        param_dict = locals().copy()
        url = '/chatroom/whitelist/add.json'
        format_str = '{% for item in obj_names %}objectnames={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(obj_names, list, '1-20')
            for obj_name in obj_names:
                self._check_param(obj_name, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, obj_names):
        """
        删除聊天室消息白名单。
        :param obj_names: 消息标识，最多不超过 20 个。
        """
        obj_names = self._tran_list(obj_names)
        param_dict = locals().copy()
        url = '/chatroom/whitelist/delete.json'
        format_str = '{% for item in obj_names %}objectnames={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(obj_names, list, '1-20')
            for obj_name in obj_names:
                self._check_param(obj_name, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self):
        """
        获取聊天室消息白名单。
        """
        url = '/chatroom/whitelist/query.json'
        return self._http_post(url)


class UserWhileList(Module):
    """
    默认聊天室成员离线 30 秒后或离线后错过 30 条消息，会被踢出聊天室。
    将用户加入白名单后，用户将处于被保护状态，在以上情况下将不会被踢出聊天室。
    白名单中用户在当前聊天室中发送消息的级别将高于 High Level。
    聊天室销毁后，对应白名单也自动销毁。
    此功能需开通专有云服务。
    """
    def __init__(self, rc):
        super().__init__(rc)

    def add(self, room_id, user_ids):
        """
        将用户添加到白名单中。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/whitelist/add.json'
        format_str = 'chatroomId={{ room_id }}' \
                     '{% for item in user_ids %}&userId={{ item }}{% endfor %}'
        try:
            self._check_param(room_id, str, '1-64')
            self._check_param(user_ids, list, '1-5')
            for user in user_ids:
                self._check_param(user, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, room_id, user_ids):
        """
        将用户从白名单中移除。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/whitelist/remove.json'
        format_str = 'chatroomId={{ room_id }}' \
                     '{% for item in user_ids %}&userId={{ item }}{% endfor %}'
        try:
            self._check_param(room_id, str, '1-64')
            self._check_param(user_ids, list, '1-5')
            for user in user_ids:
                self._check_param(user, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, room_id):
        """
        获取聊天室用户白名单。
        """
        param_dict = locals().copy()
        url = '/chatroom/user/whitelist/query.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
