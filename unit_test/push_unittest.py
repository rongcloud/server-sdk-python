import unittest

from rongcloud.rongcloud import RongCloud

rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz')


class PushTestCase(unittest.TestCase):
    def test_broadcast(self):
        platform = ['ios', 'android']
        from_user_id = 'fromuseId1'
        tag = ['女', '年轻']
        tag_or = ['北京', '上海']
        user_id = ['123', '456']
        is_to_all = False
        content = {'content': '1111', 'extra': 'aa'}
        object_name = 'RC:TxtMsg'
        alert = 'this is a push'
        ios_alert = 'iOS 通知显示内容'
        ios_extras = {'id': '1', 'name': '2'}
        ios_content_available = 1
        android_alert = 'Android 通知显示内容'
        android_extras = {'id': '1', 'name': '2'}
        rep = rc.get_push().broadcast(platform, from_user_id, tag, tag_or, user_id, is_to_all,
                                      content, object_name, alert, ios_alert, ios_extras,
                                      ios_content_available, android_alert, android_extras)
        self.assertEqual(rep['code'], 200, rep)

    def test_push(self):
        platform = ['ios', 'android']
        tag = ['女', '年轻']
        tag_or = ['北京', '上海']
        user_id = ['123', '456']
        is_to_all = False
        alert = 'this is a push'
        ios_title = '标题'
        ios_alert = 'iOS 通知显示内容'
        ios_extras = {'id': '1', 'name': '2'}
        android_alert = 'Android 通知显示内容'
        android_extras = {'id': '1', 'name': '2'}
        rep = rc.get_push().push(platform, tag, tag_or, user_id, None, is_to_all,
                                 alert, ios_title, ios_alert, ios_extras, None, None, None, None,
                                 android_alert, android_extras)
        self.assertEqual(rep['code'], 200, rep)


if __name__ == '__main__':
    unittest.main()
