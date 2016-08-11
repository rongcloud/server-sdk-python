#! /usr/bin/env python
# coding=utf-8

import os
import json
import unittest
import logging

from rong import ApiClient

app_key = os.environ.get('APP_KEY')
app_secret = os.environ.get('APP_SECRET')

logging.basicConfig(level=logging.INFO)

client = ApiClient(app_key, app_secret)


class ApiTest(unittest.TestCase):
    def test_token_get(self):
        result = client.user_get_token(
            'test-userid1',
            'test-name1',
            'http://www.rongcloud.cn/images/logo.png')

        result2 = client.user_get_token(
            'test-userid2',
            'test-name2',
            'http://www.rongcloud.cn/images/logo.png')

        self.assertEqual(result[u'code'], 200)
        self.assertEqual(result2[u'code'], 200)
        self.assertEqual(result[u'userId'], 'test-userid1')
        self.assertEqual(result2[u'userId'], 'test-userid2')

        self.assertTrue(u"token" in result)

    def test_user_refresh(self):
        result = client.user_refresh(
            'test-userid2',
            'test-name2',
            'http://www.rongcloud.cn/images/logo_new.png'
        )

        self.assertEqual(result[u'code'], 200)

    def test_user_check_online(self):
        result = client.user_check_online(
            'test-userid2'
        )

        self.assertEqual(result[u'code'], 200)
        self.assertTrue(u"status" in result)

    def test_user_block(self):
        result = client.user_block('test-userid1', 10)
        self.assertEqual(result[u'code'], 200)

        block_user_list = client.user_block_query()
        self.assertEqual(block_user_list[u'code'], 200)
        self.assertTrue('test-userid1' in [r.get("userId") for r in block_user_list.get("users")])

    def test_user_unblock(self):
        result = client.user_unblock('test-userid2')
        self.assertEqual(result[u'code'], 200)

        block_user_list = client.user_block_query()
        self.assertEqual(block_user_list[u'code'], 200)
        self.assertTrue('test-userid2' not in [r.get("userId") for r in block_user_list.get("users")], "检查解封是否成功")

    def test_user_blocklist_add(self):
        result = client.user_blocklist_add('test-userid1', ['test-userid2', 'test-userid3'])
        self.assertEqual(result[u'code'], 200)

    def test_user_blocklist_query(self):
        result = client.user_blocklist_query('test-userid1')
        self.assertTrue('test-userid2' in result.get('users'))
        self.assertTrue('test-userid3' in result.get('users'))

    def test_user_blocklist_remove(self):
        client.user_blocklist_remove('test-userid1', ['test-userid2', 'test-userid3'])
        result = client.user_blocklist_query('test-userid1')
        self.assertTrue('test-userid2' not in result.get('users'))
        self.assertTrue('test-userid3' not in result.get('users'))

    def test_message_publish(self):
        result = client.message_publish(
            from_user_id='test-userid1',
            to_user_id='test-userid2',
            object_name='RC:TxtMsg',
            content=json.dumps({"content":"hello"}),
            push_content='thisisapush',
            push_data='aa')

        self.assertEqual(result[u'code'], 200)

    def test_message_system_publish(self):
        result = client.message_system_publish(
            from_user_id='test-userid1',
            to_user_id='test-userid2',
            object_name='RC:TxtMsg',
            content=json.dumps({"content":"hello"}),
            push_content='thisisapush',
            push_data='aa')

        self.assertEqual(result[u'code'], 200)

    def test_group_create(self):
        result = client.group_create(
            user_id_list=["test-userid1", "test-userid2"],
            group_id="groupid1",
            group_name="groupname1"
        )

        self.assertEqual(result[u'code'], 200)

    def test_message_group_publish(self):
        result = client.message_group_publish(
            from_user_id='test-userid1',
            to_group_id="groupid1",
            object_name='RC:TxtMsg',
            content=json.dumps({"content":"hello"}),
            push_content='this is push content',
            push_data='this is pushdata'
        )
        self.assertEqual(result[u'code'], 200)

    def test_chatroom_create(self):
        result = client.chatroom_create(
            chatrooms={
                'tr001':'room1',
                'tr002':'room2'
            }
        )
        self.assertEqual(result[u'code'], 200)

    def test_message_chatroom_publish(self):
        result = client.message_chatroom_publish(
            from_user_id="test-userid1",
            to_chatroom_id="tr001",
            object_name="RC:TxtMsg",
            content=json.dumps({"content":"hello"})
        )
        self.assertEqual(result[u'code'], 200)

    def test_message_history(self):
        result = client.message_history(
            date=2014010101
        )
        self.assertEqual(result[u'code'], 200)
        self.assertTrue(u'url' in result)

    def test_group_sync(self):
        result = client.group_sync(
            user_id='test-userid1',
            groups={
                "groupid1":"groupname1"
            }
        )
        self.assertEqual(result[u'code'], 200)

    def test_group_join(self):
        result = client.group_join(
            user_id_list=['test-userid1', 'test-userid2'],
            group_id="groupid1",
            group_name="groupname1"
        )
        self.assertEqual(result[u'code'], 200)

    def test_group_quit(self):
        result = client.group_quit(
            user_id_list=['test-userid1', 'test-userid2'],
            group_id="groupid1"
        )
        self.assertEqual(result[u'code'], 200)

    def test_group_refresh(self):
        result = client.group_refresh(
            group_id="groupid1",
            group_name="groupname1"
        )
        self.assertEqual(result[u'code'], 200)

    def test_group_dismiss(self):
        result = client.group_dismiss(
            user_id='test-userid1',
            group_id="groupid1")
        self.assertEqual(result[u'code'], 200)

    def test_chatroom_query(self):
        result = client.chatroom_query(["tr001","tr002"])
        self.assertEqual(result[u'code'], 200)

    def test_chatroom_destroy(self):
        result = client.chatroom_destroy(
            chatroom_id_list=["tr001", "tr002"]
        )
        self.assertEqual(result[u'code'], 200)

