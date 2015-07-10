__author__ = 'Yuancheng Zhang'
__date__ = '2015-06-24'

import requests
import pickle
import re
import datetime
import logging
from bs4 import BeautifulSoup

# static variable
TODAY = str(datetime.date.today()).replace("-", "")
LOG_FILENAME = r'crawler_' + TODAY + r'.log'
OUT_FILE_ALL = "CRAIG" + TODAY + r"_ALL" + r".txt"
OUT_FILE_7D = "CRAIG" + TODAY + r"_7D" + r".txt"
PAGE_MAX = 25  # Max 25


def house_spider(max_pages, house_list, house_list_7d):
    page = 1

    # counter: [0] for house_list_all; [1] for house_list_7d
    cnt = 0

    # scrape the searching pages one by one
    while page <= max_pages:

        # 100 items per page, max 25 pages
        if page is 1:
            url = 'http://chicago.craigslist.org/search/apa'
        else:
            url = 'http://chicago.craigslist.org/search/apa?s=' + str((page - 1) * 100)
        log("Page: " + str(page) + ": " + url)

        # prepare for parse
        source_code = requests.get(url)  # get the html file
        plain_text = source_code.text  # convert source code into plain text
        soup = BeautifulSoup(plain_text)  # create a BeautifulSoup obj

        # find and scrape item links
        for link in soup.findAll('a', {'class': 'hdrlnk'}):

            # get all link with class "hdrlnk"
            href = "http://chicago.craigslist.org" + link.get('href')
            id = get_id(href)

            # get a url, counter +1
            cnt += 1

            # if the id has been scraped, skip it.
            if id in house_list:
                log('ID #' + str(id) + " already exist!\n")
                continue

            # log title, accumulate the counter
            title = clean(link.string)
            log('#' + str(cnt), 'ID #' + str(id), title)
            log('#' + str(cnt), href)

            # scrape data on the item page. 'house' is a info list.
            house = (get_single_house_data(href))

            # add the item info into house listfor all download. 'house_list' type is dictionary.
            house_list[id] = house
            log('ID #' + str(id) + " has been added in house list of all download today.")
            log("Ready to save in " + OUT_FILE_ALL + " file.\n")

            # parse the post date
            post_date = house[-3]

            # convert string to date obj
            # http://stackoverflow.com/questions/466345/converting-string-into-datetime
            date_obj = datetime.datetime.strptime(post_date, '%Y-%m-%d').date()

            # add the item info into house list of last week. 'house_list_7d' type is dictionary.
            if date_filter(date1=date_obj):
                house_list_7d[id] = house
                log('ID #' + str(id) + " has been added in house list of last week items.")
                log("Ready to save in " + OUT_FILE_7D + " file.\n")

            # DEBUG: uncomment 'break'; only show 5 items
            if cnt > 5:
                # break
                pass
        page += 1

    return cnt


# filter items within a week
# date1: post date
# date2: current date
# delta: the threshold of difference between these two dates
def date_filter(date1, date2=datetime.date.today(), delta=7):
    # the difference between date1 and date2
    diff = date2 - date1

    # remove current date items, because this code will run at 1:00 AM everyday
    if diff <= datetime.timedelta(days=0):
        return False

    # choose those item posted in this certain period
    if diff <= datetime.timedelta(days=delta):
        return True

    return False


