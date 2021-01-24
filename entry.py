from queue import Empty, Queue
from threading import Thread
from PyQt5 import QtCore, QtWidgets
import socket
from playinghost import Dialoghoster
from playing import Dialogplaying
from time import sleep

class Client:
    HEADER = 64
    PORT = 8744
    DISCONNECT_MSG = "#!DC#"
    CONNECT_MSG = "#!CONNECTED#"

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.rv = Queue()
        Thread(target=self.recv, daemon=True).start()
        self.send(Client.CONNECT_MSG)

    @classmethod
    def _len_message(cls, msg):
        message = msg.encode()
        send_length = str(len(message)).encode()
        send_length += b' ' * (cls.HEADER - len(send_length))
        return send_length

    def send(self, msg):
        send_length = Client._len_message(msg)
        self.conn.send(send_length)
        self.conn.send(msg.encode())

    def recv(self):
        while True:
            try:
                msg_length = self.conn.recv(Client.HEADER).decode()
                if msg_length:
                    self.rv.put(self.conn.recv(int(msg_length)).decode())
            except ConnectionError:
                self.conn.close()
                return
            except Exception as e:
                print(f"Some not connection related Exception occured: {e}")

    def rv_catch_timeout(self):
        try:
            return self.rv.get(block=True, timeout=5)
        except Empty:
            # ui.write("Code 408: Timeout-error", color="red") TODO
            return False

    def __repr__(self):
        return "Client(conn, addr)"


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
        ADDR = (socket.gethostbyname(socket.gethostname()), 9312)
        if self.hosting:
            self.connectionstatusbttn.setText(f"Hoste Server auf {ADDR}")
            return
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectionstatusbttn.setText(f"Hoste Server auf {ADDR}")
        server.bind(ADDR)
        self.hosting = True

        def inner():
            server.listen(1)
            conn, addr = server.accept()
            dialog = Dialoghoster(conn, addr)
            dialog.Dialog.show()
            dialog.Dialog.exec_()

        Thread(target=inner, daemon=True).start()

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
            def inner():
                while self.connecting:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        client.connect((ADDR[0], int(ADDR[1])))
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect(ADDR)
                    except ConnectionResetError:
                        self.connectionstatusbttn.setText("Your opponent disconnected")
                        client.shutdown(socket.SHUT_RDWR)
                        client.close()
                    except ConnectionRefusedError:
                        self.connectionstatusbttn.setText("Waiting for Connection")
                    except TimeoutError:
                        self.connectionstatusbttn.setText("Timeout Error - maybe change IP")
                    except Exception:
                        self.connectionstatusbttn.setText("Input should be in format: IP, Port")
                        return
                    else:
                        self.run_connected(client)
                    finally:
                        sleep(0.5)

            Thread(target=inner, daemon=True).start()
        else:
            self.connectionstatusbttn.setText("Input should be in format: IP, Port")

    def run_connected(self, client):
        dialog = Dialogplaying(client)
        print("init ui")
        dialog.Dialog.show()
        dialog.Dialog.exec_()

    def on_abort(self):
        self.connecting = True


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Entry()
    sys.exit(app.exec_())
