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

import requests

class ScrapperWebsite2Science( Scrapper ):

    def __init__( self, db, wpinfo, table, url, slug, log ):
        Scrapper.__init__( self, db, wpinfo, table, url, slug, log )

