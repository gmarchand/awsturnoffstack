import boto3
import json
import time
import os


def lambda_handler(event, context):
    """
        SFN Task fails SFN Activity
    """

    client = boto3.client("stepfunctions")
    activityArn = os.environ['ACTIVITY_ARN']

    " Polling Activity Task "
    response = client.get_activity_task(
        activityArn=activityArn,
        workerName='LambdaWorker'
    )

    " Worker executes the activity task "
    client.send_task_failure(
        taskToken=response["taskToken"]
    )
    return ""

