  Description:
    Lambda fn() Get EC2 regions using boto3
    Use sam tool to test and deploy (command line)

  steps:
    1. sam init --runtime python3.7 --name aws-sam-lambda-fn
        # this scaffolds the lambda dir [options ->1(quick template) -> 1(zip) ->1 (hello)]
    2. change template.yaml
        - Resources
        - Outputs
    3. Create role
        - <ac>:role/myLambdaRole
            - with 'Trust relationship' = lambda.amazonaws.com
            - with Permissions = AmazonEC2FullAccess,AWSLambdaBasicExecutionRole
    4. sam local invoke --no-event --debug # run lambda function locally
    5. sam local start-api      # start api gateway locally

    prereq:
    6. create s3 bucket: aws s3 mb s3://shankar-tbr-lambda-sam-demo

    7.  sam package --template-file template.yaml --output-template-file deploy.yaml --s3-bucket shankar-tbr-lambda-sam-demo
    8.  sam deploy --template-file <path from 7>/deploy.yaml --stack-name my-lambda-stack-sam --capabilities CAPABILITY_IAM

    run:
    9.  curl -k https://tr4u4p7xji.execute-api.us-west-1.amazonaws.com/Prod/getec2regions/ | jq
        
    cleanup:
    10. aws cloudformation delete-stack --stack-name my-lambda-stack-sam
    11. aws s3 rb s3://shankar-tbr-lambda-sam-demo

