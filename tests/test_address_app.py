#!/usr/bin/env python
"""Unit Testing for the address_app."""
import unittest
import json

from address_app.app import create_app
from address_app.models import db, Person, Group


class TestCase(unittest.TestCase):
    """Address App Test."""

    @classmethod
    def setUpClass(cls):
        app = create_app(db_name='testing', testing=True)
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.db.connection.drop_database('testing')
        del(cls.app)

    def setUp(self):
        """Setup per test."""
        pass

    def tearDown(self):
        """Teardown per test."""
        pass

    def test_01_add_person_to_book(self):
        """Add a person to the address book."""
        data = {"first_name": "Nidhin", "last_name": "Bose",
                "street_address": ["street number 1", "street number 2"],
                "email": ["test1@email.com", "test2@email.com"],
                "phone": ["123123123", "345345345"]}

        rv = self.app.post('/address_book/person',
                           data=json.dumps(data),
                           follow_redirects=True)
        data = json.loads(rv.data)
        self.assertEqual(data["message"], "saved person to Address Book")

    def test_02_add_group_to_book(self):
        """Add a group to the address book."""
        p1 = Person.query.first().mongo_id
        data = {"title": "Hello Data", "persons": [str(p1)]}
        rv = self.app.post('/address_book/group',
                           data=json.dumps(data),
                           follow_redirects=True)
        data = json.loads(rv.data)
        self.assertEqual(data["message"], "saved group to Address Book")

    def test_03_get_members_of_group(self):
        """Given a group we want to easily find its members."""
        g1 = Group.query.first().mongo_id
        rv = self.app.get('groups/' + str(g1) + '/members')
        data = json.loads(rv.data)
        self.assertEqual(data["status"], "success")

    def test_04_get_group_of_person(self):
        """Given a person we want to easily find the groups the person belongs to."""
        p1 = Person.query.first().mongo_id
        rv = self.app.get('person/' + str(p1) + '/groups')
        data = json.loads(rv.data)
        self.assertEqual(data["status"], "success")

    def test_05_get_person_by_name(self):
        """Find person by name (can supply either first name, last name, or both)."""
        p1 = Person.query.first()
        p1_data = p1.wrap()
        p1_f_name = p1_data["first_name"]
        # find by first name only
        # get part of name and search
        q_string = "?first_name={}".format(p1_f_name[:3])  # TODO - verify the length
        rv = self.app.get('persons', query_string=q_string)
        data = json.loads(rv.data)
        self.assertEqual(data["count"], 1)

        # find by first name and last name
        p1_l_name = p1_data["last_name"]
        q_string = "?first_name={}&last_name={}".format(p1_f_name[:3], p1_l_name)
        rv = self.app.get('persons', query_string=q_string)
        data = json.loads(rv.data)
        self.assertEqual(data["count"], 1)

        # find by first name and non-existing last name
        q_string = "?first_name={}&last_name={}".format(p1_f_name[:3], "iAmNotThere")
        rv = self.app.get('persons', query_string=q_string)
        data = json.loads(rv.data)
        self.assertEqual(data["count"], 0)

    def test_06_get_person_by_email(self):
        """Find person by email address - can supply either the exact string or a prefix."""
        p1 = Person.query.first()
        p1_data = p1.wrap()
        p1_email = p1_data["email"]
        q_string = "?email={}".format(p1_email[2:10])  # TODO - verify the length of email before slicing
        rv = self.app.get('persons', query_string=q_string)
        data = json.loads(rv.data)
        self.assertEqual(data["count"], 1)


if __name__ == '__main__':
    unittest.main()
