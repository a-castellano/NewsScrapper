#!/usr/bin/python3

# Alvaro Castellano Vela - 20/07/2016
# https://github.com/a-castellano

from subprocess import call

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

import time

class Scrapper:

    def __init__( self, db, wpinfo, table, url, slug, log ):

        self.items = []
        self.db = db
        self.table = table
        self.wpinfo = wpinfo
        self.url = url
        self.slug = slug
        self.log = log

##############################################################################################################

    def addItemsToMysql( self ):

        # Last items should be the older ones
        items = list( reversed( self.items ) )
        self.db.addData( self.table, items )

##############################################################################################################

    def numberOfItems( self ):

        return len( self.items )

##############################################################################################################

    def addItemsToWordpress( self ):

        items = self.items

        if items:
            wp = Client('http://' + self.wpinfo['website']  + '/xmlrpc.php', self.wpinfo['user'], self.wpinfo['pass'])
            pass

        for item in items:
            self.log.info("[ Scrapper {} ] - [ Publishing \"{}\" into WP ]".format( self.table, item["title"] ))
            now = time.strftime("%c")
            post = WordPressPost()
            post.terms_names = {
                'category': ['Scrapped'] # This need to be changed in next release
            }

            post.title = '{}'.format(item['title'])

            if item['slug']:
                post.slug = item['slug']
            if item['image_url']:
                call(['curl',item['image_url'].replace(' ','%20'),'-o','image.jpg.scrapper_data'])
                filename = 'image.jpg.scrapper_data'
                data = {
                    'name': 'image.jpg',
                    'type': 'image/jpeg',  # mimetype
                }
                with open(filename, 'rb') as img:
                    data['bits'] = xmlrpc_client.Binary(img.read())
                    response = wp.call(media.UploadFile(data))
                    attachment_id = response['id']
                post.thumbnail = attachment_id

                content = ''
                if item['content']:
                    content += '{}'.format(item['content'])
                    content += 'Source: <a href="{}">{}</a>\n\n'.format(item['url'],item['referer'])
                    post.content = content
                    wp.call(NewPost(post))
                    # An article without content won't be published

##############################################################################################################

    def scrape( self ):

        pass

##############################################################################################################
