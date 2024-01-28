import requests 
from bs4 import BeautifulSoup
import re
import math



def parse_pages():
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(" ")

    response = requests.get(f"https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=0&country.import.id=840&price.currency=1&abroad.not=-1&custom.not=-1&damage.not=0&page=0&size=10")

    match = re.search(r'Number\((\d+)\)', response.text)


    number_value = int(match.group(1))
    n = math.ceil(number_value/20)


    try:
        for i in range(n):
            response = requests.get(f"https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=0&country.import.id=840&price.currency=1&abroad.not=-1&custom.not=-1&damage.not=0&page={i}&size=20")
            if response.status_code=="200":
                print("Yes")
            with open("index.html", "a", encoding="utf-8") as f:
                f.write(response.text)
            print(f"{i} - page is closed")
    except:
        print(f"{i} pages")

    with open("index.html", "r", encoding="utf-8") as f:
        src = f.read()

    soup = BeautifulSoup(src,"html.parser")

    all_cars = soup.find_all("div", class_="content-bar")

    all_links = []

    for i in all_cars:
        all_links.append(i.find("a", class_="m-link-ticket").get("href"))

    return all_links




