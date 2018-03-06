import os
import boto3
import json


def lambda_handler(event, context):
    """
        Send SNS Notifications from states of AWS StepFunctions
    """

    snsTopicSendNotif = os.environ['SNS_SEND_NOTIF_ARN']
    snsTopicTerminateAction = os.environ['SNS_TERMINATE_ACTION_ARN']

    client = boto3.client("sns")

    client.publish(
        TopicArn=snsTopicSendNotif,
        Message=json.dumps(event)
    )

    if event['terminate']:
        """ If input has terminate=true, so send a SNS notification to terminate the stack     """
        client.publish(
            TopicArn=snsTopicTerminateAction,
            Message=json.dumps(event)
        )
