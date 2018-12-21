from newspaper import Article, ArticleException
import json
import requests
#from data_url import urls_brasil, urls_pt, urls_uk, urls_us
#from urllib.parse import urlparse
from pony.orm.core import *
import db_init
import pandas as pd
import time

def save_html_file(fname, html):
    filename = '%s.html' % fname
    with open("data_html/"+filename, 'wb') as f:
            f.write(html.encode())
    return filename


@db_session
def find_urls_to_fecth():
    to_fetch = db_init.Url.select(lambda p: p.fetch_status == "To Fetch")[:]
    return to_fetch

@db_session
def save_news(article,tweet,url_id,original_url,status,filename):
    if status:
        ## SAVE NEWS
        db_init.News(
            url_source = article.url,
            url_original = original_url,
            tweet_id = tweet.id,
            url_id = url_id,
            authors = str(article.authors),
            date = str(article.publish_date),
            meta = "",
            title = article.title,
            text = article.text.replace('\n\n','\n'),
            html_file = filename )
        ## UPDATE URL STATUS
        db_init.Url[url_id].fetch_status = "OK" 
        
    else:
        ## UPDATE URL STATUS
        db_init.Url[url_id].fetch_status = "ERROR" 
    commit()

@db_session
def parse_url_list(list_urls):
    for url_to_parse in list_urls:
        url = url_to_parse.expanded_url
        article = Article(url=url,fetch_images=False)

        try:
            article.download()
            article.parse()
            filename = save_html_file(url_to_parse.tweet.id,article.html)  
            
            save_news(  article,
                        url_to_parse.tweet, 
                        url_to_parse.id,
                        url_to_parse.expanded_url,
                        True,
                        filename)
            
        except ArticleException:
            
            save_news(  None,
                        None, 
                        url_to_parse.id,
                        None,
                        False,
                        None)
@db_session
def capture_new_urls():
    start_time = 0
    
        
    while True:
        to_fetch = find_urls_to_fecth()
        if to_fetch:
            print(len(to_fetch) , " New Urls")
            start_time = time.time()
            parse_url_list(to_fetch)
            print("time: ",time.time() - start_time)    
            start_time = 0       
        else: 
            print("Não existem urls novas")
            time.sleep(5)

capture_new_urls()

