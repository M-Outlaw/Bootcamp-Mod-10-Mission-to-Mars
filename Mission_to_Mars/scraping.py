
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemisphere = mars_hemispheres(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere
    }
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
   
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p


# ## JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ## Mars Facts
def mars_facts():
    try:
        # use 'read_html' to scarpe the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# ## Mars Hemispheres
def mars_hemispheres(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Find and click the full image button

    cerb_image_elem = browser.find_by_tag('section').find_by_tag('a')[1]
    cerb_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # First image
    cerb_img_url = img_soup.find_all('a',target='_blank')
    cerb_img_url_rel = cerb_img_url[2].get('href')
    cerb_img_url = f'https://marshemispheres.com/{cerb_img_url_rel}'
    cerb_title = img_soup.find('h2',class_='title').text
    hemisphere_image_urls.append({'img_url': cerb_img_url,'title': cerb_title})

    # Second image
    browser.visit(url)
    schi_image_elem = browser.find_by_tag('section').find_by_tag('a')[3]
    schi_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    schi_img_url = img_soup.find_all('a',target='_blank')
    schi_img_url_rel = schi_img_url[2].get('href')
    schi_img_url = f'https://marshemispheres.com/{schi_img_url_rel}'
    schi_title = img_soup.find('h2',class_='title').text
    hemisphere_image_urls.append({'img_url': schi_img_url,'title': schi_title})

    # Third image
    browser.visit(url)
    sy_image_elem = browser.find_by_tag('section').find_by_tag('a')[5]
    sy_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    sy_img_url = img_soup.find_all('a',target='_blank')
    sy_img_url_rel = sy_img_url[2].get('href')
    sy_img_url = f'https://marshemispheres.com/{sy_img_url_rel}'
    sy_title = img_soup.find('h2',class_='title').text
    hemisphere_image_urls.append({'img_url': sy_img_url,'title': sy_title})

    # Fourth image
    browser.visit(url)
    v_image_elem = browser.find_by_tag('section').find_by_tag('a')[7]
    v_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    v_img_url = img_soup.find_all('a',target='_blank')
    v_img_url_rel = v_img_url[2].get('href')
    v_img_url = f'https://marshemispheres.com/{v_img_url_rel}'
    v_title = img_soup.find('h2',class_='title').text
    hemisphere_image_urls.append({'img_url': v_img_url,'title': v_title})
    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())