from __future__ import print_function

import json
import boto3
import os
import time

def lambda_handler(event, context):

    """
        Lambda receives SNS Notification and executes SFN State Machine
    """

    sfnArn = os.environ['SFN_ARN']

    client = boto3.client("stepfunctions")

    client.start_execution(
        stateMachineArn=sfnArn,
        name=time.strftime('FromLambda%Y%m%d%H%M%S')
    )
