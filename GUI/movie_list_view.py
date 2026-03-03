from sys import exception

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QPushButton, QGridLayout, QLabel, QFrame
from sqlalchemy import ColumnElement

import db_manager
import movieFinder
from GUI.movie_display_widget import MovieDisplayWidget
from GUI.sel_management import MovieSelectionManagement
from models import Movie


class movieListView(QFrame):
    rows = 5
    cols = 10
    page_max = rows * cols

    def __init__(self,parent=None):
        super().__init__(parent)
        self.page_num = 0
        self.movieList:list[Movie]=[]
        self.selectionManager = MovieSelectionManagement(self.scrapeForMovies,self.reloadMovieList)

        self.initUI()
        self.scrapeForMovies()

    def initUI(self):
        layout = QVBoxLayout(self)
        actionsLayout = self.selectionManager.getLayout()

        pageManagementLayout = QHBoxLayout()
        self.moviesShown = QLabel( self.getPageText() )
        prevPage = QPushButton("<")
        prevPage.clicked.connect(self.changePageFunc(-1))
        nextPage = QPushButton(">")
        nextPage.clicked.connect(self.changePageFunc(1))
        pageManagementLayout.addStretch(20)
        pageManagementLayout.addWidget(prevPage)
        pageManagementLayout.addStretch(5)
        pageManagementLayout.addWidget(self.moviesShown)
        pageManagementLayout.addStretch(5)
        pageManagementLayout.addWidget(nextPage)
        pageManagementLayout.addStretch(20)

        self.movie_grid = QGridLayout()
        self.movie_grid.setHorizontalSpacing(30)
        self.movie_grid.setVerticalSpacing(15)



        layout.addLayout(actionsLayout)
        layout.addLayout(self.movie_grid)
        layout.addLayout(pageManagementLayout)

    def getPageText(self):
        if  (self.page_num+1)*self.rows * self.cols -1 < len(self.movieList):
            s =  str(self.page_num*self.rows * self.cols+1)+"-"+str((self.page_num+1)*self.rows * self.cols)+" out of "+str(len(self.movieList))
        else:
            s= str(self.page_num*self.rows * self.cols+1)+"-"+str(len(self.movieList))+" out of "+str(len(self.movieList))
        return s


    def changePageFunc(self,direction:int):
        def changePage():
            old_num = self.page_num
            self.page_num+=direction
            if self.page_num < 0:
                self.page_num = 0
            if self.page_num * self.rows * self.cols > len(self.movieList):
                self.page_num = int ( len(self.movieList) / (self.rows * self.cols) )
            if not old_num == self.page_num:
                self.populateMovieGrid()
        return changePage

    def clearMovieGrid(self):
        while self.movie_grid.count():
            item = self.movie_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()



    def populateMovieGrid(self):
        self.clearMovieGrid()

        start = self.page_num * self.page_max
        end = min(start + self.page_max, len(self.movieList))
        index = start

        for i in range(self.rows):
            for j in range(self.cols):
                if index>=end:
                    return
                movie = self.movieList[index]
                widget = MovieDisplayWidget(movie)
                self.movie_grid.addWidget(widget, i, j)
                index+=1

    def scrapeForMovies(self):
        movieFinder.scrape_directories_for_movies()
        self.reloadMovieList()

    def reloadMovieList(self):
        self.movieList = db_manager.get_movies(self.selectionManager.getSelector(),self.selectionManager.getOrderBy())
        self.populateMovieGrid()
        self.moviesShown.setText(self.getPageText() )

