__author__ = 'yzhang96'

import requests
from bs4 import BeautifulSoup

def house_spider(max_pages):
    page = 1
    while page <= max_pages:
        url = 'http://chicago.craigslist.org/search/apa?s=' + str(page * 100)
        source_code = requests.get(url)
        plain_text = source_code.text  # convert source code into plain text
        soup = BeautifulSoup(plain_text)  # create a BeautifulSoup obj
        cnt = 0
        for link in soup.findAll('a', {'class': 'hdrlnk'}):
            # get all link with class "hdrlnk"
            href = "http://chicago.craigslist.org" + link.get('href')
            title = link.string
            cnt += 1
            print(cnt, title)
            # print(href)
            get_single_house_data(href)
        page += 1

def get_single_house_data(house_url):
    source_code = requests.get(house_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    for price in soup.findAll('span', {'class': 'price'}):
        print(price.string)
    for link in soup.findAll('a'):
        href = link.get('href')
        print(href)

house_spider(1)
