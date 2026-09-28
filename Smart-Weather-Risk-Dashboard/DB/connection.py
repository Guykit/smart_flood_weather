import psycopg


def connect_database():
    connection = psycopg.connect(
        host = "localhost",
        port = 5433,
        dbname="smart_weather_db",
        user="postgres",
        password = "0000"
    )
    return connection