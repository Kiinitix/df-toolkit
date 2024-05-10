import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from configparser import ConfigParser

def mail():
    configur = ConfigParser()
    configur.read('configurations.ini')

    msg = MIMEMultipart()

    msg['Subject'] = 'Test mail with attachment'
    msg['From'] = configur.get('SMTPlogin', 'sender_address')
    msg['To'] = configur.get('SMTPlogin', 'receiver_address')

    filename = 'private_key.pem'
    with open(filename, 'r') as f:
        part = MIMEApplication(f.read(), Name=basename(filename))
    
    filename1 = 'public_key.pem'
    with open(filename, 'r') as f:
        part1 = MIMEApplication(f.read(), Name=basename(filename1))

    part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
    msg.attach(part)
    msg.attach(part1)
    

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login(configur.get('SMTPlogin', 'mailtrap_user'), configur.get('SMTPlogin', 'mailtrap_password'))
        server.sendmail(configur.get('SMTPlogin', 'sender_address'), configur.get('SMTPlogin', 'receiver_address'), msg.as_string())
        print("Successfully sent email")

    print("Mail sent!!!")

