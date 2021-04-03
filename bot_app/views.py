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
        came_from = request.POST['Wald']
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

#     quotes = {
#         'money' : [
# """“Use money to gain control over your time, because not having control of your time is such a powerful and universal drag on happiness. The ability to do what you want, when you want, with who you want, for as long as you want to, pays the highest dividend that exists in finance.”
#     ― *Morgan Housel*""",
# """“It's nice to have a lot of money, but you know, you don't want to keep it around forever. I prefer buying things. Otherwise, it's a little like saving sex for your old age.”
#     ― *Warren Buffett*""",
# """“$1,000,000 in the bank isn't the fantasy. The fantasy is the lifestyle of complete freedom it supposedly allows.”
#     ― *Timothy Ferriss*"""],
#
#         'life': [
# """“Life is what happens to us while we are making other plans.”
#     ― *Allen Saunders*""",
# """“Life is like riding a bicycle. To keep your balance, you must keep moving.”
#     ― *Albert Einstein*""",
# """“There are two basic motivating forces: fear and love. When we are afraid, we pull back from life. When we are in love, we open to all that life has to offer with passion, excitement, and acceptance. We need to learn to love ourselves first, in all our glory and our imperfections. If we cannot love ourselves, we cannot fully open to our ability to love others or our potential to create. Evolution and all hopes for a better world rest in the fearlessness and open-hearted vision of people who embrace life.”
#     ― *John Lennon*"""],
#
#         'health': [
# """“The primary reason diseases tend to run in families may be that diets tend to run in families.”
#    ― *Michael Greger*""",
# """“We humans have known since time immemorial something that science is only now discovering: our gut feeling is responsible in no small measure for how we feel. We are “scared shitless” or we can be “shitting ourselves” with fear. If we don’t manage to complete a job, we can’t get our “ass in gear.” We “swallow” our disappointment and need time to “digest” a defeat. A nasty comment leaves a “bad taste in our mouth.” When we fall in love, we get “butterflies in our stomach.” Our self is created in our head and our gut—no longer just in language, but increasingly also in the lab.”
#    ― *Giulia Enders*""",
# """“It is easy to get bogged down trying to find the optimal plan for change: the fastest way to lose weight, the best program to build muscle, the perfect idea for a side hustle. We are so focused on figuring out the best approach that we never get around to taking action. As Voltaire once wrote, “The best is the enemy of the good.”
#    ― *James Clear*"""]
#
#     }
    random.seed(came_from-time.time())
    quote_row = category_dict[random.randrange(0, category_count-1)]

    return emoji.emojize(quote_row[0] + '\n' + ' - *{0}*, *{1}*'.format(quote_row[1], quote_row[2]))
