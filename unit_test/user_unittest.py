import unittest

from rongcloud.rongcloud import RongCloud

rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz')


class UserTestCase(unittest.TestCase):
    def test_register(self):
        user_id = 'AAA'
        user_name = '忘情水'
        portrait = 'https://www.baidu.com/img/bd_logo1.png?where=super'
        rep = rc.get_user().register(user_id, user_name, portrait)
        self.assertEqual(rep['code'], 200, rep)

    def test_update(self):
        user_id = 'AAA'
        user_name = '青花瓷'
        portrait = 'https://box.bdimg.com/static/fisp_static/common/img/searchbox/logo_news_276_88_1f9876a.png'
        rep = rc.get_user().update(user_id, user_name, portrait)
        self.assertEqual(rep['code'], 200, rep)

    def test_blacklist_add(self):
        user_id = 'AAA'
        target = ['BBB', 'CCC']
        rep = rc.get_user().get_blacklist().add(user_id, target)
        self.assertEqual(rep['code'], 200, rep)

    def test_blacklist_remove(self):
        user_id = 'AAA'
        target = ['BBB', 'CCC']
        rep = rc.get_user().get_blacklist().remove(user_id, target)
        self.assertEqual(rep['code'], 200, rep)

    def test_blacklist_query(self):
        user_id = 'AAA'
        rep = rc.get_user().get_blacklist().query(user_id)
        self.assertEqual(rep['code'], 200, rep)

    def test_block(self):
        target = ['AAA', 'BBB']
        rep = rc.get_user().get_block().add(target, 300)
        self.assertEqual(rep['code'], 200, rep)

    def test_block_remove(self):
        target = 'AAA'
        # target = ['AAA', 'BBB']
        rep = rc.get_user().get_block().remove(target)
        self.assertEqual(rep['code'], 200, rep)

    def test_block_query(self):
        rep = rc.get_user().get_block().query()
        self.assertEqual(rep['code'], 200, rep)

    def test_tag_set(self):
        user_id = '31232'
        tags = ['bj', '男']
        rep = rc.get_user().get_tag().set(user_id, tags)
        self.assertEqual(rep['code'], 200, rep)

    def test_tag_set_batch(self):
        user_id = ['id1', 'id2']
        tags = ['bj', '男']
        rep = rc.get_user().get_tag().set(user_id, tags)
        self.assertEqual(rep['code'], 200, rep)

    def test_tag_get(self):
        user_ids = ['id1', 'id2']
        rep = rc.get_user().get_tag().get(user_ids)
        self.assertEqual(rep['code'], 200, rep)


if __name__ == '__main__':
    unittest.main()
