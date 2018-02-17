import boto3
import json
import time
import os

class AwsCloudFormationException(Exception): pass

# @TODO : Add IAM Policy based on tag parameter : http://garbe.io/blog/2017/07/17/cloudformation-hacks/
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    # find tags and verify format
    print("Terminate cfn stack")
    client = boto3.client("cloudformation")
    response = client.list_stacks()
    iterator = client.get_paginator('describe_stacks')
    output = json.dumps({'cancel': False, 'terminate': True})
    return output