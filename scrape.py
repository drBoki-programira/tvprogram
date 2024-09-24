from datetime import datetime, date, timedelta
from typing import Generator

import bs4
import requests

from config import DAYS, START_URL
from items import Record


class TvCrawler:
    """
    Class for scraping naslovi.net and getting information about tv schedule.
    """
    def __init__(
            self, channels: list[str],
            start_url: str = START_URL,
            date_offsets: dict[str] = DAYS
                                      ) -> None:
        """Initilizes class with channel names to scrape."""
        self.start_url = start_url
        self.channels = channels
        self.date_offsets = date_offsets
        self.date = date.today()
        self.records = {channel: [] for channel in self.channels}

    def run(self) -> Generator[str, str, timedelta]:
        """Runs the crawler and generates response pages"""
        for url in self._list_urls():
            table_name, date_offset = url.split('/')[-2:]
            ofsset = self.date_offsets[date_offset]
            yield self._get_page(url), table_name, ofsset

    def _get_page(self, url: str) -> str:
        """Downloads the page for the given url."""
        response = requests.get(url)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)

        return response.text

    def _list_urls(self) -> list[str]:
        """Produces a list of urls to scrape from."""
        return [f'{self.start_url}{channel}/{offset}'
                for channel in self.channels
                for offset in self.date_offsets.keys()]

    def get_records(self, response: requests.Response,
                    table_name: str,
                    offset: timedelta | None) -> dict[str, Record]:
        """
        Parses the response page and fills dictionary with scraped records.
        """
        page = bs4.BeautifulSoup(response, 'html.parser')
        all_elements = page.select('div.tvrow')

        for element in all_elements:
            time, tag, title, descr = self._extract_fields(element)

            if offset:
                time += offset
            if self.records[table_name] and self.records[table_name][-1].time > time:  # noqa: E501
                time += timedelta(days=1)

            record = Record(time=time, tag=tag, title=title, descr=descr)
            self.records[table_name].append(record)

        return self.records

    def _fmt_time(self, time_str: str) -> datetime:
        """Formats time fields for the records."""
        t = datetime.strptime(time_str, '%H:%M')
        return datetime(self.date.year,
                        self.date.month,
                        self.date.day,
                        t.hour,
                        t.minute)

    def _extract_fields(self,
                        element: bs4.element.Tag) -> tuple[str, datetime]:
        """Extracts fields for the records."""
        try:
            tag = element.select_one('div.category').getText()
        except AttributeError:
            tag = ''
        time_str = element.select_one('div.time').getText()
        time = self._fmt_time(time_str)
        title = element.select_one('div.title').getText()
        descr = element.select_one('div.descr').getText()
        return (time, tag, title, descr)
