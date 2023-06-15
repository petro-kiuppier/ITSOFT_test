import requests
import json
import uuid
import os
import shutil


# Fetch data from the API
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data from {url}")


# Save data to a JSON file
def save_to_json(data, filename, folder):
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


# Generate a unique ID
def generate_id():
    return str(uuid.uuid4())


# Fetch all pages of data for a resource
def fetch_all_pages(url):
    all_data = []
    while url:
        data = fetch_data(url)

        all_data.extend(data['results'])
        url = data['info']['next']
    return all_data


# Create folders for each resource, clear them if they already exist
def create_folders():
    folders = ['characters', 'locations', 'episodes']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            shutil.rmtree(folder)
            os.makedirs(folder)


if __name__ == '__main__':
    create_folders()

    # Fetch character data
    characters_url = "https://rickandmortyapi.com/api/character"
    characters_data = fetch_all_pages(characters_url)

    for character in characters_data:
        filename = f"character_{generate_id()}.json"
        character_data = {
            'Id': generate_id(),
            'Metadata': character['name'],
            'RawData': character
        }
        save_to_json(character_data, filename, 'characters')

    # Fetch location data
    locations_url = "https://rickandmortyapi.com/api/location"
    locations_data = fetch_all_pages(locations_url)

    for location in locations_data:
        filename = f"location_{generate_id()}.json"
        location_data = {
            'Id': generate_id(),
            'Metadata': location['name'],
            'RawData': location
        }
        save_to_json(location_data, filename, 'locations')

    # Fetch episode data
    episodes_url = "https://rickandmortyapi.com/api/episode"
    episodes_data = fetch_all_pages(episodes_url)

    output = []
    for episode in episodes_data:
        filename = f"episode_{generate_id()}.json"
        episode_data = {
            'Id': generate_id(),
            'Metadata': episode['name'],
            'RawData': episode
        }
        save_to_json(episode_data, filename, 'episodes')

        # Check if the episode aired between 2017 and 2021 and has more than three characters
        air_date = episode['air_date']

        if air_date.endswith(('2017', '2018', '2019', '2020', '2021')) and len(episode['characters']) > 3:
            output.append(episode['name'])
    print("Episodes aired between 2017 and 2021 with more than three characters:")
    print(output)
