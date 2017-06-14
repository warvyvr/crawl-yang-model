# crwal-yang-model
A scrapy spider to crwal yang model from ietf website.  
its depends uses the following python package: 
- [xym](https://github.com/xym-tool/xym).

install dependent packages:
```
 pip install -r requirements.txt 
```
run the spider:
```
scrapy crawl ietf-yang
```
several paramters are changed in `settings.py` file:
- user agent
- a pipeline entity to generate `r.json`
- tcp timeout 10S
- enable download cache middleware, store the cache file locally

for the first time, it needs approximately 20 minutes, scrapy will cache all request and download objects.  


The extracted yang model files are stored in `yang-files` folder. 
a dedicated json file `r.json` (will be changed soon) is a summary for crwal activity result. 

