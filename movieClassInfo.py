# -*- coding: utf-8 -*-
from imdb import IMDb
import time

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
    def __init__(self,filename,path,modifiedTime,size,actualName=None,hasSeen=False,imdb=None,personalRating=None):
        self.filename = filename
        self.path = path
        self.modifiedTime = modifiedTime
        self.size = size
    
    def __eq__(self,other):
        if self.name == other.name and self.path == other.path and self.modifiedTime== other.modifiedTime and self.size == other.size:
            return True
        else:
            return False
    
    def __str__(self):
        return( self.filename )