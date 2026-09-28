import pandas as pd

from DB.connection import connect_database


def save_daily_weather():

    conn = connect_database()

    weather_sql = """
        SELECT
            s.province_id,
            DATE(w.date_time) AS date,
            AVG(w.rainfall) AS rainfall_avg,
            MAX(w.rainfall) AS rainfall_max,
            AVG(w.humidity) AS humidity_avg,
            AVG(w.wind_speed) AS wind_speed_avg,
            COUNT(DISTINCT w.station_number) AS station_count
        FROM weather_3hours w
        JOIN stations s
            ON w.station_number = s.station_number
        WHERE s.province_id IS NOT NULL
        GROUP BY s.province_id, DATE(w.date_time)
        ORDER BY s.province_id, DATE(w.date_time)
    """

    df = pd.read_sql(weather_sql, conn)
    conn.close()

    df["date"] = pd.to_datetime(df["date"])

    conn = connect_database()

    today_sql = """
        SELECT
            s.province_id,
            DATE(w.date_time) AS date,
            AVG(w.rainfall) AS rainfall_avg,
            MAX(w.rainfall) AS rainfall_max,
            AVG(w.temperature) AS temperature_avg,
            AVG(w.humidity) AS humidity_avg,
            AVG(w.wind_speed) AS wind_speed_avg,
            COUNT(DISTINCT w.station_number) AS station_count
        FROM weather_today w
        JOIN stations s
            ON w.station_number = s.station_number
        WHERE s.province_id IS NOT NULL
        AND DATE(w.date_time) = CURRENT_DATE
        GROUP BY s.province_id, DATE(w.date_time)
    """

    today_df = pd.read_sql(today_sql, conn)
    conn.close()

    if not today_df.empty:

        today_df["date"] = pd.to_datetime(
            today_df["date"]
        )

        today_date = today_df["date"].dt.date.iloc[0]

        df = df[
            df["date"].dt.date != today_date
        ]

        df = pd.concat(
            [df, today_df],
            ignore_index=True
        )

    conn = connect_database()

    temperature_sql = """
        SELECT
            s.province_id,
            DATE(w.date_time) AS date,
            AVG(w.temperature) AS temperature_avg
        FROM weather_today w
        JOIN stations s
            ON w.station_number = s.station_number
        WHERE s.province_id IS NOT NULL
        AND w.temperature IS NOT NULL
        GROUP BY s.province_id, DATE(w.date_time)
    """

    temperature_df = pd.read_sql(
        temperature_sql,
        conn
    )

    conn.close()

    temperature_df["date"] = pd.to_datetime(
        temperature_df["date"]
    )

    if "temperature_avg" in df.columns:
        df = df.drop(
            columns=["temperature_avg"]
        )

    df = df.merge(
        temperature_df,
        on=["province_id", "date"],
        how="left"
    )

    df = df.sort_values(
        ["province_id", "date"]
    ).reset_index(drop=True)

    rainfall_3d_list = []
    rainfall_7d_list = []

    for province_id, group in df.groupby("province_id"):

        group = group.sort_values("date")

        rainfall = group.set_index(
            "date"
        )["rainfall_avg"]

        dates = pd.date_range(
            rainfall.index.min(),
            rainfall.index.max(),
            freq="D"
        )

        rainfall = rainfall.reindex(
            dates
        ).fillna(0)

        rainfall_3d = rainfall.rolling(
            3,
            min_periods=3
        ).sum()

        rainfall_7d = rainfall.rolling(
            7,
            min_periods=7
        ).sum()

        for date in group["date"]:

            rainfall_3d_list.append(
                (
                    province_id,
                    date,
                    rainfall_3d.get(date)
                )
            )

            rainfall_7d_list.append(
                (
                    province_id,
                    date,
                    rainfall_7d.get(date)
                )
            )

    rainfall_3d_df = pd.DataFrame(
        rainfall_3d_list,
        columns=[
            "province_id",
            "date",
            "rainfall_3d"
        ]
    )

    rainfall_7d_df = pd.DataFrame(
        rainfall_7d_list,
        columns=[
            "province_id",
            "date",
            "rainfall_7d"
        ]
    )

    df = df.merge(
        rainfall_3d_df,
        on=["province_id", "date"],
        how="left"
    )

    df = df.merge(
        rainfall_7d_df,
        on=["province_id", "date"],
        how="left"
    )

    df["date"] = pd.to_datetime(
        df["date"]
    ).dt.date

    df = df.sort_values(
        ["province_id", "date"]
    ).reset_index(drop=True)

    conn = connect_database()

    sql = """
        INSERT INTO daily_weather_dataset (
            province_id,
            date,
            rainfall_avg,
            rainfall_max,
            temperature_avg,
            humidity_avg,
            wind_speed_avg,
            station_count,
            created_at,
            rainfall_3d,
            rainfall_7d
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            NOW(), %s, %s
        )
        ON CONFLICT (province_id, date)
        DO UPDATE SET
            rainfall_avg = EXCLUDED.rainfall_avg,
            rainfall_max = EXCLUDED.rainfall_max,
            temperature_avg = EXCLUDED.temperature_avg,
            humidity_avg = EXCLUDED.humidity_avg,
            wind_speed_avg = EXCLUDED.wind_speed_avg,
            station_count = EXCLUDED.station_count,
            rainfall_3d = EXCLUDED.rainfall_3d,
            rainfall_7d = EXCLUDED.rainfall_7d,
            created_at = NOW()
    """

    try:

        cursor = conn.cursor()

        for _, row in df.iterrows():

            cursor.execute(
                sql,
                (
                    int(row["province_id"]),
                    row["date"],
                    row["rainfall_avg"],
                    row["rainfall_max"],
                    row["temperature_avg"],
                    row["humidity_avg"],
                    row["wind_speed_avg"],
                    int(row["station_count"]),
                    row["rainfall_3d"],
                    row["rainfall_7d"]
                )
            )

        conn.commit()
        cursor.close()

        print("บันทึก Daily Weather")
        print("วันที่ล่าสุด:", df["date"].max())

    except Exception as e:

        conn.rollback()
        print("เกิดข้อผิดพลาด:", e)

    finally:

        conn.close()


if __name__ == "__main__":
    save_daily_weather()