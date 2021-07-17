import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import sqlite3

conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()
groups_list = cur.execute('SELECT group_id, group_name, email FROM groups').fetchall()
conn.close()

for i in groups_list[:2]:
    try:
        from_name = '[SS::STA - Web]Keyboard L'  # 发件人名
        from_addr = 'keyboard-l@outlook.com'  # 发件地址
        to_addr = i[2]  # 收件地址
        subject = '软为黑客松 - 报名成功'  # 邮件主题
        # 邮件正文
        html = """
<h2>报名成功</h2>
<p>恭喜你，你的团队“%s”已成功报名“软为”Hackathon</p>
<p>请加入比赛QQ答疑群：软为清明黑客松（578076813）</p>
<p>我们将在2018.03.31在QQ答疑群发布比赛题目，题目也会在该网站主页和“参观”页展示，请注意适时查看。</p>
<p>2018.04.04可开始实现你们的作品，上交作品的最后期限是2018.04.06 20:00，请完成后及时提交</p>
<p>2018.04.07 6:00前我们会公示进入下一论评选的团队，并于当天09:00组织集中展示和评选，请留意QQ答疑群中的公告和相关通知邮件</p>
<p>比赛最终结果会于2018.04.07的最后评选后公示，比赛奖品将在当时送出</p>
<hr>
<p>
    这是报名确认邮件，无需回复，对此若有疑问请联系该项负责人<a href="mailto: keyboard-l@outlook.com">keyboard-l@outlook.com</a>
</p>
<p>关于比赛的更多细节或疑问，请加入比赛交流QQ群（578076813）交流或询问，或发送邮件到该邮件发件人</p>""" % (i[1])

        password = '******'  # 邮箱密码
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
        print(i[0], i[1], 'success')
    except:
        print(i[0], i[1], i[2], 'fail')
