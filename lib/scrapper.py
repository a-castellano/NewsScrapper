# Alvaro Castellano Vela - 20/07/2016
# https://github.com/a-castellano

import codecs
import re
import time
import unicodedata

from bs4 import BeautifulSoup
from subprocess import call
from DataBaseManager import DataBaseManager

from lxml import html
import requests

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

class Scraper:

    def __init__( self, db, wpinfo, table ):
        self.url = ''
        self.items = []
        self.db = db
        self.table = table
        self.wpinfo = wpinfo

##############################################################################################################

    def addItemsToMysql( self, items ):
        # Last items should be the older ones
        items = list( reversed( self.items ) )
        self.db.addData( self.table, items )

##############################################################################################################
