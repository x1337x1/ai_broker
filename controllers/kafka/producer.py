import os
from dotenv import load_dotenv
from confluent_kafka import Producer
from constants.kafka_topics import TOPIC_REPLY_QUERY
import json

load_dotenv()

kafka_server = os.getenv('KAFKA_URL')
print("> kafka host <", kafka_server)


class kafka_producer:
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': kafka_server})


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def serialize(self, data):
      try:
        return bytes(json.dumps(data), "utf-8")
      except Exception as e:
        print(f"Serialization error: {e}")
        return None 
      

def send_reply(self, message):
    self.producer.poll(0)
    self.producer.produce(TOPIC_REPLY_QUERY, mvalue=self.serialize(message), callback= delivery_report)
    self.producer.flash()

  

