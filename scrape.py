import csv
import urllib3
from datetime import datetime
import time
from bs4 import BeautifulSoup

RANK_PAGE = 'https://osu.ppy.sh/rankings/osu/performance?country=KR&page='
MAX_PAGE = 20  # top 1k
CSV_FILE = 'osu_data.csv'

http = urllib3.PoolManager()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_play_time(text):
    sub = text[text.find('play_time') + 11:]
    return sub[:sub.find(',')]


for i in range(1, MAX_PAGE + 1):
    # save per page in case something happens
    with open(CSV_FILE, 'a') as csv_file:
        start = time.time()
        writer = csv.writer(csv_file)
        page = http.request('GET', RANK_PAGE + str(i))
        parsed_page = BeautifulSoup(page.data, 'html.parser')
        rows = parsed_page.find_all(
            'tr', attrs={'class': 'ranking-page-table__row'})

        for row in rows:
            cols = row.find_all('td', {'class': 'ranking-page-table__column'})
            links = cols[1].find_all('a', href=True)
            user_profile_link = links[1]['href'].strip()
            user_row = []
            for val in cols:
                user_row.append(val.text.strip())

            profile = http.request('GET', user_profile_link)
            profile_text = profile.data.decode('utf-8')
            profile.close()
            user_row.append(get_play_time(profile_text))
            writer.writerow(user_row)
            # According to https://github.com/ppy/osu-api/wiki the limit for what
            # is acceptable without contacting peppy (in the osu! api) is 60 requests
            # a minute, I don't suggest going above that.
            #
            # This means that, not counting the opening of the site itself, a pause
            # of one second should be made between each request. I'm still suggest the
            # use at least 2, just because I dont wanna make peppy-san mad;;;
            time.sleep(2)

        print('processed page', i, ' time-taken: ', time.time() - start)
        page.close()
