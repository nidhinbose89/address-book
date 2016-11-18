#!/usr/bin/env python
import unittest
import flask_mongoalchemy as mongoalchemy
from address_app import app


class TestCase(unittest.TestCase):
    """Address App Test."""

    def setUp(self):
        """SetUp."""
        app.config['TESTING'] = True
        app.config['MONGOALCHEMY_DATABASE'] = 'testing'
        db = mongoalchemy.MongoAlchemy(app)
        self.app = app.test_client()

    def tearDown(self):
        """Teardown."""
        del(self.app)

    def test_add_person_to_book(self):
        """Add a person to the address book."""
        assert False

    def test_add_group_to_book(self):
        """Add a group to the address book."""
        assert False

    def test_get_members_of_group(self):
        """Given a group we want to easily find its members."""
        assert False

    def test_get_group_of_person(self):
        """Given a person we want to easily find the groups the person belongs to."""
        assert False

    def test_get_person_by_name(self):
        """Find person by name (can supply either first name, last name, or both)."""
        assert False

    def test_get_person_by_email(self):
        """Find person by email address - can supply either the exact string or a prefix."""
        assert False

if __name__ == '__main__':
    unittest.main()
