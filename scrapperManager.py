#!/usr/bin/python3

# Alvaro Castellano Vela - 19/07/2016
# https://github.com/a-castellano


from lib.config import Config
from lib.db import DB
from lib.scrapper import Scrapper

from lib.scrapperFactory import ScrapperFactory

def main():

    scrapperFactory = ScrapperFactory()

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
            cfg.log.info( "[ Scrapper ] - [ \t\turl -> \"{}\" ]".format( cfg.websitesConf[website][section]["url"] ) )
            cfg.log.info( "[ Scrapper ] - [ \t\tslug -> \"{}\" ]".format( cfg.websitesConf[website][section]["slug"] ) )


    db = DB(cfg)
    wpinfo = { "website" : cfg.wphost, "user" : cfg.wpuser, "pass" : cfg.wppass }

    if db.hasError():
        cfg.log.info( "[ Scrapper ] - [ Conection to database has failed ]".format( website ) )
        cfg.log.error( "[ Scrapper ] - [ Conection to database has failed ]".format( website ) )
        return

    for website in cfg.websitesConf:
        cfg.log.info( "[ Scrapper ] - [ Looking for \"{}\" sections ]".format( website ) )
        for section in cfg.websitesConf[website]:
            # table name and type are the same as section name
            cfg.log.info( "[ Scrapper ] - [ Accesing to \"{}\" table ]".format( section ) )
            db.createTableIfNotExist( section )
            cfg.log.info( "[ Scrapper ] - [ Calling \"{}\" scrapper ]".format( section ) )

            #factory -> ( type, db, wpinfo, table, url, slug, log )
            scrapperInstance = scrapperFactory.factory( section, db, wpinfo, section, cfg.websitesConf[website][section]["url"], cfg.websitesConf[website][section]["slug"], cfg.log )

            cfg.log.info( "[ Scrapper ] - [ \"{}\" scrapper begins ]".format( section ) )
            scrapperInstance.scrape()
            cfg.log.info( "[ Scrapper ] - [ \"{}\" scrapper has finished ]".format( section ) )

            scrappedItems = scrapperInstance.numberOfItems()

            cfg.log.info( "[ Scrapper ] - [ \"{}\" scrapper has scrapped {} new items ]".format( section, scrappedItems ) )

            if scrappedItems:
                cfg.log.info( "[ Scrapper \"{}\" ] - [ storing items into db ]".format( section ) )
                scrapperInstance.addItemsToMysql()
                cfg.log.info( "[ Scrapper \"{}\" ] - [ writting articles into Wordpress ]".format( section ) )
                scrapperInstance.addItemsToWordpress()


                cfg.log.info( "[ Scrapper ] - [ Bye ]" )
                scrapperInstance.addItemsToWordpress()

if __name__ == "__main__":
    main()
