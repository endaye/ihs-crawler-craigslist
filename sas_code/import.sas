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

option compress = yes;

libname f	"./";
libname all_in	"../daily_download/all_download/";
libname 7d_in	"../daily_download/7_days/";
libname all_out	"../dataset/all/";
libname 7d_in	"../dataset/7d/";


/*****************************/
/* Step 0:	Upload text files from Windows server to SAS server*/
/*****************************/
data f.a;
infile "../daily_download/all_download/"