from flask import Flask, request, g, redirect, render_template, session, url_for
from flask.ext.cors import CORS
import sqlite3
import os
import json
import time
from hashlib import md5
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

DATABASE = 'db.sqlite'
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


@app.route('/group_base_info')
def group_base_info():
    group_id = session.get('group_id')
    if group_id:
        cur = g.db.cursor()
        old_group = cur.execute('SELECT group_name FROM groups WHERE group_id = ?', (group_id, )).fetchall()
        if old_group:
            return old_group[0][0], 200, {'Access-Control-Allow-Credentials': 'true'}
    return 'no one', 403, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/group_info')
def group_info():
    group_id = session.get('group_id')
    if not group_id:
        return 'error', 403, {'Access-Control-Allow-Credentials': 'true'}
    cur = g.db.cursor()
    old_group = cur.execute('SELECT group_id, group_name, email, grade, members, work_name, work_description FROM groups WHERE group_id = ?', (group_id, )).fetchall()
    if not old_group:
        return 'error', 403, {'Access-Control-Allow-Credentials': 'true'}
    return json.dumps(old_group[0]), 200, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/groups_list')
def groups_list():
    cur = g.db.cursor()
    groups_old = cur.execute('SELECT group_id, group_name, grade, members, work_name, work_description FROM groups ORDER BY grade, group_id').fetchall()
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


@app.route('/get_votes')
def get_votes():
    token = request.args.get('token')
    if not token:
        return 'bad', 404, {'Access-Control-Allow-Credentials': 'true'}
    cur = g.db.cursor()
    old_vote = cur.execute('SELECT vote1, vote2, vote3 FROM votes WHERE token = ?', (token, )).fetchall()
    if not old_vote:
        return 'bad', 404, {'Access-Control-Allow-Credentials': 'true'}
    return json.dumps(old_vote), 200, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/check_registered')
def check_registered():
    name = request.args.get('name')
    value = request.args.get('value')
    if not name or not value:
        return 'error', 400, {'Access-Control-Allow-Credentials': 'true'}
    elif 'group_name' == name:
        cur = g.db.cursor()
        old_groud = cur.execute('SELECT group_id FROM groups WHERE group_name = ?', (value, )).fetchall()
    elif 'email' == name:
        cur = g.db.cursor()
        old_groud = cur.execute('SELECT group_id FROM groups WHERE email = ?', (value,)).fetchall()
    else:
        return 'error', 400, {'Access-Control-Allow-Credentials': 'true'}
    if not old_groud:
        return 'unregistered', 404, {'Access-Control-Allow-Credentials': 'true'}
    else:
        return 'registered', 200, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/register', methods=['POST'])
def register():
    group_name = request.form.get('group_name')
    email = request.form.get('email')
    password = request.form.get('password')
    grade = request.form.get('grade')
    if not group_name or not email or not password or not grade:
        return 'error', 400, {'Access-Control-Allow-Credentials': 'true'}
    cur = g.db.cursor()
    old_groud = cur.execute('SELECT group_id FROM groups WHERE group_name = ? OR email = ?',
                            (group_name, email)).fetchall()
    if old_groud:
        return 'registed', 403, {'Access-Control-Allow-Credentials': 'true'}
    cur.execute('INSERT INTO groups VALUES (null, ?, ?, ?, "", "", "", ?)', (group_name, grade, email, password))
    g.db.commit()
    group_id = cur.execute('SELECT group_id FROM groups WHERE group_name = ?', (group_name, )).fetchall()[0][0]
    session['group_id'] = group_id
    return 'success', 200, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/detail', methods=['POST'])
def detail():
    group_id = session.get('group_id')
    if not group_id:
        return 'error', 403, {'Access-Control-Allow-Credentials': 'true'}
    cur = g.db.cursor()
    old_group = cur.execute('SELECT * FROM groups WHERE group_id = ?', (group_id,)).fetchall()
    if not old_group:
        return 'error', 404, {'Access-Control-Allow-Credentials': 'true'}
    members = request.form.get('members')
    work_name = request.form.get('work_name')
    work_description = request.form.get('work_description')
    cur.execute('UPDATE groups SET members = ?, work_name = ?, work_description = ? WHERE group_id = ?',
                (members, work_name, work_description, group_id))
    g.db.commit()
    return 'ok', 200, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/vote')
