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
        user_id_list = ['1', '2']
        group_id = '123'
        group_name = 'TestGroup'
        rep = rc.get_group().create(user_id_list, group_id, group_name)
        self.assertEqual(rep['code'], 200, rep)

    def test_query(self):
        group_id = '123'
        rep = rc.get_group().query(group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_update(self):
        group_id = '123'
        group_name = 'new'
        rep = rc.get_group().update(group_id, group_name)
        self.assertEqual(rep['code'], 200, rep)

    def test_join(self):
        user_id_list = ['1', '2']
        group_id = '123'
        group_name = 'TestGroup'
        rep = rc.get_group().join(user_id_list, group_id, group_name)
        self.assertEqual(rep['code'], 200, rep)

    def test_quit(self):
        user_id_list = ['1', '2']
        group_id = '123'
        rep = rc.get_group().quit(user_id_list, group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_dismiss(self):
        user_id = '1'
        group_id = '123'
        rep = rc.get_group().dismiss(user_id, group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_gag_add(self):
        user_id_list = ['2582', '2583']
        group_id = '16'
        minute = 1
        rep = rc.get_group().get_gag().add(user_id_list, group_id, minute)
        self.assertEqual(rep['code'], 200, rep)

    def test_gag_remove(self):
        user_id_list = ['2582', '2583']
        group_id = '16'
        rep = rc.get_group().get_gag().remove(user_id_list, group_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_gag_query(self):
        group_id = '16'
        rep = rc.get_group().get_gag().query(group_id)
        self.assertEqual(rep['code'], 200, rep)


if __name__ == '__main__':
    unittest.main()
