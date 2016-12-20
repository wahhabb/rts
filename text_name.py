#! /usr/bin/env python
import MySQLdb
import re

host = "localhost"
passwd = "rtsunl!mited"
user = "tim"
dbname = "rts_db"

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
cursor = db.cursor()

sql = "SELECT id, name FROM gcd_series ORDER BY id"
cursor.execute(sql)

results = cursor.fetchall()
count = 0
for row in results:
    old_name = row[1]
    new_name = old_name.replace("&", "and")
    new_name = re.sub(r' L.S.', '', new_name)
    new_name = re.sub(r'[-"\',.:! ]', '', new_name)
    sql = "UPDATE tmp_name SET text_name = '" + new_name + "' WHERE id = " + str(row[0]) + ';'
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
