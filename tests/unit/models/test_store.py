from models.store import StoreModel
# Be careful: we use a different parent classes BaseTest and UnitBaseTest for integration/system and unit tests
from tests.unit.unit_base_test import UnitBaseTest


# We test the functions from models.store witch don't require connection to DB or mocking.
class StoreTest(UnitBaseTest):
    def test_init(self):
        store = StoreModel('coat_store')

        self.assertEqual('coat_store', store.name)
