#! /usr/bin/python

import addr_pb2
import sys
def PromptForAddress(person):
  person.id = int(input("Enter person ID number: "))
  person.name = input("Enter name: ")
  email = input("Enter email address (blank for none): ")
  if email != "": person.email = email
  while True:
    number = input("Enter a phone number (or leave blank to finish): ")
    if number == "": break
    phone_number = person.phones.add()
    phone_number.number = number
    type = input("Is this a mobile, home, or work phone? ")
    if type == "mobile": phone_number.type = addr_pb2.Person.PhoneType.MOBILE
    elif type == "home": phone_number.type = addr_pb2.Person.PhoneType.HOME
    elif type == "work": phone_number.type = addr_pb2.Person.PhoneType.WORK
    else: print("Unknown phone type; leaving as default value.")
if len(sys.argv) != 2:
  print("Usage:", sys.argv[0], "ADDRESS_BOOK_FILE")
  sys.exit(-1)
address_book = addr_pb2.AddressBook()
try:
  f = open(sys.argv[1], "rb")
  address_book.ParseFromString(f.read())
  f.close()
except IOError:
  print(sys.argv[1] + ": Could not open file.  Creating a new one.")
PromptForAddress(address_book.people.add())
f = open(sys.argv[1], "wb")
f.write(address_book.SerializeToString())
f.close()
