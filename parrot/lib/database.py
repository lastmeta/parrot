''' database can just be a csv for now '''
from parrot import config
import pandas as pd


def get_schema(database: pd.DataFrame = None) -> list:
    if database:
        return database.columns.tolist()
    return ['path', 'hash', 'removed', 'created', 'timestamp']


def get_key_schema(database: pd.DataFrame = None) -> tuple:
    schema = get_schema(database)
    return schema[0], schema


def get():
    try:
        return pd.read_csv(config.root('database', 'database.csv'))
    except Exception as e:
        return pd.DataFrame([], columns=get_schema())


def save(database: pd.DataFrame):
    return database.to_csv(config.root('database', 'database.csv'), index=False)


def upsert(database: pd.DataFrame, record: dict):
    ''' record.keys() = get_schema '''
    key, schema = get_key_schema(database)
    if len(database.loc[database[key] == record[key]]) > 0:
        for item in schema[1:]:
            database.loc[database[key] == record[key], item] = record[item]
    else:
        database = pd.concat([database, pd.DataFrame({k: [v] for k, v in record.items()})])
    return database
