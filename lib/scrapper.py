#!/usr/bin/python3

# Alvaro Castellano Vela - 20/07/2016
# https://github.com/a-castellano

class Scrapper:

    def __init__( self, db, wpinfo, table, url, slug ):
        self.items = []
        self.db = db
        self.table = table
        self.wpinfo = wpinfo
        self.url = url
        self.slug = slug

##############################################################################################################

    def addItemsToMysql( self, items ):
        # Last items should be the older ones
        items = list( reversed( self.items ) )
        self.db.addData( self.table, items )

##############################################################################################################

    def scrape( self ):
        pass

##############################################################################################################
