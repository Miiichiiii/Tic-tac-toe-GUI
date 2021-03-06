from PyQt5 import QtCore, QtGui, QtWidgets
from Confirmation_dialog import Confirmation
import socket
from enum import Enum

class WorkerThread(QtCore.QThread):
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, instance):
        QtCore.QThread.__init__(self)
        self.instance = instance

    def run(self):
        while True:
            try:
                msg_length = self.instance.conn.recv(Dialoghoster.HEADER).decode()
                if msg_length:
                    self.signal.emit(self.instance.conn.recv(int(msg_length)).decode())
            except ConnectionError:
                self.instance.conn.close()
                self.instance.dc()
                return
            except Exception as e:
                self.instance.Outputlabel.setText(f"Some not connection related Exception occured: {str(e)}")

class GameStatus(Enum):
    Loose, Draw, Win = range(3)

class Dialoghoster(QtWidgets.QDialog):
    HEADER = 64

    def __init__(self, conn: socket.socket, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
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
        self.circle = QtGui.QPixmap("pictures/Circle.png")
        self.X = QtGui.QPixmap("pictures/X.png")
        self.playerTurn = True
        self.elements_dict_str = {"00": self.l00, "01": self.l01, "02": self.l02, "10": self.l10, "11": self.l11, "12": self.l12, "20": self.l20, "21": self.l21, "22": self.l22}
        self.elements_dict = {self.l00: "00", self.l01: "01", self.l02: "02", self.l10: "10", self.l11: "11", self.l12: "12", self.l20: "20", self.l21: "21", self.l22: "22"}
        self.playerOpponent_drawings = {"00": False, "01": False, "02": False, "10": False, "11": False, "12": False, "20": False, "21": False, "22": False}
        self.playerOwn_drawings = {"00": False, "01": False, "02": False, "10": False, "11": False, "12": False, "20": False, "21": False, "22": False}
        self.gamedone = False

        self.setupUi()
        self.reset()
        self.Dialog.show()
        self.thread = WorkerThread(self)
        self.thread.start()
        self.thread.signal.connect(self.recv)

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
        self.newGame.setAutoDefault(False)
        self.newGame.clicked.connect(self.newGameaction)

        for i in self.label_drawed.keys():
            i.installEventFilter(self)

        self.Inputlineedit.returnPressed.connect(self.lineeditpressed)

        self.Dialog.setWindowTitle("Tic tac toe")
        self.Multiplayerlabel.setText("Multiplayer")

        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    def dc(self):
        """Handels the clients disconnection"""
        pass
        # TODO Client disconnection

    @classmethod
    def _len_message(cls, msg):
        """Internal Method used in send to pad messages"""
        message = msg.encode()
        send_length = str(len(message)).encode()
        send_length += b' ' * (cls.HEADER - len(send_length))
        return send_length

    def send(self, msg):
        """Send messages to the Client"""
        send_length = Dialoghoster._len_message(msg)
        self.conn.send(send_length)
        self.conn.send(msg.encode())

    def recv(self, msg):  # recv messages
        """Recieve the clients response"""
        if msg.startswith("!ACTIONDRAW-"):
            self.playerTurn = True
            self.draw(self.elements_dict_str[(msg.split("-")[1])], self.circle)
            self.playerOpponent_drawings[msg.split("-")[1]] = True
            self.label_drawed[self.elements_dict_str[(msg.split("-")[1])]] = True
            finished = self.is_game_finished()
            if finished[0]:
                if finished[1] == GameStatus.Loose:
                    self.send("!FINISHED-LOST")
                    self.won()
                elif finished[1] == GameStatus.Win:
                    self.send("!FINISHED-WON")
                    self.lost()
                else:
                    self.send("!FINISHED-DRAW")
                    self.draw_()
        elif msg.startswith("!MSG-"):
            self.write(msg.split("-")[1])

    def won(self):
        self.Outputlabel.setText("You have won")
        self.gamedone = True

    def lost(self):
        self.Outputlabel.setText("You have lost")
        self.gamedone = True

    def draw_(self):
        self.Outputlabel.setText("Draw!")
        self.gamedone = True

    @staticmethod
    def await_confirmation(msg):
        confirmation_box = Confirmation(msg)
        if confirmation_box.Dialog.exec_():
            return True
        else:
            return False

    def is_game_finished(self):
        d = {0: GameStatus.Loose, 1: GameStatus.Win}
        for e, u in enumerate([self.playerOwn_drawings, self.playerOpponent_drawings]):
            if all([u["00"], u["10"], u["20"]]):
                return True, d[e]
            elif all([u["01"], u["11"], u["21"]]):
                return True, d[e]
            elif all([u["02"], u["12"], u["22"]]):
                return True, d[e]
            elif all([u["00"], u["01"], u["02"]]):
                return True, d[e]
            elif all([u["10"], u["11"], u["12"]]):
                return True, d[e]
            elif all([u["20"], u["21"], u["22"]]):
                return True, d[e]
            elif all([u["00"], u["11"], u["22"]]):
                return True, d[e]
            elif all([u["20"], u["11"], u["02"]]):
                return True, d[e]
        if all([x or y for x, y in zip(self.playerOpponent_drawings.values(), self.playerOwn_drawings.values())]):
            return True, GameStatus.Draw
        return False, False

    def newGameaction(self):
        if not self.is_game_finished()[0]:
            if self.await_confirmation("Are you sure you want to start a new Game - Old Game isn't completed"):
                self.reset()
                self.send("!NEWGAME")
        else:
            self.reset()
            self.send("!NEWGAME")

    def draw(self, obj: QtWidgets.QLabel, picture: QtGui.QPixmap):
        obj.setPixmap(picture)
        self.Outputlabel.setText("")

    def reset(self):
        for i in self.label_drawed.keys():
            i.setPixmap(self.blanked)
            self.label_drawed[i] = False
        self.playerOpponent_drawings = {"00": False, "01": False, "02": False, "10": False, "11": False, "12": False, "20": False, "21": False, "22": False}
        self.playerOwn_drawings = {"00": False, "01": False, "02": False, "10": False, "11": False, "12": False, "20": False, "21": False, "22": False}
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
        if text.replace(" ", ""):
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
                        self.playerOwn_drawings[self.elements_dict[source]] = True
                        self.send(f"!ACTIONDRAW-{self.elements_dict[source]}")
                        finished = self.is_game_finished()
                        if finished[0]:
                            if finished[1] == GameStatus.Loose:
                                self.send("!FINISHED-LOST")
                                self.won()
                            elif finished[1] == GameStatus.Win:
                                self.send("!FINISHED-WON")
                                self.lost()
                            elif finished[1] == GameStatus.Draw:
                                self.send("!FINISHED-DRAW")
                                self.draw_()
                    else:
                        self.Outputlabel.setText("You can't override an already printed field")
                else:
                    self.Outputlabel.setText("It's not your turn")
            else:
                self.Outputlabel.setText("Game is already finished")
        return super(Dialoghoster, self).eventFilter(source, event)
