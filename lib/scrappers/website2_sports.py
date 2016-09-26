#!/usr/bin/python3

# Alvaro Castellano Vela - 21/07/2016
# https://github.com/a-castellano

import sys
sys.path.append('../../')

import codecs
import re
import time
import unicodedata

from bs4 import BeautifulSoup
from subprocess import call

from lxml import html
import requests

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

class ScraperWebsite2Sports( Scraper ):

    def __init__( self, db, wpinfo, table, url, slug ):
        Scraper.__init__( self, dbinfo,wpinfo, table, url, slug )

