import toml


data = toml.load('.streamlit/secrets.toml')
DB_CONN = [data['connections']['postgresql']['database'],
           data['connections']['postgresql']['username'],
           data['connections']['postgresql']['password'],
           data['connections']['postgresql']['host'],
           data['connections']['postgresql']['port']]

CHANNELS = ['hbo',
            'hbo-2',
            'hbo-3',
            'cinestar-tv-action-thriller',
            'cinestar-tv-fantasy',
            'cinestar-tv-comedy',
            'cinestar-tv-premiere-1',
            'cinestar-tv-premiere-2']

START_URL = 'https://naslovi.net/tv-program/'

SELECTORS = ['.time', '.category', '.title', '.descr']
