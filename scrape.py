from datetime import datetime, date, timedelta
from enum import Enum
from typing import Generator

import bs4
import requests

from config import START_URL
from items import Record, Days


class TvCrawler:
    """
    Class for scraping naslovi.net and getting information about tv schedule.
    """
    def __init__(
            self, channels: list[str],
            start_url: str = START_URL,
            days: Enum = Days
                                      ) -> None:
        """Initilizes class with channel names to scrape."""
        self.start_url = start_url
        self.channels = channels
        self.days = days
        self.date = date.today()
        self.records = {channel: [] for channel in self.channels}

    def run(self) -> Generator[str, str, timedelta]:
        """Runs the crawler and generates response pages"""
        for url in self._list_urls():
            channel, day_name = url.split('/')[-2:]
            ofsset = self.days[day_name.upper()].value
            yield self._get_page(url), channel, ofsset

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
        return [f'{self.start_url}{channel}/{day}'
                for channel in self.channels
                for day in [day.name.lower() for day in Days]]

    def get_records(self, response: requests.Response,
                    table_name: str,
                    offset: timedelta) -> dict[str, Record]:
        """
        Parses the response page and fills dictionary with scraped records.
        """
        page = bs4.BeautifulSoup(response, 'html.parser')
        all_elements = page.select('div.tvrow')

        for element in all_elements:
            time, tag, title, descr = self._extract_fields(element)
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
        if tag_element := element.select_one('div.category'):
            tag = tag_element.getText()
        else:
            tag = ''
        time_str = element.select_one('div.time').getText()
        time = self._fmt_time(time_str)
        title = element.select_one('div.title').getText().replace('\'', ' ')
        descr = element.select_one('div.descr').getText().replace('\'', ' ')
        return (time, tag, title, descr)
