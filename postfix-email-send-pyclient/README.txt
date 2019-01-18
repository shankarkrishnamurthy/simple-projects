Sending Email using Python email client
---------------------------------------
https://docs.python.org/3/library/email.examples.html
http://www.postfix.org/BASIC_CONFIGURATION_README.html

1. start a postfix local email MTA
2. run the below email client programs

--------------------------------
#!/bin/env python3
import smtplib
from email.message import EmailMessage

with open(textfile) as fp:
    msg = EmailMessage()
    msg.set_content(fp.read())

msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = "me@src.com"
msg['To'] = "me@yahoo.com"
s = smtplib.SMTP('localhost') # port 25 - run postfix
s.send_message(msg)
s.quit()
--------------------------

The incoming email addr is checked agains 'mydestination' and if its same, saved in the /var/mail/<user> file

=================================

******MAKE SURE PORT 25 IS NOT BLOCKED******

(email-test) [root@zela-f29 py-dir]# host citrix.com
citrix.com has address 162.221.156.156
citrix.com mail is handled by 20 sinpmail.citrite.net.
citrix.com mail is handled by 20 sjcpmail.citrite.net.
citrix.com mail is handled by 30 lonpmail.citrite.net.
citrix.com mail is handled by 10 mail.citrix.com.
(email-test) [root@zela-f29 py-dir]# host sjcpmail.citrite.net.
sjcpmail.citrite.net has address 10.9.164.206
(email-test) [root@zela-f29 py-dir]#
(email-test) [root@zela-f29 py-dir]# telnet 10.9.164.206 25
Trying 10.9.164.206...
Connected to 10.9.164.206.
Escape character is '^]'.

220 smtprelay.citrix.com Microsoft ESMTP MAIL Service ready at Fri, 11 Jan 2019 21:46:28 -0500
