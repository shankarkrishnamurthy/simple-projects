#!/usr/bin/python3
import mysql.connector as mariadb
import yaml
import sys


HOST = "10.221.50.14"
PORT = 3306
USER = "root"
PASS = "rootpass"
DB = "hellodb"

#mariadb_connection = mariadb.connect(user='root', password='rootpass', database='hellodb')
mydb = mariadb.connect(host=HOST, port=PORT, user=USER, password=PASS, database=DB)
cursor = mydb.cursor()

#CREATE DATABASE
#my_cursor.execute("CREATE DATABASE hellodb")

#SHOW DATABASE
#my_cursor.execute("SHOW DATABASES")

#CREATE TABLE
cursor.execute("CREATE TABLE sdx (sdxfield VARCHAR(255), value VARCHAR(255))")
cursor.execute("SHOW TABLES")
for i in cursor:
    print (i)

# INSERT only 1 ROW in 1 TABLE
#sqlcmd = "INSERT INTO sdx (sdxfield,value) VALUES (%s, %s)"
#rec1 = ("Device Name", "SDX-Zela-SHAN")
#cursor.execute(sqlcmd, rec1)

# INSERT n ROW in 1 TABLE
with open(sys.argv[1], 'r') as stream:
    try:
        y = yaml.load(stream)
        rec = []
        for k,v in y.items():
            rec.append((k,v))
            #print(rec[-1])
        sqlcmd = "INSERT INTO sdx (sdxfield,value) VALUES (%s, %s)"
        cursor.executemany(sqlcmd, rec)
    except yaml.YAMLError as exc:
        print(exc)

mydb.commit()

# pull and print all the rows in a table
cmd = "SELECT * from sdx"
cursor.execute(cmd)
rec = cursor.fetchall()
for i in rec:
    print (i)

# Drop the table that we created
cmd= "DROP TABLE sdx"
cursor.execute(cmd)
