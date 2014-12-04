#! /usr/bin/env python
# coding=utf-8

from test_helper import unittest
from test_helper import client


class ApiTest(unittest.TestCase):

    def test_token_get(self):
        client.user_get_token(
            'test-userid1',
            'test-name1',
            'http://www.baidu.com/img/bd_logo1.png'
        )

        result = client.user_get_token(
            'test-userid2',
            'test-name2',
            'http://www.baidu.com/img/bd_logo1.png'
        )

        self.assertEqual(result[u'code'], 200)
        self.assertEqual(type(result[u'token']), unicode)
        self.assertEqual(result[u'userId'], 'test-userid2')

    def test_message_publish(self):
        result = client.message_publish(
            'test-userid1', 'test-userid2', 'RC:TxtMsg', '{"content":"hello"}', 'this is push content', 'this is pushdata'
        )

        result2 = client.message_publish(
            'test-userid1', 'test-userid2', 'RC:TxtMsg', '{"content":"hello"}', None, None
        )

        self.assertEqual(result[u'code'], 200)
        self.assertEqual(result2[u'code'], 200)

    def test_message_system_publish(self):
        result = client.message_system_publish(
            'test-userid1', 'test-userid2', 'RC:TxtMsg', '{"content":"hello"}', 'this is push content', 'this is pushdata'
        )

        result2 = client.message_system_publish(
            'test-userid1', 'test-userid2', 'RC:TxtMsg', '{"content":"hello"}', None, None
        )

        self.assertEqual(result[u'code'], 200)
        self.assertEqual(result2[u'code'], 200)

    def test_message_system_publish(self):
        result = client.message_system_publish(
            'test-userid1', 'test-userid2', 'RC:TxtMsg', '{"content":"hello"}', 'this is push content', 'this is pushdata'
        )

        result2 = client.message_system_publish(
            'test-userid1', 'test-userid2', 'RC:TxtMsg', '{"content":"hello"}', None, None
        )

        self.assertEqual(result[u'code'], 200)
        self.assertEqual(result2[u'code'], 200)

    def test_group_create(self):
        result = client.group_create(["test-userid1","test-userid2"], "groupid1", "groupname1")
        result2 = client.group_create(["test-userid1","test-userid2"], "groupid2", "groupname2")
        result3 = client.group_create(["test-userid1","test-userid2"], "groupid2", "groupname2")

        self.assertEqual(result[u'code'], 200)
        self.assertEqual(result2[u'code'], 200)
        self.assertEqual(result3[u'code'], 200)

    def test_message_group_publish(self):
        result = client.message_group_publish(
            'test-userid1',
            "groupid1",
            'RC:TxtMsg',
            '{"content":"hello"}',
            'this is push content',
            'this is pushdata'
        )
        self.assertEqual(result[u'code'], 200)

    def test_group_sync(self):
        result = client.group_sync(
            'test-userid1',{
                "groupid1":"groupname1",
                "groupid2":"groupname2",
                "groupid3":"groupname3",
            }
        )
        self.assertEqual(result[u'code'], 200)

    def test_group_join(self):
        result = client.group_join(
            ['test-userid1','test-userid2','test-userid3','test-userid4'],
            "groupid1",
            "groupname1"
        )
        self.assertEqual(result[u'code'], 200)

    def test_group_dismiss(self):
        result = client.group_dismiss('test-userid1', "groupid1")
        self.assertEqual(result[u'code'], 200)

    def test_chatroom_create(self):
        result = client.chatroom_create({'tr001':'room1','tr002':'room2'})
        self.assertEqual(result[u'code'], 200)

    def test_chatroom_query(self):
        result = client.chatroom_query(["tr001","tr002"])
        print result
        result = client.chatroom_query(None)

        print result
        self.assertEqual(result[u'code'], 200)



if __name__ == "__main__":
    unittest.main()