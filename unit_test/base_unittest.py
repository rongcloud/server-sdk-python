import unittest

from rongcloud.rongcloud import RongCloud


class BaseTestCase(unittest.TestCase):
    def test_second_url(self):
        rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz', 'http://wrong-url.com;http://api2-cn.ronghub.com')
        rep = rc.get_user().get_block().query()
        if rep['code'] != 200:
            rep = rc.get_user().get_block().query()
        self.assertEqual(rep['code'], 200, rep)


if __name__ == '__main__':
    unittest.main()
