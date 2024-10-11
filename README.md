# tvprogram :tv:
## Overview
Scrapes tv schedule data from https://naslovi.net and stores it in the postgres database. Check out the results at https://tvprogram-7-dana-unazad.streamlit.app/

## Detailed description
It scrapes data for tv schedule of channels emmited in the Balkans for today and next three days. Then stores data in a postgres database.
When database is filled it can display information for the past seven days, so you can rewind to your favourite show.
Currently it is set up to scrape data for some movie channels.
Any other channel can be added to the list for scraping in the config.py file.
