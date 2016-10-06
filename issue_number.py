#! /usr/bin/env python
import MySQLdb
import re

host = "localhost"
passwd = "rtsunl!mited"
user = "tim"
dbname = "rts_db"

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
cursor = db.cursor()

sql = "SELECT id, old_number FROM gcd_issue ORDER BY id"
cursor.execute(sql)

results = cursor.fetchall()
count = 0
for row in results:
    old_number = row[1]
    matches = re.match('.+\[(\d+)\].*', old_number)
    if matches:
        old_number = matches.group(1)
    else:
        try:
            old_number = int(old_number)
        except:
            old_number = '???'
    sql = "INSERT INTO tmp_number VALUES ('%s',  '%s');" % (row[0], old_number)
    if (count < 5):
        print(sql, row[0], row[1])
    cursor.execute(sql)
    count += 1
    if count % 2000 == 0:
        print("count:", count)
print('ready to commit')
db.commit()
print('ready to close')
db.close()
print('done')
