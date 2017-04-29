#!/usr/bin/env python

import sys
import json
from collections import defaultdict

from visionary import GoogleCloudVision, LabelDetection


GOOGLE_API_KEY = "AIzaSyBYV-2hKWaQHffLXclCabrehYrmtZss_bc"

client = GoogleCloudVision(GOOGLE_API_KEY)
scores = defaultdict(float)
count = defaultdict(int)
city_json = {}
total, errors = 0, 0
list_of_paths = ['../instagram/photos/discoverhongkong0.jpg']
for filename in list_of_paths:
    try:
        total += 1
        print >>sys.stderr, total, errors
        sys.stderr.flush()
        response = client.annotate(filename, LabelDetection())
        for r in response.data["responses"]:
            for a in r["labelAnnotations"]:
                phrase, score = a["description"], a["score"]
                scores[phrase] += score
                count[phrase] += 1
    except Exception as e:
        errors += 1

print >>sys.stderr, total, errors

for phrase, score in sorted(scores.items(), key=lambda (k,v): v, reverse=True):
    city_json.update({'{}'.format(phrase.encode("utf-8").ljust(30)): {
        'score': str(score).ljust(30),
        'count': count[phrase]
    }})
    print phrase.encode("utf-8").ljust(30), str(score).ljust(30), count[phrase]

with open('data.json', 'w') as outfile:
    json.dump(city_json, outfile, indent=4, sort_keys=True, separators=(',', ':'))
