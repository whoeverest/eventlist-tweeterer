#!/usr/bin/python

import twitter
import requests
import json
import os

# local
import config

current_dir = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(current_dir, 'data')
old_events_path = os.path.join(current_dir, 'data/old.json')

if not os.path.isdir(data_path):
    os.makedirs(data_path)

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

old_events = json.loads(open(old_events_path, 'r').read())
old_event_ids = map(lambda ev: ev['id'], old_events)

new_events = json.loads(response.content)

to_tweet = []

for event in new_events:
    if event['id'] not in old_event_ids:
        print 'added event with id', event['id']
        to_tweet.append(event)

if len(to_tweet) == 0:
    print 'No new events, exiting'

for event in to_tweet:
    print event

    name = event['name']
    link = 'https://facebook.com/' + event['id']

    if len(name) > 100:
        name = name[:97] + '...'
    
    api.PostUpdate(name + ' ' + link)


open(old_events_path, 'w').write(json.dumps(new_events))
