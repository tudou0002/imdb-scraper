import scrapy
from imdb.items import KeywordItem
from scrapy.http import Request, FormRequest, JsonRequest
# from scrapy.spiders import CSVFeedSpider
from scrapy.utils.project import get_project_settings
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime
import re

class KeywordSpider(scrapy.Spider):
    name = "keyword"
    # start_urls = [
    #     'https://www.imdb.com/title/tt0386676/keywords/', # the office
    #     'https://www.imdb.com/title/tt0108778/keywords/',  # friends
    #     ]
    df = pd.read_csv('../../data/netflix_shows_list_full.csv').dropna(subset='imdbID', axis=0)
    urls = []
    for id in df['imdbID']:
        url = f'https://www.imdb.com/title/{id}/keywords/'
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
        self.keywordXpath = '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[1]/div/ul/li/div/div/a/text()'
        

    def declare_css(self):
        pass
 
    def parse(self, response):
        item = KeywordItem()

        # use space to concat multiple genres
        keywords = response.xpath(self.keywordXpath).extract()
     
        Crawldate = datetime.now().isoformat(timespec='minutes')  #current date
        
        item['show_id'] = str(response.url).split('/')[4]
        item['keyword'] = keywords
        # item['upvote_cnt'] = 
        # item['downvote_cnt'] = 
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