import smtplib
import sqlite3
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

sql = sqlite3.connect('emails.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS emails(TITLE TEXT, MSG TEXT)')
print('Loaded Email Database')
sql.commit()

#Import Settings from Config.py
try:
    import Config
    EPASSWORD = Config.EPASSWORD
    EUSERNAME = Config.EUSERNAME
except ImportError:
    print("Error Importing Config.py")
    
def send_mail(send_from, send_to, subject, text, files=None):
    #assert isinstance(send_to, list)
    
    print(subject)
    
    cur.execute('SELECT * FROM emails WHERE TITLE=?', [subject])
    if not cur.fetchone():
        msg = MIMEMultipart(
            From=send_from,
            Date=formatdate(localtime=True),
            Subject=subject
        )
        msg.preamble = subject
        msg['Subject'] = subject
        msg['To'] = COMMASPACE.join(send_to)
        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, "rb") as fil:
                msg.attach(MIMEApplication(
                    fil.read(),
                    Content_Disposition='attachment; filename="Test.mp4";'# File name is not working, but youtube still uploads it so its fine for now
                ))
        
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        try:
            server.login(EUSERNAME, EPASSWORD)
            server.sendmail(send_from, send_to, msg.as_string())
            cur.execute('INSERT INTO emails VALUES(?, ?)', [subject, text])
            print("Email Sent, Title is:",subject)
        except smtplib.SMTPAuthenticationError:
            print("Invalid Password!")
        server.close()
    else:
        print("Already sent that email")