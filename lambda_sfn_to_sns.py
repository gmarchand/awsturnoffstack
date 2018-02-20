from __future__ import print_function

import json
import boto3
import os

def lambda_handler(event, context):
    print("Received Task from SFN to SNS")
    print("Received event: " + event)
    snsTopicSendNotif = os.environ['SNS_SEND_NOTIF_ARN']
    snsTopicTerminateAction = os.environ['SNS_TERMINATE_ACTION_ARN']

    return ""
