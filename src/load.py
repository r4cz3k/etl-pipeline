import logging
import pandas as pd
import pathlib
from sqlalchemy import Engine

logger = logging.getLogger(__name__)

def save_to_csv(dataframes: dict[str, pd.DataFrame], output_dir: str = 'output') -> None:
    path = pathlib.Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    for name, df in dataframes.items():
        file_path = path / f'{name}.csv'
        logger.info(f"Saving {name} dataframe to {file_path}")
        df.to_csv(file_path, index=False)

def save_to_postgres(dataframes: dict[str, pd.DataFrame], engine: Engine) -> None:
    for name, df in dataframes.items():
        logger.info(f"Saving {name} dataframe to database")
        df.to_sql(name, con=engine, if_exists='replace', index=False)