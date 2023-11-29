# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 14:33:57 2023

@author: Lucas Finney

Purpose: Turn the Jupyter Notebook into a single script.
"""

from bs4 import BeautifulSoup # this module helps in web scrapping.
import requests  # this module helps us to download a web page

path = input("Enter your path: ")

# Get from user if the path is local or internet
while(True):
    choice = int(input("Is this a local HTML file (1) or a url (2)? Press 1 or 2:  "))
    if choice == 1 :
        print(choice)
        with open(path,"r",encoding='utf-8') as f:
            data = f.read()
            break
    else:
        data  = requests.get(path).text
        break
            
            
    
#Note that this cell is currently formatted for doing the scraping from a saved HTML file of the main gallery page. This was my way of 
# getting around the problem that the page would load more content as the user scrolled.

soup = BeautifulSoup(data,"html5lib")

#Find the "content"
cont = soup.find(id = "content")

#get the links to all of the content
links = cont.find_all('a',href=True)

sub_pages = []
for link in links:
    sub_pages.append(link.get('href'))
    print(link.get('href'))
    
input("Press enter to continue...")

import os

# Create a directory 'Images' if it doesn't exist
tag = input('What string should I scrape for?: ')
images_dir = tag
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

n = int(input('How many images should I scrape?: '))
for i in range(0, min(n,len(sub_pages)) ):
    _data = requests.get(sub_pages[i]).text
    _soup = BeautifulSoup(_data,"html5lib")
    # Find all images with 'alt' containing 'tag'
    images = _soup.find_all('img', alt=lambda x: x and tag in x)

    for img in images:
        img_url = img['src']
        # Download the image
        img_data = requests.get(img_url).content
        img_name = os.path.join(images_dir, os.path.basename(img_url))

        with open(img_name, 'wb') as file:
            file.write(img_data)
            print(f"Downloaded {img_name}")
    i+=1

input("Press enter to close")