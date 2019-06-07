#!/usr/bin/python
############# IMPORT STUFF ##################
import urllib2,re,requests,json,subprocess,smtplib,os
from bs4 import BeautifulSoup
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

############ CONFIG ########################
movierating = 7.3 #or 7.0 or 8.9 ...
serierating = 7.9
moviequality = re.escape('2160') #720 or more means hd, 1080 or more means full-hd, 2160 or more means uhd
seriequality = re.escape('1080')
year = "2007"
databasefile = '' #WHERE IS YOUR DATABASE or where to store the file? If there is no one the script will create one
#MAILING STUFF
senderEmail = "<enter your mail address>" #from whom comes the mail?
empfangsEmail = "<enter the contact address>" #who gets the mail?
server = smtplib.SMTP('<server>', <port>) 
password = '<your password>'



### GET DATABASE ###
if(os.path.isfile(databasefile)):
        with open(databasefile) as json_file:
                database = json.load(json_file)
else:
        database = {}
        database['movie'] = []


#functions
def addSeries(tit,lnk):
        addMovie(tit,lnk) #maybe later there are changes

def addMovie(tit,lnk):
        #search if movie was already added
        for movie in database['movie']:
                if(movie['title'] == tit):
                        return #movie already added
        database['movie'].append({'title':shorttitle}) #if not found add this movie to database
        #write new database
        with open(databasefile, 'w') as outfile:
                json.dump(database, outfile)
        sendMail(tit,lnk) #send notification

def sendMail(tit,lnk):
        msg = MIMEMultipart()
        msg['From'] = senderEmail
        msg['To'] = empfangsEmail
        msg['Subject'] = "Pyload update"
        emailText = "Added: "+tit+ " via: " +lnk
        msg.attach(MIMEText(emailText, 'html'))
        server.starttls()
        server.login(senderEmail, password) #login with username and password
        text = msg.as_string()
        server.sendmail(senderEmail, empfangsEmail, text)
        server.quit()

###################### START SCRAPING ############
quote_page = 'http://hd-area.org'
page = urllib2.urlopen(quote_page)
data = requests.get(quote_page)
soup = BeautifulSoup(page, 'html.parser')
#content with links to movies and so
el = soup.findAll(class_='beschreibung') #movie/serie content
el2 = soup.findAll(class_='boxrechts') #all imdb ratings
#new soup for shortned page
soup = BeautifulSoup(str(el), 'html.parser')
#get movie/series rating
imdbs = re.findall(r'<div class="boxrechts">.*\n(.*)<',data.text) #find all imdb-ratings (requests version)
#get titles
titles = soup.findAll('input')
ind = 0 #index for imdbs
for title in titles:
        #searching for movies! not for series
        if (re.search('.*?\.\d\d\d\d\.',title.get('value')) != None and re.search('\.\d{3}p|\.\d{4}p',title.get('value')) != None):
                shorttitle = re.search('.*?\.\d\d\d\d\.',title.get('value')).group(0)[:-1] #movie title (remove last character (.)
                #get quality for movie
                if(re.search('\.\d{3}p|\.\d{4}p',title.get('value')) != None):
                        qual = str(re.search('\.\d{3}p|\.\d{4}p',title.get('value')).group(0)).replace('.','').replace('p','') #quality
                else:
                        qual = 0.0
                mediayear = str(re.search('\.\d\d\d\d\.',title.get('value')).group(0)).replace('.','') #year of movie
                if(re.search(r'>*\d[,|.]\d',str(imdbs[ind])) != None):
                        imdb = str(re.search(r'>*\d[,|.]\d',str(imdbs[ind])).group(0)).replace(',','.') #getting imdb rating for this movie
                else:
                        imdb = 0.0
                print (shorttitle, mediayear, imdb)
                if(int(mediayear) >= int(year) and int(qual) >= int(moviequality) and float(imdb) >= float(movierating)): #if year/quality/imdb rating matches our requirements
                        #print (shorttitle, mediayear) #gives us shorttitle and year of the movie
                        links = re.findall(r'</span><span style=\"display:inline;\"><a href=\"(.*?)target=',str(el[ind])) #all links of this movie/series
                        imdb = re.search(r'>*\d[,|.]\d',str(imdbs[ind])).group(0)
                        for link in links:
                                if (link.find('filecrypt.cc/Container') != -1):
                                        dllink = str(link)
                                        break
                        addMovie(shorttitle,dllink)
        #searching for series
        if(re.search('(.*?S...)COMPLETE',title.get('value')) != None): #handle series
                shorttitle = str(re.search('(.*?S...)COMPLETE',title.get('value')).group(0))[:-9] #title of the serie
                if(re.search('\.\d{3}p|\.\d{4}p',title.get('value')) != None): #get the quality of the serie
                        qual = str(re.search('\.\d{3}p|\.\d{4}p',title.get('value')).group(0)).replace('.','').replace('p','') #quality
                else:
                        qual = 0.0 #if no quality was found (like BD or HDDVD..)
                if(re.search(r'>*\d[,|.]\d',str(imdbs[ind])) != None):
                        imdb = str(re.search(r'>*\d[,|.]\d',str(imdbs[ind])).group(0)).replace(',','.') #get rating for this serie
                else:
                        imdb = 0.0 #if no rating was found set it to 0
                if(float(imdb) >= float(serierating) and int(qual) >= int(seriequality)):
                        for link in links:
                                if (link.find('filecrypt.cc/Container') != -1): #get the correct link
                                        dllink = str(link)
                                        break
                        addSerie(storttitle,dllink)
        ind = ind + 1
