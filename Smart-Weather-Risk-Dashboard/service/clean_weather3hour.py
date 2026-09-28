from service.TMD_Weather3hour import get_weathers
import pandas as pd


def clean_weather3hours():

    # ดึงข้อมูลจาก TMD API
    weather_data = get_weathers()

    # แปลงข้อมูลเป็น DataFrame
    data = pd.DataFrame(weather_data)

    # คอลัมน์ที่เป็นตัวเลข
    numeric_columns = [
        "mean_sea_level_pressure",
        "temperature",
        "humidity",
        "vapor_pressure",
        "land_visibility",
        "wind_direction",
        "wind_speed",
        "rainfall",
        "rainfall_24hr"
    ]

    # แปลง String เป็นตัวเลข
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

    # TMD ใช้ 990 เป็นค่าพิเศษ
    # จึงเปลี่ยนเป็น None
    data.loc[
        data["wind_direction"] == 990,
        "wind_direction"
    ] = None

    # ตรวจสอบข้อมูลที่ผิดปกติ
    invalid_humidity = data[
        (data["humidity"] < 0) |
        (data["humidity"] > 100)
    ]

    invalid_rainfall = data[
        data["rainfall"] < 0
    ]

    invalid_rainfall_24hr = data[
        data["rainfall_24hr"] < 0
    ]

    invalid_wind_direction = data[
        (data["wind_direction"] < 0) |
        (data["wind_direction"] > 360)
    ]

    invalid_wind_speed = data[
        data["wind_speed"] < 0
    ]

    invalid_temperature = data[
        (data["temperature"] < -50) |
        (data["temperature"] > 60)
    ]

    invalid_pressure = data[
        data["mean_sea_level_pressure"] < 0
    ]

    invalid_vapor_pressure = data[
        data["vapor_pressure"] < 0
    ]

    invalid_visibility = data[
        data["land_visibility"] < 0
    ]

    # เปลี่ยน NaN เป็น None
    data = data.where(
        pd.notnull(data),
        None
    )

    print("Clean Weather 3 Hours สำเร็จ")
    print("ข้อมูลทั้งหมด:", len(data))

    return data


if __name__ == "__main__":

    data = clean_weather3hours()