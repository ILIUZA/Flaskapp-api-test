from unittest.mock import patch
from models.item import ItemModel
from models.store import StoreModel
# Be careful: we use a different parent classes BaseTest and UnitBaseTest for integration/system and unit tests
from tests.base_test import BaseTest


# To save DB integrity we need to create a store in DB and an item
# although SQLite lets us not do it without errors

class ItemTest(BaseTest):
    """
    We test the functions from models.item witch require connection to DB or mocking.
    1) Create a StoreModel and an ItemModel instances
    2) Check that the instance doesn't exist in DB
    3) Save the instance in DB
    4) Check that the instance does exist in DB
    5) Delete the instance from DB
    6) Check that the instance doesn't exist in DB anymore
    """
    def test_crud(self):
        with self.app_context():
            StoreModel('coat_store').save_to_db()
            item = ItemModel('coat', 200.99, 1)

            self.assertIsNone(ItemModel.find_by_name('coat'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('coat'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('coat'))

    # We test the relationship: store = db.relationship('StoreModel')
    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('coat_store')
            store2 = StoreModel('coat_store2')
            item = ItemModel('coat', 200.33, 2)

            store.save_to_db()
            store2.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, 'coat_store2')
            self.assertIsNotNone(item.store)

    # We test that find_by_name return the correct ItemModel object
    def test_find_by_name(self):
        with self.app_context():
            StoreModel('coat_store').save_to_db()
            ItemModel('coat', 200.33, 1).save_to_db()
            self.assertIsInstance(ItemModel.find_by_name('coat'), ItemModel)

    # We use patch from unittest.mock to test that save_to_db calls db.session.add and commit
    def test_save_to_db(self):
        with self.app_context():
            with patch('models.item.db.session.add') as mocked_add:
                with patch('models.item.db.session.commit') as mocked_commit:
                    StoreModel('coat_store').save_to_db()
                    ItemModel('coat', 200.33, 1).save_to_db()

                    mocked_add.assert_called()
                    mocked_commit.assert_called()

    # We use patch from unittest.mock to test that delete_from_db calls db.session.delete and commit
    def test_delete_from_db(self):
        with self.app_context():
            with patch('models.item.db.session.delete') as mocked_delete:
                with patch('models.item.db.session.commit') as mocked_commit:
                    StoreModel('coat_store').save_to_db()
                    ItemModel('coat', 200.33, 1).save_to_db()
                    ItemModel('coat', 200.33, 1).delete_from_db()

                    mocked_delete.assert_called()
                    mocked_commit.assert_called()
