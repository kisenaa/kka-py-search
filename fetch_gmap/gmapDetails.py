from googlemaps import Client
from googlemaps.places import place
import json
import time

gmaps = Client(key='')

fields = ['price_level']

with open('hotelFixed.json', 'r', encoding='UTF-8') as file:
    data= json.load(file)

i = 0
for item in data:
    result = place(client=gmaps, place_id=item['place_id'], fields=fields)
    res = result.get('result', {}).get('price_level', None)
    if res:
        item['price_level'] = res
    i = i + 1;
    print(i)
    time.sleep(1)
    
with open('hotelFixed.json', 'w', encoding='UTF-8') as files:
    json.dump(data,files)

#print(result['result']['opening_hours'])
