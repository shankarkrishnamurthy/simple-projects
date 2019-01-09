#
For running simple ./hello.py, follow the below steps:
cd simple-projects/redis-examples/

0. pip3 install virtualenv
1. virtualenv redis-env
2. source redis-env/bin/activate
3. pip3 install -r requirements
4. docker run -d --name redis-test -p 6379:6379 redis
5. ./hello.py
