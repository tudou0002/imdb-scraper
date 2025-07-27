# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EpisodeItem(scrapy.Item):
    show_id = scrapy.Field()  # unique identifier parsed from the url 
    show_name = scrapy.Field()
    season_num = scrapy.Field()
    epi_num = scrapy.Field()
    epi_name = scrapy.Field()
    epi_desc = scrapy.Field()
    epi_airdate = scrapy.Field()
    epi_rate = scrapy.Field()
    epi_vote_cnt = scrapy.Field()
    crawl_date = scrapy.Field()
    
class ShowItem(scrapy.Item):
    show_id = scrapy.Field()  # unique identifier parsed from the url 
    show_name = scrapy.Field()
    show_genre = scrapy.Field()
    show_desc = scrapy.Field()
    show_date = scrapy.Field()
    show_rate = scrapy.Field()
    show_vote_cnt = scrapy.Field()
    similar_show = scrapy.Field()
    crawl_date = scrapy.Field()

class KeywordItem(scrapy.Item):
    show_id = scrapy.Field()
    keyword = scrapy.Field()
    # upvote_cnt = scrapy.Field()
    # downvote_cnt = scrapy.Field()
    crawl_date = scrapy.Field()
