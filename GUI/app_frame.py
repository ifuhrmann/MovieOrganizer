from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QApplication, QGridLayout, QVBoxLayout, QWidget

import db_manager
from GUI.movie_list_view import movieListView
from models import Movie


class ApplicationFrame(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName("ApplicationFrame")
        self.initUI()

    def initUI(self):

        menuItemDescList = [
            ['Add Directory', 'Ctrl+D',self.addNewDirectory,'open.png'],
            ['Quit', 'Ctrl+Q', QApplication.quit]
        ]

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        for menuItemDesc in menuItemDescList:
            action = QAction(menuItemDesc[0],self)
            action.setShortcut(menuItemDesc[1])
            action.triggered.connect(menuItemDesc[2])

            if len(menuItemDesc) == 4:
                action.setIcon(QIcon(menuItemDesc[3]))

            fileMenu.addAction(action)

        central = QWidget(self)
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.addWidget(movieListView(central))

        # self.setStyleSheet("""
        #     QWidget#ApplicationFrame {
        #         background-color: #494949;  /* dark background */
        #     }
        # """)
        self.setWindowTitle('Movie Organizer')
        self.showMaximized()

    def addNewDirectory(self):
        fname = QFileDialog.getExistingDirectory(self, 'Set Initial Directory', '/home')

