import requests
from bs4 import BeautifulSoup
import random

def scrape_opentable():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
    ]
    URL = 'https://www.opentable.com/lolz-view-all/H4sIAAAAAAAA_6tWMlKyUjIyMDLWNTDTNTAPMTC0MjC2MjBQ0lEyRpEBCpgABYDyxgYQeVMlKyMdJTOQKkM9IxNLEx1dCzM9C2NzS6CkBVA4wDUo2N_P0cczyjUoPjDUNSgSKGEJlFB2LEvMzElMykl1yy_ySSxJdcnMy0st8ssvByowBNobHQukgdalJeYUp9YCAHKAnWOlAAAA?originid=0e6cdce0-377b-4043-9a39-5ff316237575'
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    response = requests.get(URL, headers=headers)

    results = []
    
    # Check if the request was successful
    if response.status_code == 200:
        # Create a BeautifulSoup object with the response content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the names
        Name_results = soup.find_all("h6", class_="tfljo0SQq0JS3FOxpvxL")

        # Find all the restaurant type/food
        Style_results = soup.find_all("div", class_="u9ONW2kqbJZxSOxtuBJq")

        #Find all price tags ( they have 4 and this code returns the missing so
        #  if it returns ($) it means ($$$$(4) - $(1)) = $$$(3))
        Price_results = soup.find_all("span", class_="AwKuroa75vy0Y4mLkyMr")

        #latest review, 
        
        review_results = soup.find_all("span", class_="t9JcvSL3Bsj1lxMSi3pz b70r5ifNREO8o2AZafOi cpEOy_DPrbjR6hnlY0ub #2d333f")

        #review number
        review_number_results = soup.find_all("a", class_="z6Naf_ZXDiazhb9aJLoe")


        ###############GETTING LINKS#############
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
        ##############GETING LINKS################

        # Combine results
        results = list(zip(Name_results, Style_results, Price_results,review_results,review_number_results, filtered_hrefs_list))
    else:
        print("Failed to retrieve data from OpenTable.")
    
    return results

result_list = scrape_opentable()

# Print combined results
for Name_results, Style_results, Price_results, review_results, review_number_results , filtered_hrefs_list in result_list:
    print( "Name: ",Name_results.text.strip() ," Style: ", Style_results.text.strip())
    print("PriceTag: ", Price_results.text.strip())
    print("Latest Rev", review_results.text.strip(),"Number of revs: ", review_number_results.text.strip())
    print("URL: ",filtered_hrefs_list)
    print()
