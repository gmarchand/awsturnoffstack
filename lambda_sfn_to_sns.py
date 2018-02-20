import os
import boto3


def lambda_handler(event, context):
    print("Received Task from SFN to SNS")
    snsTopicSendNotif = os.environ['SNS_SEND_NOTIF_ARN']
    snsTopicTerminateAction = os.environ['SNS_TERMINATE_ACTION_ARN']

    client = boto3.client("sns")
    client.publish(
        TopicArn=snsTopicSendNotif,
        Message=event
    )
    if event['terminate']:
        print('terminate')
        client.publish(
            TopicArn=snsTopicTerminateAction,
            Message=event
        )
