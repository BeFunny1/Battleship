import sys

from PyQt5 import QtWidgets

from logic.main_application import Application

if __name__ == '__main__':
    application_for_window = QtWidgets.QApplication(sys.argv)
    app = Application()
    app.create_config_window()
    application_for_window.exec_()
