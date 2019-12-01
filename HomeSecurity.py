import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
from datetime import datetime
import os
import smtplib


from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email import encoders
gmail_user = "wasisaifniloy@gmail.com" #Sender email address
gmail_pwd = "01985654277" #Sender email password
to = "ibtida.wasi@gmail.com" #Receiver email address
subject = "Security Breach"
text = "There has been a security breach in your home. See the attached picture of the intruder."

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False

while True:
    previous_state = current_state
    current_state = GPIO.input(sensor)
    print(current_state)

    if current_state != previous_state:
        new_state = "HIGH" if current_state else "LOW"
        print("GPIO pin %s is %s" % (sensor, new_state))
        print(gmail_user)
    if current_state:
         cap = cv2.VideoCapture(-1)
         ret, frame = cap.read()
         print ("Saving Photo")
         picname = datetime.now().strftime("%y-%m-%d-%H-%M")
         picname = picname+'.jpg'
         cv2.imwrite(picname, frame)
         print ("Sending email")
         attach = picname
         msg = MIMEMultipart()
         msg['From'] = gmail_user
         msg['To'] = to
         msg['Subject'] = subject
         msg.attach(MIMEText(text))
         part = MIMEBase('application', 'octet-stream')
         part.set_payload(open(attach, 'rb').read())
         encoders.encode_base64(part)
         part.add_header('Content-Disposition',
         'attachment; filename="%s"' % os.path.basename(attach))
         msg.attach(part)
         mailServer = smtplib.SMTP("smtp.gmail.com", 587) #"smtp.gmail.com", 587
         mailServer.ehlo()
         mailServer.starttls()
         mailServer.ehlo()
         mailServer.login(gmail_user, gmail_pwd)
         mailServer.sendmail(gmail_user, to, msg.as_string())
         # Should be mailServer.quit(), but that crashes...
         mailServer.close()
         print ("Email Sent")
         os.remove(picname)
         
         cap.release()
         cv2.destroyAllWindows()
         
    
    


