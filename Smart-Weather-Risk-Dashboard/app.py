from flask import Flask, render_template, jsonify, request
from DB import connection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/provinces")
def province():

    con = connection.connect_database()
    cursor = con.cursor()

    sql = """
        SELECT province_id, province_name
        FROM province
        ORDER BY province_id
    """

    cursor.execute(sql)

    rows = cursor.fetchall()

    cursor.close()
    con.close()

    province = []

    for row in rows:
        province.append({
            "province_id": row[0],
            "province_name": row[1]
        })

    return jsonify(province)


@app.route("/api/dates")
def dates():

    con = connection.connect_database()
    cursor = con.cursor()

    sql = """
        SELECT DISTINCT date
        FROM daily_weather_dataset
        ORDER BY date DESC
    """

    cursor.execute(sql)

    rows = cursor.fetchall()

    cursor.close()
    con.close()

    dates = []

    for row in rows:
        dates.append({
            "date": row[0].isoformat()
        })

    return jsonify(dates)


@app.route("/api/weather/<int:province_id>")
def weather(province_id):

    date = request.args.get("date")

    con = connection.connect_database()
    cursor = con.cursor()

    sql = """
        SELECT
            w.date,
            w.temperature_avg,
            w.humidity_avg,
            w.wind_speed_avg,
            w.rainfall_avg,
            w.rainfall_3d,
            w.rainfall_7d,
            p.flood_probability,
            p.prediction
        FROM daily_weather_dataset w
        LEFT JOIN daily_flood_prediction p
            ON w.province_id = p.province_id
            AND w.date = p.date
        WHERE w.province_id = %s
        AND w.date = %s
    """

    cursor.execute(sql,(province_id, date))

    row = cursor.fetchone()

    cursor.close()
    con.close()

    return jsonify({
        "date": row[0].isoformat(),
        "temperature": row[1],
        "humidity": row[2],
        "wind_speed": row[3],
        "rainfall": row[4],
        "rainfall_3d": row[5],
        "rainfall_7d": row[6],
        "flood_probability": row[7],
        "prediction": row[8]
    })



@app.route("/api/top-province")
def top_province():

    con = connection.connect_database()
    cursor = con.cursor()

    sql = """
        SELECT
            p.province_name,
            f.flood_probability,
            f.prediction
        FROM daily_flood_prediction f
        JOIN province p
        ON f.province_id = p.province_id
        WHERE f.date = CURRENT_DATE
        ORDER BY f.flood_probability DESC
        LIMIT 5
    """

    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    con.close()

    data = []

    for row in rows:
        data.append({
            "province_name": row[0],
            "flood_probability": float(row[1]),
            "prediction": row[2]
        })

    return jsonify(data)



if __name__ == "__main__":
    app.run(
        debug=True,
        port=5001
    )