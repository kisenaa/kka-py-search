import json

def filter_and_merge(json_file1, json_file2):
    # Load JSON data from the first file
    with open(json_file1, 'r', encoding='UTF-8') as f1:
        data1 = json.load(f1)

    # Load JSON data from the second file
    with open(json_file2, 'r', encoding='UTF-8') as f2:
        data2 = json.load(f2)

    # Dictionary to store unique JSON objects based on place ID
    unique_results = {}

    # Function to add unique JSON objects to the dictionary
    def add_to_unique(json_data):
        for item in json_data['places']:
            place_id = item.get('id')
            if place_id and place_id not in unique_results:
                unique_results[place_id] = item

    # Add unique JSON objects from the first file
    add_to_unique(data1)

    # Add unique JSON objects from the second file
    add_to_unique(data2)

    # Convert the dictionary values to a list
    unique_results_list = list(unique_results.values())

    # Use json.dumps to convert the list to a JSON-formatted string
    with open('touristFixed.json', 'w') as file:
    # Use json.dump to write the JSON object to the file
        result_json = json.dump(unique_results_list, file)  # Optional: indent for pretty printing

    # Print the JSON-formatted string or save it to a file
    print(result_json)

# Replace 'file1.json' and 'file2.json' with your actual file names
filter_and_merge('touristv1.json', 'touristv2.json')
