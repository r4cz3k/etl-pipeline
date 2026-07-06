import pandas as pd
import logging

logger = logging.getLogger(__name__)


def create_products_dataframe(products_values_list: list[dict]) -> pd.DataFrame:
    logger.info("Creating products dataframe")
    return pd.json_normalize(products_values_list, sep="_")


def transform_products_dataframe(products_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transforming products dataframe")
    return products_df.drop(columns=["reviews", "images", "tags"])


def create_reviews_dataframe(products_values_list: list[dict]) -> pd.DataFrame:
    logger.info("Creating reviews dataframe")
    return pd.json_normalize(products_values_list, record_path=["reviews"], meta=["id"])


def transform_reviews_dataframe(reviews_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transforming reviews dataframe")
    reviews_df = reviews_df.rename(columns={"id": "product_id"})
    reviews_df.insert(0, "product_id", reviews_df.pop("product_id"))
    return reviews_df


def create_one_column_dataframe(products_df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    logger.info(f"Creating {column_name} dataframe")
    return products_df[["id", column_name]].explode(f"{column_name}")


def transform_one_column_dataframe(df: pd.DataFrame, previous: str, correct: str) -> pd.DataFrame:
    return df.rename(columns={"id": "product_id", previous: correct})


def transform_all(raw_data: list[dict]) -> dict[str, pd.DataFrame]:
    # Create DataFrames
    products_full = create_products_dataframe(raw_data)
    reviews = create_reviews_dataframe(raw_data)
    images = create_one_column_dataframe(products_full, "images")
    tags = create_one_column_dataframe(products_full, "tags")

    # Transform DataFrames
    products = transform_products_dataframe(products_full)
    reviews = transform_reviews_dataframe(reviews)
    images = transform_one_column_dataframe(images, "images", "image_url")
    tags = transform_one_column_dataframe(tags, "tags", "tag")

    return {"products": products, "reviews": reviews, "images": images, "tags": tags}
