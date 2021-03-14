import psycopg2
import psycopg2.extensions
from datetime import *
import select
from random import randint
import math
from heapq import *

class Schema:
    NOTIF_COL=3
    NOTIF_HDR="notif"
    FDATE_COL=2
    FDATE_HDR="fdate"
    DONE_COL=4

class DB():
    def _create_db(self):
        db_name  = "remainder_events"
        conn = psycopg2.connect(user="postgres", password="mysecret", host="localhost")
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        curs = conn.cursor()
        try:
            curs.execute("create database %s" %(db_name))
            print ("%s db created"% db_name)
        except:
            print ("%s already exists"% db_name)
        curs.close()
        conn.close()
        try:
            conn = psycopg2.connect(user="postgres", password="mysecret", database="remainder_events", host="localhost")
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        except:
            print ("%s db connected"% db_name)
        self.conn,self.curs = conn, conn.cursor()

    def _create_table(self):
        table_name = 'events'
        cmd = "CREATE TABLE %s ( snum SERIAL, descr VARCHAR(256) NOT NULL, fdate DATE NOT NULL, notif DATE NOT NULL, done boolean default False);" % table_name
        try:
            self.curs.execute(cmd)
            print("%s table created"% table_name) 
        except:
            print("%s table already exists"% table_name)

    def getall(self):
        cmd='select * from events'
        self.curs.execute(cmd)
        return self.curs.fetchall()
    
    def delete(self,id):
        print("DB Delete ", id)
        self.curs.execute("delete from events where snum=%s",(id,))
    
    def create(self,msg,d):
        print("DB Insert ", msg,d)
        cmd = "INSERT INTO events VALUES(DEFAULT,%s,%s,%s,%s);"
        d1 = d2 = datetime.strptime(d,'%Y-%m-%d')
        self.curs.execute(cmd, (msg, d1, d2,False))
        
    def done(self, snum):
        print("DB Update ", snum)
        cmd="update events set done=%s where snum=%s;"
        self.curs.execute(cmd, (True, snum,))
        
    def __init__(self):
        self._create_db()
        self._create_table()
        self.trigger_notify()
        
    def close(self):
        self.curs.close()
        self.conn.close()

    def trigger_notify(self):
        cmd = """create or replace function notify()
        returns trigger as $$
        declare
        begin
        perform pg_notify('create_chan', row_to_json(new)::text); return new;
        end;
        $$ language plpgsql;"""
        self.curs.execute(cmd)

        cmd = """create or replace function notify_del()
        returns trigger as $$
        declare
        begin
        perform pg_notify('delete_chan', row_to_json(old)::text); return old;
        end;
        $$ language plpgsql;"""
        self.curs.execute(cmd)

        cmd = """create trigger create_change
        after insert on events
        for each row
        execute procedure notify();"""
        try:
            self.curs.execute(cmd)
        except:
            print("create_change trigger already exists")

        cmd = """create trigger delete_change
        after delete on events
        for each row
        execute procedure notify_del();"""
        try:
            self.curs.execute(cmd)
        except:
            print("delete_change trigger already exists")

        self.curs.execute("LISTEN delete_chan;")
        self.curs.execute("LISTEN create_chan;")
        print("Done DB creation")

if __name__ == '__main__':
    d = db()
    d.close()
