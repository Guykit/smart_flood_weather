import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from DB.connection import connect_database


FEATURES = [
    "rainfall",
    "rainfall_24h",
    "rainfall_3d",
    "rainfall_7d",
    "temperature",
    "humidity",
    "wind_speed"
]

TARGET = "flood"


def load_train_data():

    conn = connect_database()

    sql = """
        SELECT
            province_id,
            date,
            rainfall,
            rainfall_24h,
            rainfall_3d,
            rainfall_7d,
            temperature,
            humidity,
            wind_speed,
            flood
        FROM daily_flood_ml
        ORDER BY date, province_id
    """

    df = pd.read_sql(sql,conn)

    conn.close()

    return df

def load_today_data():
    con = connect_database()

    sql = """
        SELECT
            province_id,
            date,
            rainfall_avg AS rainfall,
            rainfall_max AS rainfall_24h,
            rainfall_3d,
            rainfall_7d,
            temperature_avg AS temperature,
            humidity_avg AS humidity,
            wind_speed_avg AS wind_speed
        FROM daily_weather_dataset
        WHERE date = CURRENT_DATE
        ORDER BY province_id
    """
    df = pd.read_sql(sql, con)

    con.close()

    return df


def train_model():

    df = load_train_data()

    df["date"] = pd.to_datetime(df["date"])


    dates = sorted(df["date"].dt.date.unique())

    x  = int(len(dates) * 0.8)

    train_dates = dates[:x]
    test_dates = dates[x:]
    
    train_df = df[df["date"].dt.date.isin(train_dates)]

    test_df = df[df["date"].dt.date.isin(test_dates)]

    x_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    model = RandomForestClassifier(
        class_weight="balanced",
        random_state=42
    )

    model.fit(x_train, y_train)

    y_pred = model.predict(X_test)

    #ดูค่า

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    print()
    print("MODEL PERFORMANCE")

    print(
        "Accuracy :",
        round(accuracy, 4)
    )

    print(
        "Precision:",
        round(precision, 4)
    )

    print(
        "Recall   :",
        round(recall, 4)
    )

    print(
        "F1 Score :",
        round(f1, 4)
    )

    print()
    print("CONFUSION MATRIX")

    cm = confusion_matrix(
        y_test,
        y_pred
    )

    print(cm)


    final_model = RandomForestClassifier(
        class_weight="balanced",
        random_state=42
    )

    X_all = df[FEATURES]
    y_all = df[TARGET]

    final_model.fit(
        X_all,
        y_all
    )

    print()
    print("TRAIN FINAL MODEL SUCCESS")

    return final_model

def predic_today():
    df = load_today_data()

    x = df[FEATURES]

    model = train_model()

    prediction = model.predict(x)

    probability = model.predict_proba(x)[:, 1]

    df["prediction"] = prediction
    df["flood_probability"] = probability

    print(prediction)
    print(probability)
    
    return df




if __name__ == "__main__":
    predic_today()

    







