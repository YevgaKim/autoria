import requests
from bs4 import BeautifulSoup
from parser_autoria import parse_pages
import re


def cars():
    links = parse_pages()

    names = []
    images = []
    values = []
    kms = []
    bidfaxs = []

    count = 0
    for i in links:
        src = requests.get(i)

        
        soup = BeautifulSoup(src.text,"html.parser")

        image = soup.find_all("img", class_="outline m-auto")[:3]
        im = ""
        for k in image:
            k = k.get("src") + "\n"
            im += k
        images.append(str(im))

        s = soup.find("span", class_="bold").text
        name = soup.find("h3", class_="auto-content_title").text + " "
        name += s if not re.search("[x]", s) else ""
        names.append(str(name))
        values.append(str(soup.find("span", class_="price_value").text))
        kms.append(str(soup.find("div", class_="bold").text.strip()))
        bidfax_url = "https://bidfax.info/" + soup.find("div",class_="hide debug161 mainTemplate").find_next().find_next().find_next().find_next().get("data-bidfax-pathname")[8:]
        bidfaxs.append(str(bidfax_url))
        count+=1
        print(f"[INFO] Car number {count} is appended")


    return names, images, values, kms, bidfaxs, links



