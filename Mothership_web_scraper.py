
from selenium import webdriver
from bs4 import BeautifulSoup
import requests 
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import openpyxl


def get_data(url,keywords,title,url_keep,date,text,keyfound):
    source = requests.get(url).content
    soup = BeautifulSoup(source,"lxml")
    
    content = soup.find_all("div",class_ = "content-article-wrap")
    headline = soup.find('h1').text
    date1 = soup.find("span",class_="publish-date").text.strip("n\n")
    related_article = False
    body_text = content[0].text.replace('\n',' ').replace('\r','').replace("\xa0"," ")
    key = []
    for keyword in keywords:
        if keyword in headline.lower():
            related_article = True
            key.append(keyword)
        if keyword in body_text.lower():
            related_article = True
            key.append(keyword)
    if related_article :
        title.append(headline)
        url_keep.append(url)
        date.append(date1)
        text.append(body_text)
        keyfound.append(key)

def get_covid_news(url,related_url):
    source = requests.get(url).content
    soup = BeautifulSoup(source,"lxml")
    
    content = soup.find_all("div",class_ = "content-article-wrap")
    headline = soup.find('h1').text
    date1 = soup.find("span",class_="publish-date").text.strip("n\n")
    related_article = False
    body_text = content[0].text.replace('\n',' ').replace('\r','').replace("\xa0"," ")
    key = ['nCov', 'virus', 'Virus', 'coronavirus', 'Coronavirus', 'wuhan', 'Wuhan', '2019-ncov','covid','covid-19']
    for keyword in key:
        if keyword in headline.lower():
            related_article = True
        if keyword in body_text.lower():
            related_article = True
    if related_article :
        related_url.append(url)

def process_data(title,url_keep,date,text,keyfound):
    dataframe = pd.DataFrame()
    dataframe["headline"] = title[1:]
    dataframe["url"] = url_keep[1:]
    dataframe["date"] = date[1:]
    dataframe["text"] = text[1:]
    dataframe["keywords"] = keyfound[1:]
    return dataframe


#scraping via covid 19 tag and searching headlines and body text for mental health keywords
path = "C:\Program Files\chromedriver.exe"
url = "https://mothership.sg/tag/covid-19/"

driver = webdriver.Chrome(path)
driver.get(url)


while True:
    try:
        load = driver.find_element_by_id("load-stories")
        load.click()
        sleep(1)
    except Exception as e:
        print("complete")
        break
sleep(3)

urls_1 = []


for div in driver.find_elements_by_class_name('ind-article'):
    for a in div.find_elements_by_tag_name('a'):
        if "mothership.sg" in a.get_attribute("href"):
            print(a.get_attribute("href"))
            urls_1.append(a.get_attribute("href"))
driver.close()
urls_1

related_urls_1 = []
for url in urls_1:
    get_covid_news(url,related_urls_1)
related_urls_1

keyword = []
with open('Mental health kw.txt', 'r') as text:
    keyword.extend(text.readlines())
keywords = [k.strip("\n") for k in keyword]
keywords
for keyword in keywords :
    print(keyword)

title = []
url_keep = []
date = []
text = []
keyfound = []
for url in related_urls_1:
    get_data(url,keywords,title,url_keep,date,text,keyfound)

url_keep

d1 = process_data(title,url_keep,date,text,keyfound)
d1

url_1 = "https://mothership.sg/search/?s=covid+"

path = "C:\Program Files\chromedriver.exe"

url_search = []
for key in keywords:
    driver = webdriver.Chrome(path)
    driver.get(url_1 + key)



    while True:
        try:
            load = driver.find_element_by_id("load-more")
            load.click()
            sleep(1)
        except Exception as e:
            break
    sleep(3)


    for div in driver.find_elements_by_class_name('ind-article'):
        for a in div.find_elements_by_tag_name('a'):
            if "mothership.sg" in a.get_attribute("href"):
                print(a.get_attribute("href"))
                url_search.append(a.get_attribute("href"))
    
    driver.close()
 
print("all done")


keywords2 = ["singapore"]
related_urls_2 =[]
for url in url_search:
    get_data(url,keywords2,[],related_urls_2,[],[],[])

title1 = []
url_keep1 = []
date1 = []
text1 = []
keyfound1 = []
for url in related_urls_2:
    get_data(url,keywords,title1,url_keep1,date1,text1,keyfound1)
d2 = process_data(title1,url_keep1,date1,text1,keyfound1)


#scraping through search mental health then finding covid keywords
url_2 = "https://mothership.sg/search/?s=mental+health"

path = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get(url_2)

url_mental = []

while True:
    try:
        load = driver.find_element_by_id("load-more")
        load.click()
        sleep(1)
    except Exception as e:
        print("complete")
        break
sleep(3)



for div in driver.find_elements_by_class_name('ind-article'):
    for a in div.find_elements_by_tag_name('a'):
        if "mothership.sg" in a.get_attribute("href"):
            print(a.get_attribute("href"))
            url_mental.append(a.get_attribute("href"))
driver.close()
url_mental


title2 = []
url_keep2 = []
date2 = []
text2 = []
keyfound2 = []

related_urls_3 = []
for url in url_mental:
    get_covid_news(url,related_urls_3)
related_urls_3

for url in related_urls_3:
    get_data(url,keywords,title2,url_keep2,date2,text2,keyfound2)
d3 = process_data(title2,url_keep2,date2,text2,keyfound2)
d3

path = 'Mothership_scrapings.xlsx'

with pd.ExcelWriter(path) as writer:
    d1.to_excel(writer, sheet_name='sheet1')
    d2.to_excel(writer, sheet_name='sheet2')
    d3.to_excel(writer, sheet_name='sheet3')

