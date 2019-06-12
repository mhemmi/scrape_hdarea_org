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
        files = os.listdir(path)
        for file in files:
                low_path = os.path.join(path,file)
                if(os.path.isdir(low_path)):
                        moveContent(low_path) #recursive call
                else:
                        print "Pfad " + path
                        video = re.search(videoregex,str(file)) #searching for mkv and iso files
                        cancel = re.search(cancelregex,str(file)) #searching for audio content
                        if(cancel != None):
                                print "Canceled at: "+file
                                exit() #if audio content was found exit whole script
                        if(video == None): #no video content -> please delete
                                oldpath = os.path.join(path,file)
                                print "Ignore and delete " + oldpath
                                if(os.path.isfile(oldpath)): #if file is not a folder
                                        os.remove(oldpath) #remove file! (not folder)
                        else: #video file found
                                movie = re.search('.*/(.*?\d\d\d\d)',str(path)) #searching for movie name in folder name
                                if movie != None: #true = movie name found
                                        oldpath = os.path.join(path,file) #remember path of the file
                                        print path
                                        newfolder = os.path.join(moviefolder,movie.group(1)) #create new folder path
                                        newpath = os.path.join(moviefolder,movie.group(1),file) #create new file path
                                        if not os.path.isdir(newfolder): #check if new folder exists
                                                os.mkdir(newfolder) # create new folder if not exists
                                                print "Neuen Folder anlegen: " + newfolder + '<<'
                                        print "Verschiebe: " + oldpath + " nach " + newpath #move file to new location
                                        shutil.move(oldpath,newpath) #move file to new location
                                serie = re.search('.*/(.*?\.S\d\d)',str(path)) #check if its a serie (and not movie)
                                if serie != None: #true = found serie
                                        seriename = str(serie.group(1))[:-4] #name of the serie (without last numbers for season) [e.g. "Testserie"]
                                        oldpath = os.path.join(path,file) #remember old path of file [e.g. /old/path/Serie]
                                        serienamefolder = os.path.join(seriefolder,seriename) #folder of the home serie [e.g. new/folder/Testserie]
                                        if not os.path.isdir(serienamefolder): #check if this serie has no home folder
                                                os.mkdir(serienamefolder) #create new home folder for this serie
                                        newfolder = os.path.join(serienamefolder,serie.group(1)) #create new folder path for season [e.g. /new/path/Testserie/Testserie.S02]
                                        newpath = os.path.join(serienamefolder,serie.group(1),file) #create new file path [e.g. /new/path/Testserie/Testserie.S02/file.mkv]
                                        if not os.path.isdir(newfolder): #check if new folder already exists
                                                os.mkdir(newfolder) # create new folder if not exists
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
