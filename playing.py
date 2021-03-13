from PyQt5 import QtCore, QtGui, QtWidgets

class WorkerThread(QtCore.QThread):
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, instance):
        QtCore.QThread.__init__(self)
        self.instance = instance

    def run(self):
        while True:
            send_length = self.instance.client.recv(Dialogplaying.HEADER).decode()
            if send_length:
                self.signal.emit(self.instance.client.recv(int(send_length)).decode())

class Dialogplaying(QtWidgets.QDialog):
    HEADER = 64

    def __init__(self, client=None):
        super().__init__()
        self.client = client
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
        self.label_drawed = {self.l00: False, self.l10: False, self.l20: False, self.l01: False, self.l11: False,
                             self.l21: False, self.l02: False, self.l12: False, self.l22: False}
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Chatplaintext = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.Inputlineedit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.Multiplayerlabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Outputlabel = QtWidgets.QLabel(self.Dialog)
        self.blanked = QtGui.QPixmap("pictures/blank.png")
        self.circle = QtGui.QPixmap("pictures/Circle.png")
        self.X = QtGui.QPixmap("pictures/X.png")
        self.playerTurn = False
        self.gamedone = False

        self.setupUi()
        self.reset()
        self.Dialog.show()
        self.elements_dict_str = {"00": self.l00, "01": self.l01, "02": self.l02, "10": self.l10, "11": self.l11, "12": self.l12, "20": self.l20, "21": self.l21, "22": self.l22}
        self.elements_dict = {self.l00: "00", self.l01: "01", self.l02: "02", self.l10: "10", self.l11: "11", self.l12: "12", self.l20: "20", self.l21: "21", self.l22: "22"}
        self.thread = WorkerThread(self)
        self.thread.start()
        self.thread.signal.connect(self.recv)

    def setupUi(self):
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(740, 367)
        self.Outputlabel.setGeometry(QtCore.QRect(10, 340, 721, 16))
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

        for i in self.label_drawed.keys():
            i.installEventFilter(self)

        self.Inputlineedit.returnPressed.connect(self.lineeditpressed)

        self.Dialog.setWindowTitle("Tic tac toe")
        self.Multiplayerlabel.setText("Multiplayer")
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    @classmethod
    def _get_size(cls, msg):
        """Internal method to pad messages"""
        send_length = str(len(msg.encode())).encode()
        send_length += b' ' * (cls.HEADER - len(send_length))
        return send_length

    def send(self, msg):
        """Send messages back to the server"""
        self.client.send(self._get_size(msg))
        self.client.send(msg.encode())

    def recv(self, msg):
        if msg.startswith("!ACTIONDRAW-"):
            self.playerTurn = True
            self.draw(self.elements_dict_str[(msg.split("-")[1])], self.circle)
            self.label_drawed[self.elements_dict_str[(msg.split("-")[1])]] = True
        elif msg.startswith("!MSG-"):
            self.write(msg.split("-")[1])
        elif msg.startswith("!FINISHED-"):
            if msg.split("-")[1] == "WON":
                self.won()
            elif msg.split("-")[1] == "LOST":
                self.lost()
            elif msg.split("-")[1] == "DRAW":
                self.draw_()
        elif msg.startswith("!NEWGAME"):
            self.reset()

    def won(self):
        self.Outputlabel.setText("You have won")
        self.gamedone = True

    def lost(self):
        self.Outputlabel.setText("You have lost")
        self.gamedone = True

    def draw_(self):
        self.Outputlabel.setText("Draw!")
        self.gamedone = True

    def draw(self, obj: QtWidgets.QLabel, picture: QtGui.QPixmap):
        obj.setPixmap(picture)
        self.Outputlabel.setText("")

    def reset(self):
        for i in self.label_drawed.keys():
            i.setPixmap(self.blanked)
            self.label_drawed[i] = False
        self.Outputlabel.setText("")
        self.gamedone = False

    def write(self, text):
        """Used to give output to the Chat"""
        self.Chatplaintext.appendPlainText(f'{text}')
        self.Chatplaintext.verticalScrollBar().maximum()
        self.Chatplaintext.update()

    def lineeditpressed(self):
        text = self.Inputlineedit.text()
        self.Inputlineedit.clear()
        self.write(">>> " + text)
        self.send(f"!MSG-{text}")

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if not self.gamedone:
                if self.playerTurn:
                    if not self.label_drawed[source]:
                        self.draw(source, self.X)
                        self.playerTurn = False
                        self.label_drawed[source] = True
                        self.send(f"!ACTIONDRAW-{self.elements_dict[source]}")
                    else:
                        self.Outputlabel.setText("You can't override an already printed field")
                else:
                    self.Outputlabel.setText("It's not your turn")
            else:
                self.Outputlabel.setText("Game is already finished")
        return super(Dialogplaying, self).eventFilter(source, event)
