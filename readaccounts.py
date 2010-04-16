#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite
from sys import argv,exit,stdout,stdin
from string import join,strip

COMMENTCHAR='#'
DELIM=','

if len(argv) == 1:
    inf,outf=stdin,stdout
elif len(argv) == 2:
    inf=open(argv[1])
    outf=stdout
elif len(argv) == 3:
    inf=open(argv[1])
    outf=open(argv[2],'w')
     

#conn=sqlite.connect(DBNAME)
#curs=conn.cursor()
#ex=curs.execute
#print('Working with %s'%DBNAME)

#ex('CREATE TABLE accounts (id INT PRIMARY KEY, balance REAL, description TEXT);')

#ex('CREATE TABLE tansactions (id INT PRIMARY KEY, date TEXT, description TEXT);')

#ex('CREATE TABLE bookings (transid INT, debit INT, credit INT, value REAL);')

for acc in inf:
    if acc.startswith(COMMENTCHAR): continue
    acc=acc.split(DELIM)
    id=acc[0]
    balance=acc[1]
    debinc=acc[2]
    descr=unicode(strip(join(acc[3:])),encoding='utf8')
    #ex('INSERT INTO accounts VALUES (?, ?, ?)',(id,balance,descr))
    sql=u'INSERT INTO bk_account VALUES ("%s", "%s", "%s", "%s");\n'%(id,balance,debinc,descr)
    outf.write(sql.encode('utf8'))

#conn.commit()
#conn.close()