def vote():
    token = request.args.get('token')
    try:
        group_id = int(request.args.get('group_id'))
    except:
        return 'error', 400, {'Access-Control-Allow-Credentials': 'true'}
    if not token or not group_id:
        return 'error', 400, {'Access-Control-Allow-Credentials': 'true'}
    cur = g.db.cursor()
    old_vote = cur.execute('SELECT vote_id, vote1, vote2, vote3 FROM votes WHERE token = ?', (token, )).fetchall()
    if not old_vote:
        return 'error', 400, {'Access-Control-Allow-Credentials': 'true'}
    group_name = cur.execute('SELECT group_name FROM groups WHERE group_id = ?', (group_id, )).fetchall()
    if not group_name:
        return 'error', 404, {'Access-Control-Allow-Credentials': 'true'}

    old_vote = list(old_vote[0])
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
    cur.execute('UPDATE votes SET vote1 = ?, vote2 = ?, vote3 = ? WHERE token = ?',
                (old_vote[1], old_vote[2], old_vote[3], token))
    g.db.commit()
    return group_name[0][0], 200, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return 'error', 400, {'Access-Control-Allow-Credentials': 'true'}
    else:
        cur = g.db.cursor()
        old_group = cur.execute('SELECT group_id, password FROM groups WHERE email = ?', (email, )).fetchall()
        if not old_group:
            return 'no one', 404, {'Access-Control-Allow-Credentials': 'true'}
        old_group = old_group[0]
        if old_group[1] != password:
            return 'wrong', 403, {'Access-Control-Allow-Credentials': 'true'}
        session['group_id'] = old_group[0]
        return 'ok', 200, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/logout')
def logout():
    session['group_id'] = None
    return 'logout', 200, {'Access-Control-Allow-Credentials': 'true'}


@app.route('/send_email', methods=['POST'])
def send_email():
    to_addr = request.form.get('email')
    if not to_addr:
        return 'bad', 400, {'Access-Control-Allow-Credentials': 'true'}
    cur = g.db.cursor()
    old_cote = cur.execute('SELECT * FROM votes WHERE email = ?', (to_addr, )).fetchall()
    if not old_cote:
        token = md5(str(time.time()).encode('ascii')).hexdigest()
        cur.execute('INSERT INTO votes VALUES (null, ?, ?, ?, 0, 0, 0)', (to_addr, token, False))
        g.db.commit()
    else:
        token = old_cote[0][2]
    try:
        from_name = '[SS::STA - Web]Keyboard L'  # 发件人名
        from_addr = 'keyboard-l@outlook.com'  # 发件地址
        to_addr = to_addr  # 收件地址
        subject = '软为黑客松 - 投票链接'  # 邮件主题
        # 邮件正文
        html = """<p>您的投票链接为：</p>
<p><a href='http://hackathon.sssta.org/visit.html?token=%s'>http://hackathon.sssta.org/visit.html?token=%s</a><p>
<p>单击该链接进入投票页面，进行投票</p>
<p>该链接带有唯一标识，请勿使用他人的投票链接投票，也不应该将该链接分享给他人</p>
<p>每个邮箱只能投出3票，重复点击投票按钮可以 投票/取消投票</p>
<p>在最终计票前，你可以通过投票链接随时修改您的选择</p>
<p>链接可重复使用，重复填写该邮箱只能获得重复的投票链接</p>""" % (token, token)
        password = '1998lyhCYT'  # 邮箱密码
        smtp_server = 'smtp-mail.outlook.com'  # 邮件服务器

        msg = MIMEMultipart('alternative')  # 创建邮件
        msg['From'] = formataddr((Header(from_name, 'utf-8').encode(), from_addr))  # 发件人
        msg['Subject'] = Header(subject, 'utf-8').encode()  # 主题

        # 构造正文
        msgHTML = MIMEText(html, 'html', 'utf-8')
        msg.attach(msgHTML)

        # 发送
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.set_debuglevel(False)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        cur.execute('UPDATE votes SET status = 1 WHERE email = ?', (to_addr, ))
        return 'success', 200, {'Access-Control-Allow-Credentials': 'true'}
    except:
        cur.execute('UPDATE votes SET status = 0 WHERE email = ?', (to_addr, ))
        return 'error', 404, {'Access-Control-Allow-Credentials': 'true'}
    finally:
        g.db.commit()


@app.route('/final_groups')
def final_groups():
    cur = g.db.cursor()
    groups_old = cur.execute(
        'SELECT group_id, group_name, grade, members, work_name, work_description FROM groups ORDER BY grade, group_id').fetchall()
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


@app.route('/final_vote')
def final_vote():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
