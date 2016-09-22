u"""Точка входа в приложение"""

import sys

from gui import MainWindow
from PyQt4 import QtGui

def main():
    app = QtGui.QApplication(sys.argv)

    w = MainWindow()
    w.move(300, 300)
    w.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()