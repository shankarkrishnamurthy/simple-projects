#!/bin/bash
# https://docs.docker.com/registry/deploying/
# Check notes

docker run -d -p 5000:5000 --restart=always --name registry registry:2
docker tag shankarkrishna/first-hello-repo:testimage localhost:5000/first-hello-repo
docker push localhost:5000/first-hello-repo
curl -L http://localhost:5000/v2/_catalog
curl -X GET http://localhost:5000/v2/my-hello/tags/list
# restart docker daemon with !--insecure-registry 10.217.211.130:5000! option in /etc/sysconfig/docker
curl -L http://10.217.211.130:5000/v2/my-hello/manifests/tfs
docker tag docker.io/redis:latest 10.217.211.130:5000/my-regis:first
docker push 10.217.211.130:5000/my-regis:first
curl -L http://10.217.211.130:5000/v2/my-hello/tags/list
curl -L http://10.217.211.130:5000/v2/_catalog
docker pull 10.217.211.130:5000/my-hello:tfs
docker container stop registry

