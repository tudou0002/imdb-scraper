# IMDB Crawler Project

A web scraper built with Scrapy to extract movie and TV show data from IMDB.

The project contains three main spiders:
1. **ShowSpider** - Extracts general show/movie information
2. **EpisodeSpider** - Extracts detailed episode information for TV series
3. **KeywordSpider** - Extracts keywords and tags for shows/movies

All spiders read from a CSV file (`data/netflix_shows_list_full.csv`) containing IMDB IDs to scrape.


## Setup Environment and use the spider

1. Create a virtual environment and install dependencies in your command line:
```shell
# go to the imdb-scraper/ directory and execute:
# create a new virtual env
python3 -m venv env 
# activate the env
source env/bin/activate
# install scrapy with pip3
pip3 install -r requirements.txt
```

2. Execute the following command and start to crawl using Scrapy
```shell
# the crawler needs to be started under its directory
cd imdb/imdb
# start the show crawler and store the crawled items into a csv
scrapy crawl show -t csv -o [filename.csv]

scrapy crawl episode -t csv -o [filename.csv]
```

## Attribute fields for each spider

### ShowItem
- `show_id`: Unique IMDB identifier
- `show_name`: Title of the show/movie
- `show_genre`: Genres (comma-separated)
- `show_desc`: Plot description
- `show_date`: Release/air date
- `show_rate`: IMDB rating
- `show_vote_cnt`: Number of votes
- `similar_show`: List of similar shows
- `crawl_date`: When the data was scraped

### EpisodeItem
- `show_id`: Parent show's IMDB identifier
- `show_name`: Name of the show
- `season_num`: Season number
- `epi_num`: Episode number
- `epi_name`: Episode title
- `epi_desc`: Episode description
- `epi_airdate`: When the episode aired
- `epi_rate`: Episode rating
- `epi_vote_cnt`: Number of votes for episode
- `crawl_date`: When the data was scraped

### KeywordItem
- `show_id`: Show's IMDB identifier
- `keyword`: List of plot keywords/tags
- `crawl_date`: When the data was scraped

## Useful links to learn Scrapy
Official tutorial of the Scrapy framwork: [https://docs.scrapy.org/en/latest/intro/tutorial.html]