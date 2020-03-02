from unittest import expectedFailure
from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemSystemTest(BaseTest):
    def setUp(self):
        super(ItemSystemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('iliuza', '12345').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'iliuza', 'password': '12345'}),
                                           headers={'Content-type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    @expectedFailure
    def test_get_item_no_auth_negative(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('coat_store').save_to_db()
                ItemModel('coat', 100.11, 1).save_to_db()

                self.assertIsNotNone(ItemModel.find_by_name('coat'))

                response = client.get('/item/{}'.format('coat'))
                expected = {'name': 'coat', 'price': 100.11}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 201)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('coat_store').save_to_db()
                ItemModel('coat', 100.11, 1).save_to_db()

                self.assertIsNotNone(ItemModel.find_by_name('coat'))

                header = {'Authorization': self.access_token}
                response = client.get('/item/{}'.format('coat'), headers=header)
                expected = {'name': 'coat', 'price': 100.11}

                self.assertIsNotNone(ItemModel.find_by_name('coat'))
                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 200)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                header = {'Authorization': self.access_token}
                response = client.get('/item/{}'.format('coat'), headers=header)
                expected = {'message': 'Item not found'}

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(expected, json.loads(response.data))

    @expectedFailure
    def test_post_item_without_store_id(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('coat_store').save_to_db()

                response = client.post('/item/{}'.format('coat'),
                                       data={'name': 'coat', 'price': 200.22})
                expected = {'name': 'coat', 'price': 200.22}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 201)

    @expectedFailure
    def test_post_item_without_price(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('coat_store').save_to_db()

                response = client.post('/item/{}'.format('coat'),
                                       data={'name': 'coat', 'store_id': 1})
                expected = {'name': 'coat', 'price': 200.22}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 201)

    def test_post_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('coat_store').save_to_db()

                response = client.post('/item/{}'.format('coat'),
                                       data={'price': 200.22, 'store_id': 1})
                expected = {'name': 'coat', 'price': 200.22}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name('coat'))
                self.assertEqual(ItemModel.find_by_name('coat').price, 200.22)

    def test_post_item_existed(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('coat_store').save_to_db()

                client.post('/item/{}'.format('coat'),
                            data={'price': 200.22, 'store_id': 1})
                response = client.post('/item/{}'.format('coat'),
                                       data={'price': 200.22, 'store_id': 1})
                expected = {'message': "An item with name '{}' already exists.".format('coat')}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 400)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('coat_store').save_to_db()
                ItemModel('coat', 300.33, 1).save_to_db()

                self.assertIsNotNone(ItemModel.find_by_name('coat'))

                response = client.delete('/item/{}'.format('coat'))
                expected = {'message': 'Item deleted'}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertIsNone(ItemModel.find_by_name('coat'))

    def test_put_new_item_without_price(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                response = client.put('/item/{}'.format('coat'))
                expected = {'message': {'price': 'This field cannot be left blank!'}}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 400)

    def test_put_new_item_without_store_id(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                response = client.put('/item/{}'.format('coat'), data={'price': 300.33})
                expected = {'message': {'store_id': 'Every item needs a store id.'}}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 400)

    def test_put_new_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                response = client.put('/item/{}'.format('coat'),
                                      data={'price': 300.33, 'store_id': 1})
                expected = {'name': 'coat', 'price': 300.33}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 200)

    # Trying to put the item with the same name and price but different store_id
    def test_put_item_2(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                client.put('/item/{}'.format('coat'), data={'price': 300.33, 'store_id': 1})

                self.assertIsNotNone(ItemModel.find_by_name('coat'))

                response = client.put('/item/{}'.format('coat'),
                                      data={'price': 300.33, 'store_id': 2})
                expected = {'name': 'coat', 'price': 300.33}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(ItemModel.find_by_name('coat'))

    # if we try to put the item with the same name and store_id the price must be updated
    def test_update_price(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                client.put('/item/{}'.format('coat'), data={'price': 300.33, 'store_id': 1})

                self.assertIsNotNone(ItemModel.find_by_name('coat'))
                self.assertEqual(ItemModel.find_by_name('coat').price, 300.33)

                response = client.put('/item/{}'.format('coat'),
                                      data={'price': 200.22, 'store_id': 1})
                expected = {'name': 'coat', 'price': 200.22}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(ItemModel.find_by_name('coat'))
                self.assertEqual(ItemModel.find_by_name('coat').price, 200.22)

    def test_get_list_empty(self):
        with self.app() as client:
            with self.app_context():

                response = client.get('/items')
                expected = {'items': []}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 200)

    # {'items': [x.json() for x in ItemModel.query.all()]}
    def test_get_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('coat_store').save_to_db()
                StoreModel('fur_coat_store').save_to_db()
                ItemModel('coat', 100.11, 1).save_to_db()
                ItemModel('fur coat', 1000.11, 2).save_to_db()

                response = client.get('/items')
                expected = {'items': [{'name': 'coat', 'price': 100.11},
                                      {'name': 'fur coat', 'price': 1000.11}]}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 200)

