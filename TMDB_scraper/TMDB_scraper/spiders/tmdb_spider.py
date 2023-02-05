# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_url = 'https://www.themoviedb.org/tv/18347-community'
    
    def parse(self, response):
        '''
        Parses the TMDB cast and crew website.
        @ input:
        - self: TmdbSpider
        - response: the call to a url
        @ output:
        - yields a request to get the page with actors.
        '''
        cast = start_url + '/cast' # hardcode the cast page
        
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
        for page in response.css('ol.people.credits li a'):
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
        for acting_gig in response.css('h3.zero + table.card.credits a'):
            title = acting_gig.css('.tooltip::text').get() # obtain the right URL
            
            yield {'actor': actor_name, 'movie_or_TV_name': title} # yield a dictionary with actor and title of movie they were in.
        
        