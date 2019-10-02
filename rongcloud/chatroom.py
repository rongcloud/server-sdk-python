import json

from rongcloud.module import Module, ParamException


class Chatroom(Module):
    """
    1. 对于同一个聊天室，只存储该聊天室的 50 条最新消息，也就是说移动端用户进入聊天室时，最多能够拉取到最新的 50 条消息。
    2、High Level 和 Low Level 的消息：当聊天室中消息并发量很高时，可以将不重要的消息设置为 Low Level 的消息，
       消息默认全是 High Level 的消息。High Level 和 Low Level 的消息的区别在于，当服务器负载高时 Low Level 的消息优先被丢弃，
       这样可以让出资源给 High Level 的消息。通过聊天室消息优先级服务设置 Low Level 消息，设置好后两小时生效。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def create(self, room_info_list):
        """
        创建聊天室。
        :param room_info_list:      要创建的聊天室的信息列表。如：[('room_id', 'room_name'), ...]。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/chatroom/create.json'
        format_str = '{% for item in room_info_list %}{% if not loop.first %}&{% endif %}' \
                     'chatroom[{{ item[0] }}]={{ item[1] }}{% endfor %}'
        try:
            self._check_param(room_info_list, list)
            for room_id, room_name in room_info_list:
                self._check_param(room_id, str, '1~64')
                self._check_param(room_name, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def destroy(self, room_ids):
        """
        销毁聊天室。
        :param room_ids:            要销毁的聊天室 Id 或 Id 列表。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        room_ids = self._tran_list(room_ids)
        param_dict = locals().copy()
        url = '/chatroom/destroy.json'
        format_str = '{% for item in room_ids %}{% if not loop.first %}&{% endif %}chatroomId={{ item }}{% endfor %}'
        try:
            self._check_param(room_ids, list)
            for room_id in room_ids:
                self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, room_ids):
        """
        查询聊天室信息。
        :param room_ids:            要查询的聊天室 Id 或 Id 列表。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；chatRooms 聊天室信息数组；chrmId 聊天室 Id；
                                    name 聊天室名称；time 聊天室创建时间。
                                    如：{
                                        "code":200,
                                        "chatRooms": [
                                            {"chatroomId":"10001","name":"name1","time":"2014-01-01 1:1:1"},
                                            {"chatroomId":"10002","name":"name2","time":"2014-01-01 1:1:2"}
                                        ]
                                    }
        """
        room_ids = self._tran_list(room_ids)
        param_dict = locals().copy()
        url = '/chatroom/query.json'
        format_str = '{% for item in room_ids %}{% if not loop.first %}&{% endif %}chatroomId={{ item }}{% endfor %}'
        try:
            self._check_param(room_ids, list)
            for room_id in room_ids:
                self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def get_user(self):
        return User(self._rc)

    def get_message(self):
        return Message(self._rc)

    def get_whitelist(self):
        return WhiteList(self._rc)

    def get_keepalive(self):
        return KeepAlive(self._rc)


class User(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def query(self, room_id, count, order):
        """
        查询聊天室内用户。
        :param room_id:             要查询的聊天室 Id。（必传）
        :param count:               要获取的聊天室成员信息数，最多返回 500 个成员信息（必传）
        :param order:               加入聊天室的先后顺序， 1 为加入时间正序， 2 为加入时间倒序（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；total 当前聊天室中用户数；
                                    users 聊天室成员数组，最多为 500 个；id 用户 Id。time 加入聊天室时间。
                                    如：{
                                        "code":200,
                                        "total":500,
                                        "users":[
                                            {"id":"uid1","time":"2015-09-10 16:38:26"},
                                            {"id":"uid2","time":"2015-09-10 16:38:26"}
                                        ]
                                    }
        """
        param_dict = locals().copy()
        url = '/chatroom/user/query.json'
        format_str = 'chatroomId={{ room_id }}&count={{ count }}&order={{ order }}'
        try:
            self._check_param(room_id, str, '1~64')
            self._check_param(count, int, '1~500')
            self._check_param(order, int, '1~2')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def isexist(self, room_id, user_ids):
        """
        查询用户是否在聊天室。
        :param room_id:             要查询的聊天室 ID（必传）
        :param user_ids:            要查询的用户 Id 或 Id 列表，每次最多不超过 1000 个。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；userid 聊天室中用户 ID；
                                    isInChrm 用户是否在聊天室中，1 表示在聊天室中，0 表示不在聊天室中。
                                    如：{
                                        "code":200,
                                        "result":[
                                            {"userid":"y41z2IXBW", "isInChrm":0},
                                            {"userid":"niCtlxnas", "isInChrm":1}
                                        ]
                                    }
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        if len(user_ids) == 1:
            url = '/chatroom/user/exist.json'
            format_str = 'chatroomId={{ room_id }}&userId={{ user_ids[0] }}'
            try:
                self._check_param(room_id, str, '1~64')
                self._check_param(user_ids, list, '1~1')
                for user_id in user_ids:
                    self._check_param(user_id, str, '1~64')
                return self._http_post(url, self._render(param_dict, format_str))
            except ParamException as e:
                return json.loads(str(e))
        else:
            url = '/chatroom/users/exist.json'
            format_str = 'chatroomId={{ room_id }}' \
                         '{% for item in user_ids %}&userId={{ item }}{% endfor %}'
            try:
                self._check_param(room_id, str, '1~64')
                self._check_param(user_ids, list, '1~1000')
                for user_id in user_ids:
                    self._check_param(user_id, str, '1~64')
                return self._http_post(url, self._render(param_dict, format_str))
            except ParamException as e:
                return json.loads(str(e))

    def get_gag(self):
        return UserGag(self._rc)

    def get_ban(self):
        return UserBan(self._rc)

    def get_block(self):
        return UserBlock(self._rc)

    def get_whitelist(self):
        return UserWhileList(self._rc)


class UserGag(Module):
    """
    在 App 中如果不想让某一用户在聊天室中发言时，可将此用户在聊天室中禁言，被禁言用户可以接收查看聊天室中用户聊天信息，但不能发送消息。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, room_id, minute):
        """
        添加禁言聊天室成员。
        :param user_ids:            用户 Id，可同时禁言多个用户，最多不超过 20 个。（必传）
        :param room_id:             聊天室 Id。（必传）
        :param minute:              禁言时长，以分钟为单位，最大值为 43200 分钟。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/gag/add.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&chatroomId={{ room_id }}' \
                     '&minute={{ minute }}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(room_id, str, '1~64')
            self._check_param(minute, int, '1~43200')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids, room_id):
        """
        移除禁言聊天室成员。
        :param user_ids:            用户 Id，可同时禁言多个用户，最多不超过 20 个。（必传）
        :param room_id:             聊天室 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/gag/rollback.json'
        format_str = '{% for item in user_ids %}userId={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}' \
                     '&chatroomId={{ room_id }}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, room_id):
        """
        查询被禁言聊天室成员。
        :param room_id:             聊天室 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；users 被禁言用户数组；
                                    time 解禁时间；userId 被禁言用户 Id。
                                    如：{"code":200,"users":[{"time":"2015-09-25 16:12:38","userId":"2582"}]}
        """
        param_dict = locals().copy()
        url = '/chatroom/user/gag/list.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class UserBan(Module):
    """
    如果不想让某一用户在所有聊天室中发言时，可将此用户添加到聊天室全局禁言中，被禁言用户可以接收查看聊天室中用户聊天信息，但不能发送消息。
    此服务在开通 IM 商用版的情况下，可申请开通，详细请联系商务，电话：13161856839。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, minute):
        """
        添加聊天室全局禁言
        :param user_ids:            用户 Id 或 Id 列表，可同时禁言多个用户，每次最多不超过 20 个。（必传）
        :param minute:              禁言时长，以分钟为单位，最大值为 43200 分钟。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/ban/add.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&minute={{ minute }}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(minute, int, '1~43200')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids):
        """
        移除聊天室全局禁言。
        :param user_ids:            用户 Id 或 Id 列表，可同时移除多个用户，每次最多不超过 20 个。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/ban/remove.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self):
        """
        查询聊天室全局禁言用户。
        :return:                    请求返回结果，code 返回码，200 为正常；users 被禁言用户数组；
                                    time 解禁时间；userId 被禁言用户 Id。
                                    如：{"code":200,"users":[{"time":"2015-09-25 16:12:38","userId":"2582"}]}
        """
        url = '/chatroom/user/ban/query.json'
        try:
            return self._http_post(url)
        except ParamException as e:
            return json.loads(str(e))


