from ingestion.bike_share_client import fetch_station_information,fetch_station_status,combine_station_data

def main():
    print("Bike station status")
    station_status = fetch_station_status()
    #print(station_status[0])
    print("Bike station information")
    station_info = fetch_station_information()
    #print(station_info[0])

    full_info_stations = combine_station_data(station_status,station_info)

    print(full_info_stations[0])


if __name__ == "__main__":
    main()
