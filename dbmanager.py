import sqlite3

from items import Record


def make_connection(db_name: str) -> sqlite3.Connection:
    """Makes connection to the database."""
    connection = None
    try:
        connection = sqlite3.connect(db_name)
    except Exception as e:
        print('DB connection error: ', e)
    return connection


def execute_sql(connection: sqlite3.Connection, sql: str) -> None:
    """Executes sql command"""
    try:
        connection.execute(sql)
    except sqlite3.IntegrityError:
        print('Preventing duplicating the rows.')
    connection.commit()
    return None


def make_create_sql(table_name: str) -> str:
    fmt_table_name = table_name.replace('-', '')
    return '''
CREATE TABLE IF NOT EXISTS {0} (
    datetime TEXT PRIMARY KEY,
    genre TEXT,
    title TEXT,
    description TEXT
);
'''.format(fmt_table_name)


def make_insert_sql(table_name: str, records: list[Record]) -> str:
    fmt_table_name = table_name.replace('-', '')
    input_str = [f"('{record.time}', '{record.tag}',"
                 f"'{record.title}', '{record.descr}')"
                 for record in records]
    return '''
INSERT INTO
    {0} (datetime, genre, title, description)
VALUES
    {1}
'''.format(fmt_table_name, ','.join(input_str))


def make_select_sql(table_name: str) -> str:
    fmt_table_name = table_name.replace('-', '')
    return '''
SELECT * FROM {0}
'''.format(fmt_table_name)
