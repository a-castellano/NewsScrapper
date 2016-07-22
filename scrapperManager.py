#!/usr/bin/python3

# Alvaro Castellano Vela - 19/07/2016
# https://github.com/a-castellano


from lib.config import Config
from lib.db import DB
from lib.scraper import Scraper
import lib.scrapers
from lib.scraperFactory import ScraperFactory

def main():

    scraperFactory = ScraperFactory()

    cfg = Config("conf/scrapper.conf")

    if (cfg.readConfig() == False):
        print( "[Main - readConfig] [Error reading config file]" )
        return

    if (cfg.createLog() == False):
        print( "[Main - createLog] [Error creating log files]" )
        return

    cfg.log.info( "[ Main - readConfig ] [ Config file read sucessfully ]" )
    cfg.log.info( "[ Main - createLog ] [ Log files created successfully ]" )
    cfg.log.info( "[ Scrapper ] - [ This is Major Tom to Ground Control! ]" )

    cfg.log.info( "[ Scrapper ] - [ Here are my orders ]" )

    for website in cfg.websitesConf:
        cfg.log.info( "[ Scrapper ] - [ Website -> \"{}\" ]".format( website ) )
        for section in cfg.websitesConf[website]:
            cfg.log.info( "[ Scrapper ] - [ \tSection -> \"{}\" ]".format( section ) )
            cfg.log.info( "[ Scrapper ] - [ \t\turl -> \"{}\" ]".format( cfg.websitesConf[website][section][0] ) )
            cfg.log.info( "[ Scrapper ] - [ \t\tslug -> \"{}\" ]".format( cfg.websitesConf[website][section][1] ) )


    db = DB(cfg)

    for website in cfg.websitesConf:
        cfg.log.info( "[ Scrapper ] - [ Looking for \"{}\" sections ]".format( website ) )
        for section in cfg.websitesConf[website]:
            cfg.log.info( "[ Scrapper ] - [ Accesing to \"{}\" table ]".format( section ) )
            db.createTableIfNotExist( section )





if __name__ == "__main__":
    main()
