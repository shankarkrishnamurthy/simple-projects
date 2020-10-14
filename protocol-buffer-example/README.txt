Definition:
  Protocol buffers are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data � think XML, but smaller, faster, and simpler. 

    Python:
        Resource:
            https://developers.google.com/protocol-buffers/docs/pythontutorial 
        steps:
         - dnf install -y protobuf-compiler
         - pip install protobuf
         - protoc -I=. --python_out=. ./addr.proto 
         - import addr_pb2.py
         - see writer and reader for producer and consumer of this message

    golang:
        Resource:
        https://ednsquare.com/story/working-with-protocol-buffers-in-golang------8g4uuR
        steps:
         - dnf install -y protobuf-devel
         - dnf install -y protobuf-compiler
         - go get -u -v github.com/golang/protobuf/proto
         - go get -u -v github.com/golang/protobuf/protoc-gen-go
         - export PATH=~/go/bin:$PATH 
         - protoc -I=. --go_out=. ./addressbook.proto 
         - mkdir -p ~/go/src/addressbook;cp ./addressbook.pb.go ~/go/src/addressbook/
         - go run writer.go