class UserBlock(Module):
    """
    在 App 中如果想将某一用户踢出聊天室并在一段时间内不允许再进入聊天室时，可实现将用户对指定的聊天室做封禁处理，
    被封禁用户将被踢出聊天室，并在设定的时间内不能再进入聊天室中。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, room_id, minute):
        """
        添加封禁聊天室成员。
        :param user_ids:            用户 Id 或 Id 列表，，可同时封禁多个用户，最多不超过 20 个。（必传）
        :param room_id:             聊天室 Id。（必传）
        :param minute:              封禁时长，以分钟为单位，最大值为 43200 分钟。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/block/add.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&chatroomId={{ room_id }}&minute={{ minute }}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(room_id, str, '1~64')
            self._check_param(minute, int, '1~43200')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids, room_id):
        """
        移除封禁聊天室成员。
        :param user_ids:            用户 Id 或 Id 列表，可同时移除多个用户，最多不超过 20 个。（必传）
        :param room_id:             聊天室 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/block/rollback.json'
        format_str = '{% for item in user_ids %}{% if not loop.first %}&{% endif %}userId={{ item }}{% endfor %}' \
                     '&chatroomId={{ room_id }}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, room_id):
        """
        查询被封禁聊天室成员。
        :param room_id:             聊天室 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常; users 被封禁用户数组；
                                    time 解禁时间；userId 封禁用户 Id。
                                    如：{"code":200,"users":[{"time":"2015-09-25 16:12:38","userId":"2582"}]}
        """
        param_dict = locals().copy()
        url = '/chatroom/user/block/list.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class UserWhileList(Module):
    """
    现在聊天室中用户在离线 30 秒后或离线后聊天室中产生 30 条消息时会被自动踢出聊天室。
    将用户加入到白名单后，用户将处于被保护状态，在以上情况下将不会被自动踢出聊天室。
    白名单中用户在当前聊天室中发送消息的级别将高于 High Level 。聊天室销毁后，对应白名单也自动销毁。
    此服务在开通 IM 商用版的情况下，可申请开通，详细请联系商务，电话：13161856839。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, room_id, user_ids):
        """
        添加聊天室白名单成员。
        :param room_id:             聊天室 Id。（必传）
        :param user_ids:            聊天室中用户 Id，可提交多个，聊天室中白名单用户最多不超过 5 个。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/whitelist/add.json'
        format_str = 'chatroomId={{ room_id }}' \
                     '{% for item in user_ids %}&userId={{ item }}{% endfor %}'
        try:
            self._check_param(room_id, str, '1~64')
            self._check_param(user_ids, list, '1~5')
            for user in user_ids:
                self._check_param(user, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, room_id, user_ids):
        """
        移除聊天室白名单成员。
        :param room_id:             聊天室 Id。（必传）
        :param user_ids:            聊天室白名单中用户 Id，可提交多个，最多不超过 5 个。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/chatroom/user/whitelist/remove.json'
        format_str = 'chatroomId={{ room_id }}' \
                     '{% for item in user_ids %}&userId={{ item }}{% endfor %}'
        try:
            self._check_param(room_id, str, '1~64')
            self._check_param(user_ids, list, '1~5')
            for user in user_ids:
                self._check_param(user, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, room_id):
        """
        查询聊天室白名单成员。
        :param room_id:             聊天室 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；users 白名单用户数组。
                                    如：{"code":200,"users":["user1","user2"]}
        """
        param_dict = locals().copy()
        url = '/chatroom/user/whitelist/query.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class Message(Module):
    """
    可实现控制对聊天室中消息是否进行分发，停止分发后聊天室中用户发送的消息，融云服务端不会再将消息发送给聊天室中其他用户。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def stop_distribution(self, room_id):
        """
        :param room_id:             聊天室 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/chatroom/message/stopDistribution.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def resume_distribution(self, room_id):
        """
        :param room_id:             聊天室 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/chatroom/message/resumeDistribution.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def get_priority(self):
        return MessagePriority(self._rc)


class MessagePriority(Module):
    """
    通过聊天室消息优先级接口，设置的消息类型为 Low Level 的消息，默认情况下全部为 High Level 的消息，
    当服务器负载高时 Low Level 的消息优先被丢弃，这样可以让出资源给 High Level 的消息，确保重要的消息不被丢弃，设置后 2 小时生效。
    此服务在开通 IM 商用版的情况下，可申请开通，详细请联系商务，电话：13161856839。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, obj_names):
        """
        添加聊天室消息优先级。
        :param obj_names:           低优先级的消息类型，每次最多提交 5 个，设置的消息类型最多不超过 20 个。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        obj_names = self._tran_list(obj_names)
        param_dict = locals().copy()
        url = '/chatroom/message/priority/add.json'
        format_str = '{% for item in obj_names %}objectName={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(obj_names, list, '1~5')
            for obj_name in obj_names:
                self._check_param(obj_name, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, obj_names):
        """
        移除聊天室消息优先级。
        :param obj_names:           低优先级的消息类型，每次最多提交 5 个。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        obj_names = self._tran_list(obj_names)
        param_dict = locals().copy()
        url = '/chatroom/message/priority/remove.json'
        format_str = '{% for item in obj_names %}objectName={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(obj_names, list, '1~5')
            for obj_name in obj_names:
                self._check_param(obj_name, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self):
        """
        查询聊天室消息优先级。
        :return:                    请求返回结果，code 返回码，200 为正常；objectNames 消息类型数组。
                                    如：{"code":200,"objectNames":["RC:ImgMsg","RC:ImgTextMsg","RC:VcMsg"]}
        """
        url = '/chatroom/message/priority/query.json'
        try:
            return self._http_post(url)
        except ParamException as e:
            return json.loads(str(e))


