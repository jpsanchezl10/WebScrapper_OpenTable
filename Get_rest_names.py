import requests
from bs4 import BeautifulSoup
import random
import sqlite3
import re
import base64
import json


def Create_Table():
    # SQLite command to create the restaurants table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_name TEXT,
            restaurant_rating TEXT,
            restaurant_price TEXT,
            restaurant_phone TEXT,
            restaurant_location TEXT,
            restaurant_style TEXT,
            restaurant_rank TEXT,
            restaurant_email TEXT,
            restaurant_url TEXT,
            restaurant_map TEXT,
            restaurant_hours TEXT,
            restaurant_image TEXT
        )
    '''

    # Execute the create table command
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    conn.commit()

#import os
def get_urls(URL, user_agents):

    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    response = requests.get(URL, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Create a BeautifulSoup object with the response content
        soup = BeautifulSoup(response.content, "html.parser")

        ###############GETTING URLS#############
        # Find URLS
        URL_results = soup.find_all('a', href=True)
        # Create an empty set to store filtered href values
        filtered_hrefs = set()
        
        # Loop over the results and filter href values
        for tag in URL_results:
            href = tag['href']
            if href.startswith("/Restaurant_Review"):
                url_before_tag = href.split('#')[0]
                new_url = "https://www.tripadvisor.com"+url_before_tag
                if new_url not in filtered_hrefs:
                    filtered_hrefs.add(new_url)
                    #print(new_url)
    
        filtered_hrefs_list = list(filtered_hrefs)


        # Combine results
    else:
        print("Failed to retrieve URLs from OpenTable.")
    
    return filtered_hrefs_list


###Get info from urls
def insert_restaurant_names(URL, user_agents):
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    response = requests.get(URL, headers=headers)
    #initialize null value string
    null_value = "?"
    
    # Check if the request was successful
    if response.status_code == 200:
        # Create a BeautifulSoup object with the response content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the name 
        Name_results = soup.find_all("h1", class_="HjBfq")
        #adds name to results
        for name in Name_results:
            filtered_name = name.text.strip()
            
            rest_name = str(filtered_name)
            
             # Check if the restaurant already exists in the database
            cursor.execute("SELECT COUNT(*) FROM restaurants WHERE restaurant_name = ?", (rest_name,))
            count = cursor.fetchone()[0]

            if count > 0:
                # Restaurant already exists, skip to the next item
                continue

            cursor.execute("INSERT INTO restaurants (restaurant_name, restaurant_rating, restaurant_price, restaurant_phone, restaurant_location, restaurant_style, restaurant_rank, restaurant_email, restaurant_url, restaurant_map, restaurant_hours, restaurant_image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (rest_name, null_value,null_value,null_value, null_value, null_value, null_value, null_value, null_value,null_value,null_value, null_value ))
            # Commit the changes to the database
    
            conn.commit()  

    else:
        print("Failed to retrieve data from Trip Advisor.")
    
    

user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
    ]

##########adds urls to the last page (46)
URLs = [
    "https://www.tripadvisor.com/Restaurants-g150807-Cancun_Yucatan_Peninsula.html"
]

page = 30
for i in range(41):
    url = f"https://www.tripadvisor.com/Restaurants-g150807-oa{page}-Cancun_Yucatan_Peninsula.html"
    URLs.append(url)
    page += 30




# Establish a connection to the SQLite database
conn = sqlite3.connect("concierge.db")
cursor = conn.cursor()

#create table 
Create_Table()

for URL in URLs:
    Rest_URL_list = get_urls(URL, user_agents)

    #returns restaurant Information 

    for url in Rest_URL_list:
        insert_restaurant_names(url,user_agents)










