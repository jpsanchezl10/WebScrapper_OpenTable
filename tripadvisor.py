import requests
from bs4 import BeautifulSoup
import random
import sqlite3
import re
import base64
import json

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
def scrape_opentable(URL, user_agents):
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    response = requests.get(URL, headers=headers)

    results = []
    
    # Check if the request was successful
    if response.status_code == 200:

        #print("######")
        # Create a BeautifulSoup object with the response content
        soup = BeautifulSoup(response.content, "html.parser")


        # Find the name 
        Name_results = soup.find_all("h1", class_="HjBfq")
        #adds name to results
        for name in Name_results:
            filtered_name = name.text.strip()
            if filtered_name:
                results.append(filtered_name)
            else:
                results.append("?")
            #print(filtered_name, "\n")


        #find Rating and append it to results 
        Rating_results = soup.find_all("span", class_="ZDEqb")
        for rating in Rating_results:
            filtered_rating = rating.text.strip()
            if filtered_rating:
                results.append(filtered_rating)
                #print(filtered_rating, "\n")
            else:
                results.append("?")

        #find price range and append to results
        Price_results = soup.find_all("div", class_="SrqKb",string=lambda t: t and t.startswith("MX"))
        for price in Price_results:
            filtered_price = price.text.strip()
            if filtered_price:
                results.append(filtered_price)
                #print(filtered_price, "\n")
            else:
                results.append("?")

        #find Phone Number 
        Phone_results = soup.find_all("a", class_="BMQDV _F G- wSSLS SwZTJ",string=lambda t: t and t.startswith("+"))
        for phone in Phone_results:
            filtered_phones = phone.text.strip()
            if filtered_phones:
                results.append(filtered_phones)
                #print(filtered_phones, "\n")
            else:
                results.append("?")

        
        #find Location in results
        Location_results = soup.find_all("a", class_="AYHFM")
        for Location in Location_results:
            filtered_location = Location.text.strip()
            if "Cancun" in filtered_location and not filtered_location.startswith("#"):
                if filtered_location:
                    results.append(filtered_location)
                    #print(filtered_location, "\n")
                else:
                    results.append("?")

        

        # Find Cusine Style 
        Cusine_results = soup.find_all("a", class_="dlMOJ")
        cusine_list = []
        for Cusine in Cusine_results:
            filtered_Cusine = Cusine.text.strip()
            if not filtered_Cusine.startswith("$"):
                if filtered_Cusine:
                    cusine_list.append(filtered_Cusine)
                else:
                    results.append("?")


        # Print the cusine styles
        if cusine_list:
            joined_cuisines = ", ".join(cusine_list)
            results.append(joined_cuisines)
            #print("Cuisine: ", joined_cuisines, "\n")


        
        #find Restaurant Position RANK
        position_results = soup.find_all("span", class_="",string=lambda t: t and t.startswith("#"))
        if position_results:
            filtered_position = position_results[0].text.strip()
            if filtered_position:
                results.append(filtered_position)
                #print(filtered_position, "\n")
            else:
                results.append("?")



        ##find restaurant mail
        ###############GETTING URLS#############
        # Find mail
        mail_results = soup.find_all('a', href=True)    
        # Loop over the results and filter href values
        for tag in mail_results:
            href = tag['href']
            if href.startswith("mailto:"):
                mail_before_tag = href.split('?')[0]
                if mail_before_tag not in results:
                    # Remove "mailto:" prefix from URL
                    mail_before_tag = mail_before_tag[len("mailto:"):]

                    if mail_before_tag:
                        results.append(mail_before_tag)
                        #print(mail_before_tag)
                    else:
                        results.append("?")



        ###############GETTING restaurnat URL#############
        # Find URLS
        URL_results = soup.find_all('a', class_='YnKZo Ci Wc _S C FPPgD')

        # Loop over the results and filter href values
        for tag in URL_results:
            encoded_url = tag.get('data-encoded-url')
            decoded_url = base64.b64decode(encoded_url).decode('utf-8')
            if decoded_url and '+' not in decoded_url and 'google' not in decoded_url:
                filtered_url = re.sub(r'.*?(http.*?)_.*', r'\1', decoded_url)
                if filtered_url not in results:
                    if filtered_url:
                        results.append(filtered_url)
                        #print(filtered_url)
                    else:
                        results.append("?")
     

        
                ###############GETTING Map url#############
        # Find URLS
        map_results = soup.find_all('a', class_='YnKZo Ci Wc _S C FPPgD')

        # Loop over the results and filter href values
        for tag in map_results:
            encoded_map = tag.get('data-encoded-url')
            decoded_map = base64.b64decode(encoded_map).decode('utf-8')
            if decoded_map and 'google' in decoded_map:
                filtered_map = re.sub(r'.*?(http.*?)_.*', r'\1', decoded_map)
                if filtered_map not in results:
                    if filtered_map:
                        results.append(filtered_map)
                        #print("Map: ", filtered_map)
                    else:
                        results.append("?")


        # Find the <script> tags
        script_tags = soup.find_all('script')
        
        # Loop over the <script> tags
        for script_tag in script_tags:
            script_text = script_tag.string
            if script_text:
                # Check if the script text contains the desired information
                if 'allOpenHours' in script_text:
                    # Extract the desired information
                    match = re.search(r'"allOpenHours":(\[.*?\]),', script_text)
                    if match:
                        all_open_hours = match.group(1)
                        #remove brackets
                        
                        # Convert the extracted information to a Python object
                        open_hours_data = json.loads(all_open_hours)
                        # Append the extracted information to the results
                        if open_hours_data:
                            results.append(open_hours_data)
                            #print("Open Hours: ", open_hours_data)
                        else:
                            results.append("?")

            
        # Find the <img> tags
        img_tags = soup.find_all('img', class_='basicImg')

        # Loop over the <img> tags
        if img_tags:
            img_tag = img_tags[0]
            if 'data-lazyurl' in img_tag.attrs:
                img_url = img_tag['data-lazyurl']
                if img_url:
                    results.append(img_url)
                    #print("Image Source:", img_url)
                else:
                    results.append("?")
 

        

    else:
        print("Failed to retrieve data from Trip Advisor.")
    
    return results



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
for i in range(46):
    url = f"https://www.tripadvisor.com/Restaurants-g150807-oa{page}-Cancun_Yucatan_Peninsula.html"
    URLs.append(url)
    page += 30

