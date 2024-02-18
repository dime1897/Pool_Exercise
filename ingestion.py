import os
from sys import argv
from google.cloud import pubsub_v1
from pool import Pool
import requests

def validate_user(user:str) -> bool:
    user = user.split('-')
    if (len(user)!=5) or (len(user[0])!=8) or (len(user[1])!=4) or (len(user[2])!=4) or (len(user[3])!=4) or (len(user[4])!=12):
        return False
    return True

PROJECT_ID = os.environ['PROJECT_ID']


def callback(message):
    message.ack()
    user = message.data.decode('utf-8')
    print("CHECKING FOR: "+user)
    if not validate_user(user):
        print("UUID non conforme.")
    result= requests.post('https://europe-west2-exercises-00.cloudfunctions.net/check_reservation', json={'user': user})
    if result.text=='True':
        print("APPROVED")
    else:
        print("PERMISSION DENIED")

if __name__=='__main__':
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, "sub_to__ENTRY")
    pull = subscriber.subscribe(subscription_path, callback=callback)
    try:
        pull.result()
    except Exception as e:
        print(e)
        pull.cancel()