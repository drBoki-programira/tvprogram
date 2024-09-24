import sqlite3

from config import DB_NAME
from items import Record


class DBM:
    """
    Class for interfacing with the database.
    """
    def __init__(self, table_name: str, db_name: str = DB_NAME) -> None:
        """Initialize channel names and optionaly database name/path"""
        self.db_name = db_name
        self.table_name = table_name.replace('-', '')
        self._connection = self._make_connection()

    def _make_connection(self) -> sqlite3.Connection:
        """Makes connection to the database."""
        connection = None
        try:
            connection = sqlite3.connect(self.db_name)
        except Exception as e:
            print(e)
        return connection

    def _create_tables(self) -> None:
        """Creates tables if they dont exist."""
        create_sql = '''
CREATE TABLE IF NOT EXISTS {0} (
    datetime TEXT PRIMARY KEY,
    genre TEXT,
    title TEXT,
    description TEXT
);
'''.format(self.table_name)

        self._connection.execute(create_sql)
        self._connection.commit()
        return None

    def insert(self, records: dict[str, Record]) -> None:
        """Inserts records in the table."""
        self._create_tables()
        insert_sqls = ["""
INSERT INTO
    {0} (datetime, genre, title, description)
VALUES
    ('{1}', '{2}', '{3}', '{4}');
""".format(self.table_name,
           record.time,
           record.tag,
           record.title,
           record.descr) for record in records]

        for sql in insert_sqls:
            try:
                self._connection.execute(sql)
            except Exception:
                pass
        self._connection.commit()

        return None