#for i in range(46):
#    print(URLs[i])
##################

result_list = []

for URL in URLs:
    Rest_URL_list = get_urls(URL, user_agents)

    #returns restaurant Information 

    for url in Rest_URL_list:
        results = scrape_opentable(url,user_agents)
        result_list.append(results)


# Establish a connection to the SQLite database
conn = sqlite3.connect("concierge.db")
cursor = conn.cursor()


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




# Iterate over each restaurant's information
for item in result_list:
    # Check the length of the item list before accessing its elements
    if len(item) < 12:
        # Append default values ("?") for missing elements
        item += ["?"] * (12 - len(item))

    # Extract the restaurant name
    restaurant_name = item[0]

    # Check if the restaurant already exists in the database
    cursor.execute("SELECT COUNT(*) FROM restaurants WHERE restaurant_name = ?", (restaurant_name,))
    count = cursor.fetchone()[0]

    if count > 0:
        # Restaurant already exists, skip to the next item
        continue

    # Extract the URL string from the list
    restaurant_url = str(item[8])

    # Convert the restaurant_hours, restaurant_map, and restaurant_email lists to strings
    restaurant_hours = str(item[10])
    restaurant_map = str(item[9])
    restaurant_email = str(item[7])

    # Insert the restaurant's information into the database
    cursor.execute("INSERT INTO restaurants (restaurant_name, restaurant_rating, restaurant_price, restaurant_phone, restaurant_location, restaurant_style, restaurant_rank, restaurant_email, restaurant_url, restaurant_map, restaurant_hours, restaurant_image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (restaurant_name, item[1], item[2], item[3], item[4], item[5], item[6], restaurant_email, restaurant_url, restaurant_map, restaurant_hours, item[11]))

# Commit the changes to the database
conn.commit()