#!/usr/bin/env python
# coding: utf-8

# In[75]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[76]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[77]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[78]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[79]:


slide_elem.find('div', class_='content_title')


# In[80]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[81]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[82]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[83]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[84]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[85]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[86]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[87]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[88]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[89]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[198]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[199]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Find and click the full image button

cerb_image_elem = browser.find_by_tag('section').find_by_tag('a')[1]
cerb_image_elem.click()
html = browser.html
img_soup = soup(html, 'html.parser')

# First image
cerb_img_url = img_soup.find_all('a',target='_blank')
cerb_img_url_rel = cerb_img_url[3].get('href')
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
schi_img_url_rel = schi_img_url[3].get('href')
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
sy_img_url_rel = sy_img_url[3].get('href')
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
v_img_url_rel = v_img_url[3].get('href')
v_img_url = f'https://marshemispheres.com/{v_img_url_rel}'
v_title = img_soup.find('h2',class_='title').text
hemisphere_image_urls.append({'img_url': v_img_url,'title': v_title})


# In[200]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[201]:


# 5. Quit the browser
browser.quit()


# In[ ]:




