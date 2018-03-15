import boto3
import json
import time
import os
import logging

class AwsCloudFormationException(Exception): pass


logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
        " List all cloudformation stacks "
        matchTagNb = 0
        for tag in stack["Tags"]:
            " List all tags of cloudformation tag "
            for tagparam in tagsparamdict:
                " List all tags of env var "
                if tag['Key'] == tagparam[0] and tag['Value'] == tagparam[1]:
                    matchTagNb += 1
                    print('tag %s:%s found for %s', tag['Key'],tag['Value'],stack['StackId'])
        if matchTagNb == len(tagsparamdict):
            "All tags of env var matched : destroy this tag"
            output['stack'].append(stack['StackId'])

    logger.info("List of stacks terminated : %s", json.dumps(output['stack']))

    return output
