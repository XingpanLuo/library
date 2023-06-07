# This Python file uses the following encoding: utf-8
import sys
from src import database
from src import main_widget
from PyQt5.QtWidgets import QApplication  # , QMainWindow

if __name__ == "__main__":
    database.init_database()
    app = QApplication([])
    window = main_widget.MainWindow()
    window.show()
    sys.exit(app.exec_())
