# Alvaro Castellano Vela - 19/07/2016
# https://github.com/a-castellano

from datetime import datetime
import logging.handlers
import ConfigParser

class Config:

    def __init__(self, fileName):

        self.cfg = ConfigParser.ConfigParser()
        self.file = fileName
        self.pathOutFile = ''
        self.pathErrFile = ''
        self.host = ''
        self.port = ''
        self.user = ''
        self.password = ''
        self.database = ''
        self.websites = []
        self.websitesConf = dict()

##############################################################################################################

    def readWebsitesConfig( self ):

        website = ""

        for website in self.websites:

            section_counter = 0

            file = "conf/{}.conf".format(website)
            if (not self.cfg.read( file )):
                print "File {} not found".format( file )
                return False

            if self.cfg.has_option( "WEBSITE", "name" ):
                website = self.cfg.get( "WEBSITE", "name" )
                self.websitesConf[website] = dict()
            else:
                print "Missing parameter \"name\" in configuration {} ".format( file )
                return False

            while True: # Get all sections
                section_name = "section{}_name".format( section_counter + 1)
                if self.cfg.has_option( "SECTIONS", section_name ):

                    section_counter += 1
                    name = self.cfg.get( "SECTIONS", section_name )
                    self.websitesConf[website][name] = []

                    section_url = "section{}_url".format( section_counter )
                    section_slug = "section{}_slug".format( section_counter )

                    if self.cfg.has_option( "SECTIONS", section_url ):
                        url = self.cfg.get( "SECTIONS", section_url )
                        self.websitesConf[website][name].append( url )
                    else:
                        print "Missing parameter \"{}\" in configuration file {}".format( section_url, file )
                        return False

                    if self.cfg.has_option( "SECTIONS", section_slug ):
                        slug = self.cfg.get( "SECTIONS", section_slug )
                    else: # There can be no slug
                        slug = ""

                    self.websitesConf[website][name].append( slug )

                else: # There are no more sections
                    break

            if section_counter == 0: # There are no sections configured, configuration files are not correct, abort
                print "There is no sections in configuration file {} - Aborting".format( file )
                return False
            print self.websitesConf
        return True


##############################################################################################################


    def readConfig( self ):
        if (not self.cfg.read( self.file )):
            print "File " + self.file + " not found"
            return False

        if self.cfg.has_option( "LOG", "pathOutFile" ):
            self.pathOutFile = self.cfg.get( "LOG", "pathOutFile" )
        else:
            print "Missing parameter \"pathOutFile\" in configuration file"
            return False

        if self.cfg.has_option( "LOG", "pathErrFile" ):
            self.pathErrFile = self.cfg.get( "LOG", "pathErrFile" )
        else:
            print "Missing parameter \"pathErrFile\" in configuration file"
            return False

        if self.cfg.has_option( "DB", "host" ):
            self.host = self.cfg.get( "DB", "host" )
        else:
            print "Missing parameter \"host\" in configuration file"
            return False

        if self.cfg.has_option ("DB", "port" ):
            self.port = int(self.cfg.get( "DB", "port" ))
        else:
            print "Missing parameter \"port\" in configuration file"
            return False

        if self.cfg.has_option( "DB", "user" ):
            self.user = self.cfg.get( "DB", "user" )
        else:
            print "Missing parameter \"user\" in configuration file"
            return False

        if self.cfg.has_option( "DB", "password" ):
            self.password = self.cfg.get( "DB", "password" )
        else:
            print "Missing parameter \"password\" in configuration file"
            return False

        if self.cfg.has_option( "DB", "database" ):
            self.database = self.cfg.get( "DB", "database" )
        else:
            print "Missing parameter \"database\" in configuration file"
            return False

        if self.cfg.has_option( "WEBSITES", "websites" ):
            self.websites = " ".join( self.cfg.get("WEBSITES", "websites").split() ).split()
        else:
            print "Missing parameter \"websites\" in configuration file"
            return False

        if not self.readWebsitesConfig():
            print "Error processing websites config"
            return False

##############################################################################################################

    def createLog(self):
        LOGLEVEL = logging.DEBUG
        logFile = 'log/' + self.pathOutFile + '.' + datetime.now().strftime("%Y-%m-%d") + ".log";
        self.log = logging.getLogger('0')
        self.log.setLevel(LOGLEVEL)
        logFormatter = logging.Formatter('[%(asctime)s] [%(levelname)s]=> [%(message)s] ')
        logHandler = logging.handlers.RotatingFileHandler(logFile, 'a',50000000,50)
        logHandler.setFormatter(logFormatter)
        self.log.addHandler(logHandler)
        # Error log
        LOGLEVEL2 = logging.ERROR
        logFile2 = 'log/' + self.pathErrFile + '.' + datetime.now().strftime("%Y-%m-%d") + ".log";
        self.logError = logging.getLogger('1')
        self.logError.setLevel(LOGLEVEL2)
        logFormatter2 = logging.Formatter('[%(asctime)s] [%(levelname)s]=> [%(message)s] ')
        logHandlerE = logging.handlers.RotatingFileHandler(logFile2, 'a',50000000,50)
        logHandlerE.setFormatter(logFormatter2)
        self.logError.addHandler(logHandlerE)
        return True

