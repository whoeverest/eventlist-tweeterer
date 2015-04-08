import os
import requests as r

current_dir = os.path.dirname(os.path.realpath(__file__))
old_events_path = os.path.join(current_dir, 'data/old.json')

response = r.get('http://eventlist.mk/events')

with open(old_events_path, 'w') as f:
	f.write(response.content)