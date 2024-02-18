import os
from google.cloud import pubsub_v1

PROJECT_ID = os.environ['PROJECT_ID']
publisher = pubsub_v1.PublisherClient()

#topic_path = publisher.topic_path(PROJECT_ID, "ENTRY")
#
#topic = publisher.create_topic(request={
#    "name": topic_path
#})
#
#subscriber = pubsub_v1.SubscriberClient()
#subscription_path = subscriber.subscription_path(PROJECT_ID, 'sub_to__ENTRY')
#
#with subscriber:
#    subscription = subscriber.create_subscription(request={
#        "name": subscription_path, 
#        "topic": topic_path
#    })
#
#print(f'Created topic: {topic.name}')
topic_path = publisher.topic_path(PROJECT_ID, "ENTRY")
publisher.publish(topic_path, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'.encode('utf-8')).result()
publisher.publish(topic_path, 'cccccccc-cccc-cccc-cccc-cccccccccccc'.encode('utf-8')).result()
publisher.publish(topic_path, 'gggggggg-gggg-gggg-gggg-gggggggggggg'.encode('utf-8')).result()
publisher.publish(topic_path, '55555555-5555-5555-5555-555555555555'.encode('utf-8')).result()
publisher.publish(topic_path, 'uuuuuuuu-uuuu-uuuu-uuuu-uuuuuuuuuuuu'.encode('utf-8')).result()
publisher.publish(topic_path, '9c5b94b1-35ad-49bb-b118-8e8fc24abf80'.encode('utf-8')).result()