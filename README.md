# Web-scraping

python3 -m venv venv  
source venv/bin/activate  

---------------------------------------------
cd spider  
scrapy genspider (name of the spider and name of the website to scrap) .com  

* pip install ipython   
add shell = ipython to scrapy.cfg file(under settings)  

## In the terminal run:   
scrapy shell     

fetch('https://..................')  
response   
scrapy crawl (name of the spider)