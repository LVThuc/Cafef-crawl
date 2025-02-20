import numpy as np 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import json
import os
# Create output directory
output_dir = 'output_links1'
os.makedirs(output_dir, exist_ok=True)
# Declare browser
driver = webdriver.Chrome()

# Open the website
driver.get("https://cafef.vn/thi-truong.chn")
sleep(random.randint(25, 25))

# Get all div elements with the class 'tlitem box-category-item loadedStock'
divs = driver.find_elements(By.CSS_SELECTOR, ".tlitem.box-category-item")

# Get the link and tittle of the product
# Extract links from h3 elements within the divs
count = 0
links = []
titles = []
for div in divs:
    try:
        h3 = div.find_element(By.TAG_NAME, "h3")
        a = h3.find_element(By.TAG_NAME, "a")
        link = a.get_attribute('href')
        title = a.text
        links.append(link)
        titles.append(title)
        
    except NoSuchElementException:
        continue
print(len(links))

contents = []
# Loop through the links
for i in range(min(251,len(links))):
    link = links[i]
    title = titles[i]

    # Navigate

    driver.get(link)

    # Get content
    try:
        # Publish date
        publish_date = driver.find_element(By.CSS_SELECTOR, ".pdate").text
        
        # content
        content = driver.find_element(By.CSS_SELECTOR, ".sapo").text
        paragraphs = driver.find_elements(By.CSS_SELECTOR, ".detail-content p")
        content += "\n".join([p.text for p in paragraphs])

        # media 
        medias = []

        # Thumbnail image
        try:
            media_div = driver.find_element(By.CSS_SELECTOR, ".media.VCSortableInPreviewMode img")
            media_src = media_div.get_attribute('src')
            media_title = media_div.get_attribute('title')
            medias.append((media_src, media_title))
        except NoSuchElementException:
            pass
        
        # Other images
        media_elements = driver.find_elements(By.CSS_SELECTOR, ".VCSortableInPreviewMode a.detail-img-lightbox")
        for media_element in media_elements:
            media_href = media_element.get_attribute('href')
            media_title = media_element.get_attribute('title')
            medias.append((media_href, media_title))

        # Create a dict for export
        item = {"url": link, "title": title, "content": content, "metadata": medias}
        # Export to Json
        file_name = f'{count}.json'
        count += 1
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w', encoding = 'utf-8') as f:
            json.dump(item, f, ensure_ascii = False, indent = 4)
    except NoSuchElementException:
        continue
    
# export links

# Get the price of the product
driver.quit()