#############################################################3
    def test_rollbackGagChatroomUser(self):
        r = client.rollbackGagChatroomUser(**{'chatroomId': 'chatroomid1',
                                                   'userId': 'userid1'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_publishTemplateMessage(self):
        r = client.publishTemplateMessage(
            **{"fromUserId": "userid1",
               "objectName": "RC:TxtMsg",
               "content": '{"content":"aa{c}{e}{d}","extra":"bb"}',
               "toUserId": ["2579", "2580"],
               "values": [{"{c}": "1",
                           "{d}": "2",
                           "{e}": "3"}, {"{c}": "4",
                                         "{d}": "5",
                                         "{e}": "6"}],
               "pushContent": ["push{c}", "push{c}"],
               "pushData": ["pushd", "pushd"]})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_addWordFilter(self):
        r = client.addWordFilter(**{'word': 'word1'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_rollbackBlockChatroomUser(self):
        r = client.rollbackBlockChatroomUser(**{'chatroomId':
                                                     'chatroomid1',
                                                     'userId': 'userid1'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_groupUserQuery(self):
        r = client.groupUserQuery(**{'groupId': 'groupid2'})
        self.assertTrue('code' in r)
        self.assertTrue('users' in r)
        self.assertEqual(str(r['code']), '200')

    def test_addGagChatroomUser(self):
        r = client.addGagChatroomUser(**{'chatroomId': 'chatroomid1',
                                              'userId': 'userid1',
                                              'minute': '43200'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_broadcastMessage(self):
        r = client.broadcastMessage(
            **{'fromUserId': 'userid1',
               'pushContent': 'userid1',
               'content': '{"content":"hello","extra":"helloExtra"}',
               'objectName': 'RC:TxtMsg',
               'pushData': 'userid1'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_systemPublishTemplateMessage(self):
        r = client.systemPublishTemplateMessage(
            **{"fromUserId": "23245",
               "objectName": "RC:TxtMsg",
               "content": "{\"content\":\"aa{c}{e}{d}\",\"extra\":\"bb\"}",
               "toUserId": ["2579", "2580"],
               "values": [{"{c}": "1",
                           "{d}": "2",
                           "{e}": "3"}, {"{c}": "4",
                                         "{d}": "5",
                                         "{e}": "6"}],
               "pushContent": ["push{c}", "push{c}"],
               "pushData": ["pushd", "pushd"]})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_listGagGroupUser(self):
        r = client.listGagGroupUser(**{'groupId': 'groupid1'})
        self.assertTrue('code' in r)
        self.assertTrue('users' in r)
        self.assertEqual(str(r['code']), '200')

    def test_HistoryMessageDelete(self):
        r = client.HistoryMessageDelete(**{'date': 2016081114})
        self.assertTrue('code' in r)
        self.assertTrue('errorMessage' in r)
        self.assertEqual(str(r['code']), '1002')
        self.assertEqual(str(r['errorMessage']), 'data is not exist.')

    def test_addGagGroupUser(self):
        r = client.addGagGroupUser(**{'userId': 'userid1',
                                           'minute': '43200',
                                           'groupId': 'groupid1'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_resumeDistributionChatroomMessage(self):
        r = client.resumeDistributionChatroomMessage(
            **{'chatroomId': 'chatroomid1'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_addChatroomBlockUser(self):
        r = client.addChatroomBlockUser(**{'chatroomId': 'chatroomid1',
                                                'userId': 'userid1',
                                                'minute': '43200'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_listBlockChatroomUser(self):
        r = client.listBlockChatroomUser(**{'chatroomId': 'chatroomid1'})
        self.assertTrue('code' in r)
        self.assertTrue('users' in r)
        self.assertEqual(str(r['code']), '200')

    def test_stopDistributionChatroomMessage(self):
        r = client.stopDistributionChatroomMessage(
            **{'chatroomId': 'chatroomid1'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_listGagChatroomUser(self):
        r = client.listGagChatroomUser(**{'chatroomId': 'chatroomid1'})
        self.assertTrue('code' in r)
        self.assertTrue('users' in r)
        self.assertEqual(str(r['code']), '200')

    def test_rooBackGagGroupUser(self):
        r = client.rooBackGagGroupUser(**{'userId': 'userid1',
                                               'groupId': 'groupid1'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_publishDiscussionMessage(self):
        r = client.publishDiscussionMessage(
            **{'pushContent': 'userid1',
               'content': '{"content":"hello","extra":"helloExtra"}',
               'pushData': 'userid1',
               'fromUserId': 'userid1',
               'toDiscussionId': 'discussionid1',
               'objectName': 'RC:TxtMsg'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_chatroomJoin(self):
        r = client.chatroomJoin(**{'chatroomId': 'tr001',
                                        'userId': 'userid3'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')

    def test_listWordfilter(self):
        r = client.listWordfilter(**{})
        self.assertTrue('code' in r)
        self.assertTrue('words' in r)
        self.assertEqual(str(r['code']), '200')

    def test_deleteWordfilter(self):
        r = client.deleteWordfilter(**{'word': 'word1'})
        self.assertTrue('code' in r)
        self.assertEqual(str(r['code']), '200')


if __name__ == "__main__":
    unittest.main()
