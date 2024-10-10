from scrape import TvCrawler
from dbmanager import (make_connection, make_create_sql, make_insert_sql)
from config import CHANNELS, START_URL, SELECTORS, settings
from items import Days


def main():
    crawler = TvCrawler(
        CHANNELS,
        START_URL,
        SELECTORS,
        Days
    )
    connection = make_connection(
        settings.database,
        settings.user,
        settings.password,
        settings.host,
        settings.port
    )
    cursor = connection.cursor()

    for response, channel, offset in crawler.run():
        crawler.get_records(response, channel, offset)

    for channel in crawler.channels:
        table_name = channel.replace('-', '_').capitalize()
        create_sql = make_create_sql(table_name)
        cursor.execute(create_sql)
        insert_sql = make_insert_sql(table_name, crawler.records[channel])
        cursor.execute(insert_sql)

    connection.commit()
    print('Done.')


if __name__ == '__main__':
    main()
