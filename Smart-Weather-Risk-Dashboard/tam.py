import pandas as pd

from DB.connection import connect_database

conn = connect_database 

def prepare_flood():

 # ตารางdaily_weather_dataset
    weather_sql = """
        SELECT
            province_id,
            date,
            rainfall_avg,
            rainfall_avg,
            rainfall_max,
            temperature_avg,
            humidity_avg,
            wind_speed_avg,
            rainfall_3d,
            rainfall_7d
        FROM daily_weather_dataset

        ORDER BY
            province_id,
            date

        """
    flood_sql = """

        SELECT
            province_id,
            date,
            SUM(flood_area) AS flood_area

        FROM flood_events

        GROUP BY
            province_id,
            date

        ORDER BY
        province_id,
        date

        """ 
    weather_df = pd.read_sql(
        weather_sql,
        conn
        )
    flood_df  = pd.read_sql(
        flood_sql,
        conn
    )

    conn.close()

 #weather
    print("="*40)
    print("จำนวนข้อมูลในตาราง Weather_df", len(weather_df))
    print("จำนวนจังหวัดใน Weather_df",weather_df["province_id"].unique ())
 #flood
    print("จำนวนข้อมูลในตาราง flood_df", len(flood_df))
    print("จำนวนจังหวัดใน flood_df",flood_df["province_id"].unique ())

 # แปลงวันที่
    weather_df["date"] = pd.to_datetime(weather_df["date"]).dt.date

    # เชื่อมสิงตาราง.  on =เงื่อนไช id , date ต้องตรงกัน   how "left" เอาตารางซ้ายเป็นหลัก
    df = weather_df.merge(flood_sql , on = ["province_id" , "date"] , how = "left")

 #ทำLabel. แปลง flood_area ให้เปน1,0
    df["flood_area"] =    (df["flood_area"].fillna(0)) #แถวไหนเปนค่าnull แทนด้วย 0

        
    #สร้าง  Traget "Flood"
    df["flood"] =    (df["flood_area"].gt(0).astype(int)) #gt = greter than มากกว่า0  ให้ เปน true , false astypeเปลี่ยน true false ให้เปน 0 1 


    # เปลี่ยนชื่อ Feature  ให้มันสื่อความหมายเฉยๆ

    df["rainfall"] = (
        df["rainfall_avg"]
    )

    df["rainfall_24h"] = (
        df["rainfall_max"]
    )

    df["temperature"] = (
        df["temperature_avg"]
    )

    df["humidity"] = (
        df["humidity_avg"]
    )

    df["wind_speed"] = (
        df["wind_speed_avg"]
    )

 #เลือก colum
    df  = df[[
        "province_id",
        "date",
        "rainfall",
        "rainfall_24h",
        "rainfall_3d",
        "rainfall_7d",
        "temperature",
        "humidity",
        "wind_speed",
        "flood_area", 
        "flood"        
    ]]

    #(ทำความสะอาดข้อมูล)

    before_clean = len(df)

    print("ทำความสะอาดข้อมูล")

    #ลบ ช่องที่เป็นค่าว่าง

    df = df.dropna(
        subset=[
            "rainfall_3d",
            "rainfall_7d"

        ]
    ).copy

    after_clean = len(df)
    print("ก่อยน clean ",before_clean)
    print("หลัง clean",after_clean)

    
  