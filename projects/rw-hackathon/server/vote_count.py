import sqlite3

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()
groups = cur.execute('SELECT group_id, group_name FROM groups ORDER BY group_id').fetchall()
votes = cur.execute('SELECT vote_id, vote1, vote2, vote3 FROM votes').fetchall()
conn.close()
groups = [{'group_id': i[0], 'group_name': i[1], 'vote': 0} for i in groups]
for i in votes:
    for j in range(1, 4):
        groups[i[j]-1]['vote'] = groups[i[j]-1]['vote'] + 1 if i[j] else groups[i[j]-1]['vote']

print('Group ID | Votes    | Group Name')
for i in groups:
    print('%-8s | %-8d | %s' % (i['group_id'], i['vote'], i['group_name']))
