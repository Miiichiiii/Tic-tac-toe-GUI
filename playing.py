from PyQt5 import QtCore, QtGui, QtWidgets
from Confirmation_dialog import Confirmation


class Dialogplaying(QtWidgets.QDialog):
    def __init__(self, client=None):
        super().__init__()
        self.connection = client
        self.Dialog = QtWidgets.QDialog()
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Dialog)
        self.l00 = QtWidgets.QLabel(self.Dialog)
        self.l10 = QtWidgets.QLabel(self.Dialog)
        self.l20 = QtWidgets.QLabel(self.Dialog)
        self.l01 = QtWidgets.QLabel(self.Dialog)
        self.l11 = QtWidgets.QLabel(self.Dialog)
        self.l21 = QtWidgets.QLabel(self.Dialog)
        self.l02 = QtWidgets.QLabel(self.Dialog)
        self.l12 = QtWidgets.QLabel(self.Dialog)
        self.l22 = QtWidgets.QLabel(self.Dialog)
        self.newGame = QtWidgets.QPushButton(self.Dialog)
        self.label_drawed = {self.l00: False, self.l10: False, self.l20: False, self.l01: False, self.l11: False,
                             self.l21: False, self.l02: False, self.l12: False, self.l22: False}
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Chatplaintext = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.Inputlineedit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.Multiplayerlabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Outputlabel = QtWidgets.QLabel(self.Dialog)
        self.blanked = QtGui.QPixmap("pictures/blank.png")
        self.circle = QtGui.QPixmap("pictures/Kreis.png")
        self.X = QtGui.QPixmap("pictures/X.png")
        self.playerTurn = False

        self.setupUi()
        self.reset()
        self.Dialog.show()

    def setupUi(self):
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(740, 395)
        self.Outputlabel.setGeometry(QtCore.QRect(13, 370, 721, 16))
        self.Outputlabel.setObjectName("Outputlabel")
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(340, 10, 391, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Multiplayerlabel.setObjectName("Multiplayerlabel")
        self.verticalLayout.addWidget(self.Multiplayerlabel)
        self.Chatplaintext.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Chatplaintext.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.Chatplaintext.setReadOnly(True)
        self.Chatplaintext.setObjectName("Chatplaintext")
        self.verticalLayout.addWidget(self.Chatplaintext)
        self.Inputlineedit.setObjectName("Inputlineedit")
        self.verticalLayout.addWidget(self.Inputlineedit)
        self.l00.setGeometry(QtCore.QRect(10, 10, 100, 100))
        self.l00.setObjectName("label")
        self.l10.setGeometry(QtCore.QRect(120, 10, 100, 100))
        self.l10.setObjectName("label_2")
        self.l20.setGeometry(QtCore.QRect(230, 10, 100, 100))
        self.l20.setObjectName("label_3")
        self.l11.setGeometry(QtCore.QRect(120, 120, 100, 100))
        self.l11.setObjectName("label_4")
        self.l21.setGeometry(QtCore.QRect(230, 120, 100, 100))
        self.l21.setObjectName("label_5")
        self.l01.setGeometry(QtCore.QRect(10, 120, 100, 100))
        self.l01.setObjectName("label_6")
        self.l12.setGeometry(QtCore.QRect(120, 230, 100, 100))
        self.l12.setObjectName("label_7")
        self.l22.setGeometry(QtCore.QRect(230, 230, 100, 100))
        self.l22.setObjectName("label_8")
        self.l02.setGeometry(QtCore.QRect(10, 230, 100, 100))
        self.l02.setObjectName("label_9")
        self.newGame.setGeometry(QtCore.QRect(10, 340, 75, 23))
        self.newGame.setObjectName("NewGamebttn")
        self.newGame.setText("New Game")
        self.newGame.clicked.connect(self.newGameaction)

        for i in self.label_drawed.keys():
            i.installEventFilter(self)

        self.Inputlineedit.returnPressed.connect(self.lineeditpressed)

        self.Dialog.setWindowTitle("Tic tac toe")
        self.Multiplayerlabel.setText("Multiplayer")

        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    @staticmethod
    def await_confirmation(msg):
        confirmation_box = Confirmation(msg)
        if confirmation_box.Dialog.exec_():
            return True
        else:
            return False

    def is_game_finished(self):
        pass  # TODO

    def newGameaction(self):
        if self.is_game_finished():
            pass
        else:
            if self.await_confirmation("Are you sure you want to start a new Game - Old Game isn't completed"):
                pass  # TODO

    @staticmethod
    def draw(obj: QtWidgets.QLabel, picture: QtGui.QPixmap):
        obj.setPixmap(picture)

    def reset(self):
        for i in self.label_drawed.keys():
            i.setPixmap(self.blanked)

    def write(self, text, color="black"):
        """Used to give output to the Chat"""
        self.Chatplaintext.appendHtml(f'<p style="color:{color};">{text}</p>')
        self.Chatplaintext.verticalScrollBar().maximum()
        self.Chatplaintext.update()

    def lineeditpressed(self):
        print("moin ich bins")
        text = self.Inputlineedit.text()
        self.Inputlineedit.clear()
        self.write(">>> " + text)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if self.playerTurn:
                if not self.label_drawed[source]:
                    self.draw(source, self.X)
                else:
                    self.Outputlabel.setText("You can't override an already printed field")
            else:
                self.Outputlabel.setText("It's not your turn")
        return super(Dialogplaying, self).eventFilter(source, event)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Dialogplaying()
    sys.exit(app.exec_())
