#! /usr/bin/env python
import MySQLdb
import re

host = "localhost"
passwd = "rtsunl!mited"
user = "tim"
dbname = "rts_db"

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
cursor = db.cursor()

sql = "SELECT s.id, s.name, sort_title, publisher_id, p.name, s.year_began FROM gcd_series s " \
      "INNER JOIN gcd_publisher p ON s.publisher_id = p.id WHERE s.country_id = 225 ORDER BY s.name;"

cursor.execute(sql)
# 0 = id, 1 = name, 2 = sort_name, 3 = publisher_id, 4 = pub. name, 5 = year_began
count = 0
row = cursor.fetchone()
while row is not None:
    row = cursor.fetchone()
    print(','.join(map(str, row)))
    count += 1
    # if count > 4:
    #     break
    row = cursor.fetchone()
db.close()