def get_single_house_data(house_url):
    # html file
    source_code = requests.get(house_url)
    # convert html to plain text
    plain_text = source_code.text
    # create a B4S obj
    soup = BeautifulSoup(plain_text)

    # ID
    id = get_id(house_url)
    log('ID: \t', id)

    # Title
    tag = soup.find('span', {'class': 'postingtitletext'})
    try:
        title = clean(tag.getText())
    except AttributeError:
        title = 'NULL'
    log('Title:\t', title)

    # Price
    tag = soup.find('span', {'class': 'price'})
    try:
        price_text = clean(tag.getText())
        price = re.search("[0-9]+", price_text).group(0)
    except AttributeError:
        price = '0'
    log("Price:\t" + price)

    # Bedroom Numbers, default is Zero.
    bedroom = '0'
    area = '0'
    tag = soup.find('span', {'class': 'housing'})
    try:
        info = clean(tag.getText()).split()
        for x in info:
            if x[-2:] == 'br':
                bedroom = x[:-2]
            if x[-3:] == 'ft2':
                area = x[:-3]
    except AttributeError:
        pass
    finally:
        bed_tag = bedroom
    log("Bed_tag:\t" + bedroom)
    log("Area(ft2):\t" + area)

    # Address on map
    tag = soup.find('div', {'class': 'mapaddress'})
    try:
        addr_map = clean(tag.getText())
    except AttributeError:
        addr_map = 'NULL'
    finally:
        log('Address_map:\t', addr_map)

    # Address from title
    try:
        addr_title_raw = re.search("\((.*)\)", title).group(1)
        addr_title = re.sub("[^A-Za-z0-9 ]+", '', addr_title_raw)
    except AttributeError:
        addr_title = 'NULL'
    finally:
        log('Address_title:\t', addr_title)

    # Post Time
    tag = soup.find('time')
    try:
        time = tag['datetime'][:10]
    except TypeError:
        time = '0000-00-00'
    finally:
        log('Post time:\t', time)

    # Details
    tag = soup.find('section', {'id': 'postingbody'})
    try:
        desc = clean(tag.getText())
    except AttributeError:
        desc = 'NULL'
    log('Description:\t', desc)

    # Bedroom and Bathroom numbers in Title
    # set default number as zero
    bed_num = 0
    bath_num = 0
    # pick out title text w/o tags
    tag = soup.find('span', {'class': 'postingtitletext'})
    [s.extract() for s in soup('span')]
    try:
        title_text = clean(tag.getText())
    except AttributeError:
        title_text = 'NULL'
    # if match 'studio', set bdrm and bathrm numbers as 1
    studio_t = re.search("studio", title_text.lower())
    if studio_t is not None:
        bed_num = 0
        bath_num = 1
    # convert English number into digit
    num_dict = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
                'ten': 10}
    # regular express of number parts
    num_re = "([1-9]|one|two|three|four|five|six|seven|eight|nine|ten)( )?"
    # regular express of bedroom parts
    bed_re = "(bedrooms|bedroom|bedrm|bed|br|bd|bdrm)"
    # regular express of bathroom parts
    bath_re = "(bathrooms|bathroom|bathrm|baths|bath|ba|bthroom|bthrm)"
    # the searching results of regex
    bed_text = re.search(num_re + bed_re, title_text.lower())
    bath_text = re.search(num_re + bath_re, title_text.lower())
    # change text to digit (bedroom parts)
    try:
        bed_num_raw = re.split('b', bed_text.group())[0].strip()
        bed_num = int(bed_num_raw)
    except AttributeError:
        bed_num = 0
    except ValueError:
        if bed_num_raw in num_dict:
            bed_num = num_dict[bed_num_raw]
        else:
            bed_num = 0
    finally:
        log("Bed_title:\t" + str(bed_num))
        bed_title = bed_num
    # change text to digit (bathroom parts)
    try:
        bath_num_raw = re.split('b', bath_text.group())[0].strip()
        bath_num = int(bath_num_raw)
    except AttributeError:
        bath_num = 0
    except ValueError:
        if bath_num_raw in num_dict:
            bath_num = num_dict[bath_num_raw]
        else:
            bath_num = 0
    finally:
        log("Bath_title:\t" + str(bath_num) + '\n')
        bath_title = bath_num

    house = [id, price, bed_tag, bed_title, bath_title, area, addr_map, addr_title, time, title, desc]

    return house


def clean(str0):
    # step 1: remove non-ASCii chars
    str1 = remove_non_ascii(str0)
    # step 2&3: replace those syntax to whitespace and strip those whitespace
    str2 = re.sub('[\[\]/{}\n\-\t\*!<>#.,=]+', ' ', str1)
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
        log(x, ':', dict[x])


# save the dictionary file as a txt file
def save_txt(file_name, housing):
    fw = open(file_name, 'w')
    for x in housing:
        # fw.write(str(x)+'\t')
        for y in housing[x]:
            fw.write(str(y) + '\t')
        fw.write('\n')
    fw.close()


# create a log file
def init_log():
    logging.basicConfig(filename=r".\\log\\" + LOG_FILENAME,
                        format='%(asctime)s %(levelname)s:\t%(message)s',
                        level=logging.DEBUG)
    logging.debug("Log initialized.")


# write log, or print(optional)
def log(*args):
    out = ''
    for s in args:
        out = out + str(s) + ' '
    logging.info(out)

    # DEBUG: pls uncomment this line (print logs in console)
    print(out)


# Load and save a dictionary into a file
# https://wiki.python.org/moin/UsingPickle
def main():
    # initialized the log file
    init_log()

    # start running
    start = datetime.datetime.now()
    log("START: \t" + str(start) + '\n')

    # 100 items per page, max search page number is 25
    pages = PAGE_MAX

    # create a empty house dict for all download
    house_list = {}
    log("Created a new house list for all download today. Target pages: " + str(pages) + '.\n')

    # create a empty house dict for the last week
    house_list_7d = {}
    last_week = [str(datetime.date.today() - datetime.timedelta(days=7)),
                 str(datetime.date.today() - datetime.timedelta(days=1))]
    log("Created a new house list from " + last_week[0] + " to " + last_week[1] + '.\n')

    # start this crawler
    add = house_spider(pages, house_list, house_list_7d)

    # output file
    save_txt(r".\\daily_download\\all_download\\" + OUT_FILE_ALL, house_list)
    save_txt(r".\\daily_download\\7_days\\" + OUT_FILE_7D, house_list_7d)

    # log summary of data
    log("DOWNLOAD: \t" + str(add) + " items have been scraped. \n")
    log("for ALL: \t" + str(len(house_list)) + " items have been copied and saved in " + OUT_FILE_ALL + " file.")
    log("for 7D: \t" + str(len(house_list_7d)) + " items for last week " +
        "(from " + last_week[0] + ' to ' + last_week[1] + ") have been saved in " + OUT_FILE_ALL + " file. \n")

    # log summary of time
    end = datetime.datetime.now()
    log("START time: \t", str(start))
    log("END time: \t\t", str(end))
    log("Time used: \t\t", str(end - start) + '\n\n\n\n\n')


main()
