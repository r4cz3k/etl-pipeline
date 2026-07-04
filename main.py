import logging
import src.extract as extract
import src.transform as transform
import src.load as load

API_URL = 'https://dummyjson.com/products'

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )

    # Get data from API
    raw_data = extract.get_data(API_URL)

    # Get transformed dataframes
    dataframes = transform.transform_all(raw_data)

    # Save to CSV dict(filename : dataframe)
    load.save_to_csv(dataframes)

if __name__ == '__main__':
    main()