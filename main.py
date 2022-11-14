""" Scrape product webpage informtaion, given it's UPC"""
import json
import logging
import os
import re
import sys
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from utils.extract_url import get_product_url

logging.basicConfig(level=logging.INFO)
load_dotenv()


def selenium_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = os.getenv("CHROMEBINARY")
    driver = webdriver.Chrome(
        service=Service(os.getenv("CHROMEDRIVER")), options=options
    )
    return driver


def get_webpage_soup():
    upc = sys.argv[1]
    logging.info("UPC: %s", upc)

    driver = selenium_driver()
    url = get_product_url(upc)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source.replace("\n", " ")
    html = " ".join(html.split())
    return BeautifulSoup(html, "lxml")


def get_webpage_data():
    soup = get_webpage_soup()
    scripts = soup.find_all("script", {"type": "text/javascript"})
    for script in scripts:
        data = re.search(r"; jQuery.ajax\({*?(.*?)},[ ]{1,}success", str(script))
        if data:
            logging.info("Data found in HTML Response")
            data = data.group(1)
            data = data.split("postdata:")[1].strip()
            logging.info(data)
            with open("data.json", "w+", encoding="utf-8") as file_:
                file_.write(str(data))
            break

    json_data = json.loads(data)
    id_ = json_data.get("id")
    product_name = json_data.get("name")
    product_sku = json_data.get("sku")
    product_price = json_data.get("price")
    product_brand = json_data.get("product_brand")
    product_model = json_data.get("model")
    additional_info = json_data.get("additional_information")

    item_list = [
        id_,
        product_name,
        product_sku,
        product_price,
        product_brand,
        product_model,
        additional_info,
    ]

    logging.info(item_list)


if __name__ == "__main__":
    get_webpage_data()
