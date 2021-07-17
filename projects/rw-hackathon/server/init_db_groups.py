import sqlite3

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()
try:
    cur.execute('DROP TABLE groups')
except:
    pass
finally:
    conn.commit()
cur.execute('CREATE TABLE groups ('
            'group_id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'group_name TEXT UNIQUE,'
            'grade INTEGER,'
            'email TEXT UNIQUE,'
            'members TEXT,'
            'work_name TEXT,'
            'work_description TEXT,'
            'password TEXT)')
cur.close()
conn.commit()
conn.close()
