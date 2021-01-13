#################################################
# Jupyter Notebook Conversion to Python Script
#################################################

# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt


#################################################
# Windows
#################################################
#Set Executable Path & Initialize Chrome Browser
executable_path = {'executable_path': "/Users/User/.wdm/drivers/chromedriver/win32/87.0.4280.88/chromedriver.exe"}
browser = Browser('chrome', **executable_path, headless=False)


#################################################
# NASA Mars News
#################################################
# NASA Mars News Site Web Scraper
def mars_news(browser):
    # Visit the NASA Mars News Site
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    # Parse Results HTML with BeautifulSoup
    nasa_html = browser.html
    soup_nasa = BeautifulSoup(nasa_html, "html.parser")
    

    # Find Everything Inside:
    #   <ul class="item_list">
    #     <li class="slide">
    try:
        required_list = soup_nasa.select_one("ul.item_list li.slide")
        required_list.find("div", class_="content_title")

        # Scrape the Latest News Title
        news_title = required_list.find("div", class_="content_title").get_text()

        # Scrape the Latest Paragraph Text
        news_paragraph = required_list.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_paragraph


#################################################
# JPL Mars Space Images - Featured Image
#################################################
# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper
# def featured_image(browser):
#     # Visit the NASA JPL (Jet Propulsion Laboratory) Site
#     url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
#     browser.visit(url)

#     # Ask Splinter to Go to Site and Click Button with Class Name full_image
#     # <button class="full_image">Full Image</button>
#     full_image_button = browser.find_by_id("full_image")
#     full_image_button.click()

#     # Find "More Info" Button and Click It
#     browser.is_element_present_by_text("more info", wait_time=1)
#     more_info_element = browser.find_link_by_partial_text("more info")
#     more_info_element.click()

#     # Parse Results HTML with BeautifulSoup
#     html = browser.html
#     image_soup = BeautifulSoup(html, "html.parser")

#     img = image_soup.select_one("figure.lede a img")
#     try:
#         img_url = img.get("src")
#     except AttributeError:
#         return None 
#    # Use Base URL to Create Absolute URL
#     img_url = f"https://www.jpl.nasa.gov{img_url}"
#     return img_url


#################################################
# Mars Facts
#################################################
# Mars Weather Twitter Account Web Scraper
def mars_facts():
    # Visit the Mars Facts webpage 
    mars_url = 'https://space-facts.com/mars/'
    browser.visit(mars_url)
    
    # Parse Results HTML with BeautifulSoup
    mars_html = browser.html
    soup_mars = BeautifulSoup(mars_html, "html.parser")
    
    #Read all the tables on the page
    tables = pd.read_html(mars_url)
    
    facts_table = tables[0]
    
    facts_table.columns=["Description", "Value"]
    facts_table.set_index("Description", inplace=True)

    return facts_table.to_html(classes="table table-striped")



#################################################
# Mars Hemispheres
#################################################
# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)'
    browser.visit(astro_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        #Store title
        title = i.find('h3').text
    
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
    
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
    
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    # Display hemisphere_image_urls
    return hemisphere_image_urls

# Helper Function
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere


#################################################
# Main Web Scraping Bot
#################################################
def scrape_all():
    executable_path = {"executable_path": "/Users/User/.wdm/drivers/chromedriver/win32/87.0.4280.88/chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    #img_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        #"featured_image": img_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())