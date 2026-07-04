import logging
import pandas as pd
import pathlib

logger = logging.getLogger(__name__)

def save_to_csv(dataframes: dict[str, pd.DataFrame], output_dir: str = 'output'):
    path = pathlib.Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    for name, df in dataframes.items():
        file_path = path / f'{name}.csv'
        logger.info(f"Saving {name} dataframe to {file_path}")
        df.to_csv(file_path, index=False)