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
libname in_all	"../daily_download/all_download/";
libname in_7d	"../daily_download/7_days/";
libname out_all	"../dataset/all/";
libname out_7d	"../dataset/7d/";

%LET in_all	= 	../daily_download/all_download/;
%LET in_7d	= 	../daily_download/7_days/;
%LET out_all = 	../dataset/all/;
%LET out_7d	= 	../dataset/7d/;


/*****************************/
/* Step 0:	Upload text files from Windows server to SAS server*/
/*****************************/

data out_all.CRAIG20150710_ALL;
infile "../daily_download/all_download/CRAIG20150710_ALL.txt" dlm='09'x dsd truncover;
input id price bed_tag bed_title bath_title area addr_map $1-60 addr_title $ time $ title $ desc $;
run;

data out_7d.CRAIG20150710_ALL;
infile "../daily_download/7_days/CRAIG20150712_ALL.txt" dlm='09'x dsd truncover;
input id price bed_tag bed_title bath_title area addr_map $1-60 addr_title $ time $ title $ desc $;
run;


filename ls_d_a pip ""