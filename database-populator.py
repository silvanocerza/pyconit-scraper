import sqlite3
import json

events = []
with open('events', 'r') as file:
    events = json.load(file)

conn = sqlite3.connect('events.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS events 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            desc, end, speakers, speakers_pages, start, summary, track, uid, starred)''')

conn.commit()

for event in events:
    desc = event['desc']
    end = event['end']
    speakers = json.dumps(event['speakers'])
    speakers_pages = json.dumps(event['speakers_pages'])
    start = event['start']
    summary = event['summary']
    track = event['track']
    uid = event['uid']
    starred = False

    cur.execute('''INSERT INTO events (desc, end, speakers, speakers_pages, start, summary, track, uid, starred) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (desc, end, speakers, speakers_pages, start, summary, track, uid, starred))
    conn.commit()

conn.close()
