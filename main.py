import sys

from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
