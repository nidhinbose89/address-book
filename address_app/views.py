"""app.py."""
import json
from flask import request, jsonify

from app import app
from models import Group, Person, AddressBook
from mongoalchemy.exceptions import MissingValueException, BadValueException
from bson.json_util import dumps


@app.route('/address_book/<string:item_type>', methods=['POST'])
def address_book(item_type):
    """Add a person or group to the address book."""
    data = json.loads(request.data)
    address_book = AddressBook.query.first()
    if not address_book:
        address_book = AddressBook()
        address_book.save()

    if item_type == "person":
        person_obj = Person(**data)
        try:
            person_obj.save()
            address_book.person_list.append(person_obj)
        except MissingValueException as e:
            return jsonify({"saved": False, "type": "person", "data": data, "message": "Missing {}".format(e)})
        except Exception as e:
            raise e
    elif item_type == "group":
        data['persons'] = [Person.query.get(x) for x in data['persons']]
        try:
            group_obj = Group(**data)
            group_obj.save()
            address_book.group_list.append(group_obj)
        except MissingValueException as e:
            return jsonify({"saved": False, "type": "person", "message": "Missing {}".format(e)})
        except BadValueException as e:
            return jsonify({"saved": False, "type": "person", "message": "One of the Ids provided is not in Database"})
        except Exception as e:
            raise e
    else:
        return jsonify({"message": "The url has to be address_book/[person|group]"}), 404

    address_book.save()
    return jsonify({"message": "saved {} to Address Book".format(item_type),
                    "data": dumps(address_book.wrap())})


@app.route('/groups/<string:group_id>/members')
def group_members(group_id=None):
    """Given a group we want to find its members."""
    group_obj = Group.query.get(group_id)
    if group_obj:
        _group_obj = group_obj.wrap()
        return jsonify({'status': "success", "type": "persons", "count": len(_group_obj['persons']), "data": dumps(_group_obj)})


@app.route('/person/<string:person_id>/groups')
def person_groups(person_id):
    """Given a person we want to easily find the groups the person belongs to."""
    person_obj = Person.query.get(person_id)
    if not person_obj:
        return jsonify({'status': "fail", "message": "Person not found."}), 404
    groups = person_obj.groups
    data = []
    for each in groups:
        data.append({"id": each.mongo_id, "title": each.title})
    return jsonify({'status': "success", "type": "groups", "count": len(data), "data": dumps(data)})


@app.route('/persons')
def persons():
    """Search on persons.

    Find person by name (can supply either first name, last name, or both).
    Find person by email address (can supply either the exact string or a prefix)
    """
    first_name = request.args.get('first_name', '')
    last_name = request.args.get('last_name', '')
    email = request.args.get('email', '')
    if first_name or last_name:
        person_objs = Person.get_by_name(first_name=first_name, last_name=last_name)
    elif email:
        person_objs = Person.get_by_email(email=email)
    else:
        person_objs = Person.query.all()

    data = []
    for each_person in person_objs:
        data.append(each_person.wrap())
    print data
    return jsonify({'status': "success", "count": len(data), "type": "person", "data": dumps(data)})
