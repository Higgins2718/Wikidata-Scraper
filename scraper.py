import urllib.request, json
from get_attr_name_from_id import attrs

people = ['Adolf Hitler',
'Carl Linnaeus',
'Abraham Lincoln',
'Franklin D. Roosevelt',
'Winston Churchill',
'Queen Victoria',
'George Washington',
'Napoleon',
'Sidney Lee',
'Joseph Stalin',
'Theodore Roosevelt',
'Dwight D. Eisenhower',
'Thomas Jefferson',
'Nikolaus Pevsner',
'Lyndon B. Johnson',
'Woodrow Wilson',
'Wolfgang Amadeus Mozart',
'Mahatma Gandhi',
'Johann Sebastian Bach',
'Karl Marx']

encoded_name = people[17].replace(" ", "%20")
wikipedia_page = "https://en.wikipedia.org/wiki/{}".format(encoded_name)

'''
response = requests.get(wikipedia_page)
if response is not None:
    html = bs4.BeautifulSoup(response.text, 'html.parser')

    title = html.select("#firstHeading")[0].text
    paragraphs = html.select("p")
    for para in paragraphs:
        print (para.text)
    
    # just grab the text up to contents as stated in question
    intro = '\n'.join([ para.text for para in paragraphs[0:5]])
    print (intro)
'''

wikidata_page = "https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&props=claims&titles={}&format=json".format(encoded_name)

def get_attr(pid):
    for a,b in attrs.items():
        if pid == a:
            return b

def _finditem(obj, key):
    result = []
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = _finditem(v, key)
            if item is not None:
                result.append(item)
                return result[0]

with urllib.request.urlopen(wikidata_page) as url:
    data = json.loads(url.read().decode())
    #values = data['entities']
    #print(values)
    influences = _finditem(data, "P737")
    #print(influences)
    n = 1
    influences_ids = []

    for influence_json in influences:
        #print(n, influences)
        #n += 1
        #print("\n**********\n")
        #identifier = _finditem(data, "id")
        #influences_ids.append(identifier)
        identifier = influence_json['mainsnak']['datavalue']['value']['id']
        influences_ids.append(identifier)
    print(influences_ids)

    for influence_id in influences_ids:
        #print(n, influence_id)
        #n += 1
        #print("\n**********\n")
        influence_wikdata ='https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&languages=en&format=json'.format(influence_id)
        with urllib.request.urlopen(influence_wikdata) as url:
            data = json.loads(url.read().decode())
            name = _finditem(data, "value")
            print(name)
