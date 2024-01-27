import os
from dotenv import load_dotenv
from confluent_kafka import Consumer
from constants.kafka_topics import TOPIC_REPLY_QUERY, TOPIC_SEND_QUERY
import asyncio
import json
from controllers.open_ai_controller.open_ai_controller import OPENAI
open_ai_instance = OPENAI()

load_dotenv()

kafka_server = os.getenv('KAFKA_URL')
print("> kafka host <", kafka_server)


class kafka_consumer:
    def __init__(self):
        self.consumer_gr_1 = self.initialize_kafka_consumers()

    def initialize_kafka_consumers(self):
        try:
            consumer_gr_1 = Consumer({
                'bootstrap.servers': kafka_server, # kafka_url must be a string not an arary of strings
                'group.id': 'msg-broker-1', # Consumer group ID for the first consumer
                'auto.offset.reset': 'earliest', # Start consuming from the beginning if no offset is stored
                'enable.auto.commit': True, # Enable automatic committing of offsets
            })
         

            consumer_gr_1.subscribe([TOPIC_SEND_QUERY])
     
            print("Kafka consumers initialized successfully.")

            return consumer_gr_1

        except Exception as err:
          print(err)



    async def process_queries(self, consumer):
      try:
        while True:
            queues = consumer.poll(1.0)
            if queues is None:
                continue
            if queues.error():
               print("Consumer error: {}".format(queues.error()))
               continue

            topic = queues.topic()
            messages =  json.loads(queues.value())
            if(topic == TOPIC_SEND_QUERY):
               print('Received messages :>', messages)
               await open_ai_instance.process_query(messages)


      except KeyboardInterrupt:
            pass
      finally:
            # Leave group and commit final offsets
            consumer.close()     
        

    async def start_consumers(self):
        # Start processing messages with both consumers in parallel
            await asyncio.gather(
                self.process_queries(self.consumer_gr_1),
            )