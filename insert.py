import sqlite3
from parser_cars import cars


try:
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM toyota_sequoia")
        data = cars()
        count = 0
        for name, image, value, km, bidfax, link in zip(data[0],data[1],data[2],data[3],data[4],data[5]):
                insert_query = """INSERT INTO toyota_sequoia (names, images, vals, kms, bidfaxs, links, is_higher, is_lower, is_sold, is_new) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                record_to_insert = (name, image, value, km, bidfax, link, 0, 0, 0, 0)
                cursor.execute(insert_query, record_to_insert)
                count += 1
                print(f"Line {count} is added")
                conn.commit()
except (Exception, sqlite3.Error) as error:
    print(error)
finally:
    conn.close()