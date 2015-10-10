__author__ = 'Yuancheng Zhang'
__date__ = '2015-06-24'

import requests
import pickle
import re
import datetime
from bs4 import BeautifulSoup
import os.path

# static variable
TODAY = str(datetime.date.today()).replace("-", "")
PATH = r".\\daily_download\\"
OUT_FILE_ALL = PATH + r"all_download\\" + "CRAIG" + TODAY + r"_ALL" + r".txt"
OUT_FILE_7D = PATH + r"7_days\\" + "CRAIG" + TODAY + r"_7D" + r".txt"

found_cnt = 0
skip_cnt = 0
download_cnt = 0
save_cnt_all = 0
save_cnt_7d = 0

PAGE_MAX = 25  # Max 25
DEBUG_MODE = False


def crawler(max_pages):
    global found_cnt
    global skip_cnt
    page = 1
    house_list = []
    # scrape the searching pages one by one
    while page <= max_pages:
        cnt = 0
        # 100 items per page, max 25 pages
        if page is 1:
            url = 'http://chicago.craigslist.org/search/apa'
        else:
            url = 'http://chicago.craigslist.org/search/apa?s=' + str((page - 1) * 100)
        print("[DOWNLOAD]Page: " + str(page) + ": " + url)

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
            found_cnt += 1

            # if the id has been scraped, skip it.
            if id in house_list:
                print("[DOWNLOAD]" + 'ID #' + str(id) + " already exist, skip to next.\n")
                skip_cnt += 1
                continue

            print("[DOWNLOAD]" + 'ID #' + str(id) + " is downloading...")

            # log title, accumulate the counter
            title = clean(link.string)
            log('#' + str(cnt), 'ID #' + str(id), title)
            log('#' + str(cnt), href)

            # scrape data on the item page. 'house' is a info list.
            get_single_house_data(href)

            # add the item info into house list for all download. 'house_list' type is dictionary.
            house_list.append(id)

            print("[DOWNLOAD]" + 'ID #' + str(id) + " download finished.\n")

            # DEBUG: uncomment 'break'; only show 5 items
            if cnt > 5:
                # break
                pass
        page += 1


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
        log("Bath_title:\t" + str(bath_num))
        bath_title = bath_num

    house = [id, price, bed_tag, bed_title, bath_title, area, addr_map, addr_title, time, title, desc]
    global download_cnt
    download_cnt += 1
    save_in_file(house, OUT_FILE_ALL)

    # parse the post date
    post_date = house[-3]

    # convert string to date obj
    # http://stackoverflow.com/questions/466345/converting-string-into-datetime
    date_obj = datetime.datetime.strptime(post_date, '%Y-%m-%d').date()

    # add the item info into house list of last week. save it in 'house_list_7d'.
    if date_filter(date1=date_obj):
        save_in_file(house, OUT_FILE_7D)

    # return house


def save_in_file(house, filename):
    fw = open(filename, 'a')
    for item in house:
        fw.write(str(item) + '\t')
    fw.write('\n')
    fw.close()
    print("[SAVE]ID #" + str(house[0]) + " is saved in " + filename)
    if filename == OUT_FILE_ALL:
        global save_cnt_all
        save_cnt_all += 1
    if filename == OUT_FILE_7D:
        global save_cnt_7d
        save_cnt_7d += 1


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


# write log, or print(optional)
def log(*args):
    out = ''
    for s in args:
        out = out + '[DEBUG]Detail: ' + str(s) + ' '
    # DEBUG: pls uncomment this line (print logs in console)
    if DEBUG_MODE:
        print(out)


# Load and save a dictionary into a file
# https://wiki.python.org/moin/UsingPickle
def main():
    # start running
    start = datetime.datetime.now()
    print("[TIME]START time: \t" + str(start) + '\n')

    # check the file exist
    exist_all = os.path.isfile(OUT_FILE_ALL)
    exist_7d = os.path.isfile(OUT_FILE_7D)
    if exist_all:
        size_all = os.path.getsize(OUT_FILE_ALL)
    if exist_all and size_all > 2 * 1024 * 1024:
        # 2MB
        # skip download process
        print("[FILE]" + OUT_FILE_ALL + "\nThe file has existed (size " + size_all + "). Do not need update again.")
    else:
        print("[FILE]" + OUT_FILE_ALL)
        print("[FILE]The file does not exist or its size is less 2M available.")
        print("[FILE]Create a new one to update.\n")

        # 100 items per page, max search page number is 25
        pages = PAGE_MAX
        print("[PAGE]Target pages to download: " + str(pages) + '.\n')

        # create a empty house dict for the last week
        last_week = [str(datetime.date.today() - datetime.timedelta(days=7)),
                     str(datetime.date.today() - datetime.timedelta(days=1))]
        print("[TIME]7 days range is from " + last_week[0] + " to " + last_week[1] + '.\n')

        # read file title.
        fw = open(OUT_FILE_ALL, 'w')
        fw.write("id\tprice\tbed_tag\tbed_title\tbath_title\tarea\taddr_map\taddr\ttitle\ttime\tdesc\t\n")
        fw.close()
        fw = open(OUT_FILE_7D, 'w')
        fw.write("id\tprice\tbed_tag\tbed_title\tbath_title\tarea\taddr_map\taddr\ttitle\ttime\tdesc\t\n")
        fw.close()
        print("[SAVE]File titles written.\n")

        # start this crawler
        print("[DOWNLOAD]Crawler starts ... \n")
        crawler(pages)
        print("[DOWNLOAD]Crawler finished.\n")

        # log summary of data
        print("[DOWNLOAD]Found: \t\t" + str(found_cnt) + "\titems.")
        print("[DOWNLOAD]Download: \t" + str(download_cnt) + "\titems.")
        print("[DOWNLOAD]Skip: \t\t" + str(skip_cnt) + "\titems.")
        if found_cnt - download_cnt == skip_cnt:
            print("[VERIFY]Download part PASSED.\n")
        else:
            print("[VERIFY]Download part FAILED!!!!! Please check the code!\n")

        # verify all
        print("[ALL]OUTPUT: " + str(save_cnt_all) + " items have been saved.")
        print("[ALL]FILE PATH: " + OUT_FILE_ALL)
        print("[ALL]SIZE: " + str(os.path.getsize(OUT_FILE_ALL)) + ' (' +
              str(os.path.getsize(OUT_FILE_ALL) >> 10) + 'KB)')
        if download_cnt == save_cnt_all:
            print("[ALL][VERIFY]Items number part PASSED.")
        else:
            print("[ALL][VERIFY]Items number part FAILED!!!!! Please check the output file!")
        if os.path.getsize(OUT_FILE_ALL) > 1024:
            print("[ALL][VERIFY]Size part PASSED.\n")
        else:
            print("[ALL][VERIFY]Size part FAILED!!!!! Please check the output file!\n")

        # verify 7d
        print("[7D]OUTPUT: " + str(save_cnt_7d) + " items have been saved.")
        print("[7D]FILE PATH: " + OUT_FILE_7D)
        print("[7D]SIZE: " + str(os.path.getsize(OUT_FILE_7D)) + ' (' +
              str(os.path.getsize(OUT_FILE_7D) >> 10) + 'KB)\n')

    # log summary of time
    end = datetime.datetime.now()
    print("[TIME]START: \t", str(start))
    print("[TIME]END: \t\t", str(end))
    print("[TIME]USED: \t", str(end - start) + '\n')


main()
