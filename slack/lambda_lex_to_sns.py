from __future__ import print_function

import json
import boto3
import os
import datetime
import time
import os
import logging
import json


logger = logging.getLogger()
logger.setLevel(logging.INFO)

class LexEvent:
    """handles incoming and outgoing params to Lex and validates slots"""

    def __init__(self, event):
        self.event = event
        self.slots = event['currentIntent']['slots']
        self.intent = event['currentIntent']['name']
        self.input_text = event['inputTranscript']
        self.sess_attr = event['sessionAttributes']
        self.invocation = event['invocationSource']


    ### Helpers to control state of the conversation

    def delegate(self, intent=None):
        return {
            'sessionAttributes': self.sess_attr,
            'dialogAction': {
                'type': 'Delegate',
                'slots': self.slots
            }
        }

    def fulfill(self, msg="Your document is complete."):
        return {
            'sessionAttributes': self.sess_attr,
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled',
                "message": {
                  "contentType": "PlainText",
                  "content": msg
                }
            }
        }



    def elicit_slot(self, err):
        return {
            'sessionAttributes': self.sess_attr,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': self.intent,
                'slots': self.slots,
                'slotToElicit': err['violatedSlot'],
                'message': {'contentType': 'PlainText', 'content': err['message'] }
            }
        }

    def elicit_intent(self, msg="How can I help you?"):
        return {
             "sessionAttributes": self.sess_attr,
             "dialogAction": {
                "type": "ElicitIntent",
                "message": {
                  "contentType": "PlainText",
                  "content": msg
            }
        }
    }

    #### Slot Validators

    def val_error(self, slot, msg):
        res = {"isValid": False, "violatedSlot": slot, 'message': msg }
        return res

    def validates_presence(self, slot, msg=None):
        if not self.slots[slot]: # raise val_error
            if not msg:
                msg = "What is the {}?".format(slot)
            err = self.val_error(slot, msg)
            return self.elicit_slot(err)

    def validates_in(self, iterable, slot, msg=None):
        if self.slots[slot] not in iterable:
            if not msg:
                iter_list = ", ".join([str(x) for x in iterable])
                msg = "Your {0} must be one of the following: {1}".format(slot, iter_list)
            err = self.val_error(slot, msg)
            return self.elicit_slot(err)

    def validates_length(self, rng, slot, msg=None):
        if not self.slots[slot]: return
        # rng = (min, max)
        if len(self.slots[slot]) > rng[1]:
            if not msg:
                msg = "Your {0} is too large. I can handle {1} characters max.".format(slot, rng[1])
            err = self.val_error(slot, msg)
            return self.elicit_slot(err)

        if len(self.slots[slot]) < rng[0]:
            if not msg:
                msg = "Your {0} is too small. I need at least {1} characters.".format(slot, rng[0])
            err = self.val_error(slot, msg)
            return self.elicit_slot(err)


    def validates_pattern(self, regex, slot, msg=None):
        if not self.slots[slot]: return

        pattern = re.compile(regex)
        if not pattern.match(self.slots[slot]):
            if not msg:
                msg = "Your {0} seems to have an invalid format".format(slot)
            err = self.val_error(slot, msg)
            return self.elicit_slot(err)


    def run_validation(self, validators):
        for error in validators:
            if error:
                return error

        return lex.delegate()



def lambda_handler(event, context):
    """
        Lambda receives Lex Intent and sends a notification to SNS
    """

    logger.info(('INPUT', event))
    lex = LexEvent(event)
    client = boto3.client("sns")

    snsSendDeletion = os.environ['SNS_SEND_DELETION']
    snsSendCancelation = os.environ['SNS_SEND_CANCELATION']
    snsResult  = ""

    try:
        if lex.intent == "SwitchOffCancel":
            snsResult= snsSendCancelation
            message = lex.fulfill("The termination of stack is canceled")
        if lex.intent == "SwitchOffTerminate":
            message = lex.fulfill("The termination of stack is starting. You can cancel if needed.")
            snsResult = snsSendDeletion
        else:
            message = lex.fulfill("I don't understand your request")
        """
        if not snsResult
            client.publish(
                TopicArn=snsResult,
                Message=json.dumps("")
        """
        return message
    except Exception as e:
        logger.error(e)
        return lex.fulfill("There is an error, Could you contact Ops Team")
