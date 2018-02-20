import time
import pprint

event = '{'terminate': False, 'cancel': False}'
print("Received Task from SFN to SNS")
print("Received event: " + str(event))

event_obj = json.loads(event)
if not event_obj['terminate'] and not event_obj['cancel']:
    print('start')
elif event_obj['terminate']:
    print('terminate')
elif event_obj['cancel']:
    print('cancel')
