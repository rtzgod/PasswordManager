from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def clicked():
    print("niigaga")

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(300, 300, 300, 300)
    win.setWindowTitle("Password Manager")

    label = QtWidgets.QLabel(win)
    label.setText("Nigga")
    label.move(400, 250)

    b1 = QtWidgets.QPushButton(win)
    b1.setText("press me")
    b1.move(100, 100)
    b1.clicked.connect(clicked)
    win.show()
    sys.exit(app.exec_())

window()