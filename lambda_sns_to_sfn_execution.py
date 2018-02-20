from __future__ import print_function

import json
import boto3
import os
import time

def lambda_handler(event, context):

    print("Execute State Machine")

    sfnArn = os.environ['SFN_ARN']

    client = boto3.client("stepfunctions")

    response = client.start_execution(
        stateMachineArn=sfnArn,
        name=time.strftime('FromLambda%Y%m%d%H%M%S')
    )
    print(response)
    return ""
