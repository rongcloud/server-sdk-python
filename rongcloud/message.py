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
             verify_blacklist=0, is_persisted=1, is_counted=1, is_include_sender=0):
        """
        发送单聊消息。
        :param from_user_id: 发送人用户 ID。
        :param to_user_ids: 接收用户 ID。可以实现向多人发送消息，每次上限为 1000 人。
        :param object_name: 发送的消息类型。
        :param content: 消息内容。
        :param push_content: 定义显示的 Push 内容，如果 objectName 为融云内置消息类型时，则发送后用户一定会收到 Push 信息。
                             如果为自定义消息，则 pushContent 为自定义消息显示的 Push 内容，如果不传则用户不会收到 Push 通知。
        :param push_data: 针对 iOS 平台为 Push 通知时附加到 payload 中，Android 客户端收到推送消息时对应字段名为 pushData。
        :param verify_blacklist: 是否过滤发送人黑名单列表，0 表示为不过滤、 1 表示为过滤，默认为 0 不过滤。
        :param is_persisted: 当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行存储，
                             0 表示为不存储、 1 表示为存储，默认为 1 存储消息。
        :param is_counted: 当前版本有新的自定义消息，而老版本没有该自定义消息时，老版本客户端收到消息后是否进行未读消息计数，
                           0 表示为不计数、 1 表示为计数，默认为 1 计数，未读消息数增加 1。
        :param is_include_sender: 发送用户自已是否接收消息，0 表示为不接收，1 表示为接收，默认为 0 不接收。
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
                     '&verifyBlacklist={{ verify_blacklist }}' \
                     '&isPersisted={{ is_persisted }}' \
                     '&isCounted={{ is_counted }}' \
                     '&isIncludeSender={{ is_include_sender }}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(to_user_ids, list, '1-1000')
            for user in to_user_ids:
                self._check_param(user, str, '1-64')
            self._check_param(object_name, str, '1-32')
            self._check_param(content, str)
            self._check_param(push_content, str)
            self._check_param(push_data, str)
            self._check_param(verify_blacklist, int, '0-1')
            self._check_param(is_persisted, int, '0-1')
            self._check_param(is_counted, int, '0-1')
            self._check_param(is_include_sender, int, '0-1')
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def recall(self, from_user_id, target_id, uid, sent_time):
        """
        撤回已发送的单聊消息，撤回时间无限制，只允许撤回用户自己发送的消息。
        :param from_user_id: 发送人用户 ID。
        :param target_id: 接收用户 ID。
        :param uid: 消息的唯一标识，各端 SDK 发送消息成功后会返回 uID。
        :param sent_time: 消息的发送时间，各端 SDK 发送消息成功后会返回 sentTime。
        """
        param_dict = locals().copy()
        url = '/message/recall.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '&targetId={{ target_id }}' \
                     '&conversationType=1' \
                     '&messageUID={{ uid }}' \
                     '&sentTime={{ sent_time }}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(target_id, str, '1-64')
            self._check_param(uid, str)
            self._check_param(sent_time, int)
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

    def recall(self, from_user_id, group_id, uid, sent_time):
        """
        撤回已发送的群聊消息，撤回时间无限制，只允许撤回用户自己发送的消息。
        """
        param_dict = locals().copy()
        url = '/message/recall.json'
        format_str = 'fromUserId={{ from_user_id }}' \
                     '&targetId={{ group_id }}' \
                     '&conversationType=3' \
                     '&messageUID={{ uid }}' \
                     '&sentTime={{ sent_time }}'
        try:
            self._check_param(from_user_id, str, '1-64')
            self._check_param(group_id, str, '1-64')
            self._check_param(uid, str)
            self._check_param(sent_time, int)
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

    def broadcast(self, from_user_id, object_name, content):
        """
        向应用内所有聊天室广播消息，此功能需开通专属服务。
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

    def broadcast(self, from_user_id, object_name, content, push_content='', push_data='', content_available=0):
        """
        发给应用内所有用户发送消息，每小时最多发 2 次，每天最多发送 3 次。
        """
        content = urllib.parse.quote(json.dumps(content))
        param_dict = locals().copy()
        url = '/message/chatroom/broadcast.json'
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
        url = '/message/private/publish_template.json'
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
