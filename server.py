import os
import asyncio
import json
import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
from multiprocessing import Process
from flask import (Flask, request, jsonify)
from flask_cors import (CORS, cross_origin)
from controllers.integrations.kafka.consumer import kafka_consumer
from controllers.integrations.kafka.producer import kafka_producer
from controllers.open_ai_controller.open_ai_controller import OPENAI
open_ai_instance = OPENAI()
load_dotenv()
app = Flask(__name__)
cors = CORS(app, allow_headers=['Content-Type', 'Access-Control-Allow-Origin',
                                'Access-Control-Allow-Headers', 'Access-Control-Allow-Methods', 'Authorization'])


@app.route('/send-reply', methods=['POST'])
def send_reply():
    try:
       payload = json.loads(request.data)
       print('Webhook received:', payload)
   
       ## send the filtered story to node server
       producer_instance =  kafka_producer()
       producer_instance.send_reply(payload)
       return jsonify(payload), 200
    except Exception as e:
       error_message = {'error': str(e)}
       return jsonify(error_message), 500


def parallelize_functions(*functions):
    processes = []
    print("Starting multiple processes")
    for function in functions:
        p = Process(target=function)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


   
def runServer(): 
    try:
        print("server working")
    except Exception as e: 
        print("error")


   

def start_server():
    print("Starting server")
    app.run(host='0.0.0.0', port=5009, threaded=True)
def start_kafka_instances():
    consumer =  kafka_consumer()
    asyncio.run(consumer.start_consumers())


    
if __name__ == '__main__':
    parallelize_functions(start_kafka_instances, start_server)    