import sqlite3

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()
cur.execute('UPDATE votes SET vote1 = 0, vote2 = 0, vote3 = 0')
conn.commit()
conn.close()
