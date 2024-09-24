from datetime import timedelta

CHANNELS = ['hbo', 'hbo-2', 'hbo-3']
DB_NAME = 'db.sqlite'
START_URL = 'https://naslovi.net/tv-program/'
DAYS = {'': None, 'sutra': timedelta(days=1),
        'prekosutra': timedelta(days=2),
        'nakosutra': timedelta(days=3)}
