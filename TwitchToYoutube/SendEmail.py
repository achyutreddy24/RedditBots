import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
#Import Settings from Config.py
try:
    import Config
    EPASSWORD = Config.EPASSWORD
    EUSERNAME = Config.EUSERNAME
except ImportError:
    print("Error Importing Config.py")
    
def send_mail(send_from, send_to, subject, text, files=None):
    #assert isinstance(send_to, list)

    msg = MIMEMultipart(
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg.attach(MIMEText(text))

    for f in files or []:
     with open(f, "rb") as fil:
         submsg = MIMEApplication(fil.read())
         sub msg.add_header('Content-Disposition', 'attachment', filename=f)
         msg.attach(submsg)
         

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    try:
        server.login(EUSERNAME, EPASSWORD)
        server.sendmail(send_from, send_to, msg.as_string())
    except smtplib.SMTPAuthenticationError:
        print("Invalid Password!")
    server.close()