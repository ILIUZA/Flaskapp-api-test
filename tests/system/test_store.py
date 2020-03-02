import json
from models.item import ItemModel
from tests.base_test import BaseTest
from models.store import StoreModel


class StoreSystemTest(BaseTest):
    def test_get_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('coat_store').save_to_db()
                response = client.get('/store/{}'.format('coat_store'), data={'name': 'coat_store'})

                expected = {'name': 'coat_store', 'items': []}

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertIsNotNone(StoreModel.find_by_name('coat_store'))

    def test_get_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('coat_store')
                item = ItemModel('coat', 200.36, 1)

                self.assertIsNone(StoreModel.find_by_name('coat_store'))
                self.assertIsNone(ItemModel.find_by_name('coat'))

                store.save_to_db()
                item.save_to_db()

                response = client.get('/store/{}'.format('coat_store'))

                # {'name': self.name, 'price': self.price}
                # {'name': self.name, 'items': [item.json() for item in self.items.all()]}
                expected = {'name': 'coat_store', 'items': [{'name': 'coat', 'price': 200.36}]}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertIsNotNone(item.store)

    def test_get_store_with_items_2(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('coat_store')
                item = ItemModel('coat', 200.36, 2)

                self.assertIsNone(StoreModel.find_by_name('coat_store'))
                self.assertIsNone(ItemModel.find_by_name('coat'))

                store.save_to_db()
                item.save_to_db()

                response = client.get('/store/{}'.format('coat_store'), data={'name': 'coat_store'})

                expected = {'name': 'coat_store', 'items': []}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertIsNone(item.store)

    def test_get_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/{}'.format('test'), data={'name': 'test'})

                expected = {'message': 'Store not found'}

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 404)

    def test_post_store(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name('coat_store'))

                response = client.post('/store/{}'.format('coat_store'), data={'name': 'coat_store'})

                expected = {'name': 'coat_store', 'items': []}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('coat_store'))

    def test_post_duplicate(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name('coat_store'))

                client.post('/store/{}'.format('coat_store'), data={'name': 'coat_store'})

                self.assertIsNotNone(StoreModel.find_by_name('coat_store'))

                response = client.post('/store/{}'.format('coat_store'), data={'name': 'coat_store'})

                expected = {'message': "A store with name '{}' already exists.".format('coat_store')}

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.delete('/store/{}'.format('store_name'))

                expected = {'message': 'Store deleted'}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertIsNone(StoreModel.find_by_name('store_name'))

    def test_delete_existing_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store_name').save_to_db()

                self.assertIsNotNone(StoreModel.find_by_name('store_name'))

                response = client.delete('/store/{}'.format('store_name'))

                expected = {'message': 'Store deleted'}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertIsNone(StoreModel.find_by_name('store_name'))

    def test_get_list_store_empty(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/stores')

                expected = {'stores': []}

                self.assertDictEqual(expected, json.loads(response.data))

    def test_get_list_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                StoreModel('coat_store').save_to_db()

                self.assertIsNotNone('test_store')
                self.assertIsNotNone('coat_store')

                response = client.get('/stores')

                expected = {'stores': [{'name': 'test_store', 'items': []},
                                       {'name': 'coat_store', 'items': []}]}

                self.assertDictEqual(expected, json.loads(response.data))

    def test_get_list_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test_store')
                store2 = StoreModel('coat_store')
                store.save_to_db()
                store2.save_to_db()

                item = ItemModel('test_item', 100.11, 1)
                item2 = ItemModel('test_item2', 200.22, 1)
                item.save_to_db()
                item2.save_to_db()

                self.assertIsNotNone('test_store')
                self.assertIsNotNone('coat_store')

                response = client.get('/stores')

                expected = {'stores':
                                [{'name': 'test_store', 'items':
                                    [{'name': 'test_item', 'price': 100.11},
                                     {'name': 'test_item2', 'price': 200.22}]},
                                 {'name': 'coat_store', 'items': []}]}

                self.assertDictEqual(expected, json.loads(response.data))
                self.assertIsNotNone(store.items)
                self.assertIsNotNone(store2.items)
                self.assertIsNotNone(item.store)
                self.assertIsNotNone(item2.store)

