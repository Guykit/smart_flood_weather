from ML.train_flood_model import predic_today
from DB.connection import connect_database

def save_predict():
    data = predic_today()


    conn = connect_database()

    sql = """
        INSERT INTO daily_flood_prediction (
            province_id,
            date,
            flood_probability,
            prediction
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (province_id, date)
        DO UPDATE SET
            flood_probability = EXCLUDED.flood_probability,
            prediction = EXCLUDED.prediction,
            created_at = CURRENT_TIMESTAMP
        """



    cursor = conn.cursor()

    for _, row in data.iterrows():

            cursor.execute(
                sql,
                (
                    int(row["province_id"]),
                    row["date"],
                    float(row["flood_probability"]),
                    int(row["prediction"])
                )
            )

    conn.commit()

    cursor.close()

    print("SAVE PREDICTION SUCCESS")

    conn.close()