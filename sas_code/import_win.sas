/*************************************************************************
Import Craigslist text files on SAS server
Step 0:	Upload text files from Windows server to SAS server
Step 1:	
Step 2:	
Step 3:	
Date:	July 15, 2015
Author:	Yuancheng Zhang
SAS server:	/opt/data/PRJ/Crawler_Craigslist/sas_code/
Github:		github.com/vmvc2v/crawler-craigslist
*************************************************************************/

/*************************************************************************
To run this code:
"C:\Program Files (x86)\SASHome\x86\SASFoundation\9.3\sas.exe" -sysin "C:\Users\yzhang96\Google Drive\DePaul Work\crawler-craigslist\sas_code\import_win.sas" -CONFIG "C:\Program Files (x86)\SASHome\x86\SASFoundation\9.3\nls\en\sasv9.cfg"
*************************************************************************/

option compress = yes;

libname f	"C:\Users\yzhang96\Google Drive\DePaul Work\crawler-craigslist\dataset\7d\";
libname ds_7d	"C:\Users\yzhang96\Google Drive\DePaul Work\crawler-craigslist\dataset\7d\";

%LET raw_all = C:\Users\yzhang96\Google Drive\DePaul Work\crawler-craigslist\daily_download\all_download\

proc import
datafile = "C:\Users\yzhang96\Google Drive\DePaul Work\crawler-craigslist\daily_download\7_days\CRAIG20150710_7D.txt"
out = a
DBMS = dlm
replace
delimiter='09'x;
run;

data ds_7d.CRAIG20150710_7D;
set a;
drop VAR12;
run;

filename ls_txt ("C:\Users\yzhang96\Google Drive\DePaul Work\crawler-craigslist\dataset\7d\*.*");
data new;
infile ls_txt;
input;
run;