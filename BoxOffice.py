import requests
from bs4 import BeautifulSoup
import re

website = input('What is the movie you are looking for? ')
website = website.replace(' ', '_')

def alternativesearch(website):
    response = requests.get(
        url=(f"https://en.wikipedia.org/w/index.php?search={website}_movie&title=Special%3ASearch&profile=advanced&fulltext=1&ns0=1"),
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    wikipedialinks = {
            'Main_Page',
            'Wikipedia:Contents',
            'Portal:Current_events',
            'Special:Random',
            'Wikipedia:About',
            'Help:Contents',
            'Help:Introduction',
            'Wikipedia:Community_portal',
            'Special:RecentChanges',
            'Wikipedia:File_upload_wizard',
            'Special:MyContributions',
            'Special:MyTalk',
            'Help:Searching',
            'Special:SpecialPages',
            'Special:Search',
            'Wikipedia:File_Upload_Wizard',
            'Wikipedia:Article_wizard',
            'Wikipedia:Articles_for_creation/Redirects_and_categories',
            'Wikipedia:General_disclaimer'
        }
    newtitle = []
    for link in links:
        match = re.search(r'(?<=href=\"/wiki/)(.*?)(?=\")',str(link))
        if match:
            newtitle.append(match.group())
    newtitlefilter = []
    for names in newtitle:
        if names not in wikipedialinks:
            newtitlefilter.append(names)
    #print(newtitlefilter) Use if Persistant error from links not ignored by wikipedialinks function
    website = newtitlefilter[0].replace(' ', '_')
    return website

website = alternativesearch(website)
response = requests.get(
    url=(f"https://en.wikipedia.org/wiki/{website}"),
)
                    
soup = BeautifulSoup(response.text, 'html.parser')
tdlist = soup.find_all('td',{'class':"infobox-data"})
moneylist = []
for item in tdlist:
    for child in item.children:
        match = re.search("(\\$.*)",str(child))
        if match:
            moneylist.append(match.group())


title = soup.find(id="firstHeading").string

if not title:
    title = website
print(f"{title}\nBudget: {moneylist[0]}\nBox Office: {moneylist[1]}")