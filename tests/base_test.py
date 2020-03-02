"""
BaseTest
This class should be the parent class to each non-unit test (system and integration).
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    # setUpClass is called once for each test-case
    @classmethod
    def setUpClass(cls) -> None:
        # SQLite allows creating Items with store_id without any store in DB. Be careful.
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        # To avoid AssertionError: A setup function was called after the first request was handled.
        app.config['DEBUG'] = False
        # responsible for 500 errors
        app.config['PROPAGATE_EXEPTIONS'] = True
        with app.app_context():
            db.init_app(app)

    # setUp and tearDown are evoked for each method
    def setUp(self):
        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
