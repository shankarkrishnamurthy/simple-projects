package main

import (
	pb "addressbook"
	"fmt"
	"log"

	p "github.com/golang/protobuf/proto"
)

func main() {
	p1 := &pb.Person {
				Id:    1234,
				Name:  "John Doe",
				Email: "jdoe@example.com",
				Phones: []*pb.Person_PhoneNumber{
					{Number: "555-4321", Type: pb.Person_HOME},
				},
			}

	p2 := &pb.Person {
				Id:    1235,
				Name:  "Alex",
				Email: "alex@example.com",
				Phones: []*pb.Person_PhoneNumber{
					{Number: "1234-5678", Type: pb.Person_HOME},
				},
			}

	b := new(pb.AddressBook)
    b.People = append(b.People, p1)
	b.People = append(b.People, p2)
	data, err := p.Marshal(b)
	if err != nil {
		log.Fatal("marshaling error: ", err)
	}
	fmt.Println("Raw data", data)

    // reverse above
	addresssBook := pb.AddressBook{}
	err = p.Unmarshal(data, &addresssBook)
	if err != nil {
		log.Fatal("unmarshaling error: ", err)
	}

	for _, person := range addresssBook.People {
		fmt.Println("===========================")
		fmt.Println("ID: ", person.GetId())
		fmt.Println("Name: ", person.GetName())
		fmt.Println("Email: ", person.GetEmail())
		fmt.Println("Phones: ", person.GetPhones())
	}
}

