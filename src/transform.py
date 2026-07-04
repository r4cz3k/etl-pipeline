import pandas as pd
import logging

logger = logging.getLogger(__name__)

def create_products_dataframe(products_values_list):
    logger.info("Creating products dataframe")
    return pd.json_normalize(products_values_list, sep='_')

def transform_products_dataframe(products_df):
    logger.info("Transforming products dataframe")
    return products_df.drop(columns=['reviews', 'images', 'tags'])

def create_reviews_dataframe(products_values_list):
    logger.info("Creating reviews dataframe")
    return pd.json_normalize(products_values_list, record_path=['reviews'], meta=['id'])

def transform_reviews_dataframe(reviews_df):
    logger.info("Transforming reviews dataframe")
    reviews_df = reviews_df.rename(columns={'id': 'product_id'})
    reviews_df.insert(0, 'product_id', reviews_df.pop('product_id'))
    return reviews_df

def create_one_column_dataframe(products_df, column_name):
    logger.info(f"Creating {column_name} dataframe")
    return products_df[['id', f'{column_name}']].explode(f'{column_name}')

def transform_one_column_dataframe(df, previous: str, correct: str):
    return df.rename(columns={'id': 'product_id', previous: correct})


