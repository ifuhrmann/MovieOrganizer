import movieLibrary as ml
import movieClassInfo

m = ml.MovieLibrary(["F:/","D:/Movies"])
m.updateAll()
mList = m.sortBy("modifiedTime desc")
for mov in mList:
    print(mov,mov.filename)
m.sortBy("modifiedTime")

"""
mList = m.sortBy('modifiedTime')
for mov in mList:
    break
    print (mov,mov.filename)
print("")

m1 = MovieLibrary(["F:/"])
mList = m1.sortBy('imdbRating')
for mov in mList:
    print (mov,mov.imdbRating)
print("")
print(len(mList))

m.updateAll()
"""