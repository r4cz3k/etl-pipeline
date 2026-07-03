import logging
import extract as e
import transform as t
import load as l

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

# Get data from API
raw_data = e.get_data('https://dummyjson.com/products')

# Create DataFrames
products = t.create_products_dataframe(raw_data)
reviews = t.create_reviews_dataframe(raw_data)
images = t.create_one_column_dataframe(products, 'images')
tags = t.create_one_column_dataframe(products, 'tags')

# Transform and clean DataFrames
products = t.transform_products_dataframe(products)
reviews = t.transform_reviews_dataframe(reviews)
images = t.transform_one_column_dataframe(images, 'images', 'image_url')
tags = t.transform_one_column_dataframe(tags, 'tags', 'tag')

# Save to CSV dict(filename : dataframe)
l.save_to_csv({
    'products': products,
    'reviews': reviews,
    'images': images,
    'tags': tags
})

