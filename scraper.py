from datetime import datetime
import time
import json

import requests
from icalendar import Calendar
from bs4 import BeautifulSoup

BASE_URL = 'https://www.pycon.it/'
ICAL_URL = 'https://www.pycon.it/p3/schedule/pycon9.ics'

ical = requests.get(ICAL_URL).text

calendar = Calendar.from_ical(ical)

events = []

for e in calendar.walk('VEVENT'):
    # Scrapes description
    desc = ''
    speakers = []
    speakers_pages = []
    if e.get('summary').params:
        desc_page = requests.get(e.get('summary').params.get('altrep')).content.decode('utf-8', 'ignore')
        soup = BeautifulSoup(desc_page, 'html.parser')
        cms = soup.select_one('div[class="cms"]')
        orators = soup.select_one('div[class="talk-speakers"]')
        # Gets talk description
        if cms:
            desc = cms.text
        # Gets speakers names and link to their pages
        if orators:
            for s in orators.select('a'):
                speakers.append(s.text)
                speakers_pages.append(BASE_URL + s['href'])
        # Let's not dos the server :)
        time.sleep(2)

    events.append({
        'uid': e.get('uid'),
        'summary': e.get('summary'),
        'track': e.get('location')[7:],
        'start': time.mktime(datetime.strptime(e.get('dtstart').to_ical().decode(), '%Y%m%dT%H%M%S').timetuple()),
        'end': time.mktime(datetime.strptime(e.get('dtend').to_ical().decode(), '%Y%m%dT%H%M%S').timetuple()),
        'desc': desc,
        'speakers': speakers,
        'speakers_pages': speakers_pages,
    })


with open('events', mode='w') as file:
    file.writelines(json.dumps(events, sort_keys=True, indent=4, separators=(',', ': ')))
