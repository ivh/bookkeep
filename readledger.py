#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite
from sys import argv,exit,stdout,stdin
from string import join,strip
import csv
import datetime
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

ledger=csv.reader(inf)     

for trans in ledger:
    m,d,y=map(int,trans[0].split('/'))
    date=datetime.date(y,m,d)
    ref=unicode(strip(trans[1]),encoding='utf8')
    descr=unicode(strip(trans[2]),encoding='utf8')
    debit=trans[3]
    credit=trans[4]
    acc=trans[5]
    #ex('INSERT INTO accounts VALUES (?, ?, ?)',(id,balance,descr))
    sql=u'INSERT OR IGNORE INTO bk_transaction VALUES ("%s", "%s", "%s");\n'%(ref,date.isoformat(),descr)
    outf.write(sql.encode('utf8'))
    sql=u'INSERT INTO bk_booking VALUES (NULL, "%s", "%s", %s, %s);\n'%(ref,acc,debit or 'NULL',credit or 'NULL')
    outf.write(sql.encode('utf8'))
    
    

#conn.commit()
#conn.close()
