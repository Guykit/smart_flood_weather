import pandas as pd

from DB.connection import connect_database


import pandas as pd

from DB.connection import connect_database


def prepare_flood_ml():

    conn = connect_database()

    weather_sql = """
        SELECT
            province_id,
            date,
            rainfall_avg,
            rainfall_max,
            rainfall_3d,
            rainfall_7d,
            temperature_avg,
            humidity_avg,
            wind_speed_avg
        FROM daily_weather_dataset
        ORDER BY province_id, date
    """

    flood_sql = """
        SELECT
            province_id,
            date,
            SUM(flood_area) AS flood_area
        FROM flood_events
        GROUP BY province_id, date
        ORDER BY province_id, date
    """

    weather_df = pd.read_sql(weather_sql, conn)
    flood_df = pd.read_sql(flood_sql, conn)

    conn.close()

    weather_df["date"] = pd.to_datetime(
        weather_df["date"]
    ).dt.date

    flood_df["date"] = pd.to_datetime(
        flood_df["date"]
    ).dt.date

    max_flood_date = flood_df["date"].max()

    weather_df = weather_df[
        weather_df["date"] <= max_flood_date
    ]

    df = weather_df.merge(
        flood_df,
        on=["province_id", "date"],
        how="left"
    )

    df["flood_area"] = df["flood_area"].fillna(0)

    df["flood"] = (df["flood_area"] > 0).astype(int)

    df["rainfall"] = df["rainfall_avg"]
    df["rainfall_24h"] = df["rainfall_max"]
    df["temperature"] = df["temperature_avg"]
    df["humidity"] = df["humidity_avg"]
    df["wind_speed"] = df["wind_speed_avg"]

    df = df[
        [
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
        ]
    ]



    df = df.dropna(
        subset=[
            "rainfall",
            "rainfall_24h",
            "rainfall_3d",
            "rainfall_7d",
            "temperature",
            "humidity",
            "wind_speed"
        ]
    )


    df = df.drop_duplicates(subset=["province_id", "date"],keep="last")

    df = df.sort_values(["province_id", "date"]).reset_index(drop=True)

    return df


if __name__ == "__main__":
    prepare_flood_ml()

def save_daily_flood_ml():

    df = prepare_flood_ml()

    if df is None or df.empty:
        print("ไม่มีข้อมูลให้บันทึก")
        return

    conn = connect_database()

    sql = """
        INSERT INTO daily_flood_ml (
            province_id,
            date,
            rainfall,
            rainfall_24h,
            rainfall_3d,
            rainfall_7d,
            temperature,
            humidity,
            wind_speed,
            flood_area,
            flood
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
        ON CONFLICT (province_id, date)
        DO UPDATE SET
            rainfall = EXCLUDED.rainfall,
            rainfall_24h = EXCLUDED.rainfall_24h,
            rainfall_3d = EXCLUDED.rainfall_3d,
            rainfall_7d = EXCLUDED.rainfall_7d,
            temperature = EXCLUDED.temperature,
            humidity = EXCLUDED.humidity,
            wind_speed = EXCLUDED.wind_speed,
            flood_area = EXCLUDED.flood_area,
            flood = EXCLUDED.flood
    """

    try:

        with conn.cursor() as cur:

            for _, row in df.iterrows():

                cur.execute(
                    sql,
                    (
                        int(row["province_id"]),
                        row["date"],
                        float(row["rainfall"]),
                        float(row["rainfall_24h"]),
                        float(row["rainfall_3d"]),
                        float(row["rainfall_7d"]),
                        float(row["temperature"]),
                        float(row["humidity"]),
                        float(row["wind_speed"]),
                        float(row["flood_area"]),
                        int(row["flood"])
                    )
                )

        conn.commit()

        print("SAVE DAILY FLOOD ML SUCCESS")
        print("วันที่ล่าสุด:", df["date"].max())

    except Exception as e:

        conn.rollback()

        print("SAVE ERROR")
        print(e)

    finally:

        conn.close()


if __name__ == "__main__":
    save_daily_flood_ml()