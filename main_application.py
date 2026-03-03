import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

import db_manager
import movieFinder
from GUI.app_frame import ApplicationFrame
from models import Movie, Directory
if __name__ == '__main__':
    # db_manager.delete_movies()

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    frame = ApplicationFrame()
    frame.show()

    sys.exit(app.exec_())

