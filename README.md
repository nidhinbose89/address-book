# Run the application

- set environment with pip install -r requirements.txt
- python run.py


# Run unit test
python -m unittest tests.test_address_app

# API Guide

- Save Person to Address Book
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/address_book/person -d '{"first_name": "Nidhin", "last_name": "Bose", "street_address": ["street number 1", "street number 2"], "email": ["test1@email.com", "test2@email.com"], "phone": ["123123123", "345345345"] }'

- Save Group to Address Book
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/address_book/group -d '{"title":"Hello Data", "persons":["582eb1a7163db2356fe6f13d", "582eb1b1163db2356fe6f13e"]}'


- Get Members of a group
curl -H "Content-type: application/json" -X GET http://127.0.0.1:5000/groups/582eb232163db2356fe6f141/members

- Get Groups of a person
curl -H "Content-type: application/json" -X GET http://127.0.0.1:5000/person/582eb1a7163db2356fe6f13d/groups

- Get Person by first_name or last_name or emai
curl -H "Content-type: application/json" -X GET "http://127.0.0.1:5000/persons?first_name=nidhin&last_name=we"
curl -H "Content-type: application/json" -X GET "http://127.0.0.1:5000/persons?first_name=nidhin"
curl -H "Content-type: application/json" -X GET "http://127.0.0.1:5000/persons?email=@"



* Find person by email address (can supply any substring, ie. "comp" should
  work assuming "alexander@company.com" is an email address in the address
  book) - discuss how you would implement this without coding the solution.

  >> With mongoDB it works out of the box, can add secondary index if required.