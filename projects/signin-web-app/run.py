#!/usr/bin/python2
# -*- coding: utf-8 -*-
from flask import Flask, request, session, g, redirect, url_for, render_template
from contextlib import closing
import sqlite3
import hashlib
import os
import math

# configuration
DATABASE = 'cache.db'
DEBUG = False
SECRET_KEY = os.urandom(987)
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# 欢迎页
@app.route("/", methods=['GET'])
def welcome():
    if session.get('account') is None:
        return render_template('welcome.html')
    else:
        return redirect(url_for('index'))


# 注册
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    cursor = g.db.cursor()
    if request.method == 'GET':
        return render_template('sign_up.html')
    elif request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        account = request.form.get('account')
        password = request.form.get('password')
        rePassword = request.form.get('rePassword')
        country = request.form.get('country')
        phoneNumber = request.form.get('phoneNumber')
        wechat = request.form.get('wechat')
        facebook = request.form.get('facebook')
        twitter = request.form.get('twitter')
        qq = request.form.get('qq')
        if password != rePassword:
            return render_template(
                'sign_up.html',
                password_wrong=u'password_wrong',
                firstName=firstName,
                lastName=lastName,
                account=account,
                phoneNumber=phoneNumber,
                wechat=wechat,
                facebook=facebook,
                twitter=twitter,
                qq=qq
            )
        else:
            name = firstName + lastName
            old_account_name = cursor.execute('SELECT name FROM user WHERE account = ?', (account,)).fetchall()
            if old_account_name:
                return render_template(
                    'sign_up.html',
                    old_account=u'old_account',
                    firstName=firstName,
                    lastName=lastName,
                    account=account,
                    phoneNumber=phoneNumber,
                    wechat=wechat,
                    facebook=facebook,
                    twitter=twitter,
                    qq=qq
                )
            else:
                password = hashlib.md5(password).hexdigest()
                cursor.execute('INSERT INTO user VALUES(?,?,?,?,?,?,?,?,?,"offline")',
                               (name, account, password, country, phoneNumber, wechat, facebook, twitter, qq))
                cursor.execute('CREATE TABLE user'+account+'(groupName varchar(50), groupId varchar(20), groupType '
                                                           'varchar(5))')
                g.db.commit()
                return render_template('sign_up_success.html', name=name)


# 登录
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    cursor = g.db.cursor()
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        account = request.form.get('account')
        password_i = request.form.get('password')
        password_s = cursor.execute('SELECT password FROM user WHERE account = ?', (account,)).fetchall()
        if not password_s:
            return render_template('login.html', unsign=u'unsigned')
        else:
            password_s = password_s[0][0]
            password_i = hashlib.md5(password_i).hexdigest()
            if password_s != password_i:
                return render_template('login.html', account=account, password_wrong=u'password_wrong')
            else:

                session['account'] = account
                session['password'] = password_i
                cursor.execute('UPDATE user SET status = "online" WHERE account = ?', (account,))
                g.db.commit()
                return redirect(url_for('index'))


# 登出
@app.route('/sign_out')
def sign_out():
    account = session.get('account')
    session.pop('account', None)
    cursor = g.db.cursor()
    cursor.execute('UPDATE user SET status = "offline" WHERE account = ?', (account,))
    g.db.commit()
    return render_template('login.html')


# 主页
@app.route('/index', methods=['GET', 'POST'])
def index():
    cursor = g.db.cursor()
    if session.get('account') is not None:
        account = session.get('account')
        name = cursor.execute('SELECT name FROM user WHERE account = ?', (account,)).fetchall()[0][0]
        myGroup = cursor.execute('SELECT groupId, groupName FROM user'+account+' WHERE groupType = "my"').fetchall()
        herGroup = cursor.execute('SELECT groupId, groupName FROM user'+account+' WHERE groupType = "her"').fetchall()
        return render_template('index.html', name=name, account=account, myGroup=myGroup, herGroup=herGroup)
    else:
        return render_template('login.html')


# 创建组
@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    cursor = g.db.cursor()
    if session.get('account') is None:
        return render_template('login.html')
    else:
        account = session.get('account')
        if request.method == 'GET':
            return render_template('createGroup.html')
        elif request.method == 'POST':
            groupName = request.form.get('groupName')
            groupId = cursor.execute('SELECT groupId FROM groups').fetchall()
            if not groupId:
                groupId = 10001
            else:
                groupId = 10001 + len(groupId)
            cursor.execute('INSERT INTO groups VALUES (?,?)', (groupName, groupId))
            cursor.execute('INSERT INTO user'+account+' VALUES (?,?,"my")', (groupName, groupId))
            cursor.execute('CREATE TABLE group'+str(groupId)+'(name VARCHAR(50), account VARCHAR(50), post VARCHAR('
                                                             '10), status VARCHAR(10))')
            g.db.commit()
            name = cursor.execute('SELECT name FROM user WHERE account = ?', (account,)).fetchall()[0][0]
            cursor.execute('INSERT INTO group' + str(groupId) + ' VALUES(?, ?,"host","close")', (name, account))
            cursor.execute('INSERT INTO group' + str(groupId) + ' VALUES("location","undefined","undefined",'
                                                                '"undefined")')
            g.db.commit()
            return render_template('createGroup_success.html', groupId=str(groupId))


# 查找组
@app.route('/search_group', methods=['GET', 'POST'])
def search_group():
    cursor = g.db.cursor()
    if session.get('account') is None:
        return render_template('login.html')
    else:
        if request.method == 'GET':
            return render_template('searchGroup.html')
        elif request.method == 'POST':
            account = session.get('account')
            groupId = request.form.get('groupId')
            groupName = cursor.execute('SELECT groupName FROM groups WHERE groupId = ?', (groupId,)).fetchall()
            if not groupName:
                return render_template('searchGroup.html', unsigned=u"unsigned")
            else:
                groupName = groupName[0][0]
                joinStatus = cursor.execute('SELECT groupName FROM user'+account+' WHERE groupId = ?', (groupId,)).fetchall()
                if not joinStatus:
                    joinStatus = "outside"
                else:
                    joinStatus = "inside"
                return render_template('joinGroup.html', groupId=groupId, groupName=groupName, joinStatus=joinStatus)


# 加入组
@app.route('/joingroup', methods=['GET', 'POST'])
def join_group():
    cursor = g.db.cursor()
    if session.get('account') is None:
        return render_template('login.html')
    else:
        account = session.get('account')
        if request.method == 'GET':
            return render_template('searchGroup.html')
        elif request.method == 'POST':
            groupId = request.form.get('groupId')
            joinStatus = cursor.execute('SELECT groupName FROM user' + account + ' WHERE groupId = ?',
                                        (groupId,)).fetchall()
            groupName = cursor.execute('SELECT groupName FROM groups WHERE groupId = ?', (groupId,)).fetchall()[0][0]
            name = cursor.execute('SELECT name FROM user WHERE account = ?', (account,)).fetchall()[0][0]
            if not joinStatus:
                cursor.execute('INSERT INTO user'+account+' VALUES(?,?,"her")', (groupName, groupId))
                cursor.execute('INSERT INTO group'+groupId+' VALUES(?, ?,"guest","close")', (name, account))
                g.db.commit()
            return render_template('joinGroup_success.html', groupId=groupId, groupName=groupName)


# 进入组界面
@app.route('/group/<path:groupId>', methods=['GET', 'POST'])
def into_group(groupId):
    cursor = g.db.cursor()
    if session.get('account') is None:
        return render_template('login.html')
    else:
        account = session.get('account')
        post, status = cursor.execute('SELECT post, status FROM group'+groupId+' WHERE account = ?', (account,)).fetchall()[0]
        groupName = cursor.execute('SELECT groupName FROM groups WHERE groupId = ?', (groupId,)).fetchall()[0][0]
        name = cursor.execute('SELECT name FROM user WHERE account = ?', (account,)).fetchall()[0][0]
        if post == 'guest':
            allPeople = len(cursor.execute('SELECT account FROM group' + groupId).fetchall()) - 1
            arrived = cursor.execute('SELECT status FROM group'+groupId).fetchall()
            count = 1
            for i in arrived[2::]:
                if i[0] == 'undefined':
                    continue
                elif i[0] == 'close':
                    count = 0
                    break
                elif i[0] >= '0.05':
                    count += 1
            return render_template('herGroup.html', name=name, account=account, groupId=groupId, groupName=groupName, status=status, number=(count, allPeople))
        else:
            members = cursor.execute('SELECT * FROM group' + groupId).fetchall()
            location = cursor.execute('SELECT account, post, status FROM group' + groupId + ' WHERE name = "location"').fetchall()[0]
            return render_template('myGroup.html', name=name, account=account, groupId=groupId, groupName=groupName, members=members, location=location)


# 签到
@app.route('/sign_on', methods=['POST'])
def sign_on():
    cursor = g.db.cursor()
    if session.get('account') is None:
        return render_template('login.html')
    else:
        account = session.get('account')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        accuracy = request.form.get('accuracy')
        groupId = request.form.get('groupId')
        extent = cursor.execute('SELECT status FROM group'+groupId+' WHERE post = "host"').fetchall()[0][0]
        centerLocation = cursor.execute('SELECT account,post,status FROM group'+groupId+' WHERE name = "location"').fetchall()
        centerLocation = (centerLocation[0][0], centerLocation[0][1], centerLocation[0][2])
        if extent == 'close':
            return redirect(url_for('into_group', groupId=groupId))
        else:
            probability = judge((latitude, longitude, accuracy), centerLocation, extent)
            cursor.execute('UPDATE group' + groupId + ' SET status = ? WHERE account = ?', (probability, account))
            g.db.commit()
            return redirect(url_for('into_group', groupId=groupId))


# 签到判决
def judge(selfLocation, centerLocation, extent):
    def distance(latitude1, latitude2, longitude1, longitude2):
        radLat1 = math.radians(latitude1)
        radLat2 = math.radians(latitude2)
        radLon1 = math.radians(longitude1)
        radLon2 = math.radians(longitude2)
        a = radLat1 - radLat2
        b = radLon1 - radLon2
        r = 6378137
        l = 2 * r * math.asin((math.sin(a / 2.) ** 2 + math.cos(radLat1) * math.cos(radLat2) * math.sin(b / 2.) ** 2) ** 0.5)
        return l

    def twoCircle(r1, r2, l):
        if r2 > r1:
            r1, r2 = r2, r1
        if r1 > l + r2:  # 整个被吞了
            return math.pi * r2 ** 2
        if r1 > l:  # 圆心被吞了
            dy = (r1 ** 2 - ((r1 ** 2 - r2 ** 2 + l ** 2) / (2 * l)) ** 2) ** 0.5
            a = 2 * math.asin(dy / r1)
            b = 2 * math.asin(dy / r2)
            s = math.pi * r2 ** 2 + r1 ** 2 / 2 * (a - math.sin(a)) - r2 ** 2 / 2 * (b - math.sin(b))
            return s
        elif r1 <= l - r2:  # 相离
            return 0
        elif r1 <= l:  # 普通相交
            dy = (r1 ** 2 - ((r1 ** 2 - r2 ** 2 + l ** 2) / (2 * l)) ** 2) ** 0.5
            a = 2 * math.asin(dy / r1)
            b = 2 * math.asin(dy / r2)
            s = r1 ** 2 / 2 * (a - math.sin(a)) + r2 ** 2 / 2 * (b - math.sin(b))
            return s

    def dProbability(x, dx):
        probability1 = (twoCircle(R1, x + dx, R) - twoCircle(R1, x, R)) / (math.pi * R1 ** 2)
        probability2 = twoCircle(T, R2, x) / (math.pi * R2 ** 2)
        return probability1 * probability2

    def integral(func, upperLimit, lowerLimit, d):
        dx = (upperLimit - lowerLimit) / d
        x = lowerLimit
        result = 0
        while x < upperLimit:
            result += func(x, dx)
            x += dx
        return result

    lat1 = float(selfLocation[0])
    lon1 = float(selfLocation[1])
    lat2 = float(centerLocation[0])
    lon2 = float(centerLocation[1])
    R = distance(lat1, lat2, lon1, lon2)
    R1 = float(centerLocation[2])
    R2 = float(selfLocation[2])
    T = float(extent)
    upper = R + R1
    lower = R - R1
    if lower <= 0:
        lower = 0.0001
    return integral(dProbability, upper, lower, 1000.)


# 签退
@app.route('/sign_off', methods=['POST'])
def sign_off():
    cursor = g.db.cursor()
    if session.get('account') is None:
        return render_template('login.html')
    else:
        account = session.get('account')
        groupId = request.form.get('groupId')
        cursor.execute('UPDATE group' + groupId + ' SET status = "undefined" WHERE account = ?', (account,))
        g.db.commit()
        return redirect(url_for('into_group', groupId=groupId))


# 开放签到
@app.route('/turn_on', methods=['POST'])
def turn_on():
    cursor = g.db.cursor()
    if session.get('account') is None:
        return render_template('login.html')
    else:
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        accuracy = request.form.get('accuracy')
        groupId = request.form.get('groupId')
        extent = request.form.get('extent')
        cursor.execute('UPDATE group' + groupId + ' SET status = "undefined"')
        cursor.execute('UPDATE group' + groupId + ' SET status = ? WHERE post = "host"', (str(extent),))
        cursor.execute('UPDATE group' + groupId + ' SET account = ?, post = ?, status = ? WHERE name = "location"',
                       (latitude, longitude, accuracy))
        g.db.commit()
        return redirect(url_for('into_group', groupId=groupId))


# 关闭签到
@app.route('/turn_off/<path:groupId>')
def turn_off(groupId):
    cursor = g.db.cursor()
    if session.get('account') is None:
        return render_template('login.html')
    else:
        cursor.execute('UPDATE group' + groupId + ' SET status = "close"')
        cursor.execute('UPDATE group' + groupId + ' SET account = "undefined", post = "undefined", status = "undefined" WHERE name = "location"')
        cursor.execute('UPDATE group'+groupId+' SET status = "close" WHERE post = "host"')
        g.db.commit()
        return redirect(url_for('into_group', groupId=groupId))


# 获取定位测试页
@app.route('/locate')
def locate():
    return render_template('location.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
