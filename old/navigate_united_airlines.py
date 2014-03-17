from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import urllib2
import random
import sys
from bs4 import BeautifulSoup
url="http://www.united.com"
path=[]
browser=webdriver.Firefox()
browser.get(url)

"""page = urllib2.urlopen(url).read()

soup = BeautifulSoup(page,"html.parser")
soup.prettify()

list_of_urls=[]
allDivs=soup.findAll("li",attrs={"id":"navDeals"})
for div in allDivs:
    a_div=div.find('a')['href']
    list_of_urls.append(a_div)
for urls in list_of_urls:
    print url
"""
browser.get("http://www.united.com/CMS/en-US/content/deals/offers/Pages/SpecialOffers.aspx")
url="http://www.united.com/CMS/en-US/content/deals/offers/Pages/SpecialOffers.aspx"
path.append(url)
print path
page = urllib2.urlopen(url).read()

soup = BeautifulSoup(page,"html.parser")
soup.prettify()

list_of_urls=[]
allDivs=soup.findAll("div",attrs={"id":"WebPartWPQ3"})
for div in allDivs:
    a_div=div.findAll('a')
    for urls in a_div:
        list_of_urls.append(urls['href'])
selected_url=random.choice(list_of_urls)
url="http://www.united.com"+selected_url
path.append(url)
print path
browser.get(url)
page = urllib2.urlopen(url).read()

soup = BeautifulSoup(page,"html.parser")
soup.prettify()


list_of_urls=[]
#abc=soup.findAll("table")
abc=soup.findAll("table",attrs={"class":"seasonal"})
for b in abc:
    links=b.findAll("td",attrs={"class","fare"})
    for l in links:
        list_of_urls.append(l.a['href'])
selected_url=random.choice(list_of_urls)
url="http://www.united.com"+selected_url
path.append(url)
print path
browser.get(url)
page = urllib2.urlopen(url).read()

soup = BeautifulSoup(page,"html.parser")
soup.prettify()
abc=soup.findAll("table",attrs={"class":"Calendar"})
for b in abc:
    links=b.findAll("td",attrs={"class","on"})
    for l in links:
        list_of_urls.append(l.a['href'])
        for x in list_of_urls:
            print x
selected_url=random.choice(list_of_urls)
print "Selected url is!!!"+selected_url
#url="http://www.united.com/web/en-US/apps/booking/flight/"+selected_url
url="http://www.united.com/web/en-US/apps/booking/flight/searchRT.aspx?SID=F2E0038065DB4318A8BFA141B77CA7B7&BRV=0&FL=1&AL=AD&DD=8/13/2013&RD=8/20/2013&BSK=Q8oxANkXXx8O3INLs5mLxB002&SX=0YAUXpGilW50VGIdsnqFRVV"
path.append(url)
print path
browser.get(url)
page = urllib2.urlopen(url).read()

soup = BeautifulSoup(page,"html.parser")
soup.prettify()


#print abc
