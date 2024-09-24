# tvprogram
Scrapes tv program data from https://naslovi.net and stores it in the local database.

It scrapes data for tv schedule of channels emmited in the Balkans for today and next three days.
When database is filled it can display information for the past seven days, so you can rewind to your favourite show.
Currently it is set up to scrape data for channels HBO, HBO2, HBO3.
Any other channel can be added to the list for scraping in the config.py file.
Data is stored in a different table for each channel. To prevent duplicate entries datetime is set up as the primary key.

This is a practice project using requests, bs4, sqlite3.

TODO: -Extend the app to display data for the last week.
      -Store data more efficently.

