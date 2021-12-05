import smtplib  #用于邮件的发信动作
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  #用于构建邮件内容


def sendemail(mail):
    if mail=="@qq.com":
        return
    smtp_server = "smtp.163.com"  #发信服务器
    asender = "micsamamsg@163.com"  #发件人地址
    text = '''
    你好，这里是Mic小助手
    今日体温填报成功！
    '''
    password = "SWRYVTPGWGMXIWQI"
    asubject = "填报成功提示！"  #邮件主题
    msg = MIMEMultipart()  #邮件设置
    msg["Subject"] = asubject
    msg["to"] = mail
    msg["from"] = "Mic小助手"
    print(msg)
    msg.attach(MIMEText(text, "plain", "utf-8"))  #添加邮件正文 #添加附件
    server = smtplib.SMTP_SSL(host="smtp.163.com")
    server.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息
    server.login(asender, password)
    server.sendmail(asender, [mail], msg.as_string())
    server.quit()
