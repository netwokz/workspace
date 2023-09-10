import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton
from PyQt6.QtCore import pyqtSlot
from ping_test import ping

class App(QWidget):
    servers = ["10.79.217.11","10.79.217.12"]

    def __init__(self):
        super().__init__()
        self.title = 'Ping Me'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400
        self.initUI()

    def click():
        print("Hy Button is clicked!")

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('Button',self)
        button.setText("Ping")
        button.move(50,50)
        button.clicked.connect(self.click)

        self.label = QLabel(self)
        self.label.adjustSize()
        self.label.move(100, 100)
        
        self.show()

    @pyqtSlot()
    def click(self):
        is_online = ping(self.servers[0])
        if is_online:
            self.label.setStyleSheet('border: 1px solid black; color: green')
            self.label.setText('Online')
        else:
            self.label.setStyleSheet('border: 1px solid black; color: red')
            self.label.setText('Offline')
        self.label.adjustSize()
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())