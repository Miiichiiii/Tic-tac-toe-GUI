from PyQt5 import QtCore, QtWidgets
import socket
from playing import Dialogplaying
from playinghost import Dialoghoster
from time import sleep


class WorkerThread(QtCore.QThread):
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, server):
        QtCore.QThread.__init__(self)
        self.server = server

    def run(self):
        self.server.listen(1)
        conn, addr = self.server.accept()
        self.signal.emit((conn, addr))


class WorkerThreadPlaying(QtCore.QThread):
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, ADDR, instance):
        QtCore.QThread.__init__(self)
        self.instance = instance
        self.ADDR = ADDR

    def run(self):
        while self.instance.connecting:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((self.ADDR[0], int(self.ADDR[1])))
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(self.ADDR)
            except ConnectionResetError:
                self.instance.connectionstatusbttn.setText("Your opponent disconnected")
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            except ConnectionRefusedError:
                self.instance.connectionstatusbttn.setText("Waiting for Connection")
            except TimeoutError:
                self.instance.connectionstatusbttn.setText("Timeout Error - maybe change IP")
            except Exception:
                self.instance.connectionstatusbttn.setText("Input should be in format: IP, Port")
                return
            else:
                self.signal.emit(client)
            finally:
                sleep(0.5)


class Entry(object):
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.hostbttn = QtWidgets.QPushButton(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.connectionstatusbttn = QtWidgets.QLabel(self.centralwidget)
        self.abortbttn = QtWidgets.QPushButton(self.centralwidget)
        self.connectbttn = QtWidgets.QPushButton(self.centralwidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.inputip = QtWidgets.QLineEdit(self.centralwidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.Multiplayerlabel = QtWidgets.QLabel(self.centralwidget)
        self.newGame = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.hosting = False
        self.connecting = False

        self.setupUi()
        self.MainWindow.show()

    def setupUi(self):
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(248, 156)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout.setObjectName("verticalLayout")
        self.newGame.setObjectName("newGame")
        self.verticalLayout.addWidget(self.newGame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Multiplayerlabel.setObjectName("Multiplayerlabel")
        self.verticalLayout_2.addWidget(self.Multiplayerlabel)
        self.inputip.setObjectName("inputip")
        self.verticalLayout_2.addWidget(self.inputip)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.hostbttn.setObjectName("hostbttn")
        self.horizontalLayout_2.addWidget(self.hostbttn)
        self.connectbttn.setObjectName("connectbttn")
        self.horizontalLayout_2.addWidget(self.connectbttn)
        self.abortbttn.setObjectName("abortbttn")
        self.horizontalLayout_2.addWidget(self.abortbttn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.connectionstatusbttn.setObjectName("connectionstatusbttn")
        self.verticalLayout_2.addWidget(self.connectionstatusbttn)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        self.hostbttn.clicked.connect(self.on_host_click)
        self.connectbttn.clicked.connect(self.on_connect_click)

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        self.MainWindow.setWindowTitle("Tic Tac Toe")
        self.newGame.setText("Neues Lokales Spiel")
        self.Multiplayerlabel.setText("Multiplayer Spiel")
        self.inputip.setToolTip("<html><head/><body><p>Hier IP und Port des gegenüber eingeben</p></body></html>")
        self.hostbttn.setText("Host")
        self.connectbttn.setText("Connect")
        self.abortbttn.setText("Abbrechen")
        self.connectionstatusbttn.setText("Warte auf Verbindung...")

    def on_host_click(self):
        self.connecting = False
        # text = self.inputip.text() TODO
        # self.inputip.clear()
        ADDR = (socket.gethostbyname(socket.gethostname()), 9312)
        if self.hosting:
            self.connectionstatusbttn.setText(f"Hoste Server auf {ADDR}")
            return
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectionstatusbttn.setText(f"Hoste Server auf {ADDR}")
        server.bind(ADDR)
        self.hosting = True

        def start(client):
            dialog = Dialoghoster(*client)
            dialog.Dialog.show()
            dialog.Dialog.exec_()

        thread = WorkerThread(server)
        thread.start()
        thread.signal.connect(start)

    def on_connect_click(self):
        text = self.inputip.text()
        self.inputip.clear()
        ADDR = text.replace(" ", "").split(",")
        try:
            ADDR = (ADDR[0], int(ADDR[1]))
        except Exception:
            self.connectionstatusbttn.setText("Input should be in format: IP, Port")
            return
        self.connecting = True
        if len(ADDR) == 2:
            pass
            thread = WorkerThreadPlaying(ADDR, self)
            thread.start()
            thread.signal.connect(self.run_connected)
        else:
            self.connectionstatusbttn.setText("Input should be in format: IP, Port")

    @staticmethod
    def run_connected(client):
        dialog = Dialogplaying(client)
        dialog.Dialog.show()
        dialog.Dialog.exec_()

    def on_abort(self):
        self.connecting = True


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Entry()
    sys.exit(app.exec_())
