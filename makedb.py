#!/usr/bin/env python2.6

from sqlite3 import dbapi2 as sqlite
from sys import argv,exit
from string import join,strip

COMMENTCHAR='#'
DELIM=','

if len(argv) < 3:
    print 'Give me a chart of accounts and database name, please!'
    exit(0)

ACCOUNTS=argv[1]
DBNAME=argv[2]

conn=sqlite.connect(DBNAME)
curs=conn.cursor()
ex=curs.execute
print('Working with %s'%DBNAME)

ex('CREATE TABLE accounts (id INT PRIMARY KEY, balance REAL, description TEXT);')

ex('CREATE TABLE tansactions (id INT PRIMARY KEY, date TEXT, description TEXT);')

ex('CREATE TABLE bookings (transid INT, debit INT, credit INT, value REAL);')

for acc in open(ACCOUNTS):
    if acc.startswith(COMMENTCHAR): continue
    acc=acc.split(DELIM)
    id=acc[0]
    balance=acc[1]
    descr=unicode(strip(join(acc[2:])),'UTF-8')
    #ex('INSERT INTO accounts VALUES (?, ?, ?)',(id,balance,descr))
    print 'INSERT INTO bk_account VALUES (NULL, "%s", "%s", "%s");'%(id,balance,descr)
conn.commit()
conn.close()
