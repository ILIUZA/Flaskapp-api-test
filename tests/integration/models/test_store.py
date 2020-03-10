from unittest.mock import patch
from models.item import ItemModel
from models.store import StoreModel
# Be careful: we use a different parent classes BaseTest and UnitBaseTest for integration/system and unit tests
from tests.base_test import BaseTest


class StoreTestIntegration(BaseTest):
    def test_json(self):
        with self.app_context():
            store = StoreModel('coat_store')
            store.save_to_db()
            ItemModel('coat', 200.36, 1).save_to_db()

            expected = {'id': 1,'name': 'coat_store', 'items': [{'name': 'coat', 'price': 200.36}]}

            self.assertDictEqual(expected, store.json())
            self.assertIsNotNone(store.items)

    def test_json_without_items(self):
        with self.app_context():
            store = StoreModel('coat_store')
            store.save_to_db()

            expected = {'id': 1, 'name': 'coat_store', 'items': []}

            self.assertDictEqual(expected, store.json())
            self.assertIsNotNone(store.items)

    """
    We test the functions from models.store witch require connection to DB or mocking.
    1) Create a StoreModel instance
    2) Check that the instance doesn't exist in DB
    3) Save the instance in DB
    4) Check that the instance does exist in DB
    5) Delete the instance from DB
    6) Check that the instance doesn't exist in DB anymore
    """
    def test_db_func(self):
        with self.app_context():
            store = StoreModel('coat_store')
            self.assertIsNone(store.find_by_name('coat_store'))
            store.save_to_db()
            self.assertIsNotNone(store.find_by_name('coat_store'))
            store.delete_from_db()
            self.assertIsNone(store.find_by_name('coat_store'))

    def test_store_items(self):
        with self.app_context():
            store = StoreModel('coat_store')
            store.save_to_db()
            item = ItemModel('coat', 200.36, 1)
            item.save_to_db()

            self.assertListEqual(store.items.all(), [item])

    def test_find_by_name(self):
        with self.app_context():
            StoreModel('test_store').save_to_db()

            self.assertIsInstance(StoreModel.find_by_name('test_store'), StoreModel)

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('coat_store')

            store.save_to_db()
            ItemModel('coat', 200.36, 1).save_to_db()

            self.assertIsNotNone(store.items)
            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'coat')

    def test_save_to_db(self):
        with self.app_context():
            with patch('models.store.db.session.add') as mocked_add:
                with patch('models.store.db.session.commit') as mocked_commit:
                    StoreModel('test_store').save_to_db()

                    mocked_add.assert_called()
                    mocked_commit.assert_called()

    def test_delete_from_db(self):
        with self.app_context():
            with patch('models.store.db.session.delete') as mocked_delete:
                with patch('models.store.db.session.commit') as mocked_commit:
                    StoreModel('test_store').save_to_db()
                    StoreModel('test_store').delete_from_db()

                    mocked_delete.assert_called()
                    mocked_commit.assert_called()

