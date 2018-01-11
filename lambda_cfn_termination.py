import boto3
import json
import time
import os


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    print("Terminate cfn stack")
    client = boto3.client("cloudformation")
    response = client.list_stacks()
    iterator = client.get_paginator('describe_stacks')
    
    return "done"