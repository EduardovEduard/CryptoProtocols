__author__ = 'ees'

import sys
import os
import json
import random
import pickle

from lab3 import EllipticCurve
from lab4 import sign, check
from lab5 import int_to_binary_array, binary_array_to_int

from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('Digital Sign Gen And Check')
        self.curve = None
        self.__get_params()
        self.d = random.randint(1, self.curve.q - 1)

        self.filename_to_process = ""

        self.status_edit = QtGui.QLineEdit("")
        self.status_edit.setReadOnly(True)
        self.status_edit.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.filename_label = QtGui.QLabel()
        self.open_button = QtGui.QPushButton('&Open file...')
        self.check_button = QtGui.QPushButton('&Check')
        self.sign_button = QtGui.QPushButton('&Sign')

        self.connect(self.open_button, QtCore.SIGNAL('clicked()'), self.openFileDialog)
        self.connect(self.check_button, QtCore.SIGNAL('clicked()'), self.check)
        self.connect(self.sign_button, QtCore.SIGNAL('clicked()'), self.sign)

        vbox_layout = QtGui.QVBoxLayout()
        hbox_layout = QtGui.QHBoxLayout()
        vbox_layout.addWidget(self.filename_label)
        vbox_layout.addWidget(self.open_button)

        vbox_layout.addLayout(hbox_layout)
        hbox_layout.addWidget(self.sign_button)
        hbox_layout.addWidget(self.check_button)

        vbox_layout.addWidget(self.status_edit)

        self.setLayout(vbox_layout)


    def openFileDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file')

        self.filename_to_process = filename
        self.filename_label.setText(filename)

        file = open(filename)
        file.close()

    def sign(self):
        if not self.filename_to_process:
            print('File should be chosen first')
            return

        with open(self.filename_to_process, 'rb') as original:
            content = original.read()
            total = int.from_bytes(content, byteorder=sys.byteorder)

            message = int_to_binary_array(total)
            sign_, Q = sign(self.d, message)

            sign_list = sign_, Q
            sign_bytes = pickle.dumps(sign_list)
            sign_len = len(sign_bytes)

            new_filename = self.filename_to_process + '.sign'

            with open(new_filename, 'wb') as output_file:
                output_file.write(sign_len.to_bytes(4, byteorder=sys.byteorder))
                output_file.write(sign_bytes)
                output_file.write(content)

        QtGui.QMessageBox.information(self, "Подпись", "Файл подписан!")


    def check(self):
        """Checking message and printing result into label"""
        if not self.filename_to_process:
            print('File should be chosen first')
            return

        with open(self.filename_to_process, 'rb') as file:
            len = int.from_bytes(file.read(4), byteorder=sys.byteorder)
            sign_bytes = file.read(len)
            sign_, Q = pickle.loads(sign_bytes)
            message = file.read()

            message_int = int.from_bytes(message, byteorder=sys.byteorder)
            result = check(sign_, Q, int_to_binary_array(message_int))

        if result:
            self.status_edit.setText('Подпись верна!')
        else:
            self.status_edit.setText('Подпись неверна!')

    def __get_params(self):
        with open('params.json') as param_file:
            params = json.load(param_file)
            self.curve = EllipticCurve(**params)


app = QtGui.QApplication(sys.argv)

mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
