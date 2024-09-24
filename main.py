from scrape import TvCrawler
from dbm import DBM
from config import CHANNELS


def main():
    crawler = TvCrawler(CHANNELS)

    for response, table_name, offset in crawler.run():
        crawler.get_records(response, table_name, offset)

    for table_name in crawler.channels:
        DBM(table_name).insert(crawler.records[table_name])

    print('Done.')


if __name__ == '__main__':
    main()
