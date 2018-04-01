#!/usr/bin/env python
#title           :mobileAlert.py
#description     : notifies remote user
#author          :
#email           :
#date            :09.01.2018
#version         :2
#notes           :A patched version of the non ADC code to utilize the MC USB 16808 ADC
#python_version  :3.6 (Tested)
#==============================================================================



import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Adapted from http://naelshiab.com/tutorial-send-email-python/
# we could also try pcs.rogers.com, but it might be a subscription service

gmail_user = 'QDGLab@gmail.com'
gmail_password = ''

# sends an individualized email to each address
def notify(text, recipients = []): 

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['Subject'] = text[:10] + '...'

    msg.attach(MIMEText(text, 'plain'))

#    filename = "<file>.xyz"
#    attachment = open("path of <file>.xyz", "rb")
#    part = MIMEBase('application', 'octet-stream')
#    part.set_payload((attachment).read())
#    encoders.encode_base64(part)
#    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
#    msg.attach(part)

    try:

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        for r in recipients:
            msg['To'] = r
            server.sendmail(gmail_user, r, msg.as_string())
        server.close()
        return 0
    except Exception as e:
        print('There was an error sending a notification to the user:')
        print(e)
        return e

if __name__ == '__main__':
    notify('This is a test notification through email and sms')
