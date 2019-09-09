import json
import urllib

from rongcloud.module import Module, ParamException


class Push(Module):
    """
    广播推送可精准及时的向符合条件的应用中用户推送消息，帮助开发者提升用户忠诚度及留存率。
    广播推送服务包括两个功能：一个是发送广播消息，一个是推送（Push）：
        * 广播（Broadcast） 是一种业务概念，是通过后台管理界面或者调用服务端接口，向 App 中的所有用户发送一条消息。
        * 推送（Push） 是一种技术概念，是指从服务端实时发送信息到客户端。
    """

    def __init__(self, rc):
        super().__init__(rc)

    def broadcast(self, platforms, from_user_id, tags, tags_or, user_ids, is_to_all, content,
                  object_name, alert, ios_alert, ios_extras, ios_content_available, android_alert, android_extras):
        """
        此方法与 /message/broadcast 广播消息方法发送机制一样，可选择更多发送条件。
        该功能开发环境下可免费使用。生产环境下，您需要在开发者后台高级功能设置中开通 IM 商用版后，在“广播消息和推送”中，开启后才能使用。
        :param platforms:           目标操作系统，iOS、Android 最少传递一个。如果需要给两个系统推送消息时，则需要全部填写。（必传）
        :param from_user_id:        发送人用户 Id。（必传）
        :param tags:                用户标签，每次发送时最多发送 20 个标签，标签之间为 AND 的关系，
                                    is_to_all 为 true 时参数无效。（非必传）
        :param tags_or:             用户标签，每次发送时最多发送 20 个标签，标签之间为 OR 的关系，
                                    is_to_all 为 true 时参数无效，tag_or 同 tag 参数可以同时存在。（非必传）
        :param user_ids:            用户 Id，每次发送时最多发送 1000 个用户，
                                    如果 tag 和 userid 两个条件同时存在时，则以 userid 为准，
                                    如果 userid 有值时，则 platform 参数无效，is_to_all 为 true 时参数无效。（非必传）
        :param is_to_all:           是否全部推送，false 表示按 tag，tag_or 或 userid 条件推送，true 表示向所有用户推送，
                                    tag，tag_or 和 userid 条件无效。（必传）
        :param content:             发送消息内容，参考融云 Server API 消息类型表.示例说明；
                                    如果 objectName 为自定义消息类型，该参数可自定义格式。（必传）
        :param object_name:         消息类型，参考融云 Server API 消息类型表，消息标志；
                                    可自定义消息类型，长度不超过 32 个字符。（必传）
        :param alert:               默认推送消息内容，如填写了 iOS 或 Android 下的 alert 时，
                                    则推送内容以对应平台系统的 alert 为准。（必传）
        :param ios_alert:           iOS 平台下的推送消息内容，传入后默认的推送消息内容失效，不能为空。（非必传）
        :param ios_extras:          iOS 平台下的附加信息，如果开发者自己需要，可以自己在 App 端进行解析。（非必传）
        :param ios_content_available:   针对 iOS 平台，对 SDK 处于后台暂停状态时为静默推送，是 iOS7 之后推出的一种推送方式。
                                    允许应用在收到通知后在后台运行一段代码，且能够马上执行，查看详细。
                                    1 表示为开启，0 表示为关闭，默认为 0（非必传）
        :param android_alert:       Android 平台下的推送消息内容，传入后默认的推送消息内容失效，不能为空。（非必传）
        :param android_extras:      iOS 平台下的附加信息，如果开发者自己需要，可以自己在 App 端进行解析。（非必传）
        :return:                    请求返回结果，code 返回码，200 为正常；id 推送唯一标识。
                                    如：{"code":200,"id":"50whSR6kQiHb7YgFwQzXIb"}
        """
        param_dict = locals().copy()
        url = '/push.json'
        try:
            # key - platform
            self._check_param(platforms, list, '1~2')
            for platform in platforms:
                self._check_param(platform, str, '1~64')
            # key - from_user_id
            self._check_param(from_user_id, str, '1~64')
            # key - audience
            for tag in tags:
                self._check_param(tag, str, '1~64')
            self._check_param(tags, list, '1~20')
            for tag in tags:
                self._check_param(tag, str, '1~64')
            self._check_param(tags_or, list, '1~20')
            for tag_or in tags_or:
                self._check_param(tag_or, str, '1~64')
            self._check_param(user_ids, list, '1~1000')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(is_to_all, bool)
            audience = {}
            if tags is not None:
                audience['tag'] = tags
            if tags_or is not None:
                audience['tag_or'] = tags_or
            if user_ids is not None:
                audience['userid'] = user_ids
            if is_to_all is not None:
                audience['is_to_all'] = is_to_all
            # key - message
            self._check_param(object_name, str, '1~32')
            content = urllib.parse.quote(json.dumps(content))
            message = {'content': content, 'objectName': object_name}
            # key - notification
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
            json_data = {'platform': platforms, 'fromuserid': from_user_id, 'audience': audience,
                         'message': message, 'notification': notification}
            format_str = json.dumps(json_data, ensure_ascii=False)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))

    def push(self, platforms, tags, tags_or, user_ids, package_name, is_to_all,
             alert, ios_title, ios_alert, ios_extras, ios_content_available, ios_badge, ios_category,
             ios_rich_media_uri, android_alert, android_extras):
        """
        该功能在开发环境下可免费使用。生产环境下，您需要登录开发者后台，开发者后台中开通 IM 商用版后，
        在“广播消息和推送”中，开启后才能使用。
        :param platforms:           目标操作系统，iOS，Android 最少传递一个。如果需要给两个系统推送消息时，则需要全部填写。（必传）
        :param tags:                用户标签，每次发送时最多发送 20 个标签，标签之间为 AND 的关系，
                                    is_to_all 为 true 时参数无效。（非必传）
        :param tags_or:             用户标签，每次发送时最多发送 20 个标签，标签之间为 OR 的关系，is_to_all 为 true 时参数无效，
                                    tags_or 同 tags 参数可以同时存在。（非必传）
        :param user_ids:            用户 Id，每次发送时最多发送 1000 个用户，
                                    如果 tags 和 user_ids 两个条件同时存在时，则以 user_ids 为准，
                                    如果 user_ids 有值时，则 platforms 参数无效，is_to_all 为 true 时参数无效。（非必传）
        :param package_name:        应用包名，is_to_all 为 true 时，此参数无效。与 tags，tags_or 同时存在时为 And 的关系，
                                    向同时满足条件的用户推送。与 user_ids 条件同时存在时，以 user_ids 为准进行推送。（非必传）
        :param is_to_all:           是否全部推送，false 表示按 tags，tags_or 或 user_ids 条件推送，
                                    true 表示向所有用户推送，tags，tags_or 和 user_ids 条件无效。（必传）
        :param alert:               notification 下 alert，默认推送消息内容，
                                    如填写了 iOS 或 Android 下的 alert 时，则推送内容以对应平台系统的 alert 为准。（必传）
        :param ios_title            通知栏显示的推送标题，仅针对 iOS 平台，支持 iOS 8.2 及以上版本，参数在 ios 节点下设置，
                                    详细可参考“设置 iOS 推送标题请求示例”。（非必传）
        :param ios_alert:           iOS 平台下的推送消息内容，传入后默认的推送消息内容失效，不能为空。（非必传）
        :param ios_extras:          iOS 平台下的附加信息，如果开发者自己需要，可以自己在 App 端进行解析。（非必传）
        :param ios_content_available:   针对 iOS 平台，静默推送是 iOS7 之后推出的一种推送方式。
                                    允许应用在收到通知后在后台运行一段代码，且能够马上执行，查看详细。
                                    1 表示为开启，0 表示为关闭，默认为 0（非必传）
        :param ios_badge:           应用角标，仅针对 iOS 平台；不填时，表示不改变角标数；为 0 或负数时，表示 App 角标上的数字清零；
                                    否则传相应数字表示把角标数改为指定的数字，最大不超过 9999，参数在 ios 节点下设置，
                                    详细可参考“设置 iOS 角标数 HTTP 请求示例”。（非必传）
        :param ios_category:        iOS 富文本推送的类型开发者自已定义，自已在 App 端进行解析判断，
                                    与 richMediaUri 一起使用。（非必传）
        :param ios_rich_media_uri:  iOS 富文本推送内容的 URL，与 category 一起使用。（非必传）
        :param android_alert:       Android 平台下的推送消息内容，传入后默认的推送消息内容失效，不能为空。（非必传）
        :param android_extras:      Android 平台下的附加信息，如果开发者自己需要，可以自己在 App 端进行解析。（非必传）
        :return:                    请求返回结果，code 返回码，200 为正常；id 推送唯一标识。
                                    如：{"code":200,"id":"50whSR6kQiHb7YgFwQzXIb"}
        """
        param_dict = locals().copy()
        url = '/push.json'
        try:
            # key - platform
            self._check_param(platforms, list, '1~2')
            for platform in platforms:
                self._check_param(platform, str, '1~64')
            # key - audience
            for tag in tags:
                self._check_param(tag, str, '1~64')
            self._check_param(tags, list, '1~20')
            for tag in tags:
                self._check_param(tag, str, '1~64')
            self._check_param(tags_or, list, '1~20')
            for tag_or in tags_or:
                self._check_param(tag_or, str, '1~64')
            self._check_param(user_ids, list, '1~1000')
            for user_id in user_ids:
                self._check_param(user_id, str, '1~64')
            self._check_param(is_to_all, bool)
            audience = {}
            if tags is not None:
                audience['tag'] = tags
            if tags_or is not None:
                audience['tag_or'] = tags_or
            if user_ids is not None:
                audience['userid'] = user_ids
            if is_to_all is not None:
                audience['is_to_all'] = is_to_all
            if package_name is not None:
                audience['packageName'] = package_name
            # key - notification
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
            json_data = {'platform': platforms, 'audience': audience, 'notification': notification}
            format_str = json.dumps(json_data, ensure_ascii=False)
            return self._http_post(url, self._render(param_dict, format_str))
        except ParamException as e:
            return json.loads(str(e))
