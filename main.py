import logging
import os
import sys
from dotenv import load_dotenv
import src.extract as extract
import src.transform as transform
import src.load as load
import src.config as config
from sqlalchemy import create_engine

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

    save_destination = os.getenv("SAVE_DESTINATION")
    if save_destination is None:
        sys.exit('Please set SAVE_DESTINATION environment variable')
    elif save_destination == 'DB':
        engine = create_engine(config.get_connection_string())
        try:
            with engine.connect():
                pass # healthcheck - fail fast - if database connection fails - pipeline won't start
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    # Get data from API
    raw_data = extract.get_data(api_url)

    # Get transformed dataframes
    dataframes = transform.transform_all(raw_data)

    # Save to CSV dict(filename : dataframe) OR DB
    match save_destination:
        case "DB":
            load.save_to_postgres(dataframes, engine)
        case "CSV":
            load.save_to_csv(dataframes)
        case _:
            sys.exit(f"Unknown SAVE_DESTINATION: {save_destination}, use CSV or DB")

if __name__ == '__main__':
    main()