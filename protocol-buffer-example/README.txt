Definition:
  Protocol buffers are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data � think XML, but smaller, faster, and simpler. 

Resource:
    
    https://developers.google.com/protocol-buffers/docs/pythontutorial 
steps:

 - pip install protobuf
 - protoc -I=. --python_out=. ./addr.proto 
 - import addr_pb2.py
 - see writer and reader for producer and consumer of this message
