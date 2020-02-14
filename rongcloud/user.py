import json

from rongcloud.module import Module, ParamException


class User(Module):
    """
    客户端通过融云 SDK 每次连接服务器时，都需要向服务器提供 Token，以便验证身份。
    后续登录过程中，就不必再向融云请求 Token，由 App Server 直接提供之前保存过的 Token。
    如果您的 App 是免登录设计，也可以将 Token 保存在 App 本地（注意保证本地数据存储安全），直接登录。
    App 获取 Token 后，根据情况可选择在 App 本地保留当前用户的 Token，如果 Token 失效，还需要提供相应的代码重新向服务器获取 Token。
    在`融云开发者平台`设置 Token 有效期，默认永久有效，除非您在开发者后台刷新 App Secret ，Token 可以获取多次，但之前的仍然可用。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def register(self, user_id, name='', portrait_uri=''):
        """
        获取 Token。
        :param user_id:             用户 Id，支持大小写英文字母、数字、部分特殊符号 + = - _ 的组合方式，最大长度 64 字节。
                                    是用户在 App 中的唯一标识，必须保证在同一个 App 内不重复，
                                    重复的用户 Id 将被当作是同一用户。（必传）
        :param name:                用户名称，最大长度 128 字节。用来在 Push 推送时显示用户的名称。（必传）
        :param portrait_uri:        用户头像 URI，最大长度 1024 字节。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；
                                    token 用户 Token，可以保存应用内，长度在 256 字节以内；
                                    userId 用户 Id，与输入的用户 Id 相同。
                                    如：{"code":200, "userId":"jlk456j5", "token":"sfd9823ihufi"}
        """
        param_dict = locals().copy()
        url = '/user/getToken.json'
        format_str = 'userId={{ user_id }}' \
                     '&name={{ name }}' \
                     '&portraitUri={{ portrait_uri }}'
        try:
            self._check_param(user_id, str, '1~64')
            self._check_param(name, str, '0~128')
            self._check_param(portrait_uri, str, '0~1024')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def update(self, user_id, name='', portrait_uri=''):
        """
        修改用户信息。
        :param user_id:             用户 Id，支持大小写英文字母、数字、部分特殊符号 + = - _ 的组合方式，最大长度 64 字节。
                                    是用户在 App 中的唯一标识，必须保证在同一个 App 内不重复，
                                    重复的用户 Id 将被当作是同一用户。（必传）
        :param name:                用户名称，最大长度 128 字节。用来在 Push 推送时，显示用户的名称，刷新用户名称后 5 分钟内生效。
                                    （可选，提供即刷新，不提供忽略）
        :param portrait_uri:        用户头像 URI，最大长度 1024 字节。用来在 Push 推送时显示。（可选，提供即刷新，不提供忽略）
        :return:                    请求返回结果，code 返回码，200 为正常。
                                    如：{"code":200}
        """
        param_dict = locals().copy()
        url = '/user/refresh.json'
        format_str = 'userId={{ user_id }}' \
                     '{% if name is not none %}&name={{ name }}{% endif %}' \
                     '{% if portrait_uri is not none %}&portraitUri={{ portrait_uri }}{% endif %}'
        try:
            self._check_param(user_id, str, '1~64')
            self._check_param(name, str, '0~128')
            self._check_param(portrait_uri, str, '0~1024')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, user_id):
        """
        查询用户信息。
        :param user_id:             用户 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；userName 用户名称；userPortrait 用户头像地址。
                                    createTime 用户创建时间。
                                    如：{"code":200,"userName":"123","userPortrait":"","createTime":"2016-05-24 10:38:19"}
        """
        param_dict = locals().copy()
        url = '/user/info.json'
        format_str = 'userId={{ user_id }}'
        try:
            self._check_param(user_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def check_online(self, user_id):
        """
        检查用户在线状态。
        :param user_id:             用户 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；status 在线状态，1为在线，0为不在线。
                                    如：{"code":200,"status":"1"}
        """
        param_dict = locals().copy()
        url = '/user/checkOnline.json'
        format_str = 'userId={{ user_id }}'
        try:
            self._check_param(user_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def get_block(self):
        return Block(self._rc)

    def get_blacklist(self):
        return Blacklist(self._rc)

    def get_whitelist(self):
        return Whitelist(self._rc)

    def get_tag(self):
        return Tag(self._rc)


class Block(Module):
    """
    当用户违反 App 中的相关规定时，可根据情况对用户进行封禁处理，封禁时间范围由开发者自行设置，
    用户在封禁期间不能连接融云服务器，封禁期满后将自动解除封禁，
    也可以通过调用 /user/unblock 方法解除用户封禁，解除后可正常连接融云服务器。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_ids, minute):
        """
        封禁用户
        :param user_ids:            用户 Id，支持一次封禁多个用户，最多不超过 20 个。（必传）
        :param minute:              封禁时长，单位为分钟，最大值为43200分钟。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/user/block.json'
        format_str = '{% for item in user_ids %}userId={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}' \
                     '&minute={{ minute }}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(minute, int, '0~43200')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_ids):
        """
        解除用户封禁。
        :param user_ids:            用户 Id，支持一次解除多个用户，最多不超过 20 个。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/user/unblock.json'
        format_str = '{% for item in user_ids %}userId={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(user_ids, list, '1~20')
            for user in user_ids:
                self._check_param(user, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self):
        """
        获取被封禁用户。
        :param                      无
        :return:                    请求返回结果，code 返回码，200 为正常；users 被封禁用户数组；userId 被封禁用户 ID；
                                    blockEndTime 封禁结束时间。
                                    如：{"code":200,"users":[{"userId":"jlk456j5","blockEndTime":"2015-01-11 01:28:20"}]}
        """
        url = '/user/block/query.json'
        try:
            return self._http_post(url)
        except ParamException as e:
            return json.loads(str(e))


