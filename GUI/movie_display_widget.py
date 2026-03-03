from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QMenu
from PyQt5 import QtCore
import subprocess

import db_manager
from GUI.rating_dialog import RatingDialog

vlc = 'C:/Program Files/VideoLAN/VLC/vlc.exe'


from models import Movie


class MovieDisplayWidget(QFrame):

    def __init__(self, movie:Movie):
        super().__init__()
        self.movie = movie
        self.setObjectName("MovieDisplayWidget")

        self.initUI()

    def initUI(self):

        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)

        self.text = QLabel(self.movie.actualName)
        self.text.setMaximumWidth(150)
        self.text.setWordWrap(True)
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        year = QLabel(str(self.movie.year))
        year.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        rate = QLabel("IMDb Rating: " + str(self.movie.imdbRating))
        rate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        vbox = QVBoxLayout()
        self.seenDescLabel:QLabel = QLabel()
        self.seenDescLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.setUserTextDesc()

        vbox.addWidget(self.seenDescLabel)
        vbox.addStretch(10)
        vbox.addWidget(self.text)
        vbox.addStretch(10)
        vbox.addWidget(year)
        vbox.addStretch(10)
        vbox.addWidget(rate)
        vbox.addStretch(10)
        self.setLayout(vbox)

        # self.setStyleSheet("""
        #     QFrame#MovieDisplayWidget {
        #         background-color: #5C5C5C;
        #     }
        #     QFrame#MovieDisplayWidget:hover {
        #         background-color: #616161;
        #     }
        # """)


    def setUserTextDesc(self):
        s = ""
        if self.movie.hasSeen:
            if self.movie.personalRating is not None:
                s += "Rating: " + str(self.movie.personalRating)
            else:
                s += "Seen"
        self.seenDescLabel.setText(s)

    def contextMenuEvent(self, event):

        cmenu = QMenu(self)

        # infoAct = cmenu.addAction("More Info")
        seenAct = cmenu.addAction("Toggle Seen")
        ratingAct = cmenu.addAction("Add Rating")
        playAct = cmenu.addAction("Play Movie")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        # if action == infoAct:
        #     m = MovieWindow(self.movie)
        #     m.exec_()
        if action == seenAct:
            self.movie.hasSeen = not self.movie.hasSeen
            self.setUserTextDesc()
            db_manager.update_movie(self.movie)
        if action == ratingAct:
            r = RatingDialog(self.movie.personalRating)
            if r.exec_():
                if r.rating is not None:
                    self.movie.hasSeen = True
                    self.movie.personalRating = r.rating
                    self.setUserTextDesc()
                db_manager.update_movie(self.movie)
        if action == playAct:
            print(self.movie.path)
            try:
                subprocess.Popen(["vlc.exe", self.movie.path.replace("/", "\\")], executable=vlc)
            except:
                print("VLC Media Player is not installed where I think it was.")
                print("Make sure it is installed correctly, then change line 12 to the correct path to the executable.")

