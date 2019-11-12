import unittest

from rongcloud.rongcloud import RongCloud

rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz')


class GroupTestCase(unittest.TestCase):
    def test_sync(self):
        user_id = 'AAA'
        group_id_list = [('10001', 'TestGroup1'), ('10002', 'TestGroup2'), ('10003', 'TestGroup3')]
        rep = rc.get_group().sync(user_id, group_id_list)
        self.assertEqual(rep['code'], 200, rep)

    def test_create(self):
        user_ids = 'user_1'
        group_id = 'group_test'
        group_name = 'TestGroup'
        rep = rc.get_group().create(user_ids, group_id, group_name)
        self.assertEqual(rep['code'], 200, rep)
        user_ids = ['user_2', 'user_3']
        group_id = 'group_test'
        group_name = 'TestGroup'
        rep = rc.get_group().create(user_ids, group_id, group_name)
        self.assertEqual(rep['code'], 200, rep)

    def test_join(self):
        user_id = '1'
        group_id = '123'
        group_name = 'TestGroup'
        rep = rc.get_group().join(user_id, group_id, group_name)
        self.assertEqual(rep['code'], 200, rep)
        user_ids = ['1', '2']
        group_id = '123'
        group_name = 'TestGroup'
        rep = rc.get_group().join(user_ids, group_id, group_name)
        self.assertEqual(rep['code'], 200, rep)

    def test_quit(self):
        user_id = '1'
        group_id = '123'
        rep = rc.get_group().quit(user_id, group_id)
        self.assertEqual(rep['code'], 200, rep)
        user_ids = ['1', '2']
        group_id = '123'
        rep = rc.get_group().quit(user_ids, group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_dismiss(self):
        user_id = '1'
        group_id = '123'
        rep = rc.get_group().dismiss(user_id, group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_update(self):
        group_id = '123'
        group_name = 'new'
        rep = rc.get_group().update(group_id, group_name)
        self.assertEqual(rep['code'], 200, rep)

    def test_query(self):
        group_id = '123'
        rep = rc.get_group().query(group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_query(self):
        group_id = '123'
        rep = rc.get_group().get_user().query(group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_gag_add(self):
        # 创建群组 '16'，并加入 '2582', '2583'
        user_ids = ['2582', '2583']
        group_id = '16'
        group_name = 'TestGroup'
        rep = rc.get_group().create(user_ids, group_id, group_name)
        self.assertEqual(rep['code'], 200, rep)
        # 禁言 '2582'
        user_id = '2582'
        minute = 10
        rep = rc.get_group().get_user().get_gag().add(user_id, group_id, minute)
        self.assertEqual(rep['code'], 200, rep)
        # 禁言 '2582', '2583'
        user_ids = ['2582', '2583']
        group_id = '16'
        minute = 10
        rep = rc.get_group().get_user().get_gag().add(user_ids, group_id, minute)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_gag_remove(self):
        user_id = '2582'
        group_id = '16'
        rep = rc.get_group().get_user().get_gag().remove(user_id, group_id)
        self.assertEqual(rep['code'], 200, rep)
        user_ids = ['2582', '2583']
        group_id = '16'
        rep = rc.get_group().get_user().get_gag().remove(user_ids, group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_gag_query(self):
        group_id = '16'
        rep = rc.get_group().get_user().get_gag().query(group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_ban_add(self):
        group_id = '16'
        rep = rc.get_group().get_user().get_ban().add(group_id)
        self.assertEqual(rep['code'], 200, rep)
        group_ids = ['16', '17']
        rep = rc.get_group().get_user().get_ban().add(group_ids)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_ban_remove(self):
        group_id = '16'
        rep = rc.get_group().get_user().get_ban().remove(group_id)
        self.assertEqual(rep['code'], 200, rep)
        group_ids = ['16', '17']
        rep = rc.get_group().get_user().get_ban().remove(group_ids)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_ban_query(self):
        group_id = '16'
        rep = rc.get_group().get_user().get_ban().query(group_id)
        self.assertEqual(rep['code'], 200, rep)
        group_ids = ['16', '17']
        rep = rc.get_group().get_user().get_ban().query(group_ids)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_ban_whitelist_add(self):
        user_id = '2582'
        group_id = '16'
        rep = rc.get_group().get_user().get_ban().get_whitelist().add(user_id, group_id)
        self.assertEqual(rep['code'], 200, rep)
        user_ids = ['2582', '2583']
        rep = rc.get_group().get_user().get_ban().get_whitelist().add(user_ids, group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_ban_whitelist_remove(self):
        user_id = '2582'
        group_id = '16'
        rep = rc.get_group().get_user().get_ban().get_whitelist().remove(user_id, group_id)
        self.assertEqual(rep['code'], 200, rep)
        user_ids = ['2582', '2583']
        rep = rc.get_group().get_user().get_ban().get_whitelist().remove(user_ids, group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_user_ban_whitelist_query(self):
        group_id = '16'
        rep = rc.get_group().get_user().get_ban().get_whitelist().query(group_id)
        self.assertEqual(rep['code'], 200, rep)


if __name__ == '__main__':
    unittest.main()
