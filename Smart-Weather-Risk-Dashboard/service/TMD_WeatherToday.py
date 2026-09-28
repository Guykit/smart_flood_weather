import requests


url = "https://data.tmd.go.th/api/WeatherToday/V2/"

params = {
    "uid": "api",
    "ukey": "api12345",
    "format": "json"
}


def get_weather_today():

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()

        weather_data = []

        for station in data["Stations"]["Station"]:

            station_number = station["WmoStationNumber"]
            station_name = station["StationNameThai"]

            province = station["Province"]
            latitude = station["Latitude"]
            longitude = station["Longitude"]

            observation = station["Observation"]

            temperature = observation["Temperature"]
            humidity = observation["RelativeHumidity"]
            rainfall = observation["Rainfall"]
            wind_speed = observation["WindSpeed"]
            date_time = observation["DateTime"]

            weather = {
                "station_number": station_number,
                "station_name": station_name,
                "province": province,
                "latitude": latitude,
                "longitude": longitude,
                "temperature": temperature,
                "humidity": humidity,
                "rainfall": rainfall,
                "wind_speed": wind_speed,
                "date_time": date_time
            }

            weather_data.append(weather)
        return weather_data

    else:
        print(f"Error: {response.status_code}")
        return None


weather = get_weather_today()

print(weather)
