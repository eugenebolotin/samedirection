import json
import os

big_dict = {}
list_of_files = os.listdir('/Users/sp41mer/HiGuys/imaged_cluster/instagram/new_cities_photos_words')
for file in list_of_files[1:]:
    with open('/Users/sp41mer/HiGuys/imaged_cluster/instagram/new_cities_photos_words/' + file, 'r') as inputfile:
        big_dict.update({
            file.split('.')[0]:json.loads(inputfile.read())
        })
with open('instagram/cities_words_2.json', 'w') as outfile:
    json.dump(big_dict, outfile, indent=4, sort_keys=True, separators=(',', ':'))