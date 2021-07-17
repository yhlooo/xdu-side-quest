import sqlite3
import time
from hashlib import md5
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


def send_email(db, to_addr, weight):
    cur = db.cursor()
    old_cote = cur.execute('SELECT * FROM finalVotes WHERE email = ?', (to_addr, )).fetchall()
    if not old_cote:
        token = md5(str(time.time()).encode('ascii')).hexdigest()
        cur.execute('INSERT INTO finalVotes VALUES (null, ?, ?, ?, ?, 0, 0, 0, 0)', (to_addr, token, 0, weight))
        db.commit()
    else:
        token = old_cote[0][2]
    try:
        from_name = 'SS::STA - KeybrL'  # 发件人名
        from_addr = 'keyboard-l@outlook.com'  # 发件地址
        to_addr = to_addr  # 收件地址
        subject = '软为黑客松 - 决赛投票链接'  # 邮件主题
        # 邮件正文
        html = """<p>您的投票链接为：</p>
<p><a href='http://hackathon.sssta.org/final_vote.html?token=%s'>http://hackathon.sssta.org/final_vote.html?token=%s</a><p>
<p>单击该链接进入投票页面，进行投票</p>
<p>该链接带有唯一标识，请勿使用他人的投票链接投票，也不应该将该链接分享给他人</p>
<p>每个邮箱只能投出4票，重复点击投票按钮可以 投票/取消投票</p>
<p>在最终计票前，你可以通过投票链接随时修改您的选择</p>""" % (token, token)
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
        cur.execute('UPDATE finalVotes SET status = 1 WHERE email = ?', (to_addr, ))
        print(to_addr, 'success')
    except:
        cur.execute('UPDATE finalVotes SET status = 0 WHERE email = ?', (to_addr, ))
        print(to_addr, 'error')
    finally:
        db.commit()


judges = [
]
groups = [
]

conn = sqlite3.connect('../db.sqlite')
for i in judges:
    send_email(conn, i, 2)
for i in groups:
    send_email(conn, i, 1)
conn.close()
