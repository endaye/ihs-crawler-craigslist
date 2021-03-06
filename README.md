# crawler-craigslist
A **crawler** for searching housing info on Craigslist.org
-------------------------------

1. Basic Info

	* Author: Yuancheng Zhang
	* Date: June 24, 2015
	* System: Windows 7, Python 3.4.3
	* IDE: PyCharm [Community Edition]
	* Package: Requests, BeautifulScraper(or urllib2, BeautifulSoup)
	* On Server: /opt/data/PRJ/Crawler_Craigslist
	* On Windows Server(140.x.x.194): F:\Work_Share\Craig_Daily_Download
	* Github: [github.com/vmvc2v/crawler-craigslist](https://github.com/vmvc2v/crawler-craigslist)

2. Description

    * This program is used for searching and copying housing info of **Chicago** area from **Craigslist.org** website.
    * It runs automatically at **1 a.m. everyday** on IHS windows server.
    * All output files need to upload to Linux server manually.

2. Goal

	* Target URL: [chicago.craigslist.org/search/hhh](chicago.craigslist.org/search/hhh)
	* Target area: title and posting info

3. Output file

    * Data file
        * **CRAIGYYYYMMDD_ALL.txt** has all items downloaded each day. 'YYYYMMDD' is the date when the code is running.
        * **CRAIGYYYYMMDD_7D.txt** has items posted within a week (not include the present day because the code runs at 1 a.m.)
    * Output format
        * Separator is '**tab**'
        * **Varialbe list** is [id, price, bed_tag, bed_title, bath_title, area, addr_map, addr_title, time, title, desc]
        * id: 10-digit pin (primary key)
        * price: posted price
        * bed_tag: bedroom number crawled from item tag
        * bed_title: bedroom number taken from title context
        * bath_title: bathroom number taken from title context
        * area: house area
        * addr_map: house address crawled from map tag (most items are NULL)
        * addr_title: house address taken from title context
        * time: posted time
        * title: title of items
        * desc: detail information of items
    * Log
        * **crawler_YYYYMMDD.log** is daily log file.

4. Setup
    * Step 1: Download and install [**Python 3**](https://www.python.org/downloads/)
        * ![Download and install Python 3](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/01.PNG?raw=true)
    * Step 2: Download and install Python IDE [**PyCharm** [Community Edition]](https://www.jetbrains.com/pycharm/download/)
        * Instruction: [Installing PyCharm](https://www.jetbrains.com/pycharm-educational/quickstart/installation.html) [[Video]](https://www.youtube.com/watch?v=-s4wKoLO520)
        * ![Download and install PyCharm](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/02.PNG?raw=true)
    * Step 3: Download crawler code from [**github.com/vmvc2v/crawler-craigslist**](https://github.com/vmvc2v/crawler-craigslist)
        * Clone the code or just download in zip file
        * ![Download code](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/03.PNG?raw=true)
    * Step 4: Import packages in PyCharm
        * Instruction [[Video]](https://www.youtube.com/watch?t=156&v=XjNm9bazxn8)
        * Click menu "**File**" -> "**Settings...**", "**Project: crawler-craigslist**" -> "**Project Interpreter**", choose 3.4.3 or later
        * ![Choose interpreter](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/04.PNG?raw=true)
        * Click ":heavy_plus_sign:" button to add "**beautifulscraper**" and "**requests**" these two packages, and install them.
        * ![install two packages](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/05.PNG?raw=true)
        * After all, click "**OK**" to finish setting parts.
    * Step 5: Run the code
        * Click menu "**Run**" -> "**Run...**", or right click ":arrow_forward:**Run 'crawler'**" in crawler.py file editor

5. Extra: Make it auto run at 1 a.m. everyday on Windows server(Windows XP)
    * Log in Windows server (by Windows Desktop)
    * Set up everything as Step 1 to 5
    * Add a batch file named as "crawler_daily.bat" or something
    * ![Batch file](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/06.PNG?raw=true)
    * Add this code into batch file as below
    ```
    C:\Python34\python.exe "F:\Work_Share\Craig_Daily_Download\crawler.py" >> crawler_latest_log.txt
    ```
    * Create a new Windows scheduled task
    * ![scheduled tast](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/07.png?raw=true)
    * ![new tast](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/08.PNG?raw=true)
    * Click "**Next**"
    * ![welcome page](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/09.PNG?raw=true)
    * Click "**Browse...**", choose "**crawler_daily.bat**", and click "**Next**"
    * ![choose batch](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/10.PNG?raw=true)
    * Type a **name** for the task and choose "**Daily**" as performance
    * ![task name](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/11.PNG?raw=true)
    * Set performing this task at 1:00 a.m. every day
    * ![time](https://github.com/vmvc2v/crawler-craigslist/blob/master/doc/img/12.PNG?raw=true)
    * Click "**Next**"s to "**Finish**", all set.
