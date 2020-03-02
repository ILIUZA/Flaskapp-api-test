# Be careful: we use a different parent classes BaseTest and UnitBaseTest for integration/system and unit tests
from tests.unit.unit_base_test import UnitBaseTest
from models.item import ItemModel


# We test the functions from models.item witch don't require connection to DB or mocking.
class ItemTest(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel('coat', 200.99, 1)

        self.assertEqual(item.name, 'coat',
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 200.99,
                         "The price of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.store_id, 1)
        self.assertIsNone(item.store)

    def test_item_json(self):
        item = ItemModel('test', 19.99, 1)
        expected = {
            'name': 'test',
            'price': 19.99}

        self.assertEqual(
            item.json(),
            expected,
            "The JSON export of the item is incorrect. Received {}, expected {}."
                .format(item.json(), expected))
