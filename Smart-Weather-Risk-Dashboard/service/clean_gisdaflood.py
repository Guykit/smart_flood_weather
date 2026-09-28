import pandas as pd
from service.gisdaflood import get_gistda_flood


def clean_gisdaflood():

    # ดึงข้อมูลจาก GISTDA
    flood_data = get_gistda_flood()

    if flood_data is None:
        print("ไม่สามารถดึงข้อมูลจาก GISTDA ได้")
        return None

    if len(flood_data) == 0:
        print("GISTDA ไม่มีข้อมูล")
        return pd.DataFrame()

    # แปลงเป็น DataFrame
    data = pd.DataFrame(flood_data)

    # คอลัมน์ที่เป็นตัวเลข
    numeric_columns = [
        "gistda_id",
        "district_id",
        "subdistrict_id",
        "flood_area"
    ]

    for column in numeric_columns:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    # แปลงวันที่
    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    ).dt.date

    # ตรวจสอบข้อมูลผิดปกติ
    invalid_flood_area = data[
        data["flood_area"] < 0
    ]

    invalid_gistda = data[
        data["gistda_id"] <= 0
    ]

    invalid_district = data[
        data["district_id"] <= 0
    ]

    invalid_subdistrict = data[
        data["subdistrict_id"] <= 0
    ]

    # ลบข้อมูลที่จำเป็นแต่ไม่มีค่า
    data = data.dropna(
        subset=[
            "gistda_id",
            "district_id",
            "date",
            "flood_area"
        ]
    )

    # ลบพื้นที่น้ำท่วมติดลบ
    data = data[
        data["flood_area"] >= 0
    ]

    # รวมพื้นที่น้ำท่วม
    # หลาย H3 รวมเป็น จังหวัด + อำเภอ + วัน
    data = data.groupby(
        [
            "gistda_id",
            "district_id",
            "date"
        ]
    )["flood_area"].sum()

    # สร้าง Label
    data["flood"] = 1

    print("Clean GISTDA Flood สำเร็จ")
    print("ข้อมูลทั้งหมด:", len(data))

    return data


if __name__ == "__main__":
    clean_gisdaflood()