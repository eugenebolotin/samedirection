import sys
import os
import json
from collections import defaultdict
from visionary import GoogleCloudVision, LabelDetection

GOOGLE_API_KEY = "AIzaSyBYV-2hKWaQHffLXclCabrehYrmtZss_bc"

class PhotoDetector():
    def detect_list_of_urls(self,list_of_urls):
        client = GoogleCloudVision(GOOGLE_API_KEY)
        scores = defaultdict(float)
        count = defaultdict(int)
        dir_dict = {}
        detailed_dict = {}
        total, errors = 0, 0
        for filename in list_of_urls:
            try:
                total += 1
                print >> sys.stderr, total, errors
                sys.stderr.flush()
                list_words = []
                response = client.annotate(filename, LabelDetection())
                for r in response.data["responses"]:
                    for a in r["labelAnnotations"]:
                        phrase, score = a["description"], a["score"]
                        scores[phrase] += score
                        count[phrase] += 1
                        list_words.append(phrase)
                detailed_dict.update({filename:list_words})
            except Exception as e:
                errors += 1
        for phrase, score in sorted(scores.items(), key=lambda (k, v): v, reverse=True):
            dir_dict.update({'{}'.format(phrase.encode("utf-8")): {
                'score': str(score).ljust(30),
                'count': count[phrase]
            }})
        return dir_dict, detailed_dict


    def detect_photos_in_dir(self,dir,photos_path):
        client = GoogleCloudVision(GOOGLE_API_KEY)
        scores = defaultdict(float)
        count = defaultdict(int)
        dir_dict = {}
        detailed_dict = {}
        total, errors = 0, 0
        list_of_files = [dir + '/'+f for f in os.listdir(dir)]
        for filename in list_of_files:
            try:
                total += 1
                list_words = []
                print >> sys.stderr, total, errors
                sys.stderr.flush()
                response = client.annotate(filename, LabelDetection())
                for r in response.data["responses"]:
                    for a in r["labelAnnotations"]:
                        phrase, score = a["description"], a["score"]
                        scores[phrase] += score
                        count[phrase] += 1
                        list_words.append(phrase)
                detailed_dict.update({filename.split(dir)[1]: list_words})
            except Exception as e:
                errors += 1
        for phrase, score in sorted(scores.items(), key=lambda (k, v): v, reverse=True):
            dir_dict.update({'{}'.format(phrase.encode("utf-8").ljust(30)): {
                'score': str(score).ljust(30),
                'count': count[phrase]
            }})
        return dir_dict, detailed_dict
