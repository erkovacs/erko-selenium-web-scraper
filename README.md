# Simple web scraper

## Prerequisites
 - Chrome webdriver installed
 - Python 3 installed
 - Pip installed

## Setup
 - `git clone https://github.com/erkovacs/erko-selenium-web-scraper.git scraper`
 - `cd scraper`
 - `pip3 install -r requirements.txt`

## Usage
 - Add search sites to search_sites.cfg (each on its own line)
 - Add search queries to search_terms.cfg (each on its own line)
 - Run `python3 scraper.py`
 - Results will appear in `./results/` as a JSON file

### Options
 - `-n` - Do not launch headless Chrome. Used for debugging mostly
 - `-p` - Pagination limit (i.e. how many pages of results should it scrape)
 - `-l` - Result limit (i.e. how many total results to scrape)
 - `-r` - Preserve raw HTML in the data (dramatically increases size but preserves markup for further usage)

## Acknowledgements
 - [This StackOverflow post](https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text)