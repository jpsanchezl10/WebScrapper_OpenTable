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



user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
    ]


URL = 'https://www.opentable.com/lolz-view-all/H4sIAAAAAAAA_6tWMlKyUjIyMDLWNTDTNbAMMTCwMjS1MjBQ0lEyRpaxAAqYAAUMLa2MDSDypkpWRjpKZiBVhnqGxiZGppY6uhZmehYGxpampiANFkC5ANegYH8_Rx_PKNeg-MBQ16BIoIQlUELZKT8_2y2_yCUzLy-1CChoCLQwOhZIA-1JS8wpTq0FAHO6hueeAAAA?originid=14383710-dd5b-48f8-a8ec-61618953eed7'
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


# Connect to the SQLite database
conn = sqlite3.connect('Cancun_Restaurants.db')
cursor = conn.cursor()

# SQLite command to create the restaurants table
create_table_query = '''
    CREATE TABLE IF NOT EXISTS restaurants (
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
    )
'''

# Execute the create table command
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
#conn.close()

def insert_empty_values_sqlite():
    values = (
        'test',
        'test',
        'test',
        'test',
        'test',
        'test',
        'test',
        'test',
        'test'
)
    # Execute the SQL statement
    cursor.execute("""
        INSERT INTO restaurants (
            restaurant_name,
            dining_style,
            cuisine_style,
            Hours_Operation,
            Phone_number,
            rest_url,
            Payment_options,
            dressing_style,
            Aditional_information
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, values)

    # Commit the changes to the database
    conn.commit()

    ##end of funtion 

#identifies in what restaurant number we are 
number = 0
#identifies in what item from the list we are 
list_item = 0
#identifies in what row of the table we are
id_table = 1;

column_name = ["restaurant_name","dining_style","cuisine_style","Hours_Operation","Phone_number","rest_url","Payment_options","dressing_style","Aditional_information"]

#iterates the result list ( all the restaurnats)
for i in result_list:
    #initializes new empty values in table  to be able to update them later 
    insert_empty_values_sqlite()

    #initializes aditional_items or resets it
    aditional_items = "ADITIONAL ITEMS: \n"

#prints the elements in each list till element 8 ( 0 to 7 = 8)
    for item in result_list[number]:
        if list_item <= 7:
            print(item, "\n")
            #add element to sql database HERE
            cursor.execute(
                f"UPDATE restaurants SET {column_name[list_item]} = ? WHERE id = ?;",
                (item, id_table)
            )

            list_item = list_item + 1
        else:
            aditional_items += item + '\n'
            
    #prints aditional Items
    print(aditional_items)
    #ADDS ADITIONAL ITEMS TO DBS HERE
    cursor.execute(
        f"UPDATE restaurants SET Aditional_information = ? WHERE id = ?;",
        (aditional_items, id_table)
    )

    #increments the list number
    number += 1

    #resets the item number
    list_item = 0

    #increments the id of the table
    id_table += 1
    
    #commits all the updates
    conn.commit()


#closes de conection with sqli
conn.close()