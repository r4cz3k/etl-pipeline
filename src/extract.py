import requests as rq
import logging

logger = logging.getLogger(__name__)

def get_data(url):
    """
    Returns a list of values from JSON response from API
    :param url:
    :return:
    """
    logger.info("Parsing JSON response from API")
    products = {}
    skip = 0
    parsed = 0

    while True:
        response = rq.request('GET', url, params={"skip": skip})

        response_len = len(response.json()['products'])
        parsed += response_len

        if response_len < 1:
            break
        else:
            logger.info(f"Parsed {parsed}/{response.json()['total']}")

        for product in response.json()['products']:
            products[product['id']] = product

        skip += 30

    return list(products.values())