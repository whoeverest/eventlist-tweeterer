import twitter
import requests
import json
import os

# local
import config

if not os.path.isdir('./data'):
    os.makedirs('./data')

response = requests.get('http://eventlist.mk/events')

if response.status_code != 200:
    print "Something bad happened. :/"
    exit(1)

api = twitter.Api(
    consumer_key=config.CONSUMER_KEY,
    consumer_secret=config.CONSUMER_KEY_SECRET,
    access_token_key=config.ACCESS_TOKEN,
    access_token_secret=config.ACCESS_TOKEN_SECRET
)

old_events = json.loads(open('./data/old.json', 'r').read())
old_event_ids = map(lambda ev: ev['id'], old_events)

print old_event_ids

new_events = json.loads(response.content)

to_tweet = []

for event in new_events:
    if event['id'] not in old_event_ids:
        print 'adding event'
        to_tweet.append(event)


for event in to_tweet:
    print event

    name = event['name']
    link = 'https://facebook.com/' + event['id']

    if len(name) > 100:
        name = name[:97] + '...'
    
    api.PostUpdate(name + ' ' + link)


open('./data/old.json', 'w').write(json.dumps(new_events))
