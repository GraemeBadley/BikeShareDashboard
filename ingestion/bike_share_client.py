import requests
from datetime import datetime, timezone

API_BASE = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/"
STATION_STATUS_ENDPOINT = "station_status"
STATION_INFORMATION_ENDPOINT = "station_information"
DEFAULT_TIMEOUT = 30

def fetch_station_status():
    url = API_BASE + STATION_STATUS_ENDPOINT
    
    data = _get_api_call(url)

    return data["data"]["stations"]

def fetch_station_information():
    url = API_BASE + STATION_INFORMATION_ENDPOINT

    data = _get_api_call(url)

    return data["data"]["stations"]

def _get_api_call(url):
    
    response = requests.get(url,timeout=DEFAULT_TIMEOUT)

    if response.status_code == 200:
        print("Request successful (200 OK)")
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        raise Exception("ApiRequestError")
    
def combine_station_data(station_status,station_information):
    full_stations_info = []

    # Pulling out id for station status to be searchable
    station_status_map = {station['station_id']: station for station in station_status}

    for station in station_information:

        
        id = station['station_id']

        

        timestamp = datetime.now(timezone.utc).isoformat()
        if id in station_status_map.keys():
            full_station_info = {**station,"station_status":station_status_map[id]}
            full_station_info["timestamp"] = timestamp

            full_stations_info.append(full_station_info)
        else:
            full_station_info = {**station,"station_status":None}
            full_station_info["timestamp"] = timestamp

            full_stations_info.append(full_station_info)

        
        

        

    return full_stations_info
        

