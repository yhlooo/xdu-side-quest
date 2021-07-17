import sqlite3

conn = sqlite3.connect('../db.sqlite')
cur = conn.cursor()
groups = cur.execute('SELECT group_id, group_name FROM groups ORDER BY group_id').fetchall()
votes = cur.execute('SELECT vote_id, vote1, vote2, vote3, vote4, weight FROM finalVotes').fetchall()
conn.close()
groups = [{'group_id': i[0], 'group_name': i[1], 'vote': [0, 0, 0, 0, 0, 0]} for i in groups]
for i in votes:
    if 2 == i[5]:
        for j in range(1, 4):
            groups[i[j]-1]['vote'][5] = groups[i[j]-1]['vote'][5] + 2 if i[j] else groups[i[j]-1]['vote'][5]
    else:
        for j in range(1, 5):
            groups[i[j]-1]['vote'][j] = groups[i[j]-1]['vote'][j] + 1 if i[j] else groups[i[j]-1]['vote'][j]

for i in groups:
    i['vote'][0] = i['vote'][1] + i['vote'][2] + i['vote'][3] + i['vote'][4] + i['vote'][5]

print('Group ID | Votes                | Group Name')
for i in groups:
    print('%-8s | %-20s | %s' % (i['group_id'], str(i['vote']), i['group_name']))
