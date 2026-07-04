import logging
import os
import sys
from dotenv import load_dotenv
import src.extract as extract
import src.transform as transform
import src.load as load


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )

    logger = logging.getLogger(__name__)
    load_dotenv()

    api_url = os.getenv('API_URL')

    if api_url is None:
        sys.exit("There was a problem loading .env file, check if .env file or API_URL variable exists")
    else:
        logger.info(".env file successfully loaded")

    # Get data from API
    raw_data = extract.get_data(api_url)

    # Get transformed dataframes
    dataframes = transform.transform_all(raw_data)

    # Save to CSV dict(filename : dataframe)
    load.save_to_csv(dataframes)

if __name__ == '__main__':
    main()