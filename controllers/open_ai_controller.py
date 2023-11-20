import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
client = OpenAI()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class OpenAIController:
         
    def openAI(self ,query):     
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
              messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
            )
            print("Prompt :)", completion.choices[0].message)
            return completion.choices[0].message
