import unittest

from rongcloud.rongcloud import RongCloud

rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz')


class ChatroomTestCase(unittest.TestCase):
    def test_create(self):
        room_id = '10001'
        name = 'name1'
        rep = rc.get_chatroom().create(room_id, name)
        self.assertEqual(rep['code'], 200, rep)

    def test_destory(self):
        room_id = '10001'
        rep = rc.get_chatroom().destory(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_query(self):
        room_id = '10001'
        rep = rc.get_chatroom().query(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_is_exist(self):
        room_id = '10001'
        user_id = 'AAA'
        rep = rc.get_chatroom().is_exist(room_id, user_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_block_add(self):
        user_id_list = ['2583', '2582']
        room_id = '16'
        minute = 1
        rep = rc.get_chatroom().get_block().add(user_id_list, room_id, minute)
        self.assertEqual(rep['code'], 200, rep)

    def test_block_remove(self):
        user_id_list = ['2583', '2582']
        room_id = '16'
        rep = rc.get_chatroom().get_block().remove(user_id_list, room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_block_query(self):
        room_id = '16'
        rep = rc.get_chatroom().get_block().query(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_ban_add(self):
        user_id_list = ['2583', '2582']
        minute = 1
        rep = rc.get_chatroom().get_ban().add(user_id_list, minute)
        self.assertEqual(rep['code'], 200, rep)

    def test_ban_remove(self):
        user_id_list = ['2582']
        rep = rc.get_chatroom().get_ban().remove(user_id_list)
        self.assertEqual(rep['code'], 200, rep)

    def test_ban_query(self):
        rep = rc.get_chatroom().get_ban().query()
        self.assertEqual(rep['code'], 200, rep)

    def test_gag_add(self):
        user_id_list = ['2583', '2582']
        room_id = '16'
        minute = 1
        rep = rc.get_chatroom().get_gag().add(user_id_list, room_id, minute)
        self.assertEqual(rep['code'], 200, rep)

    def test_gag_remove(self):
        user_id_list = ['2583', '2582']
        room_id = '16'
        rep = rc.get_chatroom().get_gag().remove(user_id_list, room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_gag_query(self):
        room_id = '16'
        rep = rc.get_chatroom().get_gag().query(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_demotion_add(self):
        obj_name_list = ['RC:VcMsg', 'RC:ImgTextMsg', 'RC:ImgMsg']
        rep = rc.get_chatroom().get_demotion().add(obj_name_list)
        self.assertEqual(rep['code'], 200, rep)

    def test_demotion_remove(self):
        obj_name_list = ['RC:VcMsg', 'RC:ImgMsg']
        rep = rc.get_chatroom().get_demotion().remove(obj_name_list)
        self.assertEqual(rep['code'], 200, rep)

    def test_demotion_query(self):
        rep = rc.get_chatroom().get_demotion().query()
        self.assertEqual(rep['code'], 200, rep)

    def test_distribute_add(self):
        room_id = '16'
        rep = rc.get_chatroom().get_distribute().stop(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_distribute_remove(self):
        room_id = '16'
        rep = rc.get_chatroom().get_distribute().resume(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_keep_alive_add(self):
        room_id = '16'
        rep = rc.get_chatroom().get_keep_alive().add(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_keep_alive_remove(self):
        room_id = '16'
        rep = rc.get_chatroom().get_keep_alive().remove(room_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_keep_alive_query(self):
        rep = rc.get_chatroom().get_keep_alive().query()
        self.assertEqual(rep['code'], 200, rep)

    def test_message_while_list_add(self):
        obj_name_list = ['RC:VcMsg', 'RC:ImgTextMsg', 'RC:ImgMsg']
        rep = rc.get_chatroom().get_message_while_list().add(obj_name_list)
        self.assertEqual(rep['code'], 200, rep)

    def test_message_while_list_remove(self):
        obj_name_list = ['RC:VcMsg', 'RC:ImgTextMsg', 'RC:ImgMsg']
        rep = rc.get_chatroom().get_message_while_list().remove(obj_name_list)
        self.assertEqual(rep['code'], 200, rep)

    def test_message_while_list_query(self):
        rep = rc.get_chatroom().get_message_while_list().query()
        self.assertEqual(rep['code'], 200, rep)

    def test_user_while_list_add(self):
        room_id = '16'
        user_id_list = ['123', '456']
        rep = rc.get_chatroom().get_user_while_list().add(room_id, user_id_list)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_while_list_remove(self):
        room_id = '16'
        user_id_list = ['123', '456']
        rep = rc.get_chatroom().get_user_while_list().remove(room_id, user_id_list)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_while_list_query(self):
        room_id = '16'
        rep = rc.get_chatroom().get_user_while_list().query(room_id)
        self.assertEqual(rep['code'], 200, rep)

if __name__ == '__main__':
    unittest.main()
