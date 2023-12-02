import googlemaps
import json

gmaps = googlemaps.Client(key='')

query = 'Hotel'
location = (-7.276016333501707, 112.74826360448981)
radius = 15000

result = gmaps.places(query, location, radius)
with open('hotelv4.json', 'w') as file:
    # Use json.dump to write the JSON object to the file
    json.dump(result, file)

print(result)