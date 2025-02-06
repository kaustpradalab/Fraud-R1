import os
from openai import OpenAI
import openai
import requests
import time
import json
import time

API_SECRET_KEY = "sk-zk2d3a435fa499305b7c89e78a0e4687a9c67a21fcfd4b1a";
BASE_URL = "https://api.zhizengzeng.com/v1/"

# chat
def chat_completions3(query):
    client = OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    #print(resp)
    print(resp.choices[0].message.content)

# chat with other model
def chat_completions4(query):
    client = OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)
    resp = client.chat.completions.create(
        model="qwen2.5-1.5b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    # print(resp)
    print(resp.choices[0].message.content)
query = "你是谁"
chat_completions4(query)