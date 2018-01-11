from __future__ import print_function

import json
import boto3
print('Loading function')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print("Execute State Machine")

    client = boto3.client("stepfunctions")
    sfnArn = os.environ['SFN_ARN']
    

    response = client.start_execution(
        stateMachineArn=sfnArn,
        name='LambdaSfnExecute',
        input=''
    )
    print(response)
    
    return ""
