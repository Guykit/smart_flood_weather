import requests
import re


def get_dates(file_name):

    if not file_name:
        return []

    dates = re.findall(
        r"\d{8}",
        file_name
    )

    return sorted(set(dates))


def get_gistda_flood():

    url = (
        "https://api-gateway.gistda.or.th/"
        "api/2.0/resources/features/flood/30days"
    )

    api_key = "vZ3p9P2Lmfkh2PLHaaZOgDfvgkvGqtOP4Fi2kemq2DCRvI6spmClYVPUpCwJdXPt"

    limit = 1000
    offset = 0

    flood_data = []

    while True:

        print("\n==============================")
        print("กำลังดึงข้อมูล")
        print("Offset:", offset)
        print("Limit:", limit)
        print("==============================")

        params = {
            "api_key": api_key,
            "limit": limit,
            "offset": offset
        }

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        print("Status:", response.status_code)

        if response.status_code != 200:

            print("API Error")
            print(response.text)

            return []

        data = response.json()

        total = data.get(
            "numberMatched",
            0
        )

        features = data.get(
            "features",
            []
        )

        print(
            "จำนวนทั้งหมด:",
            total
        )

        print(
            "จำนวนที่ได้:",
            len(features)
        )

        if not features:
            break

        for feature in features:

            properties = feature.get(
                "properties",
                {}
            )

            file_name = properties.get(
                "file_name"
            )

            flood = {

                "gistda_id":
                    properties.get("pv_idn"),

                "district_id":
                    properties.get("ap_idn"),

                "subdistrict_id":
                    properties.get("tb_idn"),

                "file_name":
                    file_name,

                "dates":
                    get_dates(file_name),

                "flood_area":
                    properties.get("f_area")
            }

            flood_data.append(flood)

        offset += len(features)

        if offset >= total:

            print("\nดึงข้อมูลครบแล้ว")
            break



    print(
        "จำนวน Feature:",
        len(flood_data)
    )

    return flood_data


if __name__ == "__main__":

    data = get_gistda_flood()