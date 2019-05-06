import unittest

from rongcloud.rongcloud import RongCloud
from rongcloud.sensitive import Sensitive

rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz')


class SensitiveTestCase(unittest.TestCase):
    def test_add(self):
        keyword = '我们'
        replace = '你们'
        rep = rc.get_sensitive().add(keyword, replace)
        self.assertEqual(rep['code'], 200, rep)

    def test_remove(self):
        keyword = ['我们', '他们']
        rep = rc.get_sensitive().remove(keyword)
        self.assertEqual(rep['code'], 200, rep)

    def test_query(self):
        type = Sensitive.SENSITIVE_ALL
        rep = rc.get_sensitive().query(type)
        self.assertEqual(rep['code'], 200, rep)


if __name__ == '__main__':
    unittest.main()
