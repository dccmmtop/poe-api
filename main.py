import logging
import json

from bottle import route, run, request, response
from .poe.src import poe

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
    for chunk in client.send_message("capybara", message, with_chat_break=False):
      answer = answer+ chunk["text_new"]
    return answer
    # client.purge_conversation("capybara", count=3)

token = "Sd1cy17-57VEULwc19wcDw=="
poe.logger.setLevel(logging.INFO)
client = poe.Client(token,proxy="socks5://127.0.0.1:7890")
run(host='localhost', port=8080)