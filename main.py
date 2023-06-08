import requests
from bs4 import BeautifulSoup
import random
import sqlite3

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
            if href.startswith("https://www.opentable.com/r/"):
                # Split the href by "?" and select the first part
                url_before_question_mark = href.split('?')[0]
                filtered_hrefs.add(url_before_question_mark)
    
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
        # Create a BeautifulSoup object with the response content
        soup = BeautifulSoup(response.content, "html.parser")


        # Find the name 
        Name_results = soup.find_all("h1", class_="eM9Li2wbkQvvjxZB11sV mPudeIT67bJGOcOfKy92")
        #adds name to results
        for name in Name_results:
            filtered_name = name.text.strip()
            results.append(filtered_name)

        # inside same class 
        # Neigborhood, hour of operation ,cusine style , dining style , dress code, parking details , payment options,chef, phonenumber
        Aditional_results = soup.find_all("p", class_="c_qirB1mFl5VRKHYJqTz")

        ##ADDS results to array
        for result in Aditional_results:
            filtered_text = result.text.strip()
            if filtered_text not in results:
                results.append(filtered_text)
        

    else:
        print("Failed to retrieve data from OpenTable.")
    
    return results



####sqlite connector 
conn = sqlite3.connect('Cancun_Restaurants')
cursor = conn.cursor()

# Create a table to store the restaurant information
cursor.execute('''CREATE TABLE IF NOT EXISTS restaurants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    restaurant_name TEXT,
                    dining_style TEXT,
                    cuisine_style TEXT,
                    Hours_Operation TEXT,
                    Phone_number TEXT,
                    rest_url TEXT,
                    Payment_options TEXT,
                    dressing_style TEXT,
                    Aditional_information TEXT

                )''')


user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
    ]


URL = 'https://www.opentable.com/lolz-view-all/H4sIAAAAAAAA_6tWMlKyUjIyMDLWNTDTNbAIMTK0MjW0MjBQ0lEyRpEBCpgABQzNgZIQeVMlKyMdJTOQKkM9Q2MTI1NLHV0LMz0LA2NLU1OQBgugXIBrULC_n6OPZ5RrUHxgqGtQJFDCEiih7FiWmJmTmJST6pZf5JKZl5da5JdfDpQ0BFocHQukgfalJeYUp9YCAC-Y-f-mAAAA?originid=cbe5cdbf-804a-486e-ada3-1443b3f195a4'
URL_two ="https://www.opentable.com/lolz-view-all/H4sIAAAAAAAA_6tWMlKyUjIyMDLWNTDTNTAPMTSzMjWwMjBQ0lEyRpEBCpgABQyNgJIQeVMlKyMdJTOQKkM9Q2NjS2NLUx1dCzM9CwMgy9QCqMQCKBngGhTs7-fo4xnlGhQfGOoaFAmUsARKKDvl52e75Rf5lOYlZ4TkpyRWAiUMgbZGxwJpoGVpiTnFqbUArHVfmqMAAAA=?originid=f3202d6c-9f7c-4e41-a42c-460ba4d0d007&corrid=3129ec52-0217-4054-83c3-600875857298&page=2"
URL_three= "https://www.opentable.com/lolz-view-all/H4sIAAAAAAAA_6tWMlKyUjIyMDLWNTDTNTAPMTSzMjWwMjBQ0lEyRpEBCpgABQyNgJIQeVMlKyMdJTOQKkM9Q2NjS2NLUx1dCzM9CwMgy9QCqMQCKBngGhTs7-fo4xnlGhQfGOoaFAmUsARKKDvl52e75Rf5lOYlZ4TkpyRWAiUMgbZGxwJpoGVpiTnFqbUArHVfmqMAAAA=?originid=f3202d6c-9f7c-4e41-a42c-460ba4d0d007&corrid=3129ec52-0217-4054-83c3-600875857298&page=3"
URL_four = "https://www.opentable.com/lolz-view-all/H4sIAAAAAAAA_6tWMlKyUjIyMDLWNTDTNTAPMTSzMjWwMjBQ0lEyRpEBCpgABQyNgJIQeVMlKyMdJTOQKkM9Q2NjS2NLUx1dCzM9CwMgy9QCqMQCKBngGhTs7-fo4xnlGhQfGOoaFAmUsARKKDvl52e75Rf5lOYlZ4TkpyRWAiUMgbZGxwJpoGVpiTnFqbUArHVfmqMAAAA=?originid=f3202d6c-9f7c-4e41-a42c-460ba4d0d007&corrid=3129ec52-0217-4054-83c3-600875857298&page=4"


#Gets restaurnant URL LIST #change with url, url_2 ...
Rest_URL_list = get_urls(URL, user_agents)

result_list = []

#returns restaurant Information 

for url in Rest_URL_list:
    results = scrape_opentable(url,user_agents)
    result_list.append(results)


number = 0
list_item = 0

#prints the elements in each list till element 8 ( 0 to 7 = 8)
for i in result_list:
    #initializes aditional_items or resets it
    aditional_items = "ADITIONAL ITEMS: \n"
    for item in result_list[number]:
        if list_item <= 7:
            print(item, "\n")
            #add element to sql database HERE
            list_item = list_item + 1
        else:
            aditional_items += item + '\n'
    #prints aditional Items
    print(aditional_items)
    #ADDS ADITIONAL ITEMS TO DBS HERE

    #increments the list number
    number = number + 1

    #resets the item number
    list_item = 0



#print(result_list[0])



#examples of extras 
# extra_one : Kilómetro 14.5 

#extra_two: Gender Neutral Restroom, Patio/Outdoor Dining, View, Wheelchair Accessnn