"""
Test accessibility of all deferred venues
"""
from playwright.sync_api import sync_playwright
import sys

venues = [
    ('Cross Club', 'https://www.crossclub.cz/cs/program/'),
    ('Lucerna Velky sal', 'https://www.lucpra.com/index.php/cz/'),
    ('U Stare Pani', 'https://www.ustarepani.cz/program/'),
    ('Sportovni hala Fortuna', 'https://www.sportovnihalafortuna.cz/'),
    ('Dum hudby Plzen', 'https://www.dumhudbyplzen.cz/program/'),
    ('Moving Station', 'https://www.movingstation.eu/program/'),
    ('Mestanska beseda', 'https://mestanskabeseda.cz/program/'),
    ('LOGSPEED CZ Arena', 'https://www.hcplzen.cz/areal-logspeed-cz-areny')
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for name, url in venues:
        try:
            print(f'\n{name}: ', end='')
            response = page.goto(url, wait_until='networkidle', timeout=15000)
            print(f'OK {response.status}')
        except Exception as e:
            error_msg = str(e)[:100]
            print(f'FAILED - {error_msg}')

    browser.close()
