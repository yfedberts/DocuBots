import sys, os
from PyQt5 import QtWidgets, uic


app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi('View/mainwindow.ui')
window.show()
app.exec()