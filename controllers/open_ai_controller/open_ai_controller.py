import os
from openai import OpenAI
from dotenv import load_dotenv
from controllers.integrations.kafka.producer import kafka_producer
import json
import pydash
OPENAI_KEY = os.getenv('OPENAI_API_KEY ')
load_dotenv()

class OPENAI:
    def __init__(self):
        self.client = OpenAI()
        
    async def process_query(self, message):
        print("processing query >_<")
        msg_in_queue = message
        query = pydash.get(msg_in_queue, 'query', default= "")
        stories = pydash.get(msg_in_queue, 'stories', default= "")
        print('incoming data', query, stories)
        message = [
            {"role": "system", "content": "You are an assistant, skilled in filtering stories and identifying story content with excellent accuracy."},
            {"role": "user", "content": f'My question is: {query}. Here are some stories: {stories}. and only replay with the story title'}
        ]

        completion = self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages= message
        )
        answer = completion.choices[0].message
        print("open ai answer :) " ,answer)
        p = kafka_producer()
        p.send_reply(answer) 

        return answer


    