import csv
import urllib3
from datetime import datetime
from datetime import date
import time
from bs4 import BeautifulSoup

PAGE_BASE = 'https://osu.ppy.sh/rankings/osu/performance'

# Check if user wants to scrape global rankings or country rankings
print('If you want to scrape the global rankings, enter "global".')
print('If you want to scrape the rankings of a specific country, enter its country code.')
print('global/xx')
COUNTRY = input()

if COUNTRY == 'global':
    PAGE_BASE = PAGE_BASE + '?page='
else:
    PAGE_BASE = PAGE_BASE + '?country=' + COUNTRY + '&page='

print('How many pages do you want to scrape?')
print('One page equals 50 users.')
MAX_PAGE = int(input())
while MAX_PAGE > 200:
    print('You can only scrape up to 200 pages.')
    MAX_PAGE = int(input())

http = urllib3.PoolManager()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def play_time(text):
    sub = text[text.find('play_time') + 11:]
    return sub[:sub.find(',')]

def maxpp(text):
    sub = text[text.find('"count_miss":0},"pp') + 21:]
    return sub[:sub.find(',')]

#def playstyle(text):
#    sub = text[text.find('playstyle') + 12:]
#    return sub[:sub.find(']')]

def join_date(text):
    sub = text[text.find('join_date') + 11:]
    return sub[:sub.find(',')]

def location(text):
    sub = text[text.find('location') + 10:]
    return sub[:sub.find(',')]

def interests(text):
    sub = text[text.find('interests') + 11:]
    return sub[:sub.find(',')]

#def twitter(text):
#    sub = text[text.find('twitter') + 9:]
#    return sub[:sub.find(',')]

def skype(text):
    sub = text[text.find('skype') + 7:]
    return sub[:sub.find(',')]

def discord(text):
    sub = text[text.find('","discord') + 12:]
    return sub[:sub.find(',')]

CSV_FILE = 'osu_data_' + COUNTRY + "_" + str(date.today()) + ".csv"

for i in range(1, MAX_PAGE + 1):
    # Save per page in case something happens
    with open(CSV_FILE, 'a', newline='') as csv_file:
        start = time.time()
        writer = csv.writer(csv_file)
        page = http.request('GET', PAGE_BASE + str(i))
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

            #            if(get_location(profile_text) == "null"):
            #                continue

            profile.close()
            user_row.append(play_time(profile_text))
            user_row.append(maxpp(profile_text))
#            user_row.append(playstyle(profile_text))
            user_row.append(join_date(profile_text))
            user_row.append(location(profile_text))
            user_row.append(interests(profile_text))
#            user_row.append(twitter(profile_text))
            user_row.append(skype(profile_text))
            user_row.append(discord(profile_text))
            writer.writerow(user_row)
            # Even though this scraper doesn't use the osu!API, according to
            # https://github.com/ppy/osu-api/wiki#terms-of-use, acceptable use
            # that can be done via the API without contacting peppy is
            # 60 requests per minute, I don't suggest going above that.
            # 
            # This means that, not counting the opening of the site itself, a pause
            # of one second should be made between each request. I still suggest the
            # use at least 2, just because I don't want to make peppy-san mad;;;
            time.sleep(2)

        print('processed page', i, ' time-taken: ',
              str(int((time.time() - start) / 60)) + ':' + str(int((time.time() - start) % 60)))
        page.close()
