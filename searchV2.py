import heapq
import math
import json
import os
from collections import defaultdict

def calculate_fn(location1, location2, cost, rating):
    distance = calculate_distance(location1, location2)
    normalized_cost = cost / 100000
    return 0.3 * distance + 0.5 * normalized_cost + 0.2 * (5-rating)   # The f(n) function for now, could be modified later

def calculate_distance(location1,location2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = map(math.radians, location1)
    lat2, lon2 = map(math.radians, location2) 

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Radius of the Earth in kilometers (mean value)  
    R = 6378.0
    
    # Calculate the distance
    distance = R * c
    return distance

def generate_timeframes(current_day, max_days):
    if current_day == 1 and max_days == 1:
        return [generate_timeframe(900, 1000, 'makan'), generate_timeframe(1000, 1300, 'wisata'),
                generate_timeframe(1300, 1400, 'makan'), generate_timeframe(1400, 1800, 'wisata'),
                generate_timeframe(1800, 1900, 'makan'), generate_timeframe(1900, 2100, 'wisata')]
    elif current_day < max_days:
        return [generate_timeframe(900, 1000, 'makan'), generate_timeframe(1000, 1300, 'wisata'),
                generate_timeframe(1300, 1400, 'makan'), generate_timeframe(1400, 1800, 'wisata'),
                generate_timeframe(1800, 1900, 'makan'), generate_timeframe(1900, 2100, 'wisata'),
                generate_timeframe(2100, 900, 'hotel')]
    else:
        return [generate_timeframe(900, 1000, 'makan'), generate_timeframe(1000, 1300, 'wisata'),
                generate_timeframe(1300, 1400, 'makan'), generate_timeframe(1400, 1800, 'wisata'),
                generate_timeframe(1800, 1900, 'makan'), generate_timeframe(1900, 2100, 'wisata')]

def generate_timeframe(start_hour, end_hour, type):
    return {'start_time': start_hour, 'end_time': end_hour, 'type': type}

def is_place_open(place, start_time, end_time):
    return place['open'] <= start_time and place['close'] >= end_time

# Main function
def a_star(destinations, cur_loc, max_days, max_budget):
    
    # initiate needed variables
    inPlan = set()
    plan = []
    budget = 0
    current_day = 1
    current_location = cur_loc
    # Calculate f(n) for every locations
    for place in destinations:
        place['fn'] = calculate_fn(current_location, place['location'], place['cost'], place['rating'])

    # Classify the destinations based on 3 types
    wisata_pqueue = [(place['fn'], place) for place in destinations if place['type'] == 'wisata']
    makan_pqueue = [(place['fn'], place) for place in destinations if place['type'] == 'makan']
    hotel_pqueue = [(place['fn'], place) for place in destinations if place['type'] == 'hotel']
    heapq.heapify(wisata_pqueue)
    heapq.heapify(makan_pqueue)
    heapq.heapify(hotel_pqueue)

    # Iterate for every day until max days
    while current_day <= max_days:
        # Generate timeframe based on the current day and max days
        time_frames = generate_timeframes(current_day, max_days)
        # Loop for every timeframe for the current day
        for time_frame in time_frames:
            # Check the current timeframe, use the pq that is the same type of the timeframe
            if time_frame['type'] == 'wisata':
                destinations_pqueue = wisata_pqueue
            elif time_frame['type'] == 'makan':
                destinations_pqueue = makan_pqueue
            elif time_frame['type'] == 'hotel':
                destinations_pqueue = hotel_pqueue
                
            # For storing deleted elements in destinations_pqueue
            temp_removed_locations = []

            # Iterate through the destinations_pqueue from the smallest fn
            while destinations_pqueue:
                # Pop place from the pq (smallest f(n))
                place = heapq.heappop(destinations_pqueue)
                #print(place[1])
                
                # If the place is open at the current timeframe, the budget is still enough, 
                # and the place is not in the plan
                if (
                    is_place_open(place[1], time_frame['start_time'], time_frame['end_time']) and
                    budget + place[1]['cost'] <= max_budget and place[1]['location'] not in inPlan
                ):
                    # Add the place in the plan, update budget, set current location to said place
                    inPlan.add(place[1]['location'])
                    budget += place[1]['cost']
                    plan.append((current_day, time_frame, place[1]['name'], place[1]['place_id']))
                    current_location = place[1]['location']

                    # Add temporarily removed locations back to the priority queues
                    while temp_removed_locations:
                        if time_frame['type'] == 'wisata':
                            heapq.heappush(wisata_pqueue, temp_removed_locations.pop())
                        elif time_frame['type'] == 'makan':
                            heapq.heappush(makan_pqueue, temp_removed_locations.pop())
                        elif time_frame['type'] == 'hotel':
                            heapq.heappush(hotel_pqueue, temp_removed_locations.pop())

                    # Update fn for remaining locations based on the new current locations
                    updated_destinations_pqueues = update_all_pqueues(
                        wisata_pqueue, makan_pqueue, hotel_pqueue, destinations, current_location
                    )
                    wisata_pqueue, makan_pqueue, hotel_pqueue = updated_destinations_pqueues
                    
                    # done for the current timeframe, continue for the next timeframe
                    break
                
                else:
                    # Store the location to be added back later
                    temp_removed_locations.append((place[0], place[1]))

        current_day += 1

    return plan


def update_all_pqueues(wisata_pqueue, makan_pqueue, hotel_pqueue, destinations, current_location):
    updated_wisata_pqueue = update_pqueue(wisata_pqueue, destinations, current_location, 'wisata')
    updated_makan_pqueue = update_pqueue(makan_pqueue, destinations, current_location, 'makan')
    updated_hotel_pqueue = update_pqueue(hotel_pqueue, destinations, current_location, 'hotel')

    return updated_wisata_pqueue, updated_makan_pqueue, updated_hotel_pqueue

def update_pqueue(destinations_pqueue, destinations, current_location, type):
    updated_destinations_pqueue = []
    for p in destinations_pqueue:
        p_location = p[1]['location']
        updated_fn = calculate_fn(current_location, p_location, p[1]['cost'], p[1]['rating'])
        updated_destinations_pqueue.append((updated_fn, p[1]))

    heapq.heapify(updated_destinations_pqueue)
    return updated_destinations_pqueue

def format_time(minutes):
    # Konversi menit menjadi jam:menit
    hours, mins = divmod(minutes, 100)
    formatted_time = f"{hours:02d}:{mins:02d}"
    return formatted_time

# Mendapatkan path dari script.py
script_path = os.path.dirname(os.path.abspath(__file__))

# Menggabungkan path dengan nama file 'data.json'
resto_path = os.path.join(script_path, './fetch_gmap/restaurant/restaurantFixed.json')

tourist_path = os.path.join(script_path, './fetch_gmap/tourist/touristFixed.json')

hotel_path = os.path.join(script_path, './fetch_gmap/hotel/hotelFixed.json')


with open(resto_path, 'r', encoding='utf-8') as file:
    resto_data = json.load(file)
with open(tourist_path, 'r', encoding='utf-8') as file:
    tour_data = json.load(file)
with open(hotel_path, 'r', encoding='utf-8') as file:
    hotel_data = json.load(file)

# Lanjutkan dengan proses parsing dan manipulasi data JSON sesuai kebutuhan Anda

# Contoh data hasil parsing
def search_destinations(max_days:int, max_budget:int, current_location:tuple[float,float]):
    print(current_location)
    destinations = []

    for indivData in resto_data:
        destination = {
            "name": indivData["name"],
            "place_id": indivData['place_id'],
            "location": (indivData["geometry"]["location"]["lng"], indivData["geometry"]["location"]["lat"]),
            "cost": 0,  # Anda mungkin perlu informasi tambahan untuk mengisi nilai ini
            "rating": indivData["rating"],
            "type": "makan",  # Mengambil tipe pertama dari daftar tipe
            "open": indivData["open_time"]["periods"][0]["open"]["time"],
            "close": indivData["open_time"]["periods"][0]["close"]["time"]
        }
        destination["open"] = int(destination["open"])
        destination["close"] = int(destination["close"])
        if destination["open"] > destination["close"]:
            destination["close"] += 2400
        destinations.append(destination)
        
    for data in tour_data:
        destination = {
            "name": data["displayName"]["text"],
            "place_id": data['id'],
            "location": (data["location"]["longitude"], data["location"]["latitude"]),
            "cost": 0,  # Anda mungkin perlu informasi tambahan untuk mengisi nilai ini
            "rating": data["rating"],
            "type": "wisata",  # Mengambil tipe pertama dari daftar tipe
            "open": 0,
            "close": 0
        }
        # Memastikan bahwa "currentOpeningHours" ada sebelum mencoba mengakses informasinya
        if "currentOpeningHours" in data and "periods" in data["currentOpeningHours"] and data["currentOpeningHours"]["periods"]:
            destination["open"] = data["currentOpeningHours"]["periods"][0]["open"]["hour"]*100 + data["currentOpeningHours"]["periods"][0]["open"]["minute"]
            destination["close"] = data["currentOpeningHours"]["periods"][0]["close"]["hour"]*100 + data["currentOpeningHours"]["periods"][0]["close"]["minute"]
        else:
            destination["open"] = 0
            destination["close"] = 2400
        if destination["open"] > destination["close"]:
            destination["close"] += 2400
        destinations.append(destination)

    for data in hotel_data:
        new_destination = {
            "name": data["name"],
            "place_id": data['place_id'],
            "location": (data["geometry"]["location"]["lng"], data["geometry"]["location"]["lat"]),
            "cost": 0,  # Anda mungkin perlu informasi tambahan untuk mengisi nilai ini
            "rating": data["rating"],
            "type": "hotel",  # Mengambil tipe pertama dari daftar tipe
            "open": 0,
            "close": 2400
        }
        destinations.append(new_destination)
    # Print hasil list destinations

    #max_days = 3  # max plan days
    #max_budget = 1000000  # max budget used in plan
    #cur_loc = (112.75, -7.25)
    # jkt = (106.8229, -6.1944)
    # print(calculate_distance(cur_loc, jkt))

    plan = a_star(destinations, current_location, max_days, max_budget)

    # Buat list baru untuk menyimpan rencana yang telah diubah
    updated_plan = defaultdict(list)

    # Iterasi melalui rencana awal
    for day, timeframe, place, ids in plan:
        # Ubah format waktu dan buat tupel baru
        updated_timeframe = {
            'start_time': format_time(timeframe['start_time']),
            'end_time': format_time(timeframe['end_time']),
            'type': timeframe['type']
        }
        
        # Tambahkan tupel baru ke dalam list updated_plan
        updated_plan[day].append({'day': day, 'timeframe': updated_timeframe, 'name': place, 'place_id': ids})
    return updated_plan

'''
# Print rencana yang telah diubah
# Now, you can access the grouped data for each day
for day, entries in updated_plan.items():
    print(f"Day {day}:")
    for entry in entries:
        print(entry)
    print()
'''

#json_string = json.dumps(grouped_dict, indent=2)

# Print or do whatever you want with the JSON string
#print(json_string)


