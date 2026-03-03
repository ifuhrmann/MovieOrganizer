from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QPushButton
from sqlalchemy import ColumnElement, and_, Column, UnaryExpression
from enum import Enum

from models import Movie

class SortDirection(Enum):
    NONE = 0
    ASC = 1
    DESC = 2

class SortButton(QPushButton):
    sortChanged = pyqtSignal(object)

    def __init__(self,default_text,table_column):
        super().__init__(default_text)
        self.sortDirection:SortDirection = SortDirection.NONE
        self.table_column:Column = table_column
        self.defaultText = default_text
        self.clicked.connect(self.toggleSort)

    def toggleSort(self):
        if self.sortDirection in (SortDirection.NONE, SortDirection.DESC):
            self.setDir(SortDirection.ASC)
        else:
            self.setDir(SortDirection.DESC)
        self.sortChanged.emit(self)


    def setDir(self,dir:SortDirection):
        self.sortDirection = dir
        arrow = ""
        if self.sortDirection == SortDirection.ASC:
            arrow = " ↑"
        elif self.sortDirection == SortDirection.DESC:
            arrow = " ↓"
        self.setText(self.defaultText+arrow)


class MovieSelectionManagement:
    filter_props = [["Seen", None, Movie.hasSeen]]
    sorter_props = [["Name", Movie.actualName], ["Rating", Movie.personalRating], ["Year", Movie.year],["Added Time",Movie.modifiedTime]]

    def __init__(self,onUpdate, reloadMovieList):
        self.onUpdate = onUpdate
        self.reloadMovieList = reloadMovieList
        self.filters={
            "Seen?":Movie.hasSeen
        }
        self.sorters:list[SortButton]=[]


    def getLayout(self):
        layout = QHBoxLayout()
        layout.setSpacing(5)

        actionsList = [
            ["Update Library",self.onUpdate]
        ]
        for act in actionsList:
            button = QPushButton(text=act[0])
            button.clicked.connect(act[1])
            layout.addWidget(button)

        for props in self.sorter_props:
            button = SortButton(props[0],props[1])
            button.sortChanged.connect(self.onSortChanged)
            self.sorters.append(button)
            layout.addWidget(button)
        self.sorters[0].setDir(SortDirection.ASC)

        return layout

    def onSortChanged(self, clicked_button:SortButton):
        for s in self.sorters:
            if s is not clicked_button:
                s.setDir(SortDirection.NONE)
        self.reloadMovieList()

    def getSelector(self) -> ColumnElement[bool]:
        # order_by = []
        # order_by.append(Movie.hasSeen.is_(True))
        #
        # for sorter in self.sorters:
        #     if sorter.sortDirection == SortDirection.ASC:
        #         order_by.append(sorter.table_column.asc())
        #     if sorter.sortDirection == SortDirection.DESC:
        #         order_by.append(sorter.table_column.desc())
        # print("survives?")
        # if order_by:
        #     selector = and_(*order_by)
        #     return selector
        # return Movie.hasSeen.is_(False)
        return True


    def getOrderBy(self) -> list[UnaryExpression]:
        order_by_columns = []
        for sorter in self.sorters:
            if sorter.sortDirection == SortDirection.ASC:
                order_by_columns.append(sorter.table_column.asc())
            elif sorter.sortDirection == SortDirection.DESC:
                order_by_columns.append(sorter.table_column.desc())
        return order_by_columns
