from service.TMD_WeatherToday import get_weather_today
import pandas as pd


def clean_weather():

    # ดึงข้อมูลจาก TMD
    weather_data = get_weather_today()

    # แปลงเป็น DataFrame
    data = pd.DataFrame(weather_data)

    # คอลัมน์ที่เป็นตัวเลข
    numeric_columns = [
        "latitude",
        "longitude",
        "temperature",
        "humidity",
        "rainfall",
        "wind_speed"
    ]

    # แปลงข้อมูลเป็นตัวเลข
    for column in numeric_columns:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    # แปลงวันที่
    data["date_time"] = pd.to_datetime(
        data["date_time"],
        errors="coerce"
    )

    # ตรวจสอบค่าที่ผิดปกติ
    invalid_humidity = data[
        (data["humidity"] < 0) |
        (data["humidity"] > 100)
    ]

    invalid_rainfall = data[
        data["rainfall"] < 0
    ]

    invalid_latitude = data[
        (data["latitude"] < -90) |
        (data["latitude"] > 90)
    ]

    invalid_longitude = data[
        (data["longitude"] < -180) |
        (data["longitude"] > 180)
    ]

    invalid_temperature = data[
        (data["temperature"] < -50) |
        (data["temperature"] > 60)
    ]

    print("Clean Weather สำเร็จ")
    print("ข้อมูลทั้งหมด:", len(data))

    return data


if __name__ == "__main__":
    clean_weather()