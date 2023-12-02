import heapq
import math
import json

def calculate_fn(location1, location2, cost, rating):
    distance = calculate_distance(location1, location2)
    res= cost / 100000
    return 0.3 * distance + 0.5* res + 0.2 * (5-rating)   # The f(n) function for now, could be modified later


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
    R = 6371.0
    
    # Calculate the distance
    distance = R * c
    return distance

def generate_timeframes(current_day, max_days):
    if current_day == 1 and max_days == 1:
        return [generate_timeframe(9, 10, 'makan'), generate_timeframe(10, 13, 'wisata'),
                generate_timeframe(13, 14, 'makan'), generate_timeframe(14, 18, 'wisata'),
                generate_timeframe(18, 19, 'makan'), generate_timeframe(19, 21, 'wisata')]
    elif current_day < max_days:
        return [generate_timeframe(9, 10, 'makan'), generate_timeframe(10, 13, 'wisata'),
                generate_timeframe(13, 14, 'makan'), generate_timeframe(14, 18, 'wisata'),
                generate_timeframe(18, 19, 'makan'), generate_timeframe(19, 21, 'wisata'),
                generate_timeframe(21, 9, 'hotel')]
    else:
        return [generate_timeframe(9, 10, 'makan'), generate_timeframe(10, 13, 'wisata'),
                generate_timeframe(13, 14, 'makan'), generate_timeframe(14, 18, 'wisata'),
                generate_timeframe(18, 19, 'makan'), generate_timeframe(19, 21, 'wisata')]

def generate_timeframe(start_hour, end_hour, type):
    return {'start_time': start_hour, 'end_time': end_hour, 'type': type}

def is_place_open(place, start_time, end_time):
    # Implementasi pengecekan apakah tempat buka pada time frame tertentu
    return place['open'] <= start_time and place['close'] >= end_time

# Modifikasi pada fungsi a_star

def a_star(destinations, max_days, max_budget):
    inPlan = set()
    plan = []
    budget = 0
    current_day = 1
    current_location = (0, 0)

    for place in destinations:
        place['fn'] = calculate_fn(current_location, place['location'], place['cost'], place['rating'])

    wisata_pqueue = [(place['fn'], place) for place in destinations if place['type'] == 'wisata']
    makan_pqueue = [(place['fn'], place) for place in destinations if place['type'] == 'makan']
    hotel_pqueue = [(place['fn'], place) for place in destinations if place['type'] == 'hotel']

    heapq.heapify(wisata_pqueue)
    heapq.heapify(makan_pqueue)
    heapq.heapify(hotel_pqueue)

    while current_day <= max_days:
        time_frames = generate_timeframes(current_day, max_days)
        # print(time_frames)
        # print("")
        i=0
        for time_frame in time_frames:
            
            if time_frame['type'] == 'wisata':
                destinations_pqueue = wisata_pqueue
            elif time_frame['type'] == 'makan':
                destinations_pqueue = makan_pqueue
            elif time_frame['type'] == 'hotel':
                destinations_pqueue = hotel_pqueue
            #print(destinations_pqueue)
            temp_removed_locations = []

            # Iterate through the destinations_pqueue from the smallest fn
            while destinations_pqueue:
                # for p in destinations_pqueue:
                #     print(p)
                #     print("")
                # print("")
                place = heapq.heappop(destinations_pqueue)
                #print(place[1])
                if (
                    is_place_open(place[1], time_frame['start_time'], time_frame['end_time']) and
                    budget + place[1]['cost'] <= max_budget and tuple(place[1]['location']) not in inPlan
                ):
                    inPlan.add(tuple(place[1]['location']))
                    budget += place[1]['cost']
                    plan.append((current_day, time_frame, place[1]['name']))
                    current_location = place[1]['location']

                    while temp_removed_locations:
                        if time_frame['type'] == 'wisata':
                            heapq.heappush(wisata_pqueue, temp_removed_locations.pop())
                        elif time_frame['type'] == 'makan':
                            heapq.heappush(makan_pqueue, temp_removed_locations.pop())
                        elif time_frame['type'] == 'hotel':
                            heapq.heappush(hotel_pqueue, temp_removed_locations.pop())
                        
                    # Update fn for remaining locations
                    updated_destinations_pqueues = update_all_pqueues(
                        wisata_pqueue, makan_pqueue, hotel_pqueue, destinations, current_location
                    )

                    wisata_pqueue, makan_pqueue, hotel_pqueue = updated_destinations_pqueues
                    
                    # Add temporarily removed locations back to the priority queues
                    break
                else:
                    # Store the location to be added back later
                    temp_removed_locations.append(place)
                    # print ("aaaa ", temp_removed_locations)
            i=i+1
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

def search_destinations(max_days:int, max_budget:int):
    with open('data_rakha.json') as f:
        destinations = json.load(f)

    plan = a_star(destinations, max_days, max_budget)
    
    if (len(plan) < (max_days * 7 - 1)):
        return {'message': 'Error: Budget is not enough'}
    else:
        return plan
    
search_destinations(3,1000000)