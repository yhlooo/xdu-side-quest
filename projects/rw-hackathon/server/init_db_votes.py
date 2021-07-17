import sqlite3

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()
try:
    cur.execute('DROP TABLE votes')
except:
    pass
finally:
    conn.commit()
cur.execute('CREATE TABLE votes ('
            'vote_id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'email TEXT UNIQUE,'
            'token TEXT UNIQUE,'
            'status INTEGER,'
            'vote1 INTEGER REFERENCES groups (group_id),'
            'vote2 INTEGER REFERENCES groups (group_id),'
            'vote3 INTEGER REFERENCES groups (group_id))')
cur.close()
conn.commit()
conn.close()
