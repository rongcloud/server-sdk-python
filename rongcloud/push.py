import json

from rongcloud.module import Module, ParamException


class Push(Module):
    def __init__(self, rc):
        super().__init__(rc)

    def broadcast(self, platform, from_user_id, tag, tag_or, user_id, is_to_all, content,
                  object_name, alert, ios_alert, ios_extras, ios_content_available, android_alert, android_extras):
        """
        :param platform:
        :param from_user_id:
        :param tag:
        :param tag_or:
        :param user_id:
        :param is_to_all:
        :param content:
        :param object_name:
        :param alert:
        :param ios_alert:
        :param ios_extras:
        :param ios_content_available:
        :param android_alert:
        :param android_extras:
        """
        param_dict = locals().copy()
        url = '/push.json'
        try:
            audience = {}
            if tag is not None:
                audience['tag'] = tag
            if tag_or is not None:
                audience['tag_or'] = tag_or
            if user_id is not None:
                audience['userid'] = user_id
            if is_to_all is not None:
                audience['is_to_all'] = is_to_all
            content = json.dumps(content)
            message = {'content': content, 'objectName': object_name}
            notification = {'alert': alert}
            ios = {}
            if ios_alert is not None:
                ios['alert'] = ios_alert
            if ios_extras is not None:
                ios['extras'] = ios_extras
            if ios_content_available is not None:
                ios['contentAvailable'] = ios_content_available
            if len(ios) > 0:
                notification['ios'] = ios
            android = {}
            if android_alert is not None:
                android['alert'] = android_alert
            if android_extras is not None:
                android['extras'] = android_extras
            if len(android) > 0:
                notification['android'] = android
            json_data = {'platform': platform, 'fromuserid': from_user_id, 'audience': audience,
                         'message': message, 'notification': notification}
            format_str = json.dumps(json_data, ensure_ascii=False)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def push(self, platform, tag, tag_or, user_id, package_name, is_to_all,
             alert, ios_title, ios_alert, ios_extras, ios_content_available, ios_badge, ios_category,
             ios_rich_media_uri, android_alert, android_extras):
        """
        :param platform:
        :param tag:
        :param tag_or:
        :param user_id:
        :param package_name:
        :param is_to_all:
        :param alert:
        :param ios_title:
        :param ios_alert:
        :param ios_extras:
        :param ios_content_available:
        :param ios_badge:
        :param ios_category:
        :param ios_rich_media_uri:
        :param android_alert:
        :param android_extras:
        :return:
        """
        param_dict = locals().copy()
        url = '/push.json'
        try:
            audience = {}
            if tag is not None:
                audience['tag'] = tag
            if tag_or is not None:
                audience['tag_or'] = tag_or
            if user_id is not None:
                audience['userid'] = user_id
            if is_to_all is not None:
                audience['is_to_all'] = is_to_all
            if package_name is not None:
                audience['packageName'] = package_name
            notification = {'alert': alert}
            ios = {}
            if ios_title is not None:
                ios['title'] = ios_title
            if ios_alert is not None:
                ios['alert'] = ios_alert
            if ios_extras is not None:
                ios['extras'] = ios_extras
            if ios_content_available is not None:
                ios['contentAvailable'] = ios_content_available
            if ios_badge is not None:
                ios['badge'] = ios_badge
            if ios_category is not None:
                ios['category'] = ios_category
            if ios_rich_media_uri is not None:
                ios['richMediaUri'] = ios_rich_media_uri
            if len(ios) > 0:
                notification['ios'] = ios
            android = {}
            if android_alert is not None:
                android['alert'] = android_alert
            if android_extras is not None:
                android['extras'] = android_extras
            if len(android) > 0:
                notification['android'] = android
            json_data = {'platform': platform, 'audience': audience, 'notification': notification}
            format_str = json.dumps(json_data, ensure_ascii=False)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
