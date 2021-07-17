import sqlite3

conn = sqlite3.connect('../db.sqlite')
cur = conn.cursor()
try:
    cur.execute('DROP TABLE finalVotes')
except:
    pass
finally:
    conn.commit()
cur.execute('CREATE TABLE finalVotes ('
            'vote_id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'email TEXT UNIQUE,'
            'token TEXT UNIQUE,'
            'status INTEGER,'
            'weight INTEGER,'
            'vote1 INTEGER REFERENCES groups (group_id),'
            'vote2 INTEGER REFERENCES groups (group_id),'
            'vote3 INTEGER REFERENCES groups (group_id),'
            'vote4 INTEGER REFERENCES groups (group_id))')
cur.close()
conn.commit()
conn.close()