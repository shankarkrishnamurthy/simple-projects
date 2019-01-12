#!/bin/env python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(whattest,platformname,useremail, param, mesg,error,html_result):
    controller_ip="10.217.220.171"
    me = "shankar@nts.citrite.net"
    you = useremail
    msg = MIMEMultipart('alternative')
    msg['Subject'] = whattest + " on " + platformname + " " + mesg
    msg['From'] = me
    msg['To'] = you
    if error:
        errorblock = """\
                    <div style="color:red; padding: 10px;">
                            The following error was observed when starting the test. <br>
                    """ + error + """ <br>
                    </div>"""
    else:
        errorblock = ""

    if html_result:
        html = """\
        <html>
          <head></head>
          <body style="background: #F5F5F5;font-size:12px;font-family:Helvetica,Arial">
                <h3>""" + whattest +  """ on """ + platformname + """</h3>
                <hr />
                <p> The exact command used to start the test is as follows </p>
                <br> """ + param + """ <br> """ + errorblock + """
                <p> Please click <a href="http://"""+ controller_ip +"""/platform/result/""" +\
                    str("inst") + """/">here </a> to see the test progress and results. </p>
                <p> """ + html_result + """</p>
                <hr />
                <div style="background: #444; color :#FFF;padding:5px">
                        This is an automated message from NetScaler Test Services. Do not reply.
           </div>
          </body>
        </html>
        """
    else:
       html = """\
        <html>
          <head></head>
          <body style="background: #F5F5F5;font-size:12px;font-family:Helvetica,Arial">
                <h3>""" + whattest +  """ on """ + platformname + """</h3>
                <hr />
                <p> The exact command used to start the test is as follows </p>
                <br> """ + str(param) + """ <br> """ + str(errorblock) + """
                <p> Please click <a href="http://"""+ controller_ip +"""/platform/result/""" +\
                    str(t) + """/">here </a> to see the test progress and results. </p>
                <p> """ + html_result + """</p>
                <hr />
                <div style="background: #444; color :#FFF;padding:5px">
                        This is an automated message from NetScaler Test Services. Do not reply.
           </div>
          </body>
        </html>
        """

    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()


if __name__ == "__main__":
    send_email("mytest","myplatform","shankar.krishnamurthy@citrix.com","params","my message",False,"htmlresult")
