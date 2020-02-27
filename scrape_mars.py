import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import re
import pymongo
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

    # News Scrape
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)
    time.sleep(5)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    news_title = news_soup.find('div', class_='content_title').find('a').text
    news_paragraph = news_soup.find('div', class_='article_teaser_body').text

    # JPL
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(5)
    html = browser.html
    images_soup = BeautifulSoup(html, 'html.parser')
    image_url  = images_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1] 
    main_url = "https://www.jpl.nasa.gov"
    image_url = main_url + image_url
    featured_image_url = image_url
    
    

    # Twitter scraped
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    weather_html = browser.html
    twitter_response = requests.get("https://twitter.com/marswxreport?lang=en")
    twitter_soup = BeautifulSoup(twitter_response.text, 'html.parser')
    tweet_containers = twitter_soup.find_all('div', class_="js-tweet-text-container")
    mars_weather = tweet_containers[0].text


    # Mars Facts
    request_mars_space_facts = requests.get("https://space-facts.com/mars/")
    mars_space_table_read = pd.read_html(request_mars_space_facts.text)
    df = mars_space_table_read[2]
    df.columns = ["Description", "Value"]
    mars_html_table = df.to_html(index=False)


    # Mars hemispheres
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_req = requests.get(usgs_url)
    usgs_soup = BeautifulSoup(usgs_req.text, "html.parser")
    browser.visit(usgs_url)
    hemi_attributes_list = usgs_soup.find_all('a', class_="item product-item")
    hemisphere_image_urls = []

    hemis_titles = usgs_soup.find_all('h3')

    for i in range(len(hemis_titles)):
        hemis_title = hemis_titles[i].text
        print(hemis_title)
    
        hemis_images = browser.find_by_tag('h3')
        hemis_images[i].click()
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        img_url = soup.find('img', class_='wide-image')['src']
        img_url = "https://astrogeology.usgs.gov" + img_url
        print(img_url)
    
        hemis_dict = {"title": hemis_title, "img_url":img_url}
        hemisphere_image_urls.append(hemis_dict)
    
        browser.back()


    # storing into a dict 
    mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict
