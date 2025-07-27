# IMDB Crawler Project

A web scraper built with Scrapy to extract movie and TV show data from IMDB.

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

## Useful links to learn Scrapy
Official tutorial of the Scrapy framwork: [https://docs.scrapy.org/en/latest/intro/tutorial.html]