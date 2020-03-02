# Be careful: we use a different parent classes BaseTest and UnitBaseTest for integration/system and unit tests
from tests.unit.unit_base_test import UnitBaseTest
from models.user import UserModel


# We test the functions from models.user witch don't require connection to DB or mocking.
class UserModuleTest(UnitBaseTest):
    def test_init(self):
        user = UserModel('iliuza', '12345')

        self.assertEqual(user.username, 'iliuza')
        self.assertEqual(user.password, '12345')

