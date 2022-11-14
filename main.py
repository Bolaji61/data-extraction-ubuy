import re
import json
import time
import logging
from post_requests import get_product_url
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

logging.basicConfig(level=logging.INFO)


def selenium_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = (
        r"/Applications/Google Chrome 3.app/Contents/MacOS/Google Chrome"
    )
    driver = webdriver.Chrome(service=Service("../chromedriver"), options=options)
    return driver


def get_webpage_source(upc):
    driver = selenium_driver()
    url = get_product_url(upc)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source.replace("\n", " ")
    html = " ".join(html.split())
    return BeautifulSoup(html, "lxml")


def get_webpage_data(upc):
    soup = get_webpage_source(upc)
    scripts = soup.find_all("script", {"type": "text/javascript"})
    for script in scripts:
        data = re.search("; jQuery.ajax\({*?(.*?)},[ ]{1,}success", str(script))
        if data:
            logging.info("Data found in HTML Response")
            data = data.group(1)
            data = data.split("postdata:")[1].strip()
            logging.info(data)
            with open("data.json", "w+") as f_:
                f_.write(str(data))
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
    get_webpage_data("B00C91Q86I")
