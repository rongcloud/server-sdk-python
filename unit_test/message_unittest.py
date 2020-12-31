import unittest

from rongcloud.rongcloud import RongCloud

rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz')


class MessageTestCase(unittest.TestCase):

    def test_broadcast(self):
        from_user_id = 'AAA'
        object_name = 'RC:TxtMsg'
        content = {'content': 'hello', 'extra': 'helloExtra'}
        push_ext = "{\"title\":\"youhaveanewmessage.\",\"forceShowPushContent\":0,\"pushConfigs\":[{\"HW\":{\"channelId\":\"hw-123\"}},{\"MI\":{\"channelId\":\"mi-123\"}},{\"OPPO\":{\"channelId\":\"oppo-123\"}},{\"VIVO\":{\"classification\":\"0\"}},{\"APNs\":{\"thread-id\":\"123\",\"apns-collapse-id\":\"123456\"}}]}"
        rep = rc.get_message().broadcast(from_user_id, object_name, content)
        # rep = rc.get_message().broadcast(from_user_id, object_name, content, push_ext=push_ext)
        self.assertEqual(rep['code'], 200, rep)

    def test_private_send(self):
        from_user_id = 'BBB'
        to_user_id = 'AAA'
        object_name = 'RC:TxtMsg'
        content = {'content': 'hello', 'extra': '...'}
        expansion = True
        disable_push = True
        push_ext = "{\"title\":\"youhaveanewmessage.\",\"forceShowPushContent\":0,\"pushConfigs\":[{\"HW\":{\"channelId\":\"hw-123\"}},{\"MI\":{\"channelId\":\"mi-123\"}},{\"OPPO\":{\"channelId\":\"oppo-123\"}},{\"VIVO\":{\"classification\":\"0\"}},{\"APNs\":{\"thread-id\":\"123\",\"apns-collapse-id\":\"123456\"}}]}"
        # rep = rc.get_message().get_private().send(from_user_id, to_user_id, object_name, content)
        # rep = rc.get_message().get_private().send(from_user_id, to_user_id, object_name, content, expansion=expansion, disable_push=disable_push)
        rep = rc.get_message().get_private().send(from_user_id, to_user_id, object_name, content, expansion=expansion, disable_push=disable_push, push_ext=push_ext)
        self.assertEqual(rep['code'], 200, rep)

    def test_private_recall(self):
        from_user_id = 'AAA'
        target_id = 'BBB'
        uid = '5FGT-7VA9-G4DD-4V5P'
        sent_time = 1507778882124
        rep = rc.get_message().get_private().recall(from_user_id, target_id, uid, sent_time)
        self.assertEqual(rep['code'], 200, rep)

    def test_private_send_template(self):
        from_user_id = 'fromuser'
        to_user_ids = ['21', '22']
        object_name = 'RC:TxtMsg'
        values = [{'{c}': '1', '{d}': '2', '{e}': '3'}, {'{c}': '4', '{d}': '5', '{e}': '6'}]
        content = {'content': '{c}{d}{e}', 'extra': 'bb'}
        push_content = ['push{c}', 'push{c}']
        push_data = ['pushd', 'pushd']
        disable_push = False
        # rep = rc.get_message().get_private().send_template(from_user_id, to_user_ids, object_name, values, content,
        #                                                    push_content, push_data)
        rep = rc.get_message().get_private().send_template(from_user_id, to_user_ids, object_name, values, content,
                                                           push_content, push_data, disable_push=disable_push)
        self.assertEqual(rep['code'], 200, rep)

    def test_group_send(self):
        from_user_id = 'AAA'
        to_group_id = 'Group_1'
        object_name = 'RC:TxtMsg'
        content = {
            'content': 'hello',
            'mentionedInfo': {
                'type': 2,
                'userIdList': ['123', '456'],
                'mentionedContent': '有人@你'
            }
        }
        expansion = True
        disable_push = True
        push_ext = "{\"title\":\"youhaveanewmessage.\",\"forceShowPushContent\":0,\"pushConfigs\":[{\"HW\":{\"channelId\":\"hw-123\"}},{\"MI\":{\"channelId\":\"mi-123\"}},{\"OPPO\":{\"channelId\":\"oppo-123\"}},{\"VIVO\":{\"classification\":\"0\"}},{\"APNs\":{\"thread-id\":\"123\",\"apns-collapse-id\":\"123456\"}}]}"
        # rep = rc.get_message().get_group().send(from_user_id, to_group_id, object_name, content)
        # rep = rc.get_message().get_group().send(from_user_id, to_group_id, object_name, content, expansion=expansion, disable_push=disable_push)
        rep = rc.get_message().get_group().send(from_user_id, to_group_id, object_name, content, expansion=expansion, disable_push=disable_push, push_ext=push_ext)
        self.assertEqual(rep['code'], 200, rep)

    def test_group_send_direction(self):
        from_user_id = 'AAA'
        to_group_id = 'Group_1'
        to_user_ids = ['21', '22']
        object_name = 'RC:TxtMsg'
        content = {
            'content': 'hello',
            'mentionedInfo': {
                'type': 2,
                'userIdList': ['123', '456'],
                'mentionedContent': '有人@你'
            }
        }
        rep = rc.get_message().get_group().send_direction(from_user_id, to_group_id, to_user_ids, object_name, content)
        self.assertEqual(rep['code'], 200, rep)

    def test_group_recall(self):
        from_user_id = 'AAA'
        to_group_id = 'Group_1'
        uid = '5FGT-7VA9-G4DD-4V5P'
        sent_time = 1507778882124
        rep = rc.get_message().get_group().recall(from_user_id, to_group_id, uid, sent_time)
        self.assertEqual(rep['code'], 200, rep)

    def test_chatroom_send(self):
        from_user_id = 'AAA'
        to_chatroom_id = 'Chatroom_1'
        object_name = 'RC:TxtMsg'
        content = {
            'content': 'hello',
            'extra': 'helloExtra'
        }
        rep = rc.get_message().get_chatroom().send(from_user_id, to_chatroom_id, object_name, content)
        self.assertEqual(rep['code'], 200, rep)

    def test_chatroom_recall(self):
        from_user_id = 'AAA'
        to_chatroom_id = 'Chatroom_1'
        uid = '5FGT-7VA9-G4DD-4V5P'
        sent_time = 1507778882124
        rep = rc.get_message().get_group().recall(from_user_id, to_chatroom_id, uid, sent_time)
        self.assertEqual(rep['code'], 200, rep)

    def test_chatroom_broadcast(self):
        from_user_id = 'AAA'
        object_name = 'RC:TxtMsg'
        content = {
            'content': 'hello',
            'extra': 'helloExtra'
        }
        rep = rc.get_message().get_chatroom().broadcast(from_user_id, object_name, content)
        self.assertEqual(rep['code'], 200, rep)

    def test_system_send(self):
        from_user_id = 'AAA'
        to_user_id = 'BBB'
        object_name = 'RC:TxtMsg'
        content = {
            'content': 'hello',
            'extra': 'helloExtra'
        }
        disable_push = False
        push_ext = "{\"title\":\"youhaveanewmessage.\",\"forceShowPushContent\":0,\"pushConfigs\":[{\"HW\":{\"channelId\":\"hw-123\"}},{\"MI\":{\"channelId\":\"mi-123\"}},{\"OPPO\":{\"channelId\":\"oppo-123\"}},{\"VIVO\":{\"classification\":\"0\"}},{\"APNs\":{\"thread-id\":\"123\",\"apns-collapse-id\":\"123456\"}}]}"
        # rep = rc.get_message().get_system().send(from_user_id, to_user_id, object_name, content)
        rep = rc.get_message().get_system().send(from_user_id, to_user_id, object_name, content, disable_push=disable_push, push_ext=push_ext)
        self.assertEqual(rep['code'], 200, rep)

    def test_system_send_template(self):
        from_user_id = 'fromuser'
        to_user_ids = ['21', '22']
        object_name = 'RC:TxtMsg'
        content = {'content': '{c}{d}{e}', 'extra': 'bb'}
        values = [{'{c}': '1', '{d}': '2', '{e}': '3'}, {'{c}': '4', '{d}': '5', '{e}': '6'}]
        push_content = ['push{c}', 'push{c}']
        push_data = ['pushd', 'pushd']
        rep = rc.get_message().get_system().send_template(from_user_id, to_user_ids, object_name, content, values,
                                                          push_content, push_data)
        self.assertEqual(rep['code'], 200, rep)

    def test_history_query(self):
        date = '2019010101'
        rep = rc.get_message().get_history().query(date)
        self.assertEqual(rep['code'], 200, rep)

    def test_history_remove(self):
        date = '2019010401'
        rep = rc.get_message().get_history().remove(date)
        self.assertEqual(rep['code'], 200, rep)

    def test_private_send_status_message(self):
        from_user_id = 'fromuser'
        to_user_ids = ['21', '22']
        object_name = 'RC:TxtMsg'
        content = {"content":"hello","extra":"helloExtra"}
        rep = rc.get_message().get_private().send_status_message(from_user_id, to_user_ids, object_name, content)
        self.assertEqual(rep['code'], 200, rep)

    def test_group_send_status_message(self):
        from_user_id = 'fromuser'
        to_group_id = ['Group_1', 'Group_2']
        object_name = 'RC:TxtMsg'
        content = {"content":"hello","extra":"helloExtra"}
        rep = rc.get_message().get_group().send_status_message(from_user_id, to_group_id, object_name, content)
        self.assertEqual(rep['code'], 200, rep)


if __name__ == '__main__':
    unittest.main()
