Simple python script to scrape the [osu! rankings](https://osu.ppy.sh/rankings/osu/performance) and each user's profile (currently only getting their playtime, will add more once I feel like it)

# Usage

* As this is a Python script, you'll obviously have to have [Python](https://www.python.org/downloads) at first. 
* Download the script [here](https://github.com/myangelaku/osu_scraper/archive/master.zip) and unzip it wherever you like.
* Open cmd in the directory you unzipped the contents to (This can be done by typing "cmd" in the address bar)
* The script requires bs4 and urllib3, you can easily install them by typing `pip install -r requirements.txt` into the shell if you have pip installed.
* As the script isn't too advanced yet, it's up to you to change the script. By now, you can change:
  * RANK_PAGE to another country or to scrape the global rankings
  * MAX_PAGE to modify the number of how many pages to scrape
  * time.sleep(2) to increase/decrease the length of the process (I do not recommend playing with this, but it's up to you whether to do it or not.)
* Once you modified the script to your preferences, execute the script by typing `scrape.py` into the shell.
