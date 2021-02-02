import requests
import json
import urllib.request
from bs4 import BeautifulSoup


def pair_to_name():
    pairs = {}

    payload = json.loads(requests.get('https://api.coingecko.com/api/v3/coins/list').content)
    for coin in payload:
        ticker = coin['symbol']
        coingecko_name = coin['id']
        pairs[ticker.upper()] = coingecko_name


def retrieve_hist_data(coingecko_name, download_path, start_dt, end_dt):
    start_dt_str = start_dt.strftime('%Y-%m-%d')
    end_dt_str = end_dt.strftime('%Y-%m-%d')

    html = requests.get(
        'https://www.coingecko.com/en/coins/%s/historical_data/usd?start_date=%s&end_date=%s' %
        (coingecko_name, start_dt_str, end_dt_str))

    soup = BeautifulSoup(html.content)
    result = soup.find('ul', attrs={'class': 'dropdown-menu'})
    path = 'https://www.coingecko.com' + result.contents[3].contents[1]['href']

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(
        path, download_path + coingecko_name + '.csv')
