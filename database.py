# database ....
# store numbers ...
# two tables ...
# table 1 -> pid, name, email address
# table 2 -> tid, ticket number, pid-table1
#-------------------------------------------
import sqlite3
import datetime

class Database():

    db_name = "raffle.db"
    db_location = "database/" # "here" need to create a dir structure

    # table creations queries here ...
    # person table, just name & email
    person_tbl = """CREATE TABLE if not exists person
                    (pid INTEGER PRIMARY KEY, name text, email text NOT NULL UNIQUE)"""

    # ticket table, just ticket# as primary key & PID to whom it belongs
    # so it's a 1 to 1 ticket to person but 1 to many person to tickets
    ticket_tbl = """CREATE TABLE if not exists ticket
                    (ticket_number INTEGER PRIMARY KEY, pid integer NOT NULL)"""

    # insert queries here.
    # insert a person into the database.
    insert_person = """INSERT INTO person (name,email) VALUES(?,?)"""

    # insert ticket into the database.
    insert_ticket = """INSERT INTO ticket (ticket_number,pid) VALUES(?,?)"""

    # select queries here.
    select_person = """SELECT * FROM person WHERE email=?"""

    # look up a person via their email and return pid
    select_email = """SELECT pid FROM person WHERE email=?"""

    select_ticket = """SELECT ticket_number FROM ticket WHERE ticket_number=?"""

    def __init__(self):
        self.con = sqlite3.connect(self.db_location + self.db_name)
        self.cur = self.con.cursor()
        self.cur.execute(self.person_tbl)
        self.cur.execute(self.ticket_tbl)
        self.con.commit()

    def add_person(self,name,email):
        if not self.cur.execute(self.select_email,(email,)).fetchall():
            self.cur.execute(self.insert_person,(name.upper(),email))
        else:
            # probably need better error handling, but w/e.
            print("ERROR: ",email, " exists, in the database!")
        self.con.commit()

    def add_ticket(self,ticket,email):
        pid = self.cur.execute(self.select_email,(email,)).fetchone()[0]
        # query by email, get the pid and insert
        if not self.cur.execute(self.select_ticket,(ticket,)).fetchall():
            self.cur.execute(self.insert_ticket,(ticket,pid))
        else:
            #TODO - proper error handling
            print("ERROR: ticket: ",ticket," already in the database!")
        self.con.commit()


    def lookup_person(self,email):
        if self.cur.execute(self.select_person,(email,)).fetchall():
            return self.cur.execute(self.select_person,(email,)).fetchone()[0]
        else:
            return -1