class Blacklist(Module):
    """
    在 App 中如果用户不想接收到某一用户的消息或不想被某一用户联系到时，可将此用户加入到黑名单中，
    应用中的每个用户都可以设置自己的黑名单列表。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_id, black_ids):
        """
        添加用户到黑名单。
        :param user_id:             用户 Id。（必传）
        :param black_ids:           被加黑的用户 Id，每次最多添加 20 个用户。(必传)
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        black_ids = self._tran_list(black_ids)
        param_dict = locals().copy()
        url = '/user/blacklist/add.json'
        format_str = 'userId={{ user_id }}' \
                     '{% for item in black_ids %}&blackUserId={{ item }}{% endfor %}'
        try:
            self._check_param(user_id, str, '1~64')
            self._check_param(black_ids, list, '1~20')
            for user in black_ids:
                self._check_param(user, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_id, black_ids):
        """
        移除黑名单中用户。
        :param user_id:             用户 Id。（必传）
        :param black_ids:           被移除的用户 Id，每次最多移除 20 个用户。(必传)
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        black_ids = self._tran_list(black_ids)
        param_dict = locals().copy()
        url = '/user/blacklist/remove.json'
        format_str = 'userId={{ user_id }}' \
                     '{% for item in black_ids %}&blackUserId={{ item }}{% endfor %}'
        try:
            self._check_param(user_id, str, '1~64')
            self._check_param(black_ids, list, '1~20')
            for user in black_ids:
                self._check_param(user, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, user_id):
        """
        获取某用户黑名单列表。
        :param user_id:             用户 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；users 黑名单用户数组。
                                    如：{"code":200,"users":["jlk454","jlk457"]}
        """
        param_dict = locals().copy()
        url = '/user/blacklist/query.json'
        format_str = 'userId={{ user_id }}'
        try:
            self._check_param(user_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class Whitelist(Module):
    """
    应用中对用户之间相互发送消息有限制要求的客户，可使用用户白名单功能，将用户加入白名单后，才能收到该用户发送的单聊消息。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def add(self, user_id, white_ids):
        """
        添加用户到白名单。
        :param user_id:             用户 Id。（必传）
        :param white_ids:           被添加的用户 Id，每次最多添加 20 个用户。(必传)
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        white_ids = self._tran_list(white_ids)
        param_dict = locals().copy()
        url = '/user/whitelist/add.json'
        format_str = 'userId={{ user_id }}' \
                     '{% for item in white_ids %}&whiteUserId={{ item }}{% endfor %}'
        try:
            self._check_param(user_id, str, '1~64')
            self._check_param(white_ids, list, '1~20')
            for user in white_ids:
                self._check_param(user, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, user_id, white_ids):
        """
        移除白名单中用户。
        :param user_id:             用户 Id。（必传）
        :param white_ids:           被移除的用户 Id，每次最多移除 20 个用户。(必传)
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
        """
        white_ids = self._tran_list(white_ids)
        param_dict = locals().copy()
        url = '/user/whitelist/remove.json'
        format_str = 'userId={{ user_id }}' \
                     '{% for item in white_ids %}&whiteUserId={{ item }}{% endfor %}'
        try:
            self._check_param(user_id, str, '1~64')
            self._check_param(white_ids, list, '1~20')
            for user in white_ids:
                self._check_param(user, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def query(self, user_id):
        """
        获取某用户白名单列表。
        :param user_id:             用户 Id。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；users 白名单用户数组。
                                    如：{"code":200,"users":["jlk454","jlk457"]}
        """
        param_dict = locals().copy()
        url = '/user/whitelist/query.json'
        format_str = 'userId={{ user_id }}'
        try:
            self._check_param(user_id, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class Tag(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def set(self, user_ids, tags):
        """
        为应用中的一个或多个用户添加标签，如果某用户已经添加了标签，再次对用户添加标签时将覆盖之前设置的标签内容。
        :param user_ids:            用户 Id 或 Id 列表，一次最多支持 1000 个用户。（必传）
        :param tags:                用户标签，一个用户最多添加 20 个标签，每个 tag 最大不能超过 40 个字节，
                                    标签中不能包含特殊字符。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常。如：{"code":200}
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
                    self._check_param(user, str, '1~64')
                return self._http_post(url, self._render(param_dict, format_str))
            except ParamException as e:
                return json.loads(str(e))
        else:
            url = '/user/tag/batch/set.json'
            format_str = '{' \
                         '"userIds":[{% for item in user_ids %}"{{ item }}"' \
                         '{% if not loop.last %},{% endif %}{% endfor %}],' \
                         '"tags":[{% for item in tags %}"{{ item }}"{% if not loop.last %},{% endif %}{% endfor %}]' \
                         '}'
            try:
                self._check_param(tags, list, '1~1000')
                for tag in tags:
                    self._check_param(tag, str, '1~40')
                return self._http_post(url, self._render(param_dict, format_str))
            except ParamException as e:
                return json.loads(str(e))

    def get(self, user_ids):
        """
        查询用户所有标签功能，支持批量查询每次最多查询 50 个用户。
        :param user_ids:            用户 Id，一次最多支持 50 个用户。（必传）
        :return:                    请求返回结果，code 返回码，200 为正常；result 用户所有的标签数组。
                                    如：{"code":200,"result":{"111":[],"222":["帅哥","北京"]}}
        """
        user_ids = self._tran_list(user_ids)
        param_dict = locals().copy()
        url = '/user/tags/get.json'
        format_str = '{% for item in user_ids %}userIds={{ item }}{% if not loop.last %}&{% endif %}{% endfor %}'
        try:
            self._check_param(user_ids, list, '1~50')
            for user in user_ids:
                self._check_param(user, str, '1~64')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
