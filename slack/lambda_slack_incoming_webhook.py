from __future__ import print_function

import json
import boto3
import os

def lambda_handler(event, context):
    """
        Lambda receives SNS Notification and successes SFN Activity
            https://github.com/codediodeio/lex-chatbot-lambda/blob/master/bot.py

    """

    client = boto3.client("stepfunctions")
    activityArn = os.environ['ACTIVITY_ARN']

    response = client.get_activity_task(
        activityArn=activityArn,
        workerName='LambdaSnsToSfnActivity'
    )

    taskToken = response["taskToken"]
    output = json.dumps({'cancel':True,'terminate':False})
    response = client.send_task_success(
        taskToken=response["taskToken"],
        output=output
    )