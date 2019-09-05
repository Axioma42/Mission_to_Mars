from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

# Open browser
def open_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Create global dictionary for mongo
mars_dict = {}

def scrape_mars_news():
    try:
        browser = open_browser()
        
        # Visit the url for JPL Featured Space
        url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url)

        # HTML object
        html = browser.html

        # Parser
        soup = BeautifulSoup(html, "html.parser")

        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find("div", class_="content_title").find("a").text
        news_p = soup.find("div", class_="article_teaser_body").text

        # Dictionary entry
        mars_dict["news_title"] = news_title
        mars_dict["news_paragraph"] = news_p

        return mars_dict
    finally:
        browser.quit()

def scrape_mars_featured_image():
    try:
        browser = open_browser()

        # Visit the url for JPL Featured Space
        url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url)

        # HTML object
        html = browser.html

        # Parser
        soup = BeautifulSoup(html, "html.parser")

        # Find image
        browser.find_by_id("full_image").click()

        browser.is_element_present_by_text("more info", wait_time=1)
        more_info_element = browser.find_link_by_partial_text("more info")
        more_info_element.click()

        # Scrap the url
        html = browser.html
        image_soup = BeautifulSoup(html, "html.parser")
        img_url = image_soup.select_one("figure.lede a img").get("src")

        # Dictionary entry
        mars_dict["featured_image_url"] = img_url

        return mars_dict
    finally:
        browser.quit()

def scrape_mars_weather():
    try:
        browser = open_browser()

        # Visit ars weather twitter 
        url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(url)

        # HTML object
        html = browser.html

        # Parser
        soup = BeautifulSoup(html, "html.parser")

        # Retrieve the latest element that contains the martian weather
        tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Look for last weather tweet
        for tweet in tweets: 
            weather_tweet = tweet.find('p').text
            if 'sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass
        
        # Dictionary entry
        mars_dict["mars_weather_tweet"] = weather_tweet

        return mars_dict
    finally:
        browser.quit()

def scrape_mars_facts():
    try:
        browser = open_browser()

        # Visit mars facts page
        url = "http://space-facts.com/mars/"
        browser.visit(url)

        # Use pandas to scrape the table containing facts about the planet
        mars_facts = pd.read_html(url)
        df = mars_facts[1]
        df.columns = ["Attribute", "Value"]

        # Use Pandas to convert the data to a HTML table string
        html_table = df.to_html()

        # Dictionary entry
        mars_dict["mars_facts"] = html_table

        return mars_dict
    finally:
        browser.quit()

def scrape_mars_hemispheres():
    try:
        browser = open_browser()

        # Visit mars hemispheres page
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)

        # HTML object
        html = browser.html

        # Parser
        soup = BeautifulSoup(html, "html.parser")

        # Empty urls list 
        image_urls = []

        # List of all the hemispheres
        links = browser.find_by_css("a.product-item h3")
        for item in range(len(links)):
            hemisphere = {}
    
            # Find Element on Each Loop
            browser.find_by_css("a.product-item h3")[item].click()
    
            # Find sample image and extract href
            sample_element = browser.find_link_by_text("Sample").first
            hemisphere["img_url"] = sample_element["href"]
    
            # Get title
            hemisphere["title"] = browser.find_by_css("h2.title").text
    
            # Append dictionary to the list
            image_urls.append(hemisphere)
    
            # Go back
            browser.back()

            # Dictionary entry
            mars_dict["mars_hemispheres"] = image_urls

        return mars_dict
    finally:
        browser.quit()

