from bs4 import BeautifulSoup
import requests
import json
url = "https://www.instagram.com/discoverhongkong"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
shared_data_string = str(soup).split('_sharedData = ')[1].split('</script>')[0][:-1]
json_data = json.loads(shared_data_string)
nodes = json_data.get(u'entry_data').get(u'ProfilePage')[0].get('user').get('media').get('nodes')
number = 0
for node in nodes:
    filename = 'photos/'+url.split('.com/')[1]+str(number)+'.jpg'
    f = open(filename, 'wb')
    f.write(requests.get(node[u'display_src']).content)
    f.close()
    number+=1