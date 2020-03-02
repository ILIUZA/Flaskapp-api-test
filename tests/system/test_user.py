from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserSystemTest(BaseTest):
    def test_registration(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'iliuza', 'password': '12345'})
                expected = {"message": "User created successfully."}

                self.assertIsNotNone(UserModel.find_by_username('iliuza'))
                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 201)

    def test_registration_without_password(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'iliuza'})
                expected = {"message": {'password': 'This field cannot be blank.'}}

                self.assertIsNone(UserModel.find_by_username('iliuza'))
                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 400)

    def test_registration_without_username(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'password': '12345'})
                expected = {"message": {'username': 'This field cannot be blank.'}}

                self.assertIsNone(UserModel.find_by_username('iliuza'))
                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 400)

    def test_login_and_auth(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'iliuza', 'password': '12345'})
                response = client.post('/auth',
                                       data=json.dumps({'username': 'iliuza', 'password': '12345'}),
                                       headers={'Content-type': 'application/json'})

                self.assertIn('access_token', json.loads(response.data).keys())

    def test_registration_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'iliuza', 'password': '12345'})
                response = client.post('/register', data={'username': 'iliuza', 'password': '12345'})

                expected = {"message": "A user with that username already exists"}

                self.assertEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 400)
