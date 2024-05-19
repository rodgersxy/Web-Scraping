- scrapy 2.4.0 (v2.8.0)

- dnspython 2.1.0 (v2.4.2)

- pymongo 3.11.4 (v3.12.0)



You can install a specific version of a library with the command conda install <name-of-library>=<version>



## scrapy crawl worldometers

## how to create scrapy project
scrapy startproject spiderproject


# running spider
```
scrapy genspider worldometers www.worldometers.info/world-population/population-by-country
```

Here's what each part of the command means:

* scrapy: This is the command-line tool that comes with the Scrapy framework. It is used to run various Scrapy commands and operations.
* genspider: This is a specific Scrapy command that generates a new spider. It creates a Python file containing a spider class with some basic code and placeholders for you to customize.
* worldometers: This is the name you're giving to the new spider you're creating. It's a good practice to choose a descriptive name that represents the website or data you'll be scraping.
www.worldometers.info/world-population/population-by-country: This is the URL or domain that the spider will initially crawl. Scrapy will use this URL as a starting point to follow links and extract data from the website.

When you run this command, Scrapy will generate a new Python file (usually in the spiders directory of your Scrapy project) with a class called WorldometersSpider (or a name derived from worldometers). 

## worldometers.py file 
# spide_project/spiders/worldometers.py


``` 
* when creating you go to your project location where scrapy.cfg file is present the run this: 
scrapy genspider audible www.audible.com/search

```
NB:
scrapy crawl audible



## The 'scrapy genspider -l' command is used to list all available templates for creating a new Scrapy spider.

```
scrapy genspider -t crawl transcripts subslikescript.com
```
The command scrapy genspider -t crawl transcripts subslikescript.com does the following:

* scrapy genspider: This is the Scrapy command to generate a new spider.
-t crawl: This option specifies the template to use for generating the spider. In this case, * it's using the crawl template, which is designed for creating spiders that automatically follow links and crawl websites.
* transcripts: This is the name you're giving to the new spider. Scrapy will create a new Python file with this name (e.g., transcripts.py) inside the spiders directory of your Scrapy project.
* subslikescript.com: This is the domain or the website URL that you want the spider to crawl. Scrapy will use this URL as the starting point for the crawling process.