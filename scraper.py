from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime
import json

def get_event():
    r = Request('https://fr.investing.com/economic-calendar/', headers={'User-Agent': 'Mozilla/5.0', 'accept-language': 'en-US,en;q=0.9'})
    response = urlopen(r).read()
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find_all(class_ = "js-event-item")

    result = []
    base = {}
    
    for bl in table:
        time = bl.find(class_ ="first left time js-time").text
        # evento = bl.find(class_ ="left event").text
        currency = bl.find(class_ ="left flagCur noWrap").text.split(' ')
        event = bl.find(class_ = 'left event').a.text.split('\n')[1]
        intensity = bl.find_all(class_="left textNum sentiment noWrap")
        id_hour = currency[1] + '_' + time
         
        if not id_hour in base:
            base.update({id_hour : {'currency' : currency[1], 'event':event, 'time' : time ,'intensity' : { "1": 0,"2": 0,"3": 0, "priority" :0},} })
        
        intencity = base[id_hour]['intensity']
            
        for intence in intensity:
            _true = intence.find_all(class_="grayFullBullishIcon")
            _false = intence.find_all(class_="grayEmptyBullishIcon")
            
            if len(_true) == 1:
                intencity['1'] += 1
                intencity['priority'] = 1
                
            elif len(_true) == 2:
                intencity['2'] += 1
                intencity['priority'] = 2
                
            elif len(_true) == 3:
                intencity['3'] += 1
                intencity['priority'] = 3
            
        base[id_hour].update({'intensity' : intencity})

    for b in base:
        result.append(base[b])

    return result

""" news = get_event()

print(json.dumps(news, indent=2)) """
