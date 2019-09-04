import json

from rongcloud.module import Module, ParamException


class Group(Module):
    """
    群组服务。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def sync(self, user_id, group_info_list):
        """
        同步用户所属群组。如果在集成融云前 App Server 已有群组数据，可使用此服务进行同步，
        当第一次连接融云服务器时，需要向融云服务器提交 userId 对应的用户当前所加入的所有群组，
        此接口主要为防止应用中用户群信息同融云已知的用户所属群信息不同步。
        :param user_id:             被同步群信息的用户 Id。（必传）
        :param group_info_list:     该用户所属的群信息，如群 Id 已经存在，则不会刷新对应群组名称，
                                    如果想刷新群组名称请调用刷新群组信息方法。此参数可传多个，如：[('id', 'name'), ...]。
        :return                     请求返回结果，code 返回码，200 为正常。
                                    如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/group/sync.json'
        format_str = 'userId={{ user_id }}' \
                     '{% for item in group_info_list %}&group[{{ item[0] }}]={{ item[1] }}{% endfor %}'
        try:
            self._check_param(user_id, str, '1~64')
            self._check_param(group_info_list, list)
            for group_id, group_name in group_info_list:
                self._check_param(group_id, str, '1~64')
                self._check_param(group_name, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def create(self, user_ids, group_id, group_name):
        """
        创建群组，并将用户加入该群组，用户将可以收到该群的消息，每个群最大至 3000 人，App 内的群组数量没有限制。
        注：其实本方法是加入群组方法。
        :param user_ids:            加入群组的用户或用户列表。
        :param group_id:            创建群组 Id。（必传）
        :param group_name:          群组 Id 对应的名称，用于在发送群组消息显示远程 Push 通知时使用，
                                    如群组名称改变需要调用刷新群组信息接口同步。（必传）
        :return                     请求返回结果，code 返回码，200 为正常。
                                    如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/group/create.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&groupId={{ group_id }}' \
                     '&groupName={{ group_name }}'
        try:
            self._check_param(user_ids, list)
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(group_id, str, '1~64')
            self._check_param(group_name, str, '1~64')
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
