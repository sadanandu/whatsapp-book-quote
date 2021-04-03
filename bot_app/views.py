from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import emoji
import random
import csv
import time
import os

curdir = os.path.dirname(__file__)

with open(os.path.join(curdir,'goodreads_health.csv'), 'r') as f:
    reader = csv.reader(f)
    index = 0
    health_dict = {}
    for row in reader:
        health_dict[index] = row
        index += 1
    health_quotes = index+1

with open(os.path.join(curdir,'goodreads_life.csv'), 'r') as f:
    reader = csv.reader(f)
    index = 0
    life_dict = {}
    for row in reader:
        life_dict[index] = row
        index += 1
    life_quotes = index + 1

with open(os.path.join(curdir,'goodreads_wealth.csv'), 'r') as f:
    reader = csv.reader(f)
    index = 0
    wealth_dict = {}
    for row in reader:
        wealth_dict[index] = row
        index += 1
    wealth_quotes = index + 1

@csrf_exempt
def index(request):
    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase
        incoming_msg = request.POST['Body'].lower()
        came_from = request.POST['WaId']
        # create Twilio XML response
        resp = MessagingResponse()
        msg = resp.message()
        if incoming_msg.lower() in ['hello', 'hey', 'hi', 'ola', 'hii', 'halo', 'helo']:
            response = emoji.emojize("""
*Hi! I am your Book-Quoter Bot* :wave:

*I want to help you be happy, motivated and healthy!!*

You can give me the following commands:
:black_small_square: *'Wealth':* A wealth related quote! :cash:
:black_small_square: *'Life'*: Tell me something about life :universe:
:black_small_square: *'Health'*: Health tip a day keeps doctor away! :heart:
            """, use_aliases=True)
            msg.body(response)
            return HttpResponse(str(resp))

        elif incoming_msg.lower() in ['money', 'finance', 'wealth']:
            response = get_quote(wealth_dict, wealth_quotes, came_from)
            msg.body(response)
            return HttpResponse(str(resp))

        elif incoming_msg.lower() in ['life', 'family']:
            response = get_quote(life_dict, life_quotes, came_from)
            msg.body(response)
            return HttpResponse(str(resp))

        elif incoming_msg.lower() in ['health', 'fitness', 'body']:
            response = get_quote(health_dict, health_quotes, came_from)
            msg.body(response)
            return HttpResponse(str(resp))

    return HttpResponse(str("Hello"))

def get_quote(category_dict, category_count, came_from):

    random.seed(int(came_from)-time.time())
    quote_row = category_dict[random.randrange(0, category_count-1)]

    return emoji.emojize(quote_row[0] + '\n' + ' - *{0}*, *{1}*'.format(quote_row[1], quote_row[2]))
