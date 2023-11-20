import os
import asyncio
import json
import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
from multiprocessing import Process
from flask import (Flask, request, jsonify)
from flask_cors import (CORS, cross_origin)
from controllers.open_ai_controller import OpenAIController
openai_controller = OpenAIController()


load_dotenv()
app = Flask(__name__)
cors = CORS(app, allow_headers=['Content-Type', 'Access-Control-Allow-Origin',
                                'Access-Control-Allow-Headers', 'Access-Control-Allow-Methods', 'Authorization'])

   
def runServer(): 
    try:
        print("server working")
    except Exception as e: 
        print("error")

@app.route('/answer', methods=['POST'])
@cross_origin()
def get_ai_reply():
    try:
        req = request.json
        prompts = req["prompt"]
        ai_reply = openai_controller.openAI(prompts)
        return jsonify({"result": ai_reply})     
    except Exception as e: 
        print("error")
        return jsonify({"error": str(e)})

   

def start_server():
    print("Starting server")
    app.run(host='0.0.0.0', port=5009, threaded=True)

    
if __name__ == "__main__":
    start_server()