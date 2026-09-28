from DB.connection import connect_database
from service.clean_weather import clean_weather


def save_weather():

    # ดึงข้อมูลที่ผ่านการ Cleaning และ Validation
    data = clean_weather()

    # เชื่อม Database
    connection = connect_database()

    # สร้าง Cursor ส่งpythonหาdatabase
    cursor = connection.cursor()

    # วนข้อมูลแต่ละแถวใน DataFrame
    for _, row in data.iterrows():

        station_number = row["station_number"]
        date_time = row["date_time"]
        temperature = row["temperature"]
        humidity = row["humidity"]
        rainfall = row["rainfall"]
        wind_speed = row["wind_speed"]

        # SQL บันทึกข้อมูลสภาพอากาศ
        sql = """
            INSERT INTO weather_Today (
                station_number,
                date_time,
                temperature,
                humidity,
                rainfall,
                wind_speed
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT(station_number,date_time)
            DO UPDATE SET
            temperature = EXCLUDED.temperature,
            humidity = EXCLUDED.humidity,
            rainfall = EXCLUDED.rainfall,
            wind_speed = EXCLUDED.wind_speed
        """
         #excute()
        cursor.execute(
            sql,
            (
                station_number,
                date_time,
                temperature,
                humidity,
                rainfall,
                wind_speed
            )
        )

    # ยืนยันการบันทึกข้อมูล
    connection.commit()

    print("บันทึกข้อมูลลง weather_Today แล้วโว้ย ")

    # ปิด Cursor
    cursor.close()

    # ปิด Connection
    connection.close()


if __name__ == "__main__":
    save_weather()