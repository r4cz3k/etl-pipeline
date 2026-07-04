import requests as rq
import logging
from time import sleep

logger = logging.getLogger(__name__)

def retry(tries=4):
    """
    :tries: Number of times to retry an API call (4 tries = 3 timeouts)
    """
    def retry_logic(func):
        def wrapper(*args, **kwargs):
            for parse_try in range(tries):
                try:
                    response = func(*args, **kwargs)
                    return response

                except rq.exceptions.HTTPError as e:
                    # Raise an exception when url does not exist or is forbidden
                    if e.response.status_code in range(400, 500):
                        logger.error(f"HTTP ERROR: {e}")
                        raise

                    if e.response.status_code in range(500, 600):
                        if parse_try == tries - 1:  # last try, otherwise impossible to raise
                            logger.error(f"HTTP ERROR: {e}")
                            raise
                        else:
                            logger.warning(f"HTTP ERROR: {e}")
                            sleep(3 ** parse_try)  # 3 intervals before raise: 1s / 3s / 9s

                except rq.exceptions.ConnectionError as e:
                    if parse_try == tries - 1:  # last try, otherwise impossible to raise
                        logger.error(f"Connection ERROR: {e}")
                        raise
                    else:
                        logger.warning(f"Connection ERROR: {e}")
                        sleep(3 ** parse_try)  # 3 intervals before raise: 1s / 3s / 9s

                except rq.exceptions.RequestException as e:
                    logger.error(f"Request ERROR: {e}")
                    raise

            raise RuntimeError('All retries failed')
        return wrapper

    return retry_logic

@retry(tries=4)
def fetch_page(url: str, params: dict[str, int]):
    response = rq.get(url, params=params)
    response.raise_for_status()
    return response


def get_data(url: str, limit: int = 30) -> list[dict]:
    """
    Returns a list of values from JSON response from API
    :param url: URL to get data from
    :param limit: Number of maximum products per API response page
    :return: Returns a list of products as dictionary
    """
    logger.info("Parsing JSON response from API")
    products = {}
    skip = 0
    parsed = 0

    while True:
        response = fetch_page(url, params={'skip': skip})

        data = response.json()

        response_len = len(data['products'])
        parsed += response_len

        if response_len < 1:
            break
        else:
            logger.info(f"Parsed {parsed}/{data['total']}")

        for product in data['products']:
            products[product['id']] = product

        skip += limit

    return list(products.values())