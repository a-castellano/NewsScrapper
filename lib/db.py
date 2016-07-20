# Alvaro Castellano Vela - 20/07/2016
# https://github.com/a-castellano

from warnings import filterwarnings
import MySQLdb
import sys

class DB:

    def __init__(self, cfg):
        self.log = cfg.log
        self.logError = cfg.logError

        try:
            self.database = MySQLdb.connect(host=cfg.host, port=cfg.port, user=cfg.user, passwd=cfg.password, db=cfg.database)
            self.database.autocommit( True )
            self.cursor = self.database.cursor()

        except MySQLdb.Error , e:
            try:
                self.logError.error("[init DB: Error connecting DB [%d]: %s]" %(e.args[0], e.args[1]))
                print "[init DB: Error connecting DB [%d]: %s]" %(e.args[0], e.args[1])
            except IndexError:
                self.logError.error("[init DB: Error connecting DB: %s]" %(str(e)))
                print "[init DB: Error connecting DB: %s]" %(str(e))
                sys.exit(1)

        filterwarnings('ignore', category = MySQLdb.Warning)
        self.log.info( "[ Scrapper - DB ] - [ Conection to database was successful ]" )

    def createTableIfNotExist( self, tableName ):

        sql_create_table = "CREATE TABLE IF NOT EXISTS {} ( id INT(22) NOT NULL AUTO_INCREMENT, title VARCHAR(400), description VARCHAR(800), url VARCHAR(500) NOT NULL, image_url VARCHAR(500), video_url VARCHAR(500), content TEXT, slug VARCHAR(200), keywords VARCHAR(200), date DATETIME, PRIMARY KEY (id) )".format(tableName)

        self.cursor.execute( sql_create_table )
