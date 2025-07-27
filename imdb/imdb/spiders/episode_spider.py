import scrapy
from imdb.items import EpisodeItem
from scrapy.http import Request, FormRequest, JsonRequest
# from scrapy.spiders import CSVFeedSpider
from scrapy.utils.project import get_project_settings
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime
import re
import urllib3

class EpisodeSpider(scrapy.Spider):
    name = "episode"
    # start_urls = [
    #     'https://www.imdb.com/title/tt0386676/episodes/?season=1', # the office
    #     # 'https://www.imdb.com/title/tt0108778/episodes/?season=1',  # friends
    #     ]
    df = pd.read_csv('../../data/netflix_shows_list_full.csv').dropna(subset='imdbID', axis=0)
    urls = []
    for id in df['imdbID']:
        url = f'https://www.imdb.com/title/{id}/episodes/?season=1'
        urls.append(url)
    start_urls = urls
    custom_settings = {
        'COLLECTION_NAME': 'episode'
    }
    base_url = 'https://www.imdb.com/'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.declare_xpath()
        self.declare_css()

    def parse(self, response):
        self.parse_item(response)
        pageXpath = '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[2]/section[1]/div[2]/ul/a/@href'
        season_list = response.xpath(pageXpath).extract()
        if season_list:
            for season in season_list[1:]:
                next_url = self.base_url + season
                yield Request(url=next_url,callback=self.parse_item, dont_filter=True,meta = {'dont_redirect': True, "handle_httpstatus_list" : [301, 302, 303]})
        
    def declare_xpath(self):
        self.showNameXpath = '//*[@id="__next"]/main/div/section/section/div[3]/section/section/div[2]/hgroup/h2'

    def declare_css(self):
        self.epiCss = 'div.ipc-title__text ::text'
        self.voteCntCss = 'span.ipc-rating-star--voteCount'
        self.rateCss = 'article.episode-item-wrapper span.ratingGroup--imdb-rating ::text'
        self.descCss = 'div.ipc-html-content-inner-div ::text'
        self.airdateCss = 'span.sc-aafba987-10 ::text'

    def parse_item(self, response):

        show_name = response.xpath(self.showNameXpath).extract()
        show_name = self.cleanText(self.parseText(self.listToStr(show_name)))

        # include episode num, episode name
        episodes = response.css(self.epiCss).extract()

        # include description for whole season
        descriptions = response.css(self.descCss).extract()
        # description = self.cleanText(self.parseText(''.join(description)))

        # include rate, votecnt for whole season
        # 0th: rate  4th: votecnt  5 elements for every episode
        allrates = response.css(self.rateCss).extract()
        rates = allrates[0::6]
        votecnts= allrates[4::6]

        # include airdate for whole season
        airedates = response.css(self.airdateCss).extract()
        
        Crawldate = datetime.now().isoformat(timespec='minutes')  #current date
        print('='*10)
        print(len(episodes), len(descriptions), len(rates), len(votecnts), len(airedates))
        
        for episode, desc, rate, vote, date in zip(episodes, descriptions, rates, votecnts, airedates):
            item = EpisodeItem()
            epi_num, epi_name = episode.split(' ∙ ')
            season_num, epi_num = epi_num.split('.')
            item['show_name'] = show_name
            item['show_id'] = str(response.url).split('/')[5]
            item['season_num'] = str(response.url).split('=')[1]
            item['epi_num'] = epi_num
            item['epi_name'] = epi_name
            item['epi_desc'] = desc
            item['epi_airdate'] = date
            item['epi_rate'] = rate
            item['epi_vote_cnt'] = vote
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