#!/usr/bin/python3

# Alvaro Castellano Vela - 21/07/2016
# https://github.com/a-castellano

import sys
sys.path.append('../../')

from lib.scrapper import Scrapper

import codecs
import re
import time
import unicodedata

from bs4 import BeautifulSoup
from subprocess import call

from lxml import html
import requests

class ScraperWebsite2Sports( Scraper ):

    def __init__( self, db, wpinfo, table, url, slug ):
        Scraper.__init__( self, dbinfo,wpinfo, table, url, slug )

