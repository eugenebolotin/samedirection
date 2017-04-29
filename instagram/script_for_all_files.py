import sys
import os
import json
import re
from models import City
from vision_class import PhotoDetector
from multiprocessing import Process
import thread

# WORKING_DIR = os.getcwd()+'/'
# number = 0
# detailed_dict = {}
# for city in City.select():
#     city_name = re.sub(' ', '_', city.city.encode("utf-8").lower())
#     city_inst = city.photos_path
#     detailed_dict[city_name] = city_inst
# with open('cities_path.json'.format(city_name), 'w') as outfile:
#     json.dump(detailed_dict, outfile, indent=4, sort_keys=True, separators=(',', ':'))


def create_detailed_dicts(list_for_parsing):
    for city in list_for_parsing:
        print("Started parsing {}".format(city.city))
        town = city.city
        detector = PhotoDetector()
        with open('photos_all_json/{}.json'.format(town),'r') as inputfile:
            list_of_urls = json.loads(inputfile.read())
        city_name = re.sub(' ', '_', city.city.encode("utf-8").lower())
        json_dict, detailed_dict = detector.detect_list_of_urls(list_of_urls)
        with open('new_cities_photos_words/{}.json'.format(city_name), 'w') as outfile:
            json.dump(detailed_dict, outfile, indent=4, sort_keys=True, separators=(',', ':'))
        print city.id
        print('Parsed {}'.format(town))

def create_word_dicts():
    big_list_of_shit = {}
    for city in City.select():
        try:
            list_of_photos = []
            town = re.sub(' ','_',city.city.encode("utf-8").lower())
            with open('new_cities_photos_words/{}.json'.format(town),'r') as inputfile:
                my_file = json.loads(inputfile.read())
            for k,v in my_file.iteritems():
                for word in v:
                    list_of_photos.append(word)
            print 'Done!'
            big_list_of_shit.update({
                town: list(set(list_of_photos))
            })
        except:
            pass
    with open('all_words.json', 'w') as outfile:
        json.dump(big_list_of_shit, outfile, indent=4, sort_keys=True, separators=(',', ':'))


create_word_dicts()

# list_for_p2 = City.select().where(City.id > 41).limit(4)
# list_for_p3 = City.select().where(City.id > 56).limit(4)
# list_for_p4 = City.select().where(City.id > 60).limit(15)
# list_for_p5 = City.select().where(City.id > 75).limit(15)
# list_for_p6 = City.select().where(City.id > 90).limit(15)
# thread.start_new_thread(create_detailed_dicts(list_for_p2))
# thread.start_new_thread(create_detailed_dicts(list_for_p3))
# thread.start_new_thread(create_detailed_dicts(list_for_p4))
# thread.start_new_thread(create_detailed_dicts(list_for_p5))
# thread.start_new_thread(create_detailed_dicts(list_for_p6))




