#! /usr/bin/env python
# coding=utf-8
import os
import json
import unittest
import logging
from rong import ApiClient
logging.basicConfig(level=logging.INFO)


class ApiTest(unittest.TestCase):
    def setUp(self):
        app_key = os.environ['APP_KEY']
        app_secret = os.environ['APP_SECRET']
        self.client = ApiClient(app_key, app_secret)

    def log(self, title, message):
        logging.info('{0}: {1}'.format(title, message))

    def test_rollbackGagChatroomUser(self):
        r = self.client.rollbackGagChatroomUser(**{'chatroomId': 'chatroomid1',
                                                   'userId': 'userid1'})
        self.log('rollbackGagChatroomUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_publishGroupMessage(self):
        r = self.client.publishGroupMessage(
            **{'pushContent': 'userid1',
               'content': '{"content":"hello","extra":"helloExtra"}',
               'pushData': 'userid1',
               'fromUserId': 'userid1',
               'toGroupId': 'groupid1',
               'objectName': 'RC:TxtMsg'})
        self.log('publishGroupMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_historyMessage(self):
        r = self.client.historyMessage(**{'date': '20160729'})
        self.log('historyMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('url' in r.result)
        self.assertTrue('date' in r.result)
        self.assertEqual(str(r.result['date']), '20160729')
        self.assertEqual(str(r.result['code']), '200')

    def test_publishTemplateMessage(self):
        r = self.client.publishTemplateMessage(
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
        self.log('publishTemplateMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_addWordFilter(self):
        r = self.client.addWordFilter(**{'word': 'word1'})
        self.log('addWordFilter', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_rollbackBlockChatroomUser(self):
        r = self.client.rollbackBlockChatroomUser(**{'chatroomId':
                                                     'chatroomid1',
                                                     'userId': 'userid1'})
        self.log('rollbackBlockChatroomUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_groupUserQuery(self):
        r = self.client.groupUserQuery(**{'groupId': 'groupid2'})
        self.log('groupUserQuery', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('users' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_groupjoin(self):
        r = self.client.groupjoin(**{'userId': 'userid1',
                                     'groupName': 'groupname',
                                     'groupId': 'groupid1'})
        self.log('groupjoin', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_unBlockUser(self):
        r = self.client.unBlockUser(**{'userId': 'userid1'})
        self.log('unBlockUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_addUserBlacklist(self):
        r = self.client.addUserBlacklist(**{'userId': 'userid1',
                                            'blackUserId': 'userid1'})
        self.log('addUserBlacklist', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_chatroomQuery(self):
        r = self.client.chatroomQuery(**{'chatroomId': 'chatroomid2'})
        self.log('chatroomQuery', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('chatRooms' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_queryBlacklistUser(self):
        r = self.client.queryBlacklistUser(**{'userId': 'userid1'})
        self.log('queryBlacklistUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('users' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_addGagChatroomUser(self):
        r = self.client.addGagChatroomUser(**{'chatroomId': 'chatroomid1',
                                              'userId': 'userid1',
                                              'minute': '43200'})
        self.log('addGagChatroomUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_groupSync(self):
        r = self.client.groupSync(**{'userId': 'userid1',
                                     'groups': [('groupid1', 'groupname2')]})
        self.log('groupSync', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_broadcastMessage(self):
        r = self.client.broadcastMessage(
            **{'fromUserId': 'userid1',
               'pushContent': 'userid1',
               'content': '{"content":"hello","extra":"helloExtra"}',
               'objectName': 'RC:TxtMsg',
               'pushData': 'userid1'})
        self.log('broadcastMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_chatroomCreate(self):
        r = self.client.chatroomCreate(**{'chatrooms': [('id9', 'chatroom9')]})
        self.log('chatroomCreate', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_getToken(self):
        r = self.client.getToken(**{'portraitUri':
                                    'http://www.rongcloud.cn/images/logo.png',
                                    'name': 'username',
                                    'userId': 'userid1'})
        self.log('getToken', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('userId' in r.result)
        self.assertTrue('token' in r.result)
        self.assertEqual(str(r.result['userId']), 'userid1')
        self.assertEqual(str(r.result['code']), '200')

    def test_chatroomUserQuery(self):
        r = self.client.chatroomUserQuery(**{'chatroomId': 'chatroomid4',
                                             'count': '2',
                                             'order': '1'})
        self.log('chatroomUserQuery', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('total' in r.result)
        self.assertTrue('users' in r.result)
        self.assertEqual(str(r.result['code']), '23410')

    def test_chatroomDestroy(self):
        r = self.client.chatroomDestroy(**{'chatroomId': 'chatroomid1'})
        self.log('chatroomDestroy', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_systemPublishTemplateMessage(self):
        r = self.client.systemPublishTemplateMessage(
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
        print(r)
        self.log('systemPublishTemplateMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_refreshUser(self):
        r = self.client.refreshUser(
            **{'portraitUri': 'http://www.rongcloud.cn/images/logo.png',
               'name': 'username',
               'userId': 'userid1'})
        self.log('refreshUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_listGagGroupUser(self):
        r = self.client.listGagGroupUser(**{'groupId': 'groupid1'})
        self.log('listGagGroupUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('users' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_HistoryMessageDelete(self):
        r = self.client.HistoryMessageDelete(**{'date': '2016010101'})
        self.log('HistoryMessageDelete', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('errorMessage' in r.result)
        self.assertEqual(str(r.result['code']), '1002')
        self.assertEqual(str(r.result['errorMessage']), 'data is not exist.')

    def test_groupCreate(self):
        r = self.client.groupCreate(**{'userId': 'userid1',
                                       'groupName': 'groupname',
                                       'groupId': 'groupid1'})
        self.log('groupCreate', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_addGagGroupUser(self):
        r = self.client.addGagGroupUser(**{'userId': 'userid1',
                                           'minute': '43200',
                                           'groupId': 'groupid1'})
        self.log('addGagGroupUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_resumeDistributionChatroomMessage(self):
        r = self.client.resumeDistributionChatroomMessage(
            **{'chatroomId': 'chatroomid1'})
        self.log('resumeDistributionChatroomMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_publishMessage(self):
        r = self.client.publishMessage(
            **{'pushContent': 'userid1',
               'toUserId': 'userid1',
               'content': '{"content":"hello","extra":"helloExtra"}',
               'pushData': 'userid1',
               'fromUserId': 'userid1',
               'objectName': 'RC:TxtMsg'})
        self.log('publishMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_addChatroomBlockUser(self):
        r = self.client.addChatroomBlockUser(**{'chatroomId': 'chatroomid1',
                                                'userId': 'userid1',
                                                'minute': '43200'})
        self.log('addChatroomBlockUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_listBlockChatroomUser(self):
        r = self.client.listBlockChatroomUser(**{'chatroomId': 'chatroomid1'})
        self.log('listBlockChatroomUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('users' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_queryBlockUser(self):
        r = self.client.queryBlockUser(**{})
        self.log('queryBlockUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('users' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_groupRefresh(self):
        r = self.client.groupRefresh(**{'groupName': 'groupname',
                                        'groupId': 'groupid1'})
        self.log('groupRefresh', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_checkOnlineUser(self):
        r = self.client.checkOnlineUser(**{'userId': 'userid1'})
        self.log('checkOnlineUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('status' in r.result)
        self.assertEqual(str(r.result['code']), '200')
        self.assertEqual(str(r.result['status']), '0')

    def test_groupDismiss(self):
        r = self.client.groupDismiss(**{'userId': 'userid1',
                                        'groupId': 'groupid1'})
        self.log('groupDismiss', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_systemPublishMessage(self):
        r = self.client.systemPublishMessage(
            **{'isPersisted': '0',
               'pushContent': 'thisisapush',
               'toUserId': 'touserid1',
               'isCounted': '0',
               'content': '{"content":"c#hello"}',
               'pushData': '{"pushData":"hello"}',
               'fromUserId': 'fromuserid1',
               'objectName': 'RC:TxtMsg'})
        self.log('systemPublishMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_stopDistributionChatroomMessage(self):
        r = self.client.stopDistributionChatroomMessage(
            **{'chatroomId': 'chatroomid1'})
        self.log('stopDistributionChatroomMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_groupQuit(self):
        r = self.client.groupQuit(**{'userId': 'userid1',
                                     'groupId': 'groupid1'})
        self.log('groupQuit', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_removeBlacklistUser(self):
        r = self.client.removeBlacklistUser(**{'userId': 'userid1',
                                               'blackUserId': 'userid1'})
        self.log('removeBlacklistUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_listGagChatroomUser(self):
        r = self.client.listGagChatroomUser(**{'chatroomId': 'chatroomid1'})
        self.log('listGagChatroomUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('users' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_rooBackGagGroupUser(self):
        r = self.client.rooBackGagGroupUser(**{'userId': 'userid1',
                                               'groupId': 'groupid1'})
        self.log('rooBackGagGroupUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_publishDiscussionMessage(self):
        r = self.client.publishDiscussionMessage(
            **{'pushContent': 'userid1',
               'content': '{"content":"hello","extra":"helloExtra"}',
               'pushData': 'userid1',
               'fromUserId': 'userid1',
               'toDiscussionId': 'discussionid1',
               'objectName': 'RC:TxtMsg'})
        self.log('publishDiscussionMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_chatroomJoin(self):
        r = self.client.chatroomJoin(**{'chatroomId': 'chatroomid4',
                                        'userId': 'userid3'})
        self.log('chatroomJoin', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '1002')
        self.assertEqual(
            str(r.result['errorMessage']), 'chatroomId is not exist.')

    def test_listWordfilter(self):
        r = self.client.listWordfilter(**{})
        self.log('listWordfilter', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertTrue('words' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_publishChatroomMessage(self):
        r = self.client.publishChatroomMessage(
            **{'fromUserId': 'userid1',
               'toChatroomId': 'groupid1',
               'content': '{"content":"hello","extra":"helloExtra"}',
               'objectName': 'RC:TxtMsg'})
        self.log('publishChatroomMessage', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_blockUser(self):
        r = self.client.blockUser(**{'userId': 'userid1', 'minute': 1})
        self.log('blockUser', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')

    def test_deleteWordfilter(self):
        r = self.client.deleteWordfilter(**{'word': 'word1'})
        self.log('deleteWordfilter', r)
        #self.assertEqual(r.status, 200)
        self.assertTrue('code' in r.result)
        self.assertEqual(str(r.result['code']), '200')


if __name__ == "__main__":
    unittest.main()
