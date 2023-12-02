import requests
import json
url = "https://places.googleapis.com/v1/places:searchNearby"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": "",
    "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location,places.photos,places.types,places.currentOpeningHours,places.rating",
}

data = {
    "includedTypes": ["amusement_center", "cultural_center", "national_park", "historical_landmark", "marina"],
    "locationRestriction": {
        "circle": {
            "center": {
                "latitude": -7.276016333501707,
                "longitude":  112.74826360448981
            },
            "radius": 15000
        }
    }
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    json_content = response.json()

    with open("touristv2.json", "w") as json_file:
        json.dump(json_content, json_file, indent=2)
    
    print(json_content)
else:
    print(f"Error: {response.status_code}\n{response.text}")
