from unittest.mock import patch
# Be careful: we use a different parent classes BaseTest and UnitBaseTest for integration/system and unit tests
from tests.base_test import BaseTest
from models.user import UserModel


class UserTestIntegration(BaseTest):
    """
    We test the functions from models.user witch require connection to DB or mocking.
    1) Create an UserModel instance
    2) Check that the instance doesn't exist in DB
    3) Save the instance in DB
    4) Check that the instance does exist in DB (by username, by id)
    5) Check that the methods return the correct UserModel objects (by username, by id)
    """
    def test_db_func(self):
        with self.app_context():
            user = UserModel('iliuza', '12345')

            self.assertIsNone(UserModel.find_by_username('iliuza'))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('iliuza'))
            self.assertIsNotNone(UserModel.find_by_id(1))

            self.assertEqual(UserModel.find_by_id(1), user)
            self.assertEqual(UserModel.find_by_username('iliuza'), user)

    # We use patch from unittest.mock to test that the method save_to_db() evokes db.session.add and commit
    def test_save_to_db(self):
        with self.app_context():
            with patch('models.user.db.session.add') as mocked_add:
                with patch('models.user.db.session.commit') as mocked_commit:
                    UserModel('iliuza', '12345').save_to_db()

                    mocked_add.assert_called()
                    mocked_commit.assert_called()

    # Check that the methods find_by_id and find_by_username return the UserModel objects
    def test_find_username(self):
        with self.app_context():
            UserModel('iliuza', '12345').save_to_db()

            self.assertIsInstance(UserModel.find_by_id(1), UserModel)
            self.assertIsInstance(UserModel.find_by_username('iliuza'), UserModel)



