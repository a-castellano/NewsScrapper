#!/usr/bin/python3

# Alvaro Castellano Vela - 20/07/2016
# https://github.com/a-castellano

from warnings import filterwarnings
import MySQLdb
import sys

class DB:

    def __init__( self, cfg ):

        self.log = cfg.log
        self.logError = cfg.logError
        self.error = False
        try:
            self.database = MySQLdb.connect(host=cfg.host, port=cfg.port, user=cfg.user, passwd=cfg.password, db=cfg.database)
            self.database.autocommit( True )
            self.database.set_character_set('utf8')
            self.cursor = self.database.cursor()
            self.cursor.execute('SET NAMES utf8;')
            self.cursor.execute('SET CHARACTER SET utf8;')
            self.cursor.execute('SET character_set_connection=utf8;')
            filterwarnings( 'ignore', category = MySQLdb.Warning )
            self.log.info( "[ Scrapper - DB  ] - [ Conection to database was successful  ]" )

        except MySQLdb.Error as e:
            try:
                self.logError.error( "[init DB: Error connecting DB [{}]: {}]".format( e.args[0], e.args[1] ) )
                print ( "[init DB: Error connecting DB [{}]: {}]".format( e.args[0], e.args[1] ) )
            except IndexError:
                self.logError.error( "[init DB: Error connecting DB: {}]".format( str(e) ) )
                print ( "[init DB: Error connecting DB: {}]".format( str(e) ) )
                sys.exit("Out")
            self.error = True

##############################################################################################################

    def hasError( self ):

        return self.error

##############################################################################################################

    def createTableIfNotExist( self, tableName ):

        sql_create_table = "CREATE TABLE IF NOT EXISTS {} ( id INT(22) NOT NULL AUTO_INCREMENT, title VARCHAR(400), description VARCHAR(800), url VARCHAR(500) NOT NULL, image_url VARCHAR(500), video_url VARCHAR(500), content TEXT, slug VARCHAR(200), keywords VARCHAR(200), date DATETIME, PRIMARY KEY (id) ) ENGINE=MyISAM CHARACTER SET=utf8".format(tableName)

        self.cursor.execute( sql_create_table )

##############################################################################################################

    def getURLs( self, tableName ):

        self.log.info( "[ Scrapper - DB ] - [ Getting url's from {} ]".format( tableName ) )
        query = "SELECT url FROM {} ;".format( tableName )
        self.cursor.execute( query )
        currentURLs = self.cursor.fetchall()

        return currentURLs

##############################################################################################################

    def addData( self, tableName, data ):

        # Data is scrapper.items
        for item in data:
            self.log.info( "[ Scrapper - DB - {} ] - [ Inserting {} ]".format( tableName, item['title'] ) )


            try:

                insert = 'INSERT INTO {} ( title, description, url, image_url, video_url, content, slug, keywords, date ) VALUES ( "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", NOW() ) '.format( tableName, item['title'], item['description'], item['url'], item['image_url'], item['video_url'], item['content'], item['slug'], item['keywords'] )
                self.cursor.execute( insert )

            except:

                try: # avoid " problem
                    insert = 'INSERT INTO {} ( title, description, url, image_url, video_url, content, slug, keywords, date ) VALUES ( \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', NOW() ) '.format( tableName, item['title'], item['description'], item['url'], item['image_url'    ], item['video_url'], item['content'], item['slug'], item['keywords'] )
                    self.cursor.execute( insert )

                except:
                    insert = 'INSERT INTO {} ( url , date ) VALUES ( "{}", NOW() ) '.format( tableName, item['url'] )
                    self.cursor.execute( insert )
                    self.log.info( "[ Scrapper - DB - {} ] - [ Broken Item ]".format( tableName ) )

##############################################################################################################
