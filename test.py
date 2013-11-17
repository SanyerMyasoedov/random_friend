import os
from friends import app
from unittest import TestCase, main

# todo: improve tests
"""
You can get TEST_TOKEN from
https://developers.facebook.com/tools/explorer/?method=GET
"""

class AppTestCase(TestCase):

    def setUp(self):
        self.client = app.test_client(self)

    def testSignInn(self):
        response = self.client.get('/')
        self.assertIn('Sign in', response.data)

    def testBadToken(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['facebook_token'] = ('myuserid', '')
                sess['logged_in'] = True
        response = self.client.get('/')
        self.assertIn('something wrong with your auth token', response.data)

    def testGetFromApi(self):
        if "TEST_TOKEN" not in os.environ:
            return True
        with self.client as c:
            with c.session_transaction() as sess:
                sess['facebook_token'] = (os.environ['TEST_TOKEN'], '')
                sess['logged_in'] = True
        response = self.client.get('/')
        self.assertIn('Logout', response.data) # weird check


if __name__ == '__main__':
    main()