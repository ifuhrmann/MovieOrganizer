# -*- coding: utf-8 -*-
from imdb import IMDb
import time
import re
import datetime

def imdbTest():
    ia = IMDb()
    tinit = time.time()
    print( tinit )
    # get a movie and print its director(s)
    m = ia.search_movie("The Matrix")
    print(m)
    ia.update(m[0])
    print(m[0].movieID,m[0].get('directed by'))
    print(time.time()-tinit)


class MovieInfo():
    def __init__(self,filename,path,modifiedTime,size,actualName=None,hasSeen=False,
                 imdb=None,personalRating=None,imdbRating = None,year=None):
        self.filename = filename
        self.path = path
        self.modifiedTime = modifiedTime
        self.size = size
        self.actualName = actualName
        self.hasSeen = hasSeen
        self.imdb = imdb
        self.personalRating = personalRating
        self.imdbRating = imdbRating
        self.year = year
        
    def __eq__(self,other):
        if self.filename == other.filename and self.path == other.path and self.modifiedTime == other.modifiedTime and self.size == other.size:
            return True
        else:
            return False
    
    def __str__(self):
        if(self.actualName is None):
            return( self.filename )
        else:
            return self.actualName
    def setSeen(self,value = True):
        self.hasSeen = value
    
    def scrapeImdb(self):
        word = re.split('\.| |-|\(|\)|\[|\]|\{|\}',self.filename)
        s=word[0]
        i=1
        if(len(word) is not 1):
            while ("20" not in word[i] and "19" not in word[i] and i != len(word) and
                   "=aka=" not in word[i].lower() and "mp4" not in word[i] and
                   "mkv" not in word[i] and "Director's" not in word[i] and 
                   'aka' != word[i].lower() and '1080' not in word[i] and 'S01' not in word[i]):
                s+=" "+word[i]
                i+=1
            for x in range(len(word)):
                i = len(word)-x-1
                try:
                    testyear = word[i]
                    if( datetime.datetime.now().year >= int(word[i]) and int(word[i]) >= 1930):
                        self.year = int(word[i])
                        break
                except:
                    pass
        print(self.year)
        print(s)
        ia = IMDb()
        m = ia.search_movie(s)
        if(len(m) is not 0):
            ia.update(m[0])
            self.actualName = m[0].get('title')
            self.imdb = m[0].movieID
            self.imdbRating=m[0].get('rating')
            print(m[0].movieID,m[0].get('title'),m[0].get('plot summary'))
        else:
            self.imdb = "Imdb Update Failed"
        
    def updateName(self,name):
        self.actualName=name
    
    def updateImdb(self,imdb):
        self.imdb=imdb
    
    def updateRating(self,rate):
        self.personalRating=rate