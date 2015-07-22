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

%LET proj = C:\Users\yzhang96\Google Drive\DePaul Work\crawler-craigslist\;

libname f	"&proj.dataset\7d\";
libname ds_7d	"&proj.dataset\7d\";

%LET raw_all = &proj.daily_download\all_download\;
%LET update_num = 0;


%macro ls_7d();
	*list of 7-day txt files;
	filename ls_txt_7 pipe 'dir "C:\Users\yzhang96\Google Drive\DePaul Work\crawler-craigslist\daily_download\7_days\*.txt"';
	data ls_txt_7;
	infile ls_txt_7 truncover;
	input raw $120.;
	is_file = findw(raw, "txt"); 
	if is_file > 0;
	fname = upcase(substr(raw, is_file-17, 16));
	if substr(fname,1,5) = "CRAIG";
	drop raw is_file;
	run;

	*list of 7-day dataset ; 
	filename ls_ds_7 pipe 'dir "C:\Users\yzhang96\Google Drive\DePaul Work\crawler-craigslist\dataset\7d\*.sas7bdat"';
	data ls_ds_7;
	infile ls_ds_7 truncover;
	input raw $120.;
	is_file = findw(raw, "sas7bdat"); 
	if is_file > 0;
	fname = upcase(substr(raw, is_file-17, 16));
	if substr(fname,1,5) = "CRAIG";
	drop raw is_file;
	run;

	data up_7;
	merge ls_txt_7(in=a) ls_ds_7(in=b);
	by fname;
	ab=cats(a,b);
	if ab = '10';
	drop ab;
	run;

	data _NULL_;
	set up_7;
	call symputx('update_num', _N_);
	call symput(cats('update_',_N_), fname);
	%put ~~~~~~~~~~~~ &update_num FILE(S) NEED TO INPUT ~~~~~~~~~~~~;
	run;
%mend ls_7d;

%macro import_single_7d(fname);
	proc import
	%put ~~~~~~~~~~~~ INPUT &fname ~~~~~~~~~~~~;
	datafile = "&proj.daily_download\7_days\&fname..txt"
	out = tmp
	DBMS = dlm
	replace;
	delimiter='09'x;
	run;

	data ds_7d.&fname.;
	set tmp;
	drop VAR12;
	run;
%mend import_single_7d;

%macro import_all_7d();
	%if &update_num = 0 %then %do;
		%put "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";
		%put "                WARNING: TXT Importing Skipped, No Update Available                 ";
		%put "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";
	%end;
	%else %do;
		%do p = 1 %to &update_num.;
			%import_single_7d(&&update_&p..);
		%end;
	%end;
%mend import_all_7d;




%macro main();
	*%ls_all();
	%ls_7d();
	%import_all_7d();
%mend main;

%main();