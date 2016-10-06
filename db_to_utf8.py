#! /usr/bin/env python
import MySQLdb

host = "localhost"
passwd = "rtsunl!mited"
user = "tim"
dbname = "rts_db"

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
cursor = db.cursor()

cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % dbname)

sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % dbname
cursor.execute(sql)
print ("step 1")

results = cursor.fetchall()
for row in results:
    sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
    print("set", row[0])
    cursor.execute(sql)
print('ready to commit')
db.commit()
print('ready to close')
db.close()
print('done')
