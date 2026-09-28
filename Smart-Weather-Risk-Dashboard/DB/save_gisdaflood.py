from DB.connection import connect_database
from service.gisdaflood import get_gistda_flood


def save_gisdaflood():


    data = get_gistda_flood()

    if not data:

        print("ไม่พบข้อมูล GISTDA")

        return





    connection = connect_database()

    cursor = connection.cursor()


    try:



        sql = """

            INSERT INTO flood_events (

                province_id,
                district_id,
                date,
                flood_area,
                flood

            )

            VALUES (%s, %s, %s, %s, %s)

            ON CONFLICT ON CONSTRAINT unique_flood_event

            DO UPDATE SET

                flood_area = EXCLUDED.flood_area,
                flood = EXCLUDED.flood

        """




        for row in data:



            province_id = row["gistda_id"]
            district_id = row["district_id"]
            flood_area = row["flood_area"]
            dates = row["dates"]

            # วนแต่ละวันที่

            for date_text in dates:

                date = (
                    date_text[:4]
                    + "-"
                    + date_text[4:6]
                    + "-"
                    + date_text[6:8]
                )


                cursor.execute(

                    sql,

                    (
                        province_id,
                        district_id,
                        date,
                        flood_area,
                        1
                    )

                )


        connection.commit()


        print("SAVE gisdaflood SUCCESS ")




    except Exception as e:


        connection.rollback()

        print("SAVE gisdaflood  ไม่ SUCCESS ")
        print(e)


    finally:


        cursor.close()

        connection.close()


if __name__ == "__main__":

    save_gisdaflood()