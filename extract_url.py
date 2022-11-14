import logging
import os

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
token = os.getenv("TOKEN")


def get_json_response(upc):
    url = "https://www.you-buy.ca/en/ubcommon/usstore/search/products"

    payload = f"q={upc}&node_id=&page=1&brand=&ufulfilled=&price_range=&sort_by=&s_id=81&lang=&dc=&csrftoken={token}"
    headers = {
        "authority": "www.you-buy.ca",
        "accept": "text/html, */*; q=0.01",
        "accept-language": "en-GB,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "__zlcmid=1CqlMVkSecMK0Yr; PHPSESSID=7013nlchs3u18s0b4tjrhcvhr0",
        "origin": "https://www.you-buy.ca",
        "referer": "https://www.you-buy.ca/en/search/?q=B00C91Q86I",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    logging.info("Get Product Url")
    response = requests.request("POST", url, headers=headers, data=payload, timeout=60)
    logging.info("Requests Status Code: %s", response.status_code)

    soup = BeautifulSoup(response.text, "lxml")

    return soup


def get_product_url(upc):
    soup = get_json_response(upc)
    try:
        product_url = soup.find("input", {"name": "product_url"}).get("value")
    except AttributeError:
        product_url = ""
    logging.info("Product Url: %s", product_url)
    return product_url
