"""
UnitBaseTest
This class should be the parent class to each unit-test.

We need to import StoreModel for unit-tests of the item's functions
because item has a relationship with Store (store_id).
But we don't do it (we have to repeat that import in each file, it can cause reducing of the effectiveness).
We create and export UnitBaseTest instead.
It is necessary to use 'import app' for integrity.
"""

from unittest import TestCase
from app import app


class UnitBaseTest(TestCase):
    pass