from ingestion.bike_share_client import fetch_station_information,fetch_station_status,combine_station_data
from kafka import KafkaProducer
import json

PRODUCER_CONFIG = {
    'bootstrap_servers':'localhost:9094',
    'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
    'key_serializer': lambda k: str(k).encode('utf-8'),
}

def main():
    producer = KafkaProducer(**PRODUCER_CONFIG)   
    print("Bike station status")
    station_status = fetch_station_status()
    #print(station_status[0])
    print("Bike station information")
    station_info = fetch_station_information()
    #print(station_info[0])

    full_info_stations = combine_station_data(station_status,station_info)

    
    for station in full_info_stations:
        producer.send('stations_update',key=station["station_id"], value=station)
    
    
    

    producer.flush()
    print(full_info_stations[0].keys())


if __name__ == "__main__":
    main()
