import json
import urllib

from rongcloud.module import Module, ParamException


class Message(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def get_private(self):
        return Private(self._rc)

    def get_group(self):
        return Group(self._rc)

    def get_chatroom(self):
        return Chatroom(self._rc)

    def get_system(self):
        return System(self._rc)

    def get_history(self):
        return History(self._rc)


class Private(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def send(self, from_user_id, to_user_ids, object_name, content, push_content=None, push_data=None,
             count=-1, verify_blacklist=0, is_persisted=1, is_include_sender=0, content_available=0):
        """
        发送单聊消息。
        :param from_user_id:        发送人用户 Id。（必传）
        :param to_user_ids:         接收用户 Id，可以实现向多人发送消息，每次上限为 1000 人。（必传）
        :param object_name:         消息类型，参考融云消息类型表.消息标志；可自定义消息类型，长度不超过 32 个字符，
                                    您在自定义消息时需要注意，不要以 "RC:" 开头，
                                    以避免与融云系统内置消息的 ObjectName 重名。（必传）
        :param content:             发送消息内容，内置消息以 JSON 方式进行数据序列化，详见融云内置消息结构详解；
                                    如果 objectName 为自定义消息类型，该参数可自定义格式，不限于 JSON。（必传）
        :param push_content:        定义显示的 Push 内容，如果 objectName 为融云内置消息类型时，则发送后用户一定会收到 Push 信息。
                                    如果为自定义消息，则 pushContent 为自定义消息显示的 Push 内容，
                                    如果不传则用户不会收到 Push 通知。(可选)
        :param push_data:           针对 iOS 平台为 Push 通知时附加到 payload 中，客户端获取远程推送内容时为 appData 查看详细，
                                    Android 客户端收到推送消息时对应字段名为 pushData。(可选)
        :param count:               针对 iOS 平台，Push 时用来控制未读消息显示数，只有在 toUserId 为一个用户 Id 的时候有效，
                                    客户端获取远程推送内容时为 badge 查看详细，
                                    为 -1 时不改变角标数，传入相应数字表示把角标数改为指定的数字，最大不超过 9999。(可选)
        :param verify_blacklist:    是否过滤接收用户黑名单列表，0 表示为不过滤、1 表示为过滤，默认为 0 不过滤。(可选)
        :param is_persisted:        针对融云服务端是否存储此条消息，客户端则根据消息注册的 ISPERSISTED 标识判断是否存储，
                                    如果旧版客户端上未注册该消息时，收到该消息后默认为存储，但无法解析显示。
                                    0 表示为不存储、 1 表示为存储，默认为 1 存储消息。(可选)
        :param is_include_sender:   发送用户自己是否接收消息，0 表示为不接收，1 表示为接收，默认为 0 不接收，
                                    只有在 toUserId 为一个用户 Id 的时候有效。（可选）
        :param content_available:   针对 iOS 平台，对 SDK 处于后台暂停状态时为静默推送，是 iOS7 之后推出的一种推送方式。
                                    允许应用在收到通知后在后台运行一段代码，且能够马上执行，查看详细。
                                    1 表示为开启，0 表示为关闭，默认为 0（可选）
        :return:                    请求返回结果。
        """
        to_user_ids = self._tran_list(to_user_ids)
        content = urllib.parse.quote(json.dumps(content))
        param_dict = locals().copy()
        url = '/message/private/publish.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '{% for item in to_user_ids %}&toUserId={{ item }}{% endfor %}' \
                     '&objectName={{ object_name }}' \
                     '&content={{ content }}' \
                     '{% if push_content is not none %}&pushContent={{ push_content }}{% endif %}' \
                     '{% if push_data is not none %}&pushData={{ push_data }}{% endif %}' \
                     '{% if count != -1 %}&count={{ count }}{% endif %}' \
                     '{% if verify_blacklist != 0 %}&verifyBlacklist={{ verify_blacklist }}{% endif %}' \
                     '{% if is_persisted != 1 %}&isPersisted={{ is_persisted }}{% endif %}' \
                     '{% if is_include_sender != 0 %}&isIncludeSender={{ is_include_sender }}{% endif %}' \
                     '{% if content_available != 0 %}&contentAvailable={{ content_available }}{% endif %}'
        try:
            self._check_param(from_user_id, str, '1~64')
            self._check_param(to_user_ids, list, '1~1000')
            for user in to_user_ids:
                self._check_param(user, str, '1~64')
            self._check_param(object_name, str, '1~32')
            self._check_param(content, str)
            self._check_param(push_content, str)
            self._check_param(push_data, str)
            self._check_param(count, '-1~9999')
            self._check_param(verify_blacklist, int, '0~1')
            self._check_param(is_persisted, int, '0~1')
            self._check_param(is_include_sender, int, '0~1')
            self._check_param(content_available, int, '0~1')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def recall(self, from_user_id, target_id, uid, sent_time, is_admin=0, is_delete=0, extra=None):
        """
        撤回已发送的单聊消息，撤回时间无限制，只允许撤回用户自己发送的消息。
        :param from_user_id:        消息发送人用户 Id。（必传）
        :param target_id:           对方用户 Id。（必传）
        :param uid:                 消息唯一标识，可通过服务端实时消息路由获取，对应名称为 msgUID。（必传）
        :param sent_time:           消息发送时间，可通过服务端实时消息路由获取，对应名称为 msgTimestamp。（必传）
        :param is_admin:            是否为管理员，默认为 0，设为 1 时，IMKit 收到此条消息后，小灰条默认显示为
                                    “管理员 撤加了一条消息”。（非必传）
        :param is_delete:           是否删除消息，默认为 0 撤回该条消息同时，用户端将该条消息删除并替换为一条小灰条撤回提示消息；
                                    为 1 时，该条消息删除后，不替换为小灰条提示消息。（非必传）
        :param extra:               扩展信息，可以放置任意的数据内容。（非必传）
        :return:                    请求返回结果。
        """
        param_dict = locals().copy()
        url = '/message/recall.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '&conversationType=1' \
                     '&targetId={{ target_id }}' \
                     '&messageUID={{ uid }}' \
                     '&sentTime={{ sent_time }}' \
                     '{% if is_admin is not none %}&isAdmin={{ is_admin }}{% endif %}' \
                     '{% if is_delete is not none %}&isDelete={{ is_delete }}{% endif %}' \
                     '{% if extra is not none %}&extra={{ extra }}{% endif %}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(target_id, str, '1-64')
            self._check_param(uid, str)
            self._check_param(sent_time, int)
            self._check_param(is_admin, int)
            self._check_param(is_delete, int)
            self._check_param(extra, str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def send_template(self, from_user_id, to_user_ids, object_name, content, values,
                      push_content=None, push_data=None, verify_blacklist=0, content_available=0):
        """
        向多个用户发送不同内容消息。
        :param from_user_id: 发送人用户 ID。
        :param to_user_ids: 接收用户 ID。可以实现向多人发送消息，每次上限为 1000 人。
        :param object_name: 发送的消息类型。
        :param content: 消息内容。
        :param values: 消息内容中，标识位对应内容。
        :param push_content: 当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行存储，
                             0 表示为不存储、 1 表示为存储，默认为 1 存储消息。
        :param push_data: 针对 iOS 平台为 Push 通知时附加到 payload 中，Android 客户端收到推送消息时对应字段名为 pushData。
        :param verify_blacklist: 是否过滤发送人黑名单列表，0 表示为不过滤、 1 表示为过滤，默认为 0 不过滤。
        :param content_available: 针对 iOS 平台，对 SDK 处于后台暂停状态时为静默推送，是 iOS7 之后推出的一种推送方式。
                                  允许应用在收到通知后在后台运行一段代码，且能够马上执行，查看详细。
                                  1 表示为开启，0 表示为关闭，默认为 0。
        """
        if push_content is None:
            push_content = []
        if push_data is None:
            push_data = []
        to_user_ids = self._tran_list(to_user_ids)
        content = json.dumps(content).replace('\"', '\\"')
        param_dict = locals().copy()
        url = '/message/private/publish_template.json'
        format_str = '{' \
                     '"fromUserId":"{{ from_user_id }}",' \
                     '"toUserId":[{% for item in to_user_ids %}"{{ item }}"{% if not loop.last %},{% endif %}{% endfor %}],' \
                     '"objectName":"{{ object_name }}",' \
                     '"values":[{% for item in values %}{% raw %}{{% endraw %}{% for key, value in item.items() %}"{{ key }}":"{{ value }}"{% if not loop.last %},{% endif %}{% endfor %}{% raw %}}{% endraw %}{% if not loop.last %},{% endif %}{% endfor %}],' \
                     '"content":"{{ content }}",' \
                     '"pushContent":[{% for item in push_content %}"{{ item }}"{% if not loop.last %},{% endif %}{% endfor %}],' \
                     '"pushData":[{% for item in push_data %}"{{ item }}"{% if not loop.last %},{% endif %}{% endfor %}],' \
                     '"verifyBlacklist":{{ verify_blacklist }},' \
                     '"contentAvailable":{{ content_available }}' \
                     '}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(to_user_ids, list, '1-1000')
            for user in to_user_ids:
                self._check_param(user, str, '1-64')
            self._check_param(object_name, str, '1-32')
            self._check_param(content, str)
            self._check_param(values, list)
            self._check_param(push_content, list)
            self._check_param(push_data, list)
            self._check_param(verify_blacklist, int, '0-1')
            self._check_param(content_available, int, '0-1')
            xx = self._render(param_dict, format_str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class Group(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def send(self, from_user_id, to_group_id, object_name, content, push_content=None, push_data=None,
             is_persisted=1, is_counted=1, is_include_sender=0, is_mentioned=0, content_available=0):
        """
        发送群组消息。
        """
        content = urllib.parse.quote(json.dumps(content))
        param_dict = locals().copy()
        url = '/message/group/publish.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '&toGroupId={{ to_group_id }}' \
                     '&objectName={{ object_name }}' \
                     '&content={{ content }}' \
                     '{% if push_content is not none %}&pushContent={{ push_content }}{% endif %}' \
                     '{% if push_data is not none %}&pushData={{ push_data }}{% endif %}' \
                     '&isPersisted={{ is_persisted }}' \
                     '&isCounted={{ is_counted }}' \
                     '&isIncludeSender={{ is_include_sender }}' \
                     '&isMentioned={{ is_mentioned }}' \
                     '&contentAvailable={{ content_available }}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(to_group_id, str, '1-64')
            self._check_param(object_name, str, '1-32')
            self._check_param(content, str)
            self._check_param(push_content, str)
            self._check_param(push_data, str)
            self._check_param(is_persisted, int, '0-1')
            self._check_param(is_counted, int, '0-1')
            self._check_param(is_include_sender, int, '0-1')
            self._check_param(is_mentioned, int, '0-1')
            self._check_param(content_available, int, '0-1')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def recall(self, from_user_id, group_id, uid, sent_time, is_admin=None, is_delete=None, extra=None):
        """
        撤回已发送的群聊消息，撤回时间无限制，只允许撤回用户自己发送的消息。
        :param from_user_id:        消息发送人用户 Id。（必传）
        :param group_id:            群组会话 Id。（必传）
        :param uid:                 消息唯一标识，可通过服务端实时消息路由获取，对应名称为 msgUID。（必传）
        :param sent_time:           消息发送时间，可通过服务端实时消息路由获取，对应名称为 msgTimestamp。（必传）
        :param is_admin:            是否为管理员，默认为 0，设为 1 时，IMKit 收到此条消息后，小灰条默认显示为
                                    “管理员 撤加了一条消息”。（非必传）
        :param is_delete:           是否删除消息，默认为 0 撤回该条消息同时，用户端将该条消息删除并替换为一条小灰条撤回提示消息；
                                    为 1 时，该条消息删除后，不替换为小灰条提示消息。（非必传）
        :param extra:               扩展信息，可以放置任意的数据内容。（非必传）
        :return:                    请求返回结果。
        """
        param_dict = locals().copy()
        url = '/message/recall.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '&conversationType=1' \
                     '&targetId={{ group_id }}' \
                     '&messageUID={{ uid }}' \
                     '&sentTime={{ sent_time }}' \
                     '{% if is_admin is not none %}&isAdmin={{ is_admin }}{% endif %}' \
                     '{% if is_delete is not none %}&isDelete={{ is_delete }}{% endif %}' \
                     '{% if extra is not none %}&extra={{ extra }}{% endif %}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(group_id, str, '1-64')
            self._check_param(uid, str)
            self._check_param(sent_time, int)
            self._check_param(is_admin, int)
            self._check_param(is_delete, int)
            self._check_param(extra, str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class Chatroom(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def send(self, from_user_id, to_chatroom_id, object_name, content):
        """
        发送聊天室消息。
        """
        content = urllib.parse.quote(json.dumps(content))
        param_dict = locals().copy()
        url = '/message/chatroom/publish.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '&toChatroomId={{ to_chatroom_id }}' \
                     '&objectName={{ object_name }}' \
                     '&content={{ content }}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(to_chatroom_id, str)
            self._check_param(object_name, str, '1-32')
            self._check_param(content, str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def recall(self, from_user_id, chatroom_id, uid, sent_time, is_admin=None, is_delete=None, extra=None):
        """
        撤回已发送的聊天室消息，撤回时间无限制，只允许撤回用户自己发送的消息。
        :param from_user_id:        消息发送人用户 Id。（必传）
        :param chatroom_id:         聊天室 Id。（必传）
        :param uid:                 消息唯一标识，可通过服务端实时消息路由获取，对应名称为 msgUID。（必传）
        :param sent_time:           消息发送时间，可通过服务端实时消息路由获取，对应名称为 msgTimestamp。（必传）
        :param is_admin:            是否为管理员，默认为 0，设为 1 时，IMKit 收到此条消息后，小灰条默认显示为
                                    “管理员 撤加了一条消息”。（非必传）
        :param is_delete:           是否删除消息，默认为 0 撤回该条消息同时，用户端将该条消息删除并替换为一条小灰条撤回提示消息；
                                    为 1 时，该条消息删除后，不替换为小灰条提示消息。（非必传）
        :param extra:               扩展信息，可以放置任意的数据内容。（非必传）
        :return:                    请求返回结果。
        """
        param_dict = locals().copy()
        url = '/message/recall.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '&conversationType=4' \
                     '&targetId={{ chatroom_id }}' \
                     '&messageUID={{ uid }}' \
                     '&sentTime={{ sent_time }}' \
                     '{% if is_admin is not none %}&isAdmin={{ is_admin }}{% endif %}' \
                     '{% if is_delete is not none %}&isDelete={{ is_delete }}{% endif %}' \
                     '{% if extra is not none %}&extra={{ extra }}{% endif %}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(chatroom_id, str, '1-64')
            self._check_param(uid, str)
            self._check_param(sent_time, int)
            self._check_param(is_admin, int)
            self._check_param(is_delete, int)
            self._check_param(extra, str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def broadcast(self, from_user_id, object_name, content):
        """
        向应用中的所有聊天室发送一条消息，单条消息最大 128k。
        此服务在开通 IM 商用版的情况下，可申请开通，详细请联系商务，电话：13161856839。
        :param from_user_id:        发送人用户 Id。（必传）
        :param object_name:         消息类型，参考融云消息类型表.消息标志；可自定义消息类型，长度不超过 32 个字符，
                                    您在自定义消息时需要注意，不要以 "RC:" 开头，
                                    以避免与融云系统内置消息的 ObjectName 重名。（必传）
        :param content:             发送消息内容，内置消息以 JSON 方式进行数据序列化，详见融云内置消息结构详解；
                                    如果 objectName 为自定义消息类型，该参数可自定义格式，不限于 JSON。（必传）
        :return:                    请求返回结果。
        """
        content = urllib.parse.quote(json.dumps(content))
        param_dict = locals().copy()
        url = '/message/chatroom/broadcast.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '&objectName={{ object_name }}' \
                     '&content={{ content }}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(object_name, str, '1-32')
            self._check_param(content, str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class System(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def send(self, from_user_id, to_user_id, object_name, content, push_content='', push_data='',
             is_persisted=1, is_counted=1, content_available=0):
        """
        发送系统消息。
        """
        content = urllib.parse.quote(json.dumps(content))
        param_dict = locals().copy()
        url = '/message/system/publish.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '&toUserId={{ to_user_id }}' \
                     '&objectName={{ object_name }}' \
                     '&content={{ content }}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(to_user_id, str, '1-64')
            self._check_param(object_name, str, '1-32')
            self._check_param(content, str)
            self._check_param(push_content, str)
            self._check_param(push_data, str)
            self._check_param(is_persisted, int, '0-1')
            self._check_param(is_counted, int, '0-1')
            self._check_param(content_available, int, '0-1')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def send_template(self, from_user_id, to_user_list, object_name, content, values,
                      push_content=None, push_data=None, content_available=0):
        """
        向多个用户发送不同内容的系统消息。。
        """
        if push_content is None:
            push_content = []
        if push_data is None:
            push_data = []
        content = json.dumps(content).replace('\"', '\\"')
        param_dict = locals().copy()
        url = '/message/system/publish_template.json'
        format_str = '{' \
                     '"fromUserId":"{{ from_user_id }}",' \
                     '"toUserId":[{% for item in to_user_list %}"{{ item }}"{% if not loop.last %},{% endif %}{% endfor %}],' \
                     '"objectName":"{{ object_name }}",' \
                     '"values":[{% for item in values %}{% raw %}{{% endraw %}{% for key, value in item.items() %}"{{ key }}":"{{ value }}"{% if not loop.last %},{% endif %}{% endfor %}{% raw %}}{% endraw %}{% if not loop.last %},{% endif %}{% endfor %}],' \
                     '"content":"{{ content }}",' \
                     '"pushContent":[{% for item in push_content %}"{{ item }}"{% if not loop.last %},{% endif %}{% endfor %}],' \
                     '"pushData":[{% for item in push_data %}"{{ item }}"{% if not loop.last %},{% endif %}{% endfor %}],' \
                     '"contentAvailable":{{ content_available }}' \
                     '}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(to_user_list, list, '1-1000')
            for user in to_user_list:
                self._check_param(user, str, '1-64')
            self._check_param(object_name, str, '1-32')
            self._check_param(content, str)
            self._check_param(values, list)
            self._check_param(push_content, list)
            self._check_param(push_data, list)
            self._check_param(content_available, int, '0-1')
            xx = self._render(param_dict, format_str)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class Broadcast(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def send(self, from_user_id, object_name, content, push_content='', push_data='', content_available=0):
        """
        发给应用内所有用户发送消息，每小时最多发 2 次，每天最多发送 3 次。
        """
        content = urllib.parse.quote(json.dumps(content))
        param_dict = locals().copy()
        url = '/message/broadcast.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '&objectName={{ object_name }}' \
                     '&content={{ content }}' \
                     '&pushContent={{ push_content }}' \
                     '&pushData={{ push_data }}' \
                     '&contentAvailable={{ content_available }}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(object_name, str, '1-32')
            self._check_param(content, str)
            self._check_param(push_content, str)
            self._check_param(push_data, str)
            self._check_param(content_available, int, '0-1')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))


class History(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def query(self, date):
        """
        按小时获取历史消息日志文件 URL，包含小时内应用产生的所有消息，消息日志文件无论是否已下载，3 天后将从融云服务器删除
        消息日志文件按 小时 生成，例如: 获取 10 - 11 点的消息， 11 点后生成。
        """
        param_dict = locals().copy()
        url = '/message/history.json'
        format_str = 'date={{ date }}'
        try:
            self._check_param(date, str, '1-30')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def remove(self, date):
        """
        删除历史消息日志文件。
        """
        param_dict = locals().copy()
        url = '/message/history/delete.json'
        format_str = 'date={{ date }}'
        try:
            self._check_param(date, str, '1-30')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
