import os
import time
from datetime import datetime
import re

import db_manager
from models import Directory, Movie

acceptableFiletypes = [".mkv",".mp4"]

def scrapeDirectory(main_folder: Directory, can_scan_sub_dirs = True) -> list[Movie]:
    directory = os.scandir(main_folder.path)
    movieList:list[Movie] = []
    for d in directory:
        if  d.is_dir() and 'System Volume Information' not in d.name and can_scan_sub_dirs:
            sub_list = scrapeDirectory(Directory(path = d), False)
            for m in sub_list:
                movieList.append(m)

        if ("sample" not in d.name.lower() and 'System Volume Information' not in d.name and
                'DVD' not in d.name and (d.path.endswith(".mkv") or d.path.endswith(".mp4")) and
                os.path.getsize(d) > 500000000 and "S0" not in d.path):
            for fileType in acceptableFiletypes:
                if d.path.endswith(fileType):
                    movieList.append(getMovie(d.name, d.path))
                    break

    return movieList


def getMovie(filename:str, path:str):
    m = Movie(filename = filename, path = path)
    datetime_object = datetime.strptime(time.ctime(os.path.getmtime(path)), "%a %b %d %H:%M:%S %Y")
    m.modifiedTime = datetime_object
    m.size = os.path.getsize(path)
    estimateName(m)
    estimateYear(m)
    return m

def estimateName(m:Movie):
    estName = ""
    words = re.split(r'[.\s()\[\]{}-]', m.filename)
    for word in words:
        if ("20" in word or "19" in word or "=aka=" in word.lower() or "mp4" in word or "mkv" in word
                or "Director's" in word or 'aka' == word.lower() or '1080' in word or 'S01' in word):
            break
        estName += word +" "
    estName = estName.strip(" ")
    m.actualName = estName

def estimateYear(m:Movie):
    words = re.split(r'[.\s()\[\]{}-]', m.filename)
    words.reverse()
    for word in words:
        try:
           yr = int(word)
           if yr in range(1930, 2080):
                m.year = yr
                break
        except(Exception):
            continue



def scrape_directories_for_movies():
    movies_in_db = db_manager.get_movies()
    paths_in_db = {}
    for m in movies_in_db:
        paths_in_db[m.path]=True

    dirs = db_manager.get_directories()
    for d in dirs:
        movies = scrapeDirectory(d,True)
        for m in movies:
            if not paths_in_db.get(m.path,False) :
                print("Inserting",m)
                db_manager.insert_movie(m)

