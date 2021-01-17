#################################################
# Jupyter Notebook Conversion to Python Script
#################################################

# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time



#################################################
# Windows
#################################################
#Set Executable Path & Initialize Chrome Browser
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


#################################################
# NASA Mars News
#################################################
# NASA Mars News Site Web Scraper
def scrape():

    browser = init_browser()
    
    # Visit the NASA Mars News Site
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    # Parse Results HTML with BeautifulSoup
    nasa_html = browser.html
    soup_nasa = BeautifulSoup(nasa_html, "html.parser")
    
    required_list = soup_nasa.find('ul', class_='item_list')

    required_list.find("div", class_="content_title")

    # Scrape the Latest News Title
    # .text or .get_text()
    news_title = required_list.find("div", class_="content_title").get_text()

    # Scrape the Latest Paragraph Text
    news_paragraph = required_list.find("div", class_="article_teaser_body").get_text()

    


    
#################################################
# JPL Mars Space Images - Featured Image
#################################################
# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper

    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_img)

    # Navigate to navbar and click on 4th button 'Galleries'
    first_button = browser.find_by_tag('button')
    first_button[4].click()
    
    #Extract the title of the image
    img_title_soup = BeautifulSoup(browser.html,'html.parser')
    title = img_title_soup.find('div', class_='col-span-3').text
    image_title = title.split('.')
    img_title = image_title[1]

    #Click on 'Featured Image' text (link)
    browser.links.find_by_partial_text('Featured Image').click()

    #Extract the title of Featured Image
    # img_soup = BeautifulSoup(browser.html,'html.parser')
    # img_soup2 = img_soup.find('div', class_='PageImageDetail ThemeLight')
    # img_title = img_soup2.find('h1', class_='text-h2').text
    
    #Click on 'Download JPG' button to get full size image
    browser.links.find_by_partial_text('Download JPG').click()

    #Scrape the webpage to get the image url
    featured_image_soup = BeautifulSoup(browser.html,'html.parser')
    featured_url = featured_image_soup.find_all('img')[0]['src']
    

#################################################
# Mars Facts
#################################################
# Mars Facts Table Web Scraper

    # Visit the Mars Facts webpage 
    mars_url = 'https://space-facts.com/mars/'
    browser.visit(mars_url)
    
    #Read all the tables on the page
    tables = pd.read_html(mars_url)
    
    facts_table = tables[0]
    
    facts_table.columns=["Description", "Mars"]
    facts_table.set_index("Description", inplace=True)

    facts_table = facts_table.to_html(classes="table, table-striped")



#################################################
# Mars Hemispheres
#################################################
# Mars Hemispheres Web Scraper

    # Visit the USGS Astrogeology site
    url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # Parse HTML with Beautiful Soup
    hemi_soup = BeautifulSoup(browser.html,'html.parser')

    # Store the main url 
    main_url = "https://astrogeology.usgs.gov"

    # Create empty list for hemisphere urls and titles
    hemisphere_image_urls = []

    # Retreive all items that contain mars hemispheres information
    url_list = hemi_soup.find_all('div', class_='description')

    # Loop through the items previously stored
    for item in url_list:
        title = item.find('h3').text
        #print(title)

        # Store link that leads to full image website
        partial_url = item.find('a')['href']
        #print(partial_url)

        #Create the complete url to the full image page
        partial_url2 = main_url+partial_url
        #print(hemi_url)

        # Visit the link that contains the full image website 
        browser.visit(partial_url2)

        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        url_soup =BeautifulSoup(browser.html, 'html.parser')

        hemi_find = url_soup.find_all('div', class_='downloads')

        # Retrieve full image source 
        for x in hemi_find:
            final_url = x.find('a', target="_blank")['href']
            #print(final_url)
            
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title": title, "hemi_url": final_url})
        

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "img_title": img_title,
        "featured_image": featured_url,
        "facts": facts_table,
        "hemispheres": hemisphere_image_urls
        
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return data 

