#!/bin/env python3
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.
with open("textfile") as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % "textfile"
msg['From'] = "shankar@linuxarium.com"
msg['To'] = "shankar.krishna@gmail.com"
#msg['To'] = "kshan_77@yahoo.com"
#msg['To'] = "shankar.krishnamurthy@citrix.com"
#msg['To'] = "shankar@localhost"

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
