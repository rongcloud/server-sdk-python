from rongcloud.chatroom import Chatroom
from rongcloud.conversation import Conversation
from rongcloud.group import Group
from rongcloud.message import Message
from rongcloud.push import Push
from rongcloud.sensitive import Sensitive
from rongcloud.user import User
import threading
import time
import datetime

class RongCloud:
    class _HostUrl:
        def __init__(self, host_url):
            self.host_list = host_url.split(';')
            self.now = 0
            self.last_change_url_duration = 30
            self.last_change_url_time = 0

        def get_url(self):
            return self.host_list[self.now]

        def switch_url(self):
            lock = threading.Lock()
            with lock:
                # 检查距离上次更换uri的时间间隔
                now = time.time()
                seconds = (datetime.datetime.fromtimestamp(now) - datetime.datetime.fromtimestamp(self.last_change_url_time)).seconds
                if seconds >= self.last_change_url_duration:
                    if self.now < len(self.host_list) - 1:
                        self.now = self.now + 1
                    else:
                        self.now = 0
                    self.last_change_url_time = time.time()

    def __init__(self, app_key, app_secret, host_url='http://api-cn.ronghub.com;http://api2-cn.ronghub.com'):
        self.app_key = app_key
        self.app_secret = app_secret
        self.host_url = self._HostUrl(host_url)

    def get_user(self):
        return User(self)

    def get_message(self):
        return Message(self)

    def get_group(self):
        return Group(self)

    def get_conversation(self):
        return Conversation(self)

    def get_chatroom(self):
        return Chatroom(self)

    def get_sensitive(self):
        return Sensitive(self)

    def get_push(self):
        return Push(self)