General:
- move_content script: is used to move movies and series automatically to the corresponding folder
- scrape_hdarea script: is used to scrape hdarea for new movies/series and to add them automatically to pyload

Installation:
1. copy scrape.py to your local computer (wget https://raw.githubusercontent.com/mhemmi/scrape_hdarea_org/master/scrape.py)
2. edit config of scrape.py (see manual below)
3. copy move_content.py to your local computer (wget https://raw.githubusercontent.com/mhemmi/scrape_hdarea_org/master/move_content.py)
4. edit config of move_content.py (see manual below)
5. create cronjob for srape.py (crontab -e) [e.g.: */10 * * * * /usr/bin/python /your/path/scrape.py] << runs every 10 minutes
6. create a shell script in your pyloadconfig-folder: ..scripts/all_archives_processed/move_content.sh with content of 2 lines:
  #!/bin/bash
  /usr/bin/python /your/path/to/move_content.py
  #this file was downloaded in step 3 and edited in step 4
7. activate external scripts for pyload (config > plugins > ExternalScripts)
   Execute script concurrently: No
   Activated: Yes
8. Have fun with these scripts.
9. Errors? Please report.
  
User manual:
1. edit scrape.py config - (above is an example):
  movierating = 7.1
  serierating = 7.4
  moviequality = re.escape('1080') #720 or more means hd, 1080 or more means full-hd, 2160 or more means uhd
  seriequality = re.escape('720')
  year = "2018"
  databasefile = '/home/database.json' #WHERE IS YOUR DATABASE or where to store the file? If there is no one the script will create one
  pyload = "/opt/pyload/pyLoadCli.py>" #path to pyloadCLI
  #MAILING STUFF
  senderEmail = "my@mail.com" #from whom comes the mail?
  empfangsEmail = "receiver@mail.com" #who gets the mail?
  server = smtplib.SMTP('mail.com', 587) 
  password = 'your-password'
  
2. edit move_content.py
  dlfolder = '/your/path/of/extracted/files' #absolut path of your files which are extracted!
  moviefolder = '/your/path/to/your/movie/folder' 
  seriefolder = '/your/path/to/your/series/folder'
  videoregex = '\.mkv|\.iso' #you can add with | \.<new ending>
  cancelregex = '\.mp3|\.wave' #you can add with |\.<new ending> #this is a regex which files must not touched 
  !!!ALL OTHER FILES IN YOUR 'DLFOLDER' WILL BE DELETED!!!
