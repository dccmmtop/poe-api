import logging
import json

import os
from bottle import route, run, request, response
from .poe.src import poe


client_list = []
ask_num = 0

@route('/api/v1/ask', method = 'POST')
def login():
    q = request.json.get('q')
    response.content_type = 'application/json'
    result = {
      'result':'OK',
      'data': ask(q)
    }
    return json.dumps(result)

def ask(message):
    answer = ""
    client = select_client()
    print(client.viewer["poeUser"]["id"] + "为你服务")
    #for chunk in client.send_message("capybara", message, with_chat_break=False):
    for chunk in client.send_message("chinchilla", message, with_chat_break=True):
      answer = answer+ chunk["text_new"]
    return answer
    # client.purge_conversation("capybara", count=3)

def select_client():
    global ask_num
    ask_num = ask_num + 1
    print(ask_num)
    return client_list[ask_num % len(client_list)]
  


poe.headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
  "Te": "trailers",
  "Upgrade-Insecure-Requests": "1"
}

poe.logger.setLevel(logging.INFO)
token_list_str = os.environ.get('poe_token')

for token in  token_list_str.split(","):
  client = poe.Client(token,proxy="http://127.0.0.1:7890")
  #client = poe.Client(token)
  client_list.append(client)
  

run(host='localhost', port=8080)

