import MySQLdb

db = MySQLdb.connect('localhost', 'bandydan', 'dreamteam')
# creating a cursor
cursor = db.cursor()
# execute a query in the terms of cursor
cursor.execute('SELECT VERSION()')
# fetching one result from the cursor
data = cursor.fetchone()
print "Database version : %s " % data
