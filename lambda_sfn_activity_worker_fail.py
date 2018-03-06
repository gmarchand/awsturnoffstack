import boto3
import json
import time
import os


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    print("Cancel Event from SNS to SFN")
    client = boto3.client("stepfunctions")
    activityArn = os.environ['ACTIVITY_ARN']
    
    print("Polling Activity Task")
    response = client.get_activity_task(
        activityArn=activityArn,
        workerName='LambdaWorker'
    )
    print(response)

    print("Send task success")
    client.send_task_failure(
        taskToken=response["taskToken"]
    )
    return ""

