import boto3
import json

ec2client = boto3.client('ec2')

def lambda_handler(event, context):
    print("Coming inside lambda handler")
    reg = ec2client.describe_regions()
    return { 
        "statusCode" : 200, 
        "body" : json.dumps({"message":reg['Regions']})
    }

if __name__ == "__main__":
    print(lambda_handler(None,None))
