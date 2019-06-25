import json

from rongcloud.module import Module, ParamException


class User(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def get_tag(self):
        return Tag(self._rc)

    def register(self, user_id, name='', portrait_uri=''):
        """
        注册用户，生成用户在融云的唯一身份标识 Token，各端 SDK 使用 Token 连接融云服务器。
        :param user_id: 用户 ID，最大长度 64 字节.是用户在 App 中的唯一标识码，必须保证在同一个 App 内不重复，重复的用户 Id 将被当作是同一用户。
        :param name: 用户名称，最大长度 128 字节.用来在 Push 推送时显示用户的名称.用户名称，最大长度 128 字节.用来在 Push 推送时显示用户的名称。
        :param portrait_uri: 用户头像 URI，最大长度 1024 字节.用来在 Push 推送时显示用户的头像。
        """
        param_dict = locals().copy()
        url = '/user/getToken.json'
        format_str = 'userId={{ user_id }}' \
                     '&name ={{ name }}' \
                     '&portraitUri={{ portrait_uri }}'
        try:
            self._check_param(user_id, str, '1-64')
            self._check_param(name, str, '0-128')
            self._check_param(portrait_uri, str, '0-1024')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def update(self, user_id, name='', portrait_uri=''):
        """
        修改用户信息。
        :param user_id: 用户 ID，最大长度 64 字节.是用户在 App 中的唯一标识码，必须保证在同一个 App 内不重复，重复的用户 Id 将被当作是同一用户。
        :param name: 用户名称，最大长度 128 字节。用来在 Push 推送时，显示用户的名称，刷新用户名称后 5 分钟内生效。（可选，提供即刷新，不提供忽略）
        :param portrait_uri: 用户头像 URI，最大长度 1024 字节。用来在 Push 推送时显示。（可选，提供即刷新，不提供忽略）
        """
        param_dict = locals().copy()
        url = '/user/refresh.json'
        format_str = 'userId={{ user_id }}' \
                     '&name ={{ name }}' \
                     '&portraitUri={{ portrait_uri }}'
        try:
            self._check_param(user_id, str, '1-64')
            self._check_param(name, str, '0-128')
            self._check_param(portrait_uri, str, '0-1024')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def get_blacklist(self):
        return Blacklist(self._rc)

    def get_block(self):
        return Block(self._rc)


class Blacklist(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_id, black_ids):
        """
        将对方加入黑名单，屏蔽对方消息，但自己仍可给对方发送消息，应用中每个用户均可设置自己的黑名单。
        :param user_id: 用户 ID。
        :param black_ids: 被设置为黑名单的用户 ID 或 ID 列表。
        """
        black_ids = self._tran_list(black_ids)
        param_dict = locals().copy()
        url = '/user/blacklist/add.json'
        format_str = 'userId={{ user_id }}' \
                     '{% for item in black_ids %}&blackUserId={{ item }}{% endfor %}'
        try:
            self._check_param(user_id, str, '1-64')
            self._check_param(black_ids, list)
            for user in black_ids:
                self._check_param(user, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_id, black_ids):
        """
        将用户从黑名单中移除。
        :param user_id: 用户 ID。
        :param black_ids: 被移除黑名单的用户 ID 或 ID 列表。
        """
        black_ids = self._tran_list(black_ids)
        param_dict = locals().copy()
        url = '/user/blacklist/remove.json'
        format_str = 'userId={{ user_id }}' \
                     '{% for item in black_ids %}&blackUserId={{ item }}{% endfor %}'
        try:
            self._check_param(user_id, str, '1-64')
            self._check_param(black_ids, list)
            for user in black_ids:
                self._check_param(user, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, user_id):
        """
        获取某个用户的黑名单列表。
        :param user_id: 用户 ID。
        """
        param_dict = locals().copy()
        url = '/user/blacklist/query.json'
        format_str = 'userId={{ user_id }}'
        try:
            self._check_param(user_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class Block(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, minute):
        """
        用户在封禁期间所有 IM 功能均不可用，例如 连接融云服务器、发送消息 封禁期满后自动解除封禁，功能恢复正常。
        :param user_ids: 用户 ID 或 ID 列表。
        :param minute: 封禁时长 1 - 1 * 30 * 24 * 60 分钟，最大值为 43200 分钟。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/user/block.json'
        format_str = '{% for item in user_ids %}userId={{ item }}&{% endfor %}' \
                     '&minute={{ minute }}'
        try:
            self._check_param(user_ids, list, '1-20')
            for user in user_ids:
                self._check_param(user, str, '1-64')
            self._check_param(minute, int, '1-43200')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids):
        """
        解除用户封禁。
        :param user_ids: 用户 ID 或 ID 列表。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/user/unblock.json'
        format_str = '{% for item in user_ids %}userId={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(user_ids, list, '1-20')
            for user in user_ids:
                self._check_param(user, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self):
        """
        获取封禁用户列表。
        """
        url = '/user/block/query.json'
        return self._http_post(url)


class Tag(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def set(self, user_ids, tags):
        """
        为应用中的用户添加标签，如果某用户已经添加了标签，再次对用户添加标签时将覆盖之前设置的标签内容。
        :param user_ids:
        :param tags:
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        if len(user_ids) == 1:
            url = '/user/tag/set.json'
            format_str = '{' \
                         '"userId":"{{ user_ids[0] }}",' \
                         '"tags":[{% for item in tags %}"{{ item }}"{% if not loop.last %},{% endif %}{% endfor %}]' \
                         '}'
            try:
                for user in user_ids:
                    self._check_param(user, str, '1-64')
                return self._http_post(url, self._render(param_dict, format_str))
            except ParamException as e:
                return json.loads(str(e))
        else:
            url = '/user/tag/batch/set.json'
            format_str = '{' \
                         '"userIds":[{% for item in user_ids %}"{{ item }}"{% if not loop.last %},{% endif %}{% endfor %}],' \
                         '"tags":[{% for item in tags %}"{{ item }}"{% if not loop.last %},{% endif %}{% endfor %}]' \
                         '}'
            try:
                self._check_param(tags, list, '1-1000')
                for tag in tags:
                    self._check_param(tag, str, '1-40')
                return self._http_post(url, self._render(param_dict, format_str))
            except ParamException as e:
                return json.loads(str(e))

    def get(self, user_ids):
        """
        为应用中的用户添加标签，如果某用户已经添加了标签，再次对用户添加标签时将覆盖之前设置的标签内容。
        :param user_ids:
        :param tags:
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/user/tags/get.json'
        format_str = '{% for item in user_ids %}userIds={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(user_ids, list, '1-50')
            for user in user_ids:
                self._check_param(user, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
