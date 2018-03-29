from __future__ import print_function

import json
import boto3
import os
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
        Lambda receives SNS Notification and push it to slack


    """
    webhook_url = os.environ['SLACK_WEBHOOK_URL']

    slack_data = {'text': json.dumps(event)}
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        logger.error('Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text))
