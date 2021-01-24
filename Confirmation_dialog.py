from PyQt5 import QtCore, QtGui, QtWidgets


class Confirmation:
    def __init__(self, msg):
        self.Dialog = QtWidgets.QDialog()
        self.Cancel_button = QtWidgets.QPushButton(self.Dialog)
        self.Confirm_button = QtWidgets.QPushButton(self.Dialog)
        self.Message = QtWidgets.QLabel(self.Dialog)
        self.Message.setText(msg)

        self.setupUi()
        self.Dialog.show()

    def setupUi(self):
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(352, 133)
        self.Message.setGeometry(QtCore.QRect(0, 9, 351, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Message.setFont(font)
        self.Message.setAlignment(QtCore.Qt.AlignCenter)
        self.Message.setWordWrap(True)
        self.Message.setObjectName("Message")
        self.Cancel_button.setGeometry(QtCore.QRect(190, 70, 131, 31))
        self.Cancel_button.setObjectName("Cancel_button")
        self.Cancel_button.clicked.connect(lambda: self.button_clicked(False))
        self.Confirm_button.setGeometry(QtCore.QRect(30, 70, 131, 31))
        self.Confirm_button.setObjectName("Confirm_button")
        self.Confirm_button.clicked.connect(lambda: self.button_clicked(True))

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    def button_clicked(self, boolean):
        if boolean:
            self.Dialog.accept()
        else:
            self.Dialog.reject()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Cancel_button.setText(_translate("Dialog", "No"))
        self.Confirm_button.setText(_translate("Dialog", "Yes"))
