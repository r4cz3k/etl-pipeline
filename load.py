import logging

logger = logging.getLogger(__name__)

def save_to_csv(dataframes: dict):
    for name, df in dataframes.items():
        logger.info(f"Saving {name} dataframe to {name}.csv")
        df.to_csv(name + '.csv', index=False)