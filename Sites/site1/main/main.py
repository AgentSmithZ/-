import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from mainwindow2 import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__ (self, *args, obj=None,  **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        res = 0
        res = 1
        res = 2
        res = 4
        


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()