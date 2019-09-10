import unittest

from rongcloud.conversation import Conversation
from rongcloud.rongcloud import RongCloud

rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz')


class ConversationTestCase(unittest.TestCase):
    def test_notification_set(self):
        conversation_type = 1
        user_id = 'AAA'
        target_id = 'BBB'
        is_mute = 1
        rep = rc.get_conversation().get_notification().set(conversation_type, user_id, target_id, is_mute)
        self.assertEqual(rep['code'], 200, rep)
        is_mute = 0
        rep = rc.get_conversation().get_notification().set(conversation_type, user_id, target_id, is_mute)
        self.assertEqual(rep['code'], 200, rep)

    def test_notification_get(self):
        conversation_type = 1
        user_id = 'AAA'
        target_id = 'BBB'
        rep = rc.get_conversation().get_notification().get(conversation_type, user_id, target_id)
        self.assertEqual(rep['code'], 200, rep)


if __name__ == '__main__':
    unittest.main()
