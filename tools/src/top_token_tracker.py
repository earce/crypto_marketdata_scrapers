import requests
import time
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup


def pull_table_html(dt):
    dt_str = dt.strftime('%Y%m%d')
    return requests.get('https://coinmarketcap.com/historical/%s/' % dt_str)


def top_n_tokens(n, html):
    soup = BeautifulSoup(html.content)

    top_n = []
    count = 0

    for row in soup.find_all('tbody')[0]:
        if count >= n:
            return top_n
        symbol = row.contents[2].text
        if symbol in ['USDT', 'USDC', 'DAI']:
            continue
        top_n.append(symbol)
        count += 1


def get_tokens_in_range(start_dt, end_dt, sample_days):
    request_ct = 0

    top3 = {}
    top5 = {}
    top10 = {}
    top20 = {}

    curr_dt = start_dt
    while curr_dt < end_dt:
        time.sleep(5)

        try:
            print('Processing %s' % curr_dt.strftime('%Y%m%d'))
            html = pull_table_html(curr_dt)

            top_3_curr = top_n_tokens(3, html)
            top_5_curr = top_n_tokens(5, html)
            top_10_curr = top_n_tokens(10, html)
            top_20_curr = top_n_tokens(20, html)

            for symbol in top_3_curr:
                top3[symbol] = symbol

            for symbol in top_5_curr:
                top5[symbol] = symbol

            for symbol in top_10_curr:
                top10[symbol] = symbol

            for symbol in top_20_curr:
                top20[symbol] = symbol

            curr_dt += timedelta(days=sample_days)

            request_ct += 1
        except Exception as e:
            print('Reached limit on %s' % curr_dt.strftime('%Y%m%d'))
            break

    print()


start_dt_val = datetime.now(tz=timezone.utc).replace(year=2015, month=1, day=1)
end_dt_val = datetime.now(tz=timezone.utc).replace(year=2021, month=1, day=1)

get_tokens_in_range(start_dt_val, end_dt_val, 3)
