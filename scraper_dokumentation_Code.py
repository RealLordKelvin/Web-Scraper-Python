# install required packages

from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import json


# Insert website link, here you can introduce for example an list of website links found on google alerts

page = requests.get("https://www.gruenderszene.de/?interstitial_click")

# start parser

soup = BeautifulSoup(page.text, 'html.parser')

## This is an example for gruenderszene, if you have already a list of links than you can skip that part to "Section 2"

last_links = soup.find(class_='sidebar_trending home')

trend_link = soup.find_all(class_='top-sidebar-entries-content left trend-content')

f = csv.writer(open('gruenderTesto.csv', 'w')) # just for storing purpose I stored the links in an csv file. 

# I could also store the values in an list in python like in the next subsection..

# Here I stored the links in an python list but it needed further prep.. 

list_trend_link = []

for i in trend_link:
    l_trend_link = i.find('a')
    list_trend_link.append(l_trend_link)
    


print (list_trend_link)

# In this section I will open link after link to get clean links in order to search for them afterwards
results = []

for link in list_trend_link:
    links = 'https://www.gruenderszene.de' + link.get('href')
    print (links)
    results.append(links)


    # Add each artist’s name and associated link to a row
    f.writerow([links])

print(results) 


# Section 2, here is where the magic starts if you have already an list with links

# first I gonna create an dict Object --> like a json Object

data = {}

# with the name Web, which you can specify with multiple website --> you should do an loop with an count for example to have different websites keys

data['web'] = []

# start an counter to give unique keys for each Category

count = 0

for i in results:
    count += 1
    c = str(count)
    r = requests.get(i) # I request first link in the list
    soup = BeautifulSoup(r.text, 'html.parser') # start parser
    a = soup.span
    
    s = str(soup.title.text) # extract title from the website
    paragraph = soup.findAll('p') # extract all paragraphs signed with p in the Website == content of the Website
    
    s_c = [] # in order to get the full article at once we create an list to store the content of the different paragraphs
    for p in paragraph:
        s_c.append(p.getText())
        s_c = [item.strip() for item in s_c if str(item)]
    complete_article = "\n".join(s_c) # we now join them all together, to get one article content
    
    # Now we just append the titles, author and content in our dictionary object
    
    data["web"].append({
        'title_' + c : s,
        'content_' + c : complete_article
    })
    
# See result
print(data["web"])
# here you should select your own folder
with open('C:\\Users\\Vincent.Uhlke\\Vincent_Aufgben\\Python_scraper\\data.txt', 'w') as outfile: 
    json.dump(data, outfile)