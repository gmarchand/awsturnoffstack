from __future__ import print_function

import json
import boto3
import os

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    client = boto3.client("stepfunctions")
    activityArn = os.environ['ACTIVITY_ARN']
    taskOutput = os.environ['ACTIVITY_TASK_OUTPUT']

    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)

    response = client.get_activity_task(
        activityArn=activityArn,
        workerName='LambdaSnsToSfnActivity'
    )
    print(response)
    
    taskToken = response["taskToken"]
    #output = json.dumps({'cancel':True,'terminate':False})
    output = json.dumps(taskOutput)
    response = client.send_task_success(
        taskToken=response["taskToken"],
        output=output
    )
    print(response)
    
    return ""
