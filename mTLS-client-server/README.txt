https://codeburst.io/mutual-tls-authentication-mtls-de-mystified-11fa2a52e9cf

prereq:
    ca.crt  ca.srl      client.csr  server.csr  server.key
    ca.key  client.crt  client.key  server.crt

    create ca certificate:
    openssl req   -new   -x509   -nodes   -days 365   -subj '/CN=my-ca'   -keyout ca.key   -out ca.crt

    create server certificate:
    openssl genrsa   -out server.key 2048
    openssl req   -new   -key server.key   -subj '/CN=localhost'   -out server.csr
    openssl x509   -req   -in server.csr   -CA ca.crt   -CAkey ca.key   -CAcreateserial   -days 365   -out server.crt
    
    create client certificate:
    openssl genrsa   -out client.key 2048
    openssl req   -new   -key client.key   -subj '/CN=my-client'   -out client.csr
    openssl x509   -req   -in client.csr   -CA ca.crt   -CAkey ca.key   -CAcreateserial   -days 365   -out client.crt

Run:
    node server.js

    curl \
    --cacert ca.crt \
    --key client.key \
    --cert client.crt \
    https://localhost:3000

Verify:
    * below will fail because server certificate cannot be verified *
    curl --key client.key --cert client.crt  https://localhost:3000
    * below will fail because client did not provide its certificate.see server.js*
    curl --cacert ca.crt https://localhost:3000
