from __future__ import print_function

import json
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
        Lambda receives Lex Intent and sends a notification to SNS
    """

    client = boto3.client("stepfunctions")
    snsSendDeletion = os.environ['SNS_SEND_DELETION']
    snsSendCancelation = os.environ['SNS_SEND_CANCELATION']
    logger.info("Lex Event : %s", event)
    """"    
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
    """"