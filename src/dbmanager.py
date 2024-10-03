import sqlite3

from items import Record


def make_connection(db_name: str) -> sqlite3.Connection:
    """Makes connection to the database."""
    connection = None
    try:
        connection = sqlite3.connect(db_name)
    except Exception as e:
        print('DB connection error: ', e)
        quit()
    return connection


def make_create_sql(table_name: str) -> str:
    """Creates SQL command for creating tables."""
    return '''
CREATE TABLE IF NOT EXISTS {0} (
    datetime TEXT PRIMARY KEY,
    genre TEXT,
    title TEXT,
    description TEXT
);
'''.format(table_name)


def make_insert_sql(table_name: str, records: list[Record]) -> str:
    """Creates SQL command for inserting records into the table."""
    input_list = [f"('{record.time}', '{record.tag}',"
                  f"'{record.title}', '{record.descr}')"
                  for record in records]
    input_str = ','.join(list(dict.fromkeys(input_list)))  # no duplicates
    return '''
INSERT OR REPLACE INTO
    {0} (datetime, genre, title, description)
VALUES
    {1}
'''.format(table_name, input_str)


def make_select_sql(table_name: str) -> str:
    """Creates SQL command for selecting all rows in the table."""
    return '''
SELECT * FROM {0}
'''.format(table_name)
