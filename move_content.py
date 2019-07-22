import re,os,shutil

############## CONFIG #############################################
dlfolder = '<download folder from pyload>'                      ###
moviefolder = 'movie folder, where they moved to'               ###
seriefolder = 'main folder of you series'                       ###
videoregex = '\.mkv|\.iso' #you can add with | \.<new ending>   ###
cancelregex = '\.mp3|\.wave' #you can add with |\.<new ending>  ###
#cancelregex means: these files will be ingored                 ###
#only videoregex files will be moved,                           ###
#all other files (except from cancelregex will be deleted!!!)   ###
###################################################################

def moveContent(path):
        global mailtext
        files = os.listdir(path)
        for file in files:
                print file
                low_path = os.path.join(path,file)
                if(os.path.isdir(low_path)):
                        print "Call: "+low_path
                        moveContent(low_path) #recursive call
                else:
                        print "Checking Pfad: " + path
                        video = re.search(videoregex,str(file)) #searching for mkv and iso files
                        cancel = re.search(cancelregex,str(file)) #searching for audio content
                        if(cancel != None):
                                print "Canceled at: "+file
                                sendMail('Unterbrochen, manuelles verschieben notwendig.')
                                exit() #if audio content was found exit whole script
                        if(video == None): #no video content -> please delete
                                oldpath = os.path.join(path,file)
                                print "Ignore and delete " + oldpath
                                if(os.path.isfile(oldpath)): #if file is not a folder
                                        print "remove file: " + oldpath
                                        os.remove(oldpath) #remove file! (not folder)
                        else: #video file found
                                serie = re.search('.*/(.*?\.S\d\d)',str(path)) #check if its a serie (and not movie)
                                if serie != None: #true = found serie
                                        seriename = str(serie.group(1))[:-4] #name of the serie (without numbers) [e.g. "Testserie"]
                                        oldpath = os.path.join(path,file) #remember old path of file [e.g. /old/path/Serie]
                                        serienamefolder = os.path.join(seriefolder,seriename) #folder of the home serie [e.g. new/folder/Testserie]
                                        if not os.path.isdir(serienamefolder): #check if this serie has a home folder
                                                print "New Home-Folder: " + serienamefolder
                                                os.mkdir(serienamefolder) #create new home folder for this serie
                                        newfolder = os.path.join(serienamefolder,serie.group(1)) #create new folder path for season [e.g. /new/path/Testserie/Testserie.S02]
                                        newpath = os.path.join(serienamefolder,serie.group(1),file) #create new file path [e.g. /new/path/Testserie/Testserie.S02/file.mkv]
                                        if not os.path.isdir(newfolder): #check if new folder already exists
                                                print "New Folder: " + newfolder
                                                os.mkdir(newfolder) # create new folder if not exists
                                        print "Verschiebe: " + oldpath + " nach " + newpath #move file to new location
                                        shutil.move(oldpath,newpath) #move file to new location
                                        mailtext = mailtext +'Verschiebe Serie: ' + oldpath + ' >> ' + newpath +  '\n'
                                        continue #required to skip the if(movie==None) -> because it is a serie, so it is None!
                                movie = re.search('.*/(.*?\d\d\d\d)',str(path)) #searching for movie name in folder name
                                if movie != None: #true = movie name found
                                        oldpath = os.path.join(path,file) #remember path of the file
                                        print "Movie gefunden: " + path,file
                                        newfolder = os.path.join(moviefolder,movie.group(1)) #create new folder path
                                        newpath = os.path.join(moviefolder,movie.group(1),file) #create new file path
                                        if not os.path.isdir(newfolder): #check if new folder exists
                                                print "Neuen Folder anlegen: " + newfolder + '<<'
                                                os.mkdir(newfolder) # create new folder if not exists
                                        print "Verschiebe: " + oldpath + " nach " + newpath #move file to new location
                                        shutil.move(oldpath,newpath) #move file to new location
                                        mailtext = mailtext + 'Film verschoben: ' + str(oldpath) + ' >> ' + str(newpath) +  '\n'
                                if (movie == None): #if there is a movie/serie without release year > move to moviefolder
                                        movie = re.search('.*/(.*)',str(path)) #get folder name of that movie
                                        newfolder = os.path.join(moviefolder,movie.group(1)) #untouched filename (group1 is foldername of that movie)
                                        oldpath = os.path.join(path,file) #oldpath of that file
                                        newpath = os.path.join(newfolder,file) #new path of that file
                                        if not os.path.isdir(newpath): #check if folder already exist, if not create this folder
                                                print "Mach neuen Ordner: " + newfolder
                                                mailtext = mailtext + "Neuer Ordner erstellt: "+str(newpath)+'\n'
                                                os.mkdir(newfolder)
                                        print "WARNUNG: Verschiebe unbekanntes Format: " + oldpath + " nach " + newpath #move file to new locati$
                                        mailtext = mailtext + 'WARNUNG: Verschiebe unbekanntes Format: ' + str(oldpath) + ' >> ' + str(newpath) + '\n'
					print "Finales verschieben: " + oldpath + " nach " + newpath
                                        shutil.move(oldpath,newpath) #move file to new location
                #check if folder is empty to delete
                removeEmptyFolders(path)

#Function to remove empty folders
def removeEmptyFolders(path, removeRoot=True):
        if not os.path.isdir(path): #check if path is a file
                return #file? = yes: do nothing
        # remove empty subfolders
        files = os.listdir(path) #if not get file/folder list in this folder
        if len(files): #check amount of files in this folder: recursiv call
                for f in files:
                        fullpath = os.path.join(path, f)
                        if os.path.isdir(fullpath): #check if this is a subfolder for recursiv call
                                removeEmptyFolders(fullpath) #recursiv call
# if folder empty, delete it
        files = os.listdir(path)
        if len(files) == 0 and removeRoot: #delete empty folder if there is no file in this folder
                print "Removing empty folder:" + path
                os.rmdir(path) #delete folder

moveContent(dlfolder)
os.mkdir(dlfolder)
