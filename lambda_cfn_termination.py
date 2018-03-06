import boto3
import json
import time
import os

class AwsCloudFormationException(Exception): pass

# @TODO : Add IAM Policy based on tag parameter : http://garbe.io/blog/2017/07/17/cloudformation-hacks/

def lambda_handler(event, context):
    tagsparam = os.environ['CFN_TAGS']
    tagsparamdict = [i.split(':') for i in tagsparam.split(",")]

    client = boto3.client("cloudformation")

    " List all stacks"
    stacks = []
    for page in client.get_paginator('describe_stacks').paginate():
        stacks += page["Stacks"]

    " compare each tag of each stack to each tag of cfn param "
    output = {'cancel': False, 'terminate': True, 'stack': []}

    for stack in stacks:
        for tag in stack["Tags"]:
            for tagparam in tagsparamdict:
                if tag['Key'] == tagparam[0] and tag['Value'] == tagparam[1]:
                    print('terminate stack %s', stack['StackId'])
                    output['terminate'] = True
                    output['stack'].append(stack['StackId'])

    return output