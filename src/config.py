import os
from dotenv import load_dotenv

def get_connection_string() -> str:
    load_dotenv()

    variables = {
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'POSTGRES_HOST': os.getenv('POSTGRES_HOST'),
        'POSTGRES_PORT': os.getenv('POSTGRES_PORT'),
        'POSTGRES_DB': os.getenv('POSTGRES_DB')
    }

    for key, value in variables.items():
        if value is None:
            raise EnvironmentError(f'Missing environment variable: {key}')


    return f'postgresql://{variables["POSTGRES_USER"]}:{variables["POSTGRES_PASSWORD"]}@{variables["POSTGRES_HOST"]}:{variables["POSTGRES_PORT"]}/{variables["POSTGRES_DB"]}'

