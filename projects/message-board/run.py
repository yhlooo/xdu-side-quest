#!/usr/bin/python2
# -*- coding: utf-8 -*-
import flask
import sqlite3
import time
import hashlib

app = flask.Flask(__name__)


@app.route("/")
def index():
    resp = flask.make_response(flask.render_template('index.html'))
    resp.set_cookie('account', '')
    resp.set_cookie('password', '')
    return resp


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if flask.request.method == 'GET':
        return flask.render_template('sign_up.html')
    elif flask.request.method == 'POST':
        firstname = flask.request.form.get('firstname')
        lastname = flask.request.form.get('lastname')
        username = flask.request.form.get('username')
        account = flask.request.form.get('account')
        password = flask.request.form.get('password')
        repassword = flask.request.form.get('repassword')
        sex = flask.request.form.get('sex')
        country = flask.request.form.get('country')
        phonenumber = flask.request.form.get('phonenumber')
        wechat = flask.request.form.get('wechat')
        facebook = flask.request.form.get('facebook')
        twitter = flask.request.form.get('twitter')
        qq = flask.request.form.get('qq')
        if password != repassword:
            return flask.render_template(
                'sign_up.html',
                password_wrong=u'password_wrong',
                firstname=firstname,
                lastname=lastname,
                username=username,
                account=account,
                phonenumber=phonenumber,
                wechat=wechat,
                facebook=facebook,
                twitter=twitter,
                qq=qq
            )
        else:
            name_r = firstname + lastname
            connection = sqlite3.connect('cache.db')
            cursor = connection.cursor()
            old_account_username = cursor.execute('SELECT username FROM user WHERE account = ?', (account,)).fetchall()
            if old_account_username != []:
                cursor.close()
                connection.commit()
                connection.close()
                return flask.render_template(
                    'sign_up.html',
                    old_account=u'old_account',
                    firstname=firstname,
                    lastname=lastname,
                    username=username,
                    account=account,
                    phonenumber=phonenumber,
                    wechat=wechat,
                    facebook=facebook,
                    twitter=twitter,
                    qq=qq
                )
            else:
                password = hashlib.md5(password).hexdigest()
                cursor.execute('INSERT INTO user VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', (
                    firstname, lastname, username, account, password, sex, country, phonenumber, wechat, facebook,
                    twitter,
                    qq))
                if sex == 'male':
                    sex_r = u'先生'
                elif sex == 'female':
                    sex_r = u'女士'
                elif sex == 'gay':
                    sex_r = u'同志'
                cursor.close()
                connection.commit()
                connection.close()
                return flask.render_template('sign_up_success.html', name_r=name_r, sex_r=sex_r)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    elif flask.request.method == 'POST':
        connection = sqlite3.connect('cache.db')
        cursor = connection.cursor()
        account_i = flask.request.form.get('account')
        password_i = flask.request.form.get('password')
        password_s = cursor.execute('SELECT password FROM user WHERE account = ?', (account_i,)).fetchall()
        cursor.close()
        connection.commit()
        connection.close()
        if password_s == []:
            return flask.render_template('login.html', unsign=u'unsign')
        else:
            password_s = password_s[0][0]
            password_i = hashlib.md5(password_i).hexdigest()
            if password_s != password_i:
                return flask.render_template('login.html', account=account_i, password_wrong=u'password_wrong')
            else:
                connection = sqlite3.connect('cache.db')
                cursor = connection.cursor()
                username = cursor.execute('SELECT username FROM user WHERE account = ?', (account_i,)).fetchall()[0][0]
                all_message = cursor.execute('SELECT * FROM msg').fetchall()[::-1]
                cursor.close()
                connection.commit()
                connection.close()
                resq = flask.make_response(
                    flask.render_template('board.html', all_message=all_message, account=account_i, username=username))
                resq.set_cookie('account', account_i)
                resq.set_cookie('password', password_i)
                return resq


@app.route('/board', methods=['GET', 'POST'])
def board():
    account = flask.request.cookies.get('account')
    password = flask.request.cookies.get('password')
    if account == '' or password == '':
        return flask.render_template('login.html')
    else:
        connection = sqlite3.connect('cache.db')
        cursor = connection.cursor()
        password_s = cursor.execute('SELECT password FROM user WHERE account = ?', (account,)).fetchall()
        if password_s == []:
            return flask.render_template('login.html')
        else:
            password_s = password_s[0][0]
            if password_s != password:
                return flask.render_template('login.html')
            else:
                if flask.request.method == 'GET':
                    return get_board(account)
                elif flask.request.method == 'POST':
                    message = flask.request.form.get('message')
                    username = cursor.execute('SELECT username FROM user WHERE account = ?', (account,)).fetchall()
                    localtime = time.strftime('%Y/%m/%d %H:%M', time.localtime(time.time())).decode()
                    cursor.execute("INSERT INTO msg VALUES(?,?,?,?)", (username[0][0], account, localtime, message))
                    cursor.close()
                    connection.commit()
                    connection.close()
                    return get_board(account)


def get_board(account):
    connection = sqlite3.connect('cache.db')
    cursor = connection.cursor()
    username = cursor.execute('SELECT username FROM user WHERE account = ?', (account,)).fetchall()[0][0]
    all_message = cursor.execute('SELECT * FROM msg').fetchall()[::-1]
    cursor.close()
    connection.commit()
    connection.close()
    return flask.render_template('board.html', all_message=all_message, account=account, username=username)


connection = sqlite3.connect('cache.db')
cursor = connection.cursor()
try:
    try:
        cursor.execute('''CREATE TABLE user(
                        firstname VARCHAR(50),
                        lastname VARCHAR(50),
                        username VARCHAR(50),
                        account VARCHAR(50),
                        password VARCHAR(100),
                        country VARCHAR(10),
                        sex VARCHAR(10),
                        phonenumber VARCHAR(20),
                        wechat VARCHAR(20),
                        twitter VARCHAR(50),
                        facebook VARCHAR(50),
                        qq VARCHAR(20))''')
    except:
        pass
    try:
        cursor.execute('''CREATE TABLE msg(
                        username VARCHAR(50),
                        account VARCHAR(50),
                        time VARCHAR(20),
                        message VARCHAR(250))''')
    except:
        pass
except:
    pass
finally:
    cursor.close()
    connection.commit()
    connection.close()

if __name__ == "__main__":
    app.run(debug=True,port=80, host='0.0.0.0')
