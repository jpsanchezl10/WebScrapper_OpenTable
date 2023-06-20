URLs = [
    "https://www.tripadvisor.com/Restaurants-g150807-Cancun_Yucatan_Peninsula.html"
]

page = 30
for i in range(46):
    url = f"https://www.tripadvisor.com/Restaurants-g150807-oa{page}-Cancun_Yucatan_Peninsula.html"
    URLs.append(url)
    page += 30

for i in range(46):
    print(URLs[i])