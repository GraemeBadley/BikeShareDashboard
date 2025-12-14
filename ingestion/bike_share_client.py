import requests

API_BASE = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/"
STATION_STATUS_ENDPOINT = "station_status"
STATION_INFORMATION_ENDPOINT = "station_information"
DEFAULT_TIMEOUT = 30

def fetch_station_status():
    url = API_BASE + STATION_STATUS_ENDPOINT
    
    data = _get_api_call(url)

    print(data["data"]["stations"][0])

def fetch_station_information():
    url = API_BASE + STATION_INFORMATION_ENDPOINT

    data = _get_api_call(url)

    print(data["data"]["stations"][0])

def _get_api_call(url):
    
    response = requests.get(url,timeout=DEFAULT_TIMEOUT)

    if response.status_code == 200:
        print("Request successful (200 OK)")
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)