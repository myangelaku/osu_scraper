Simple python script to scrape the [osu! rankings](https://osu.ppy.sh/rankings/osu/performance) and each user's profile (currently only getting their playtime and location)

For now, the purpose of this script heavily lies in obtaining the specified location of players in order to potentially build a local community, so players which don't have any location specified will be removed from the resulting file.

# Usage

* As this is a Python script, you'll obviously have to have [Python](https://www.python.org/downloads) at first. 
* Download the script [here](https://github.com/myangelaku/osu_scraper/archive/master.zip) and unzip it wherever you like.
* Open cmd in the directory you unzipped the contents to (This can be done by typing "cmd" in the address bar)
* The script requires bs4 and urllib3, you can easily install them by typing `pip install -r requirements.txt` into the shell if you have pip installed.
* Execute the script by typing `scrape.py` into the shell and follow the instructions.
