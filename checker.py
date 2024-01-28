import sqlite3
from parser_cars import cars
import re


def check():
    all_links = []
    all_links_and_price = []

    data = cars()
    try:
        conn = sqlite3.connect("cars.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM toyota_sequoia WHERE is_sold=1")
        cursor.execute("UPDATE toyota_sequoia SET is_new = 0 WHERE is_new= 1")
        cursor.execute("UPDATE toyota_sequoia SET is_lower = 0 WHERE NOT is_lower = 0")
        cursor.execute("UPDATE toyota_sequoia SET is_higher = 0 WHERE NOT is_higher = 0")
        conn.commit()
        cursor.execute("SELECT * FROM toyota_sequoia")
        results = cursor.fetchall()
        for i in results:
            all_links_and_price.append([i[-5],i[2]])
            all_links.append(i[-5])
        if len(data[5])!=len(all_links_and_price):
            for i in all_links_and_price:
                if not i[0] in data[5]:
                    cursor.execute(f"UPDATE toyota_sequoia SET is_sold = 1 WHERE links = ?", (i[0],))
                    conn.commit()
            for i in range(len(data[5])):
                if not data[5][i] in all_links:
                    insert_query = """INSERT INTO toyota_sequoia (names, images, vals, kms, bidfaxs, links, is_higher, is_lower, is_sold, is_new) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                    record_to_insert = (data[0][i], data[1][i], data[2][i], data[3][i], data[4][i], data[5][i], 0, 0, 0, 1,)
                    cursor.execute(insert_query, record_to_insert)
                    conn.commit()
                
        for i in all_links_and_price:
            for j in range(len(data[-4])):
                if i[0]==data[-1][j]:
                    price_str_1 = i[1]
                    price_int_1 = int(re.sub("[^0-9]", "", price_str_1))
                    price_str_2 = data[2][j]
                    price_int_2 = int(re.sub("[^0-9]", "", price_str_2))
                    
                    r = price_int_2 - price_int_1

                    if price_int_1 == price_int_2:
                        break
                    
                    if price_int_1 > price_int_2:
                        cursor.execute(f"UPDATE toyota_sequoia SET is_lower = {r} WHERE links = ?", (i[0],))
                        cursor.execute(f"UPDATE toyota_sequoia SET vals = '{price_str_2}' WHERE links = ?", (i[0],))
                        conn.commit()
                        break
            
                    if price_int_1 < price_int_2:

                        cursor.execute(f"UPDATE toyota_sequoia SET is_higher = {r} WHERE links = ?", (i[0],))
                        cursor.execute(f"UPDATE toyota_sequoia SET vals = '{price_str_2}' WHERE links = ?", (i[0],))
                        conn.commit()
                        break
                    break
        
    


    except (Exception, sqlite3.Error) as error:
        print(1)
        print(error)
    finally:
        conn.close()