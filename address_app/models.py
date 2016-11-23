"""models.py."""
from mongoalchemy.exceptions import MissingValueException
from flask_mongoalchemy import MongoAlchemy

db = MongoAlchemy()


def email_validator(val):
    """Validate email."""
    if val:
        for each_email in val:
            pass
        return val
    raise MissingValueException('email')


def phone_validator(val):
    """Validate phone number."""
    if val:
        for each_phone in val:
            pass
        return val
    raise MissingValueException('phone')


def street_validator(val):
    """Validate street_address."""
    if val:
        for each_street in val:
            pass
        return val
    raise MissingValueException('street address')


class Person(db.Document):
    """Person model."""

    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    street_address = db.ListField(
        db.StringField(), validator=street_validator, required=True)
    email = db.ListField(
        db.StringField(), validator=email_validator, required=True)
    phone = db.ListField(
        db.StringField(), validator=phone_validator, required=True)

    @property
    def groups(self):
        """Atrribute property to get groups of a Person object."""
        return db.session.query(Group).filter(
            {Group.persons: {'$elemMatch': {
                Person.mongo_id: self.mongo_id}}}).all()

    @classmethod
    def get_by_email(cls, email=''):
        """Class methof to get person by email."""
        q1 = Person.email.regex(r'.*{}.*'.format(email), ignore_case=True)
        return db.session.query(Person).filter(q1).all()

    @classmethod
    def get_by_name(cls, first_name='', last_name=''):
        """Class methof to get person by first_name, last_name."""
        q1 = Person.first_name.regex(
            r'.*{}.*'.format(first_name), ignore_case=True)
        q2 = Person.last_name.regex(
            r'.*{}.*'.format(last_name), ignore_case=True)
        return db.session.query(Person).filter(q1, q2).all()


class Group(db.Document):
    """Group model."""

    title = db.StringField(required=True)
    persons = db.ListField(
        db.DocumentField(Person), required=False, default=[])


class AddressBook(db.Document):


    person_list = db.ListField(
        db.DocumentField(Person), required=False, default=[])
    group_list = db.ListField(
        db.DocumentField(Group), required=False, default=[])