class WhiteList(Module):
    """
    设置消息类型，确保在服务器负载高时聊天室中重要类型的消息不被丢弃，设置后 2 小时生效。
    此服务在开通 IM 商用版的情况下，可申请开通，详细请联系商务，电话：13161856839。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, obj_names):
        """
        添加聊天室消息白名单。
        :param obj_names:           消息标识，最多不超过 20 个，自定义消息类型，长度不超过 32 个字符，参见内置消息类型表。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        obj_names = self._tran_list(obj_names)
        param_dict = locals().copy()
        url = '/chatroom/whitelist/add.json'
        format_str = '{% for item in obj_names %}objectnames={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(obj_names, list, '1~20')
            for obj_name in obj_names:
                self._check_param(obj_name, str, '1~32')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, obj_names):
        """
        删除聊天室消息白名单。
        :param obj_names:           消息标识，最多不超过 20 个，自定义消息类型，长度不超过 32 个字符，参见内置消息类型表。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        obj_names = self._tran_list(obj_names)
        param_dict = locals().copy()
        url = '/chatroom/whitelist/delete.json'
        format_str = '{% for item in obj_names %}objectnames={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(obj_names, list, '1~20')
            for obj_name in obj_names:
                self._check_param(obj_name, str, '1~32')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self):
        """
        查询聊天室消息白名单。
        :return:                    请求返回结果，code 返回码，200 为正常；whitlistMsgType 消息类型数组。
                                    如：{"code":200,"whitlistMsgType":["RC:ImgMsg","RC:ImgTextMsg","RC:VcMsg"]}
        """
        url = '/chatroom/whitelist/query.json'
        try:
            return self._http_post(url)
        except ParamException as e:
            return json.loads(str(e))


class KeepAlive(Module):
    """
    当聊天室中 1 小时无人说话，同时没有人加入聊天室时，融云服务端会自动把聊天室内所有成员踢出聊天室并销毁聊天室。
    如果不希望聊天室自动销毁，可以使用此服务将指定聊天室进行保活处理，保活的聊天室不会被自动销毁，需要调用 API 接口销毁聊天室。
    此服务在开通 IM 商用版的情况下，可申请开通，详细请联系商务，电话：13161856839。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, room_id):
        """
        添加保活聊天室。
        :param room_id:             聊天室 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/chatroom/keepalive/add.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, room_id):
        """
        移除保活聊天室。
        :param room_id:             聊天室 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/chatroom/keepalive/remove.json'
        format_str = 'chatroomId={{ room_id }}'
        try:
            self._check_param(room_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self):
        """
        查询保活聊天室。
        :return:                    请求返回结果，code 返回码，200 为正常；chatroomIds 保活聊天室数组。
                                    如：{"code":200,"chatroomIds":["1000","1001"]}
        """
        url = '/chatroom/keepalive/query.json'
        try:
            return self._http_post(url)
        except ParamException as e:
            return json.loads(str(e))
