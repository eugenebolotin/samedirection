import os
import logging
import json
import requests
import tornado.ioloop
import tornado.web
import tornado.wsgi
from bs4 import BeautifulSoup
from tornado import gen

from instagram.vision_class import PhotoDetector

logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s [%(name)s.%(levelname)s] {%(process)d/%(thread)d} %(message)s')

def parse_photos(account):
    url = "https://www.instagram.com/"+account
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    shared_data_string = str(soup).split('_sharedData = ')[1].split('</script>')[0][:-1]
    json_data = json.loads(shared_data_string)
    nodes = json_data.get(u'entry_data').get(u'ProfilePage')[0].get('user').get('media').get('nodes')
    number = 0
    list_of_urls = []
    for node in nodes:
        list_of_urls.append(node[u'display_src'])
    return list_of_urls


class ParseHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        account = self.get_argument('account')
        print account
        logging.info(account)
        try:
            vision = PhotoDetector()
            for_set, for_scan = vision.detect_list_of_urls(parse_photos(account))
            if len(for_set) == 0 or len(for_scan) == 0:
                logging.info('Account {} is blocked or private'.format(account))
                reply = {
                    'error': 1
                }
            else:
                set_test = set(for_set.keys())
                with open('all_words_2.json', 'r') as inputfile:
                    dict_from_file = json.loads(inputfile.read())
                with open('cities_words_2.json', 'r') as inputfile:
                    dict_of_words = json.loads(inputfile.read())
                with open('cities_path.json', 'r') as inputfile:
                    dict_of_paths = json.loads(inputfile.read())
                result_dict = {k: len(set_test & set(v)) ** 2 for k, v in dict_from_file.iteritems()}
                res = sorted(result_dict, key=result_dict.__getitem__, reverse=True)[:3]
                cities = {}
                for city in res:
                    max = 0
                    list_matches = []
                    list_of_photos = dict_of_words[city]
                    for k, v in for_scan.iteritems():
                        for k1, v1 in list_of_photos.iteritems():
                            list_matches.append({
                                'match': len(set(v1) & set(v)),
                                'set': list(set(v1) & set(v)),
                                'user': k,
                                'city': k1
                            })
                            # if (len(set(v1)&set(v)) > max):
                            #     print set(v1)&set(v)
                            #     max = len(set(v1) & set(v))
                            #     max_url_user.append(k)
                            #     max_url_account.append(k1)
                    all_list = sorted(list_matches, key=lambda k: k['match'], reverse=True)
                    uniq_list = []
                    uniq_big_list = []
                    for photo in all_list:
                        if photo['user'] not in uniq_list:
                            uniq_list.append(photo['user'])
                            uniq_big_list.append(photo)
                    cities.update({
                        city: uniq_big_list[:5]
                    })
                print('REPLY!')
                reply = {
                    'cities': res,
                    'photos': cities,
                    'error': 0
                }
        except Exception as e:
            logging.exception(e)
            print e
            reply = {
                'error': 1
            }
        self.write(json.dumps(reply))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")

def make_app():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_url_prefix": "/vision/static"
    }
    return tornado.web.Application([
        (r"/vision", MainHandler),
        (r"/vision/parse_photos", ParseHandler),
        ],**settings)

app = tornado.wsgi.WSGIAdapter(make_app())

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

