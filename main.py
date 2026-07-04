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

    # Create DataFrames
    products = transform.create_products_dataframe(raw_data)
    reviews = transform.create_reviews_dataframe(raw_data)
    images = transform.create_one_column_dataframe(products, 'images')
    tags = transform.create_one_column_dataframe(products, 'tags')

    # Transform and clean DataFrames
    products = transform.transform_products_dataframe(products)
    reviews = transform.transform_reviews_dataframe(reviews)
    images = transform.transform_one_column_dataframe(images, 'images', 'image_url')
    tags = transform.transform_one_column_dataframe(tags, 'tags', 'tag')

    # Save to CSV dict(filename : dataframe)
    load.save_to_csv({
        'products': products,
        'reviews': reviews,
        'images': images,
        'tags': tags
    })

if __name__ == '__main__':
    main()