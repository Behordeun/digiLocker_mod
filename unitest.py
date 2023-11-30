import unittest
from flask import Flask
from main import app

class YourAppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to your app', response.data)

    def test_login_route(self):
        response = self.app.get('/api/login/metamask')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration', response.data)

    def test_dashboard_route(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        
    def test_registration_route(self):
        response = self.app.get('/api/user/registration')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Registration', response.data)
        
    def test_upload_route(self):
        response = self.app.get('/post/api/upload/doc')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Document Upload', response.data)
        
    def test_user_access_key_route(self):
        response = self.app.get('/api/user/accesskey')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Key', response.data)
        
    def test_registration_route(self):
        response = self.app.get('/registration')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration', response.data)
        
    def test_masterkey_verification_route(self):
        response = self.app.get('/api/get/verify/master/code')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration', response.data)

    # Add more test cases for other routes and functionalities

if __name__ == '__main__':
    unittest.main()
    