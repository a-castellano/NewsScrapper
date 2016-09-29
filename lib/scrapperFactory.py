#!/usr/bin/python3

# Alvaro Castellano Vela - 22/07/2016
# https://github.com/a-castellano

import sys
sys.path.append('../')

from lib.scrappers import clarin_politica
from lib.scrappers import clarin_boxeo

class ScrapperFactory( object ):

    def factory( type, db, wpinfo, table, url, slug, log ):
        if type == "clarin_politica": return clarin_politica.ScrapperClarinPolitica( db, wpinfo, table, url, slug, log )
        if type == "clarin_boxeo": return clarin_boxeo.ScrapperClarinBoxeo( db, wpinfo, table, url, slug, log )
        #if type == "website1_economy": return ScrapperWebsite1Economy( db, wpinfo, table, url, slug, log )
        #if type == "website1_politics": return ScrapperWebsite1Politics( db, wpinfo, table, url, slug, log )
        #if type == "website2_science": return ScrapperWebsite2Science( db, wpinfo, table, url, slug, log )
        #if type == "website2_sport": return ScrapperWebsite2Sports( db, wpinfo, table, url, slug, log )
    factory = staticmethod(factory)
