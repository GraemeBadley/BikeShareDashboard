from ingestion.bike_share_client import fetch_station_information,fetch_station_status

def main():
    print("Bike station status")
    fetch_station_status()
    print("Bike station information")
    fetch_station_information()


if __name__ == "__main__":
    main()
