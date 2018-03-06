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
    input = {}
    if type(event) is list:
        for element in event:
            if 'terminate' in element.keys():
              input = element
    if type(event) is dict and 'terminate' in event.keys():
        input = event
    client.publish(
        TopicArn=snsTopicSendNotif,
        Message=json.dumps(input)
    )
    if input['terminate']:
        """ If input has terminate=true, send a SNS notification to terminate ressources """
        client.publish(
            TopicArn=snsTopicTerminateAction,
            Message=json.dumps(input)
        )
