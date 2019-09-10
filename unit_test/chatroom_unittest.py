import unittest

from rongcloud.rongcloud import RongCloud

rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz')


class ChatroomTestCase(unittest.TestCase):
    def test_create(self):
        room_info_list = [('10001', 'name1')]
        rep = rc.get_chatroom().create(room_info_list)
        self.assertEqual(rep['code'], 200, rep)

    def test_destroy(self):
        room_id = '10001'
        rep = rc.get_chatroom().destroy(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_query(self):
        room_id = '10001'
        rep = rc.get_chatroom().query(room_id)
        self.assertEqual(rep['code'], 200, rep)
        room_ids = ['10001', '10002']
        rep = rc.get_chatroom().query(room_ids)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_query(self):
        room_id = '10001'
        count = 10
        order = 1
        rep = rc.get_chatroom().get_user().query(room_id, count, order)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_isexist(self):
        room_id = '10001'
        user_id = 'name1'
        rep = rc.get_chatroom().get_user().isexist(room_id, user_id)
        self.assertEqual(rep['code'], 200, rep)
        user_ids = ['name1', 'name2']
        rep = rc.get_chatroom().get_user().isexist(room_id, user_ids)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_gag_add(self):
        user_id_list = ['2583', '2582']
        room_id = '16'
        minute = 1
        rep = rc.get_chatroom().get_user().get_gag().add(user_id_list, room_id, minute)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_gag_remove(self):
        user_id_list = ['2583', '2582']
        room_id = '16'
        rep = rc.get_chatroom().get_user().get_gag().remove(user_id_list, room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_gag_query(self):
        room_id = '16'
        rep = rc.get_chatroom().get_user().get_gag().query(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_ban_add(self):
        user_id = '2583'
        minute = 1
        rep = rc.get_chatroom().get_user().get_ban().add(user_id, minute)
        self.assertEqual(rep['code'], 200, rep)
        user_ids = ['2583', '2582']
        rep = rc.get_chatroom().get_user().get_ban().add(user_ids, minute)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_ban_remove(self):
        user_id_list = ['2582']
        rep = rc.get_chatroom().get_user().get_ban().remove(user_id_list)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_ban_query(self):
        rep = rc.get_chatroom().get_user().get_ban().query()
        self.assertEqual(rep['code'], 200, rep)

    def test_user_block_add(self):
        user_id_list = ['2583', '2582']
        room_id = '16'
        minute = 1
        rep = rc.get_chatroom().get_user().get_block().add(user_id_list, room_id, minute)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_block_remove(self):
        user_id_list = ['2583', '2582']
        room_id = '16'
        rep = rc.get_chatroom().get_user().get_block().remove(user_id_list, room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_block_query(self):
        room_id = '16'
        rep = rc.get_chatroom().get_user().get_block().query(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_whitelist_add(self):
        room_id = '10001'
        user_id = 'name1'
        rep = rc.get_chatroom().get_user().get_whitelist().add(room_id, user_id)
        self.assertEqual(rep['code'], 200, rep)
        user_ids = ['name1', 'name2']
        rep = rc.get_chatroom().get_user().get_whitelist().add(room_id, user_ids)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_whitelist_remove(self):
        room_id = '10001'
        user_id = 'name1'
        rep = rc.get_chatroom().get_user().get_whitelist().remove(room_id, user_id)
        self.assertEqual(rep['code'], 200, rep)
        user_ids = ['name1', 'name2']
        rep = rc.get_chatroom().get_user().get_whitelist().remove(room_id, user_ids)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_whitelist_query(self):
        room_id = '10001'
        rep = rc.get_chatroom().get_user().get_whitelist().query(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_message_stop_distribution(self):
        room_id = '10001'
        rep = rc.get_chatroom().get_message().stop_distribution(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_message_resume_distribution(self):
        room_id = '10001'
        rep = rc.get_chatroom().get_message().resume_distribution(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_message_priority_add(self):
        obj_name = 'RC:TxtMsg'
        rep = rc.get_chatroom().get_message().get_priority().add(obj_name)
        self.assertEqual(rep['code'], 200, rep)
        obj_names = ['RC:VcMsg', 'RC:ImgMsg']
        rep = rc.get_chatroom().get_message().get_priority().add(obj_names)
        self.assertEqual(rep['code'], 200, rep)

    def test_message_priority_remove(self):
        obj_name = 'RC:TxtMsg'
        rep = rc.get_chatroom().get_message().get_priority().remove(obj_name)
        self.assertEqual(rep['code'], 200, rep)
        obj_names = ['RC:VcMsg', 'RC:ImgMsg']
        rep = rc.get_chatroom().get_message().get_priority().remove(obj_names)
        self.assertEqual(rep['code'], 200, rep)

    def test_message_priority_query(self):
        rep = rc.get_chatroom().get_message().get_priority().query()
        self.assertEqual(rep['code'], 200, rep)

    def test_whitelist_add(self):
        obj_name = 'RC:TxtMsg'
        rep = rc.get_chatroom().get_whitelist().add(obj_name)
        self.assertEqual(rep['code'], 200, rep)
        obj_names = ['RC:VcMsg', 'RC:ImgMsg']
        rep = rc.get_chatroom().get_whitelist().add(obj_names)
        self.assertEqual(rep['code'], 200, rep)

    def test_whitelist_remove(self):
        obj_name = 'RC:TxtMsg'
        rep = rc.get_chatroom().get_whitelist().remove(obj_name)
        self.assertEqual(rep['code'], 200, rep)
        obj_names = ['RC:VcMsg', 'RC:ImgMsg']
        rep = rc.get_chatroom().get_whitelist().remove(obj_names)
        self.assertEqual(rep['code'], 200, rep)

    def test_whitelist_query(self):
        rep = rc.get_chatroom().get_whitelist().query()
        self.assertEqual(rep['code'], 200, rep)

    def test_keepalive_add(self):
        room_id = '10001'
        rep = rc.get_chatroom().get_keepalive().add(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_keepalive_remove(self):
        room_id = '10001'
        rep = rc.get_chatroom().get_keepalive().remove(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_keepalive_query(self):
        rep = rc.get_chatroom().get_keepalive().query()
        self.assertEqual(rep['code'], 200, rep)
