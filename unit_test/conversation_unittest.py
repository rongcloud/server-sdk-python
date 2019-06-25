import unittest

from rongcloud.conversation import Conversation
from rongcloud.rongcloud import RongCloud

rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz')


class ConversationTestCase(unittest.TestCase):
    def test_mute(self):
        user_id = 'AAA'
        target_id = 'BBB'
        rep = rc.get_conversation().mute(Conversation.CONVERSATION_PRIVATE, user_id, target_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_unmute(self):
        user_id = 'AAA'
        target_id = 'BBB'
        rep = rc.get_conversation().unmute(Conversation.CONVERSATION_PRIVATE, user_id, target_id)
        self.assertEqual(rep['code'], 200, rep)


if __name__ == '__main__':
    unittest.main()
