import boto3
import os

class notif():
    def __init__(self):
        if 'PHONE' in os.environ:
            print("SMS phone ", os.environ["PHONE"])
        else:
            print("SMS phone Not Define")
        self.cl = boto3.client( "sns",
                region_name="us-west-1")

    def sms(self,msg):
        if 'PHONE' in os.environ:
            to=os.environ["PHONE"] # +19992224444
            self.cl.publish(PhoneNumber=to,Message=msg)
        else:
            print("(dry run) sending SMS")

    def email(self):
        pass
