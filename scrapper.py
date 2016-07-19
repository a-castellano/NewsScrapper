# Alvaro Castellano Vela - 19/07/2016
# https://github.com/a-castellano


from lib.config import Config

def main():
    cfg = Config("conf/scrapper.conf")
    if (cfg.readConfig() == False):
        print "BROKEN"
    else:
        print "NOT BROKEN"
        print cfg.websitesConf

if __name__ == "__main__":
    main()
