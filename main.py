from scrape import TvCrawler
from dbmanager import (make_connection, execute_sql,
                       make_create_sql, make_insert_sql)
from config import CHANNELS, DB_NAME


def main():
    crawler = TvCrawler(CHANNELS)
    connection = make_connection(DB_NAME)

    for response, table_name, offset in crawler.run():
        crawler.get_records(response, table_name, offset)

    for table_name in crawler.channels:
        create_sql = make_create_sql(table_name)
        execute_sql(connection, create_sql)
        insert_sql = make_insert_sql(table_name, crawler.records[table_name])
        execute_sql(connection, insert_sql)

    print('Done.')


if __name__ == '__main__':
    main()
