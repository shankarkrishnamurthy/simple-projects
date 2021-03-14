#! /usr/bin/python

from addr_pb2 import Person,AddressBook
import sys

def ListPeople(address_book):
  for person in address_book.people:
    print("Person ID:", person.id)
    print("  Name:", person.name)
    if person.HasField('email'):
      print("  E-mail address:", person.email)

    for phone_number in person.phones:
      if phone_number.type == Person.PhoneType.MOBILE:
        print("  Mobile phone #: ",)
      elif phone_number.type == Person.PhoneType.HOME:
        print("  Home phone #: ",)
      elif phone_number.type == Person.PhoneType.WORK:
        print("  Work phone #: ",)
      print(phone_number.number)

if len(sys.argv) != 2:
  print("Usage:", sys.argv[0], "ADDRESS_BOOK_FILE")
  sys.exit(-1)
address_book = AddressBook()
f = open(sys.argv[1], "rb")
address_book.ParseFromString(f.read())
f.close()

ListPeople(address_book)
