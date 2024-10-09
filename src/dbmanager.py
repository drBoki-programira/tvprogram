import psycopg2

from items import Record


def make_connection(db_name, db_user, db_password, db_host, db_port):
    connection = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    print('Connection to PostgreSQL DB succesful.')
    return connection


def make_create_sql(table_name: str) -> str:
    """Creates SQL command for creating tables."""
    return '''
CREATE TABLE IF NOT EXISTS {0} (
    datetime TIMESTAMP PRIMARY KEY,
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
INSERT INTO
    {0} (datetime, genre, title, description)
VALUES
    {1}
ON CONFLICT (datetime)
DO NOTHING
'''.format(table_name, input_str)


def make_select_sql(table_name: str) -> str:
    """Creates SQL command for selecting all rows in the table."""
    return '''
SELECT * FROM {0}
'''.format(table_name)
