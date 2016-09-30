#!/usr/bin/python3

# Alvaro Castellano Vela - 22/07/2016
# https://github.com/a-castellano

import sys
sys.path.append('../')

from lib.scrappers import website1_economy
from lib.scrappers import website1_politics
from lib.scrappers import website2_science
from lib.scrappers import website2_sports

class ScrapperFactory( object ):

    def factory( type, db, wpinfo, table, url, slug, log ):
        if type == "website1_economy": return website1_economy.ScrapperWebsite1Economy( db, wpinfo, table, url, slug, log )
        if type == "website1_politics": return website1_politics.ScrapperWebsite1Politics( db, wpinfo, table, url, slug, log )
        if type == "website2_science": return website2_science.ScrapperWebsite2Science( db, wpinfo, table, url, slug, log )
        if type == "website2_sports": return website2_sports.ScrapperWebsite2Sports( db, wpinfo, table, url, slug, log )
    factory = staticmethod(factory)
