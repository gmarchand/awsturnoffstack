from __future__ import print_function

import json
import boto3
print('Loading function')


def lambda_handler(event, context):
    print("Received Task from SFN to SNS")
    print("Received event: " + json.dumps(event, indent=2))

    snsArn = ''
    message = ''
    client = boto3.client("sns")

    response = client.publish(
        TargetArn=snsArn,
        Message=json.dumps(message)
    )
    return ""
