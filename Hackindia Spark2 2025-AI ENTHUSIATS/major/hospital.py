import requests


# Replace with your actual API keys
GOOGLE_PLACES_API_KEY = 'AIzaSyD8CrXNiARphJI6L6172TzO4kO0ssKLDb0'
GOOGLE_GEOLOCATION_API_KEY = 'AIzaSyD8CrXNiARphJI6L6172TzO4kO0ssKLDb0'
GOOGLE_GEOCODING_API_KEY = 'AIzaSyD8CrXNiARphJI6L6172TzO4kO0ssKLDb0'



def get_location_from_google_geolocation(api_key):
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"
    payload = {
        "considerIp": "true"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        location_data = response.json().get('location', {})
        lat = location_data.get('lat', None)
        lon = location_data.get('lng', None)
        return lat, lon
    except requests.exceptions.RequestException as e:
        print(f"Error getting location from Google Geolocation API: {e}")
        return None, None

def get_area_name(api_key, location):
    lat, lon = location
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'latlng': f"{lat},{lon}",
        'key': api_key
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        results = response.json().get('results', [])
        if results:
            address_components = results[0].get('address_components', [])
            for component in address_components:
                if 'sublocality' in component['types'] or 'locality' in component['types']:
                    return component['long_name']
            return results[0]['formatted_address']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting area name from Google Geocoding API: {e}")
        return None

def find_nearby_hospitals(api_key, location, radius):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'key': api_key,
        'location': f"{location[0]},{location[1]}",
        'radius': radius,
        'type': 'hospital'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        results = response.json().get('results', [])
        hospitals = []
        for result in results:
            hospitals.append({
                'name': result['name'],
                'address': result.get('vicinity', 'N/A'),
                'location': result['geometry']['location']
            })
        return hospitals
    except requests.exceptions.RequestException as e:
        print(f"Error finding hospitals: {e}")
        return []

def main():
    lat, lon = get_location_from_google_geolocation(GOOGLE_GEOLOCATION_API_KEY)
    if lat is not None and lon is not None:
        location = (lat, lon)
        area_name = get_area_name(GOOGLE_GEOCODING_API_KEY, location)
        radius = 5000  # Search radius in meters
        print(f"Current location: {location}")
        print(f"Area: {area_name}")
        print(f"Searching for hospitals near: {location}")
        hospitals = find_nearby_hospitals(GOOGLE_PLACES_API_KEY, location, radius)
        if hospitals:
            print("Nearby Hospitals:")
            for hospital in hospitals:
                print(f"Name: {hospital['name']}")
                print(f"Address: {hospital['address']}")
                print(f"Location: {hospital['location']}")
                print()
        else:
            print("No hospitals found.")
    else:
        print("Could not determine location.")

if __name__ == "__main__":
    main()
