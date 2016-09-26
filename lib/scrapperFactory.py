#!/usr/bin/python3

# Alvaro Castellano Vela - 22/07/2016
# https://github.com/a-castellano


class ScrapperFactory( object ):

    def factory( type, db, wpinfo, table, url, slug ):
        if type == "website1_economy": return ScrapperWebsite1Economy( db, wpinfo, table, url, slug )
        if type == "website1_politics": return ScrapperWebsite1Politics( db, wpinfo, table, url, slug )
        if type == "website2_science": return ScrapperWebsite2Science( db, wpinfo, table, url, slug )
        if type == "website2_sport": return ScrapperWebsite2Sports( db, wpinfo, table, url, slug  )
    factory = staticmethod(factory)
