from PyQt5 import QtCore, QtGui, QtWidgets
from Confirmation_dialog import Confirmation
from threading import Thread
import socket

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
        self.circle = QtGui.QPixmap("pictures/Kreis.png")
        self.X = QtGui.QPixmap("pictures/X.png")
        self.playerTurn = True
        self.elements_dict_str = {"00": self.l00, "01": self.l01, "02": self.l02, "10": self.l10, "11": self.l11, "12": self.l12, "20": self.l20, "21": self.l21, "22": self.l22}
        self.elements_dict = {self.l00: "00", self.l01: "01", self.l02: "02", self.l10: "10", self.l11: "11", self.l12: "12", self.l20: "20", self.l21: "21", self.l22: "22"}

        self.setupUi()
        self.reset()
        self.Dialog.show()
        Thread(target=self.recv, daemon=True).start()

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

    def _dc(self):
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
        print(msg)
        print(type(self.conn))
        print(type(self.addr))
        self.conn.send(msg.encode())

    def recv(self):  # recv messages
        """Recieve the clients response"""
        while True:
            try:
                msg_length = self.conn.recv(Dialoghoster.HEADER).decode()
                if msg_length:
                    msg = self.conn.recv(int(msg_length)).decode()
                    if msg.startswith("!ACTIONDRAW-"):
                        self.draw(self.elements_dict_str[(msg.split("-")[1])], self.circle)
            except ConnectionError:
                self.conn.close()
                self._dc()
                return
            except Exception as e:
                ui.write(f"Some not connection related Exception occured: {e}", color="red")

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
        text = self.Inputlineedit.text()
        self.Inputlineedit.clear()
        self.write(">>> " + text)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if self.playerTurn:
                if not self.label_drawed[source]:
                    self.draw(source, self.X)
                    self.send(f"!ACTIONDRAW-{self.elements_dict[source]}")
                else:
                    self.Outputlabel.setText("You can't override an already printed field")
            else:
                self.Outputlabel.setText("It's not your turn")
        return super(Dialoghoster, self).eventFilter(source, event)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Dialoghoster()
    sys.exit(app.exec_())
