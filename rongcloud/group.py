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
                                    如果想刷新群组名称请调用刷新群组信息方法。此参数可传多个，如：[('id', 'name'), ...]。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
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
        :param user_ids:            加入群组的用户 Id 或用户 Id 列表。
        :param group_id:            创建群组 Id。（必传）
        :param group_name:          群组 Id 对应的名称，用于在发送群组消息显示远程 Push 通知时使用，
                                    如群组名称改变需要调用刷新群组信息接口同步。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
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

    def join(self, user_ids, group_id, group_name):
        """
        将用户加入指定群组，用户将可以收到该群的消息，每个群最大至 3000 人。
        :param user_ids:            要加入群的用户 Id 或 Id 列表，可提交多个，最多不超过 1000 个。（必传）
        :param group_id:            要加入的群 Id。（必传）
        :param group_name:          要加入的群 Id 对应的名称。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/group/join.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&groupId={{ group_id }}' \
                     '&groupName={{ group_name }}'
        try:
            self._check_param(user_ids, list, '1~1000')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(group_id, str, '1~64')
            self._check_param(group_name, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def quit(self, user_ids, group_id):
        """
        将用户从群中移除，不再接收该群组的消息。
        :param user_ids:            要退出群的用户 Id 或 Id 列表。（必传）
        :param group_id:            要退出的群 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/group/quit.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&groupId={{ group_id }}'
        try:
            self._check_param(user_ids, list, '1~1000')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(group_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def dismiss(self, user_id, group_id):
        """
        将该群解散，所有用户都无法再接收该群的消息。
        :param user_id:             操作解散群的用户 Id，可以为任何用户 Id ，非群组创建者也可以解散群组。（必传）
        :param group_id:            要解散的群 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/group/dismiss.json'
        format_str = 'userId={{ user_id }}' \
                     '&groupId={{ group_id }}'
        try:
            self._check_param(user_id, str, '1~64')
            self._check_param(group_id, str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def update(self, group_id, group_name):
        """
        刷新群组信息。
        :param group_id:            群组 Id。（必传）
        :param group_name:          群组名称。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/group/refresh.json'
        format_str = 'groupId={{ group_id }}' \
                     '&groupName={{ group_name }}'
        try:
            self._check_param(group_id, str, '1~64')
            self._check_param(group_name, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, group_id):
        """
        查询群成员。
        :param group_id:            群 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；users 群成员数组；id 群成员 ID。
                                    如：{"code":200,"users":[{"id":"10001"},{"id":"10002"},{"id":"10000"},{"id":"10003"}]}
        """
        param_dict = locals().copy()
        url = '/group/user/query.json'
        format_str = 'groupId={{ group_id }}'
        try:
            self._check_param(group_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def get_user(self):
        return User(self._rc)


class User(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def query(self, group_id):
        """
        查询群成员。
        :param group_id:            群 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；users 群成员数组；id 群成员 Id。
                                    如：{"code":200,"users":[{"id":"10001"},{"id":"10002"},{"id":"10000"},{"id":"10003"}]}
        """
        param_dict = locals().copy()
        url = '/group/user/query.json'
        format_str = 'groupId={{ group_id }}'
        try:
            self._check_param(group_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def get_gag(self):
        return Gag(self._rc)

    def get_ban(self):
        return Ban(self._rc)


class Gag(Module):
    """
    如果不想让某一用户在群中发言时，可将此用户在群组中禁言，被禁言用户可以接收查看群组中用户聊天信息，但不能通过客户端 SDK 发送消息。
    提示：被禁言用户通过 Server API 发送的消息权限级别较高，不受禁言限制。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, group_id, minute):
        """
        添加禁言群成员。
        :param user_ids:            用户 Id 或 Id 列表，每次最多设置 20 个用户。（必传）
        :param group_id:            群组 Id，为空时则设置用户在加入的所有群组中都不能发送消息。（非必传）
        :param minute:              禁言时长，以分钟为单位，最大值为 43200 分钟，为 0 表示永久禁言。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/group/user/gag/add.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '{% if group_id is not none %}&groupId={{ group_id }}{% endif %}' \
                     '&minute={{ minute }}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(group_id, str, '1~64')
            self._check_param(minute, int, '0~43200')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids, group_id):
        """
        移除禁言群成员。
        :param user_ids:            用户 Id 或 Id 列表，每次最多设置 20 个用户。（必传）
        :param group_id:            群组 Id，为空时则移除用户在所有群组中的禁言设置。（非必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/group/user/gag/rollback.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '{% if group_id is not none %}groupId={{ group_id }}{% endif %}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(group_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, group_id):
        """
        查询被禁言群成员。
        :param group_id:            群组 Id，为空时则获取所有群组禁言用户列表。（非必传）
        :return:                    请求返回结果，code 返回码，200 为正常；time 解禁时间；userId 群成员 Id。
                                    如：{"code":200,"users":[{"time":"2015-09-25 16:12:38","userId":"2582"}]}
        """
        param_dict = locals().copy()
        url = '/group/user/gag/list.json'
        format_str = '{% if group_id is not none %}groupId={{ group_id }}{% endif %}'
        try:
            self._check_param(group_id, str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class Ban(Module):
    """
    设置某一群组全部成员禁言，如果在群组全部成员禁言状态下，需要某些用户可以发言时，可将此用户加入到群禁言用户白名单中。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, group_ids):
        """
        添加禁言群。
        :param group_ids:           群组 Id 或 Id 列表，，支持一次设置多个，最多不超过 20 个。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        group_ids = self._tran_list(group_ids)
        param_dict = locals().copy()
        url = '/group/ban/add.json'
        format_str = '{% for item in group_ids %}{% if not loop.first %}&{% endif %}groupId={{ item }}{% endfor %}'
        try:
            self._check_param(group_ids, list, '1~20')
            for group_id in group_ids:
                self._check_param(group_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, group_ids):
        """
        移除禁言群。
        :param group_ids:           群组 Id 或 Id 列表，，支持一次设置多个，最多不超过 20 个。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        group_ids = self._tran_list(group_ids)
        param_dict = locals().copy()
        url = '/group/ban/rollback.json'
        format_str = '{% for item in group_ids %}{% if not loop.first %}&{% endif %}groupId={{ item }}{% endfor %}'
        try:
            self._check_param(group_ids, list, '1~20')
            for group_id in group_ids:
                self._check_param(group_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, group_ids):
        """
        查询被禁言群。
        :param group_ids:           群组 Id 或 Id 列表，不传此参数，表示查询所有设置禁言的群组列表；
                                    传此参数时，表示查询传入的群组 Id 是否被设置为群组禁言，
                                    支持一次查询多个，最多不超过 20 个。（非必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        group_ids = self._tran_list(group_ids)
        param_dict = locals().copy()
        url = '/group/ban/query.json'
        format_str = '{% for item in group_ids %}{% if not loop.first %}&{% endif %}groupId={{ item }}{% endfor %}'
        try:
            self._check_param(group_ids, list, '1~20')
            for group_id in group_ids:
                self._check_param(group_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def get_whitelist(self):
        return Whitelist(self._rc)


class Whitelist(Module):
    """
    在群组被禁言状态下，如果需要某些用户可以发言时，可将此用户加入到群组禁言用户白名单中。
    群禁言用户白名单，只有群组被设置为全部禁言时才会生效。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, group_id):
        """
        添加禁言白名单用户。
        :param user_ids:            用户 Id，支持一次添加多个用户，最多不超过 20 个。（必传）
        :param group_id:            群组 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/group/user/ban/whitelist/add.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&groupId={{ group_id }}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(group_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids, group_id):
        """
        移除禁言白名单用户。
        :param user_ids:            用户 Id，支持同时移除多个用户，每次最多不超过 20 个。（必传）
        :param group_id:            群组 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/group/user/ban/whitelist/rollback.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&groupId={{ group_id }}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(group_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, group_id):
        """
        查询禁言白名单用户列表。
        :param group_id:            群组 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；userIds 用户 Id。
                                    如：{"code":200,"userIds":["2111","2582"]}
        """
        param_dict = locals().copy()
        url = '/group/user/ban/whitelist/query.json'
        format_str = 'groupId={{ group_id }}'
        try:
            self._check_param(group_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
