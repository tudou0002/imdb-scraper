import scrapy
from imdb.items import ShowItem
from scrapy.http import Request, FormRequest, JsonRequest
# from scrapy.spiders import CSVFeedSpider
from scrapy.utils.project import get_project_settings
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime
import re
import urllib3

class ShowSpider(scrapy.Spider):
    name = "show"
    # start_urls = [
    #     'https://www.imdb.com/title/tt0386676', # the office
    #     'https://www.imdb.com/title/tt0108778',  # friends
    #     ]
    df = pd.read_csv('../../data/netflix_shows_list_full.csv').dropna(subset='imdbID', axis=0)
    urls = []
    for id in df['imdbID']:
        url = f'https://www.imdb.com/title/{id}'
        urls.append(url)
    start_urls = urls
    custom_settings = {
        'COLLECTION_NAME': 'show'
    }
    base_url = 'https://www.imdb.com/'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.declare_xpath()
        self.declare_css()

    # def parse(self, response):
    #     self.parse_item(response)
       
    def declare_xpath(self):
        self.showNameXpath = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span/text()'
        self.descXpath = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[1]/text()'
        self.dateXpath = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]/a/text()'
        self.rateXpath = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[1]/div/div[1]/a/span/div/div[2]/div[1]/span[1]/text()'
        self.voteXpath = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[1]/div/div[1]/a/span/div/div[2]/div[3]/text()'

    def declare_css(self):
        self.genreCss = 'a.ipc-chip--on-baseAlt span.ipc-chip__text ::text'
        self.similarCss = 'a.ipc-poster-card__title ::text'
 
    # similar_show = scrapy.Field()

    def parse(self, response):
        item = ShowItem()

        show_name = response.xpath(self.showNameXpath).extract()
        show_name = self.cleanText(self.parseText(''.join(show_name)))

        # use space to concat multiple genres
        genre = response.css(self.genreCss).extract()
        genre = self.cleanText(self.parseText(','.join(genre)))

        # include description for whole season
        description = response.xpath(self.descXpath).extract()
        description = self.cleanText(self.parseText(''.join(description)))

        rate = response.xpath(self.rateXpath).extract()
        rate = self.cleanText(self.parseText(''.join(rate)))

        vote_cnt = response.xpath(self.voteXpath).extract()
        vote_cnt = self.cleanText(self.parseText(''.join(vote_cnt)))

        # include date for whole show
        date = response.xpath(self.dateXpath).extract()
        date = self.cleanText(self.parseText(''.join(date)))

        similars = response.css(self.similarCss).extract()
        
        Crawldate = datetime.now().isoformat(timespec='minutes')  #current date
        
        item['show_name'] = show_name
        item['show_id'] = str(response.url).split('/')[4]
        item['show_genre'] = genre
        item['show_desc'] = description
        item['show_date'] = date
        item['show_rate'] = rate
        item['show_vote_cnt'] = vote_cnt
        item['similar_show'] = similars
        item['crawl_date'] = Crawldate
        
        yield item
    
    #Methods to clean and format text to make it easier to work with later
    def listToStr(self,MyList):
        return ' '.join(MyList)
    
    def list2BStr(self, MyList):
        dumm = ""
        MyList = [i.encode('utf-8') for i in MyList]
        for i in MyList:dumm = "{0}{1}".format(dumm,i)
        return dumm
 
    def parseText(self, str):
        soup = BeautifulSoup(str, 'html.parser')
        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0",' ',soup.get_text()).strip()
 
    def cleanText(self,text):
        soup = BeautifulSoup(text,'html.parser')
        text = soup.get_text()
        text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+",' ',text).strip()
        return text