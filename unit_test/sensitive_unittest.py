import unittest

from rongcloud.rongcloud import RongCloud
from rongcloud.sensitive import Sensitive

rc = RongCloud('8luwapkvucoil', 'y0icysjl4h3LWz')


class SensitiveTestCase(unittest.TestCase):
    def test_add(self):
        word = '我们'
        replace_word = '你们'
        rep = rc.get_sensitive().add(word, replace_word)
        self.assertEqual(rep['code'], 200, rep)

    def test_remove(self):
        words = ['我们', '他们']
        rep = rc.get_sensitive().remove(words)
        self.assertEqual(rep['code'], 200, rep)
        words = '我们'
        rep = rc.get_sensitive().remove(words)
        self.assertEqual(rep['code'], 200, rep)

    def test_query(self):
        word_type = 2
        rep = rc.get_sensitive().query(word_type)
        self.assertEqual(rep['code'], 200, rep)


if __name__ == '__main__':
    unittest.main()
