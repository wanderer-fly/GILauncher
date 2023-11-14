import sys
from PyQt5.QtWidgets import QApplication
from window import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = Launcher()
    sys.exit(app.exec())
