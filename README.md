# NewsScrapper

This project pretends to be a scrapper manager which scrape news from different websites. You have create your own scrappers from the parent class. The scrapper manager will call all of them.

Each scrapper posts processed content inside a database defined in a config file.
The scrapped content will be published in a WordPress site too.

# Table of Contents
1. Required software
2. Configuration files
3. Database Class
4. Defining new scrappers
5. Defining new scrappers
6. Example
7. TODO

## Required software

This project needs the following packages to run:

- python3-pip (via apt-get)
- python3-mysqldb (via apt-get)
- python-wordpress-xmlrpc (via pip3)

## Configuration files

In order to make this manager work we have to write a config file and place it in **conf/scrapper.conf**. Use **conf/scrapper.conf.example** as template.

```
[LOG]
pathOutFile = The name of your log files
pathErrFile = The name of your error log files.
```

For example, if our *pathOutFile* is called *myscrapper* the log files will be stored in **log/mysrapper.YYYY-MM-DD.log**

We must also specify our database settings such as **host**, **user**, **pass**, **port** and the **database** name.

```
[DB]
host = YOUR_HOST
port = YOUR_PORT
user = YOUR_USER
password = YOUR_PASSWORD
database = YOUR_DATABASE_NAME
```

We also have to set our WordPress site address and its credentials, **host** has to be set without "http://", only with the domain name.
```
[WP]
host = YOUR_WP_HOST
user = YOUR_WP_USER
password = YOUT_WP_PASS
```

Finally, we need to define which websites we want to scrape.
```
[WEBSITES]
websites = website1.example.com website2.example.com
```

For each website we define we will have to create a file called **domain.conf**. In the example case we have defined **conf/website1.example.com.conf** and **conf/website2.example.com.conf**. Let's review one of them.

```
[WEBSITE]
name = website1.example.com

[SECTIONS]

section1_name = website1_politics
section1_url = http://website1.example.com/news/politics
section1_slug = news/politics

section2_name = website1_economy
section2_url = http://website1.example.com/news/economy
section2_slug = news/economy
```
 Each website has a name that identifies it. We also have to define the sections of this website that we want to scrape. In this example website1.example.com has two sections that interest us, economy section and politics section.

**section_name** will name the table which will contain the scrapped content from that section.

 For each section we will set its name, url, and the slug prefix (the scrapper does not use this variable yet).

 **Section name will be unique for all sections and all websites**.

## Database Class

The Database class (db) will create a table for each function if it does not exist and it will store the scrapped items.

- **createTableIfNotExist()**: if there is no table called as the section the manager is scrapping it will create that table.
- **getURLs()**: Get the list of scrapped URL's of current section. This function is very useful to avoid storing repeated content into our database.
- **addData()**: add items into database.

## Scrapper definition

In **lib** folder we will find our **Scrapper** parent class which defines the common functions for all scrappers. These functions are:

- **addItemsToMysql()** : This function calls the db functions addData which will store the scrapped items into our database.
- **addItemsToWordpress()** : This function will store our scrapped content into our WordPress site.

For each new scrapper we create we must write a new class in **lib/scrappers** folder and add its definition to **lib/scrapperFactory.py**.

## Defining new scrappers

To create a new scrapper we have to follow these steps:

### Create a new scrapper class in lib/scrappers folder

The class skeleton would be like this:

``` python3
#!/usr/bin/python3

import sys
sys.path.append('../../')

from lib.scrapper import Scrapper

class ScrapperWebsite1Economy( Scrapper ):

    def __init__( self, db, wpinfo, table, url, slug, log ):
        Scrapper.__init__( self, db, wpinfo, table, url, slug, log )

    def scrape():
        # Write here your scrape function

        self.log.info( "We can write logs from this function too")

        # I recommend you to get the URL's that have been already scrapped to avoid repeated content into tour database.

        storedItems = db.getURLs()

        # At the end of this function we need to store our items into self.items

        self.items = ourScrappedContent
```

Each item you scrape would have the following data:

- **item['title']** -> The title of the article.
- **item['description']** -> The description of the article.
- **item['url']** -> The original url of the article.
- **item['image_url']** -> And image about this article.
- **item['video_url']** -> A youtube video about this article.
- **item['content']** -> The content of this article.
- **item['slug']** -> the slug (permalink) of this article.
- **item['keywords']** -> keywords for this article.
- **item['referer']** -> name of the referer.
- **item['referer_url']** -> referer url.

The manager only needs to store the title and the URL of each article, the other parts are optional.

Finally we need to add our new class into our **scrapperFactory** class.

```
import sys
sys.path.append('../')

from lib.scrappers import website1_economy
from lib.scrappers import website1_politics
from lib.scrappers import website2_science
from lib.scrappers import website2_sports
from lib.scrappers import YOUR_NEW_SCRAPPER

class ScrapperFactory( object ):

    def factory( type, db, wpinfo, table, url, slug, log ):
        if type == "website1_economy": return website1_economy.ScrapperWebsite1Economy( db, wpinfo, table, url, slug, log )
        if type == "website1_politics": return website1_politics.ScrapperWebsite1Politics( db, wpinfo, table, url, slug, log )
        if type == "website2_science": return website2_science.ScrapperWebsite2Science( db, wpinfo, table, url, slug, log )
        if type == "website2_sports": return website2_sports.ScrapperWebsite2Sports( db, wpinfo, table, url, slug, log )
        if type == "YOUR_NEW_SCRAPPER": return YOUR_NEW_SCRAPPER.ScrapperYOUR_NEW_SCRAPPER( db, wpinfo, table, url, slug, log )        
    factory = staticmethod(factory)
```

## Example

[Here](https://gist.github.com/a-castellano/402b11f157fa486cd79420fb840739a6) is an ownmade scrapper which gets news from boxing section of [clarin.com](http://www.clarin.com/deportes/boxeo/)

## TODO

 - Allow to set WordPress post categories name.
 - The WordPress client is http, it ccould be https too.
 - "Source" name should be able to change.
 - The origin "source" of the content should be optional.
 - Write argument parssing module to disable post submiting to WordPress.
 - Dockerize this app
