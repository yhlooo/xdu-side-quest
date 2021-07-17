from flask import Flask, request, g, redirect, render_template, session, url_for
from flask.ext.cors import CORS
import sqlite3
import os
import json


DATABASE = '../db.sqlite'
SECRET_KEY = os.urandom(233)
app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def hhh():
    return 'Hello World!', {'Access-Control-Allow-Credentials': 'true'}


@app.route('/final_groups')
def final_groups():
    groups_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    cur = g.db.cursor()
    groups_old = []
    for i in groups_id:
        groups_old.append(cur.execute('SELECT group_id, group_name, grade, members, work_name, work_description FROM groups WHERE group_id = ?', (i, )).fetchall()[0])
    groups = []
    for group in groups_old:
        grade = '大一'
        if 2 == group[2]:
            grade = '大二'
        elif 3 == group[2]:
            grade = '大三'
        groups.append({
            'group_id': group[0],
            'group_name': group[1],
            'grade': grade,
            'members': group[3],
            'work_name': group[4],
            'work_description': group[5]
        })
    return json.dumps(groups), 200, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/get_final_votes')
def get_final_votes():
    token = request.args.get('token')
    if not token:
        return 'bad', 404, {'Access-Control-Allow-Credentials': 'true'}
    cur = g.db.cursor()
    old_vote = cur.execute('SELECT weight, vote1, vote2, vote3, vote4 FROM finalVotes WHERE token = ?', (token,)).fetchall()
    if not old_vote:
        return 'bad', 404, {'Access-Control-Allow-Credentials': 'true'}
    return json.dumps(old_vote), 200, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/final_vote')
def final_vote():
    token = request.args.get('token')
    try:
        group_id = int(request.args.get('group_id'))
        number = int(request.args.get('number'))
    except:
        return 'error', 400, {'Access-Control-Allow-Credentials': 'true'}
    if not token or not group_id or number > 4 or number < 1:
        return 'error', 400, {'Access-Control-Allow-Credentials': 'true'}
    cur = g.db.cursor()
    old_vote = cur.execute('SELECT vote_id, vote1, vote2, vote3, vote4, weight FROM finalVotes WHERE token = ?', (token,)).fetchall()
    if not old_vote:
        return 'error', 400, {'Access-Control-Allow-Credentials': 'true'}
    group_name = cur.execute('SELECT group_name FROM groups WHERE group_id = ?', (group_id,)).fetchall()
    if not group_name:
        return 'error', 404, {'Access-Control-Allow-Credentials': 'true'}
    old_vote = list(old_vote[0])
    if 2 == old_vote[5]:
        if group_id in [old_vote[1], old_vote[2], old_vote[3]]:
            old_vote[1] = 0 if old_vote[1] == group_id else old_vote[1]
            old_vote[2] = 0 if old_vote[2] == group_id else old_vote[2]
            old_vote[3] = 0 if old_vote[3] == group_id else old_vote[3]
        else:
            if old_vote[1] and old_vote[2] and old_vote[3]:
                return 'error', 403, {'Access-Control-Allow-Credentials': 'true'}
            for i in range(1, 4):
                if not old_vote[i]:
                    old_vote[i] = group_id
                    break
        cur.execute('UPDATE finalVotes SET vote1 = ?, vote2 = ?, vote3 = ? WHERE token = ?',
                    (old_vote[1], old_vote[2], old_vote[3], token))
        g.db.commit()
        return group_name[0][0], 200, {'Access-Control-Allow-Credentials': 'true'}
    else:
        if group_id in [old_vote[1], old_vote[2], old_vote[3], old_vote[4]] and old_vote[number] != group_id:
            return 'error', 403, {'Access-Control-Allow-Credentials': 'true'}
        if old_vote[number] == group_id:
            cur.execute('UPDATE finalVotes SET vote%d = 0 WHERE token = ?' % number, (token, ))
            g.db.commit()
            return group_name[0][0], 200, {'Access-Control-Allow-Credentials': 'true'}
        elif 0 == old_vote[number]:
            cur.execute('UPDATE finalVotes SET vote%d = ? WHERE token = ?' % number, (group_id, token))
            g.db.commit()
            return group_name[0][0], 200, {'Access-Control-Allow-Credentials': 'true'}
        else:
            return 'error', 403, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/final_res')
def final_res():
    cur = g.db.cursor()
    groups = cur.execute('SELECT group_id, group_name FROM groups ORDER BY group_id').fetchall()
    votes = cur.execute('SELECT vote_id, vote1, vote2, vote3, vote4, weight FROM finalVotes').fetchall()
    groups = [{'group_id': i[0], 'group_name': i[1], 'vote': [0, 0, 0, 0, 0, 0]} for i in groups]
    for i in votes:
        if 2 == i[5]:
            for j in range(1, 4):
                groups[i[j] - 1]['vote'][5] = groups[i[j] - 1]['vote'][5] + 2 if i[j] else groups[i[j] - 1]['vote'][5]
        else:
            for j in range(1, 5):
                groups[i[j] - 1]['vote'][j] = groups[i[j] - 1]['vote'][j] + 1 if i[j] else groups[i[j] - 1]['vote'][j]
    for i in groups:
        i['vote'][0] = i['vote'][1] + i['vote'][2] + i['vote'][3] + i['vote'][4] + i['vote'][5]
    top5 = []
    groups_cp = groups.copy()
    for i in range(5):
        top5.append({'group_name': '', 'point': 0, 'per': 0})
        group_rm = None
        for j in groups_cp:
            if j['vote'][0] > top5[i]['point']:
                top5[i] = {'group_name': j['group_name'], 'point': j['vote'][0], 'per': 0}
                group_rm = j
        if group_rm:
            groups_cp.remove(group_rm)
    point_sum = 1
    for i in top5:
        point_sum += i['point']
    for i in top5:
        i['per'] = str(i['point'] / point_sum * 100)

    best4 = []
    for i in range(4):
        best4.append(['', 0])
        for j in groups:
            if j['group_name'] != best4[i][0] and j['vote'][i+1] > best4[i][1]:
                best4[i] = [j['group_name'], j['vote'][i+1]]
    res = {
        'top5': top5,
        'best4': best4
    }
    return json.dumps(res), 200, {'Access-Control-Allow-Credentials': 'true'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
