# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy
from urllib.parse import urlencode

API_KEY = '9fff5868-6a6e-4cd6-b217-f633bb727fd0'

def get_scrapeops_url(url):
    payload = {'api-key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/18347-community']
    
    def parse(self, response):
        '''
        Parses the TMDB cast and crew website.
        @ input:
        - self: TmdbSpider
        - response: the call to a url
        @ output:
        - yields a request to get the page with actors.
        '''
        cast = self.start_urls[0] + '/cast' # hardcode the cast page
        
        # go to cast & crew page, run parse_full_credits
        yield scrapy.Request(cast, callback = self.parse_full_credits)
        
    def parse_full_credits(self, response):
        '''
        for each actor, goes to their respective acting profile page on TMDB.
        @ input:
        - self: TmdbSpider
        - response: the call to the url
        @ output:
        - yields a request to get the profile page of each actor.
        '''
        
        # for each page redirection on the cast photos
        for page in response.css('ol.people.credits:not(.crew) li a'):
            actor_page = page.attrib['href'] # obtain the hyperlink
            actor_page = 'https://www.themoviedb.org' + actor_page # append to main url
            
            # go to the actor's page, run parse_actor_page
            yield scrapy.Request(actor_page, callback = self.parse_actor_page)
            
    def parse_actor_page(self, response):
        '''
        obtains the cinematography of the actor.
        @ input:
        - self: TmdbSpider
        - response: the call to the url
        @ output:
        - yields a dictionary with actor name and movie.
        '''
        
        # obtain the actor name
        actor_name = response.css('div.title a::text').get()
        
        # for each of the links in the acting section of his or her page
        for acting_gig in response.css('h3.zero + table.card.credits a.tooltip bdi::text'):
            title = acting_gig.get() # obtain the right URL
            
            yield {'actor': actor_name, 'movie_or_TV_name': title} # yield a dictionary with actor and title of movie they were in.
        
        