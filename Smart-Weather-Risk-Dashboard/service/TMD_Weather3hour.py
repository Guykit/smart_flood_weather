import requests

url = "https://data.tmd.go.th/api/Weather3Hours/V2/"

params = {
    "uid": "api",
    "ukey": "api12345",
    "limit": 200,
    "format": "json"
}


def get_weathers():

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    print("Status:", response.status_code)

    if response.status_code != 200:
        print("Error:", response.status_code)
        return None

    data = response.json()

    stations = data.get("Stations", {})

    # API ไม่มีข้อมูล
    if not stations:
        print("TMD API ไม่มีข้อมูลสถานีในขณะนี้")
        return []

    station_list = stations.get("Station", [])

    # กรณีมีสถานีเดียว
    if isinstance(station_list, dict):
        station_list = [station_list]

    weather_data = []

    for d in station_list:

        station_number = d.get("WmoStationNumber")
        province = d.get("Province")

        observation = d.get("Observation", {})

        weather = {
            "station_number": station_number,
            "province": province,
            "date_time": observation.get("DateTime"),

            "mean_sea_level_pressure":
                observation.get("MeanSeaLevelPressure"),

            "temperature":
                observation.get("Temperature"),

            "humidity":
                observation.get("RelativeHumidity"),

            "vapor_pressure":
                observation.get("VaporPressure"),

            "land_visibility":
                observation.get("LandVisibility"),

            "wind_direction":
                observation.get("WindDirection"),

            "wind_speed":
                observation.get("WindSpeed"),

            "rainfall":
                observation.get("Rainfall"),

            "rainfall_24hr":
                observation.get("Rainfall24Hr")
        }

        weather_data.append(weather)

    return weather_data