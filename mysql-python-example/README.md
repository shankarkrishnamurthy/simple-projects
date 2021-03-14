Installed mysql server:
----------------------
dnf install -y mariadb

MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'rootpass' WITH GRANT OPTION;

installing mariadb connector (was not easy):
-------------------------------------------
pip3 search mysql-connector | grep --color mysql-connector-python
pip3 install -U setuptools
pip3 install -U wheel
pip3 install mysql-connector-python-rf

for gui access to db:
---------------------
dnf install -y phpmyadmin
/etc/phpMyAdmin/config.inc.php <-- 'localhost' to '127.0.0.1'

Source/Reference:
=================
https://www.youtube.com/watch?v=tGinfzlp0fE
