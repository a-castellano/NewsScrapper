#!/usr/bin/python3

# Alvaro Castellano Vela - 22/07/2016
# https://github.com/a-castellano

# Import all the scrappers here


#import scrapers
#from scrapers import ScraperWebsite1Economy
#from scrapers import ScraperWebsite1Politics
#from scrapers import ScraperWebsite2Science
#from scrapers import ScraperWebsite2Sports


class ScraperFactory( object ):

    def factory( type, db, wpinfo, table, url, slug ):
        if type == "website1_economy": return ScraperWebsite1Economy( db, wpinfo, table, url, slug )
        if type == "website1_politics": return ScraperWebsite1Politics( db, wpinfo, table, url, slug )
        if type == "website2_science": return ScraperWebsite2Science( db, wpinfo, table, url, slug )
        if type == "website2_sport": return ScraperWebsite2Sports( db, wpinfo, table, url, slug  )
    factory = staticmethod(factory)
