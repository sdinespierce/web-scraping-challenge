from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    
    ## MARS NEWS

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # find title and blurb
    news_title  = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()


    # Quit the browser after scraping
    browser.quit()



    ## MARS SPACE IMAGES

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit site
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #find mars image
    url_ext = soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = "https://spaceimages-mars.com/" + url_ext 


    # Quit the browser after scraping
    browser.quit()


    ##MARS FACTS
    table_list = pd.read_html("https://galaxyfacts-mars.com/")
    comparison_table = table_list[0]
    comparison_table_html = comparison_table.to_html()

    ## HEMISPHERES

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit site
    url = "https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(1)

    #find images and urls
    hemisphere_image_urls = []

    for i in range(0, 4):
        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")

        link_list = browser.links.find_by_partial_text('Hemisphere Enhanced')
        link_list[i].click()

        #redefine html
        html = browser.html
        soup = bs(html, "html.parser")

        title = soup.find('h2', class_='title').text
        img = soup.find('img', class_='wide-image')['src']
        browser.links.find_by_partial_text('Back').click()

        hemisphere_image_urls.append({"title": title, "img_url": "https://marshemispheres.com/" + img})

    # Quit the browser after scraping
    browser.quit()

    mars_data = {
        'news': news_p,
        'news_headline':news_title,
        'img_url': featured_image_url,
        'facts': comparison_table_html,
        'hemispheres': hemisphere_image_urls
    }

    return (mars_data)

