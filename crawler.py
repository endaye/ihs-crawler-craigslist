__author__ = 'Yuancheng Zhang'
__date__ = '2015-06-24'

import requests
import pickle
import re
import datetime
from bs4 import BeautifulSoup

def house_spider(max_pages, housing):
    page = 1
    cnt = 0
    while page <= max_pages:
        if page is 1:
            url = 'http://chicago.craigslist.org/search/apa'
        else:
            url = 'http://chicago.craigslist.org/search/apa?s=' + str((page - 1) * 100)
        print("Page: " + str(page) + ": " + url)
        source_code = requests.get(url)
        plain_text = source_code.text  # convert source code into plain text
        soup = BeautifulSoup(plain_text)  # create a BeautifulSoup obj
        for link in soup.findAll('a', {'class': 'hdrlnk'}):
            # get all link with class "hdrlnk"
            href = "http://chicago.craigslist.org" + link.get('href')
            id = get_id(href)
            if id in housing:
                print('ID #' + str(id) + " already exist!\n")
                continue
            title = clean(link.string)
            print('#' + str(cnt), 'ID #' + str(id), title)
            print('#' + str(cnt), href)
            cnt += 1
            house = (get_single_house_data(href))
            housing[id] = house
            print('\n')

            if cnt > 1:  # debug
                # break
                pass
        page += 1

    return cnt

def get_single_house_data(house_url):
    source_code = requests.get(house_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    # ID
    id = get_id(house_url)
    print('ID: \t', id)

    # Title
    tag = soup.find('span', {'class': 'postingtitletext'})
    try:
        title = clean(tag.getText())
    except AttributeError:
        title = 'NULL'
    print('Title:\t', title)

    # Price
    tag = soup.find('span', {'class': 'price'})
    try:
        price = clean(tag.getText())
    except AttributeError:
        price = 0
    print("Price:\t", price)

    # Bedroom Numbers, default is Zero.
    bedroom = '0br'
    area = '0ft2'
    tag = soup.find('span', {'class': 'housing'})
    try:
        info = clean(tag.getText()).split()
        for x in info:
            if x[-2:] == 'br':
                bedroom = x
            if x[-3:] == 'ft2':
                area = x
    except AttributeError:
        pass
    print("Bedroom:\t", bedroom)

    # Address on map
    tag = soup.find('div', {'class': 'mapaddress'})
    try:
        addr = clean(tag.getText())
    except AttributeError:
        addr = 'NULL'
    print('Address:\t', addr)

    # Post Time
    tag = soup.find('time')
    time = tag['datetime'][:10]
    print('Post time:\t', time)

    # Details
    tag = soup.find('section', {'id': 'postingbody'})
    try:
        desc = clean(tag.getText())
    except AttributeError:
        desc = 'NULL'
    print('Description:\t', desc)

    house = [id, price, bedroom, area, addr, time, title, desc]

    return house

def clean(str0):
    str1 = remove_non_ascii(str0)
    str2 = re.sub('[\[\]/{}\n\-\t\*!.,]+', ' ', str1)
    str3 = re.sub('[ ]+', ' ', str2.strip())
    return str3

# Stackoverflow.com "Replace non-ASCII characters with a single space"
# http://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space
def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

# get id from link
def get_id(href):
    return int(href.split('/')[-1].split('.')[0])

# print a dictionary
def print_dict(dict):
    for x in dict:
        print(x, ':', dict[x])

# save the dictionary file as a txt file
def save_txt(file_name, housing):
    fw = open(file_name + r'.txt', 'w')
    for x in housing:
        # fw.write(str(x)+'\t')
        for y in housing[x]:
            fw.write(str(y)+'\t')
        fw.write('\n')
    fw.close()

# Load and save a dictionary into a file
# https://wiki.python.org/moin/UsingPickle
def main():

    file_name = str(datetime.date.today()).replace("-", "")
    pages = 1
    try:
        housing = pickle.load(open(file_name + r'.p', "rb"))
    except FileNotFoundError:
        housing = {}
    housing = {}  # debug: create a new empty dict
    print(housing)
    add = house_spider(pages, housing)
    pickle.dump(housing, open(file_name + r'.p', "wb"))
    save_txt(file_name, housing)
    # print_dict(housing)
    print(str(add) + " items added into the list \n" +
          "total " + str(len(housing)) + " items in the list \n" +
          str(datetime.datetime.now()))
    print(a)
main()
