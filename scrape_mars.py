
import time
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    mars_data = {}
 
    mars_news_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_news_url)
 

    html = browser.html
    mars_news = bs(html, 'html.parser')

    news_title = mars_news.find('div', class_='content_title').text


    news_p = mars_news.find('div', class_="rollover_description_inner").text

    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p


    #JPL Mars Space Images - Featured Image
   
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

  
    html = browser.html
    jpl_soup = bs(html, 'html.parser')
    image_url = jpl_soup.find('a', {'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')

    jpl_logo_href = jpl_soup.find_all('div', class_='jpl_logo')

    response = requests.get(jpl_url)

    html_page = browser.html
    JPL_soup = bs(html_page, "html.parser")

    links = []
    for link in JPL_soup.find_all('a'):
        links.append(link.get('href'))

    jpl_link = links[1].strip('/')

    featured_image_url = "https://"+jpl_link + image_url


    mars_data["featured_image_url"] = featured_image_url


    # Mars Weather 
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(10)
  
    html = browser.html
    twitter_news = bs(html, 'html.parser')

    tweet = twitter_news.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')


    mars_weather = tweet.text

    mars_data["mars_weather"] = mars_weather

    # Mars Facts

    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)

    
    mars_df = pd.read_html(mars_facts_url)
    mars_facts_df = pd.DataFrame(mars_df[0])

    mars_facts_df.columns = ['Characteristic','Data']
    mars_df_table = mars_facts_df.set_index("Characteristic")

    mars_html_table = mars_df_table.to_html(classes='marsdata')
    mars_table = mars_html_table.replace('\n', ' ')

    mars_data["mars_table"] = mars_table


    #  Mars Hemispheres
   
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)


    html = browser.html
    mars_hemispheres = bs(html, 'html.parser')

 
    images = mars_hemispheres.find('div', class_='collapsible results')
    

    hemispheres_image_urls = []

    for i in range(len(images.find_all("div", class_="item"))):
        time.sleep(5)
        image = browser.find_by_tag('h3')
        image[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find("h2", class_="title").text
        div = soup.find("div", class_="downloads")
        for li in div:
            link = div.find('a')
        url = link.attrs['href']
        hemispheres = {
                'title' : title,
                'img_url' : url
            }
        hemispheres_image_urls.append(hemispheres)
        browser.back()

        mars_data["hemispheres_image_urls"] = hemispheres_image_urls

     
        return mars_data
