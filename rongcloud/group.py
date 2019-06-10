import json

from rongcloud.module import Module, ParamException


class Group(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def sync(self, user_id, group_info_list):
        """
        把用户的多个群同步到融云服务器，每次同步是全量群组数据，群组关系会以最后一次同步为准。
        :param user_id: 被同步群信息的用户 Id。
        :param group_info_list: 用户所在群组列表。
        """
        param_dict = locals().copy()
        url = '/group/sync.json'
        format_str = 'userId={{ user_id }}' \
                     '{% for item in group_info_list %}&group[]={{ item }}{% endfor %}'
        try:
            self._check_param(user_id, str, '1-64')
            self._check_param(group_info_list, list)
            for group_id, group_name in group_info_list:
                self._check_param(group_id, str, '1-64')
                self._check_param(group_name, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def create(self, user_id_list, group_id, group_name):
        """
        创建群组，每个群最多 3000 人，应用内群组数量无限制。
        :param user_id_list: 加入群组的用户列表。
        :param group_id: 群组 Id，最大长度 64 个字符，建议使用 英文字母、数字 混排。
        :param group_name: 群组名称，最大长度 64 个字符。
        """
        param_dict = locals().copy()
        url = '/group/create.json'
        format_str = '{% for item in user_id_list %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&groupId={{ group_id }}' \
                     '&groupName={{ group_name }}'
        try:
            self._check_param(user_id_list, list)
            for user_id in user_id_list:
                self._check_param(user_id, str, '1-64')
            self._check_param(group_id, str, '1-64')
            self._check_param(group_name, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, group_id):
        """
        获取群信息。
        :param group_id: 群组 Id。
        """
        param_dict = locals().copy()
        url = '/group/user/query.json'
        format_str = 'groupId={{ group_id }}'
        try:
            self._check_param(group_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def update(self, group_id, group_name):
        """
        修改群信息。
        :param group_id: 群组 Id。
        :param group_name: 群组新名称。
        """
        param_dict = locals().copy()
        url = '/group/refresh.json'
        format_str = 'groupId={{ group_id }}' \
                     '&groupName={{ group_name }}'
        try:
            self._check_param(group_id, str, '1-64')
            self._check_param(group_name, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def join(self, user_id_list, group_id, group_name):
        """
        加入群组。
        :param user_id_list: 加入群组的用户列表。
        :param group_id: 群组 Id，最大长度 64 个字符，建议使用 英文字母、数字 混排。
        :param group_name: 群组名称，最大长度 64 个字符。
        """
        param_dict = locals().copy()
        url = '/group/join.json'
        format_str = '{% for item in user_id_list %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&groupId={{ group_id }}' \
                     '&groupName={{ group_name }}'
        try:
            self._check_param(user_id_list, list)
            for user_id in user_id_list:
                self._check_param(user_id, str, '1-64')
            self._check_param(group_id, str, '1-64')
            self._check_param(group_name, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def quit(self, user_id_list, group_id):
        """
        退出群组。
        :param user_id_list: 要退出群组的用户列表。
        :param group_id: 群组 Id。
        """
        param_dict = locals().copy()
        url = '/group/quit.json'
        format_str = '{% for item in user_id_list %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&groupId={{ group_id }}'
        try:
            self._check_param(user_id_list, list)
            for user_id in user_id_list:
                self._check_param(user_id, str, '1-64')
            self._check_param(group_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def dismiss(self, user_id, group_id):
        """
        解散群组。
        :param user_id: 操作解散群的用户 Id。
        :param group_id: 群组 Id。
        """
        param_dict = locals().copy()
        url = '/group/dismiss.json'
        format_str = 'userId={{ user_id }}' \
                     '&groupId={{ group_id }}'
        try:
            self._check_param(user_id, str, '1-64')
            self._check_param(group_id, str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def get_gag(self):
        return Gag(self._rc)


class Gag(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, group_id, minute):
        """
        添加群组禁言，禁止群成员在群内发送消息，禁言后只能接收消息。
        :param user_ids: 禁言群成员 ID 或 ID 列表。
        :param group_id: 群组 ID。
        :param minute: 禁言时长，以分钟为单位，最大值为43200分钟。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/group/user/gag/add.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&groupId={{ group_id }}' \
                     '&minute={{ minute }}'
        try:
            self._check_param(user_ids, list)
            for user_id in user_ids:
                self._check_param(user_id, str, '1-64')
            self._check_param(group_id, str, '1-64')
            self._check_param(minute, int, '0-43200')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids, group_id):
        """
        解除禁言。
        :param user_ids: 解除禁言群成员 ID 或 ID 列表。
        :param group_id: 群组 ID。
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/group/user/gag/rollback.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&groupId={{ group_id }}'
        try:
            self._check_param(user_ids, list)
            for user_id in user_ids:
                self._check_param(user_id, str, '1-64')
            self._check_param(group_id, str, '1-64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, group_id):
        """
        查询禁言成员列表。
        :param group_id: 群组 ID。
        """
        param_dict = locals().copy()
        url = '/group/user/gag/list.json'
        format_str = 'groupId={{ group_id }}'
        try:
            self._check_param(group_id, str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
