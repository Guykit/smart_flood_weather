import pandas as pd

from DB.connection import connect_database
from service.clean_weather3hour import clean_weather3hours


def save_weather3hours():

    data = clean_weather3hours()

    connection = connect_database()
    cursor = connection.cursor()

    sql = """
        INSERT INTO weather_3hours (
            station_number,
            date_time,
            mean_sea_level_pressure,
            temperature,
            humidity,
            vapor_pressure,
            land_visibility,
            wind_direction,
            wind_speed,
            rainfall,
            rainfall_24hr
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        ON CONFLICT (station_number, date_time)
        DO NOTHING
    """

    for _, row in data.iterrows():

        wind_direction = row["wind_direction"]

        if pd.isna(wind_direction):
            wind_direction = None

        cursor.execute(
            sql,
            (
                row["station_number"],
                row["date_time"],
                row["mean_sea_level_pressure"],
                row["temperature"],
                row["humidity"],
                row["vapor_pressure"],
                row["land_visibility"],
                wind_direction,
                row["wind_speed"],
                row["rainfall"],
                row["rainfall_24hr"]
            )
        )

    connection.commit()

    print("บันทึกข้อมูล weather3hour แล้วโว้ย")

    cursor.close()
    connection.close()