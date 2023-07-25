from PyQt5.QtWidgets import (QWidget,
                             QLabel,
                             QPushButton,
                             QGridLayout,
                             QVBoxLayout,
                             QDesktopWidget,
                             QApplication)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QPixmap
from textwrap import wrap

# ""


class Message(QWidget):
    # ""
    def __init__(self, title, message, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QGridLayout())
        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet(
            "font-family: 'Roboto', sans-serif; font-size: 14px; font-weight: bold; padding: 0; color: rgb(200, 200, 200);")
        self.messageLabel = QLabel(message, self)
        self.messageLabel.setStyleSheet(
            "font-family: 'Roboto', sans-serif; font-size: 12px; font-weight: normal; padding: 0; color: rgb(200, 200, 200);")
        self.buttonClose = QPushButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap("YtExtraFiles/close.png"), QIcon.Normal, QIcon.Off)
        self.buttonClose.setIcon(icon)
        self.buttonClose.setFlat(True)
        self.buttonClose.setFixedSize(16, 16)
        self.layout().addWidget(self.titleLabel, 0, 0)
        self.layout().addWidget(self.messageLabel, 1, 0)
        self.layout().addWidget(self.buttonClose, 0, 1, 2, 1)

# ""


class Notification(QWidget):
    doubleClick = pyqtSignal(int)
    # ""

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint | Qt.ToolTip)
        resolution = QDesktopWidget().screenGeometry(-1)
        self.screenWidth = resolution.width()
        self.screenHeight = resolution.height()
        self.nMessages = 0
        self.setStyleSheet("background-color: #202020;")
        self.mainLayout = QVBoxLayout(self)

    # ""
    def set_notify(self, title, message):
        if len(message) > 42:
            w = wrap(message, 42, break_long_words=True)
            message = f"{w[0]}..."

        m = Message(title, message, self)
        self.mainLayout.addWidget(m)
        m.buttonClose.clicked.connect(self.on_clicked)
        self.nMessages += 1
        self.show()
        width = self.frameGeometry().width()
        self.move(self.screenWidth - width - 30, 30)

    # ""
    def on_clicked(self):
        self.mainLayout.removeWidget(self.sender().parent())
        
        # if self.sender().parent() is not None:
        #     self.sender().parent().deleteLater()

        # else:
        #     self.mainLayout.clearLayout(self.sender().parent())

        self.nMessages -= 1
        self.adjustSize()
        if self.nMessages == 0:
            self.close()

    # ""
    def mouseDoubleClickEvent(self, event):
        self.doubleClick.emit(1)



if __name__ == '__main__':
    import sys
    class Example(QWidget):
        counter = 0

        def __init__(self, parent=None):
            QWidget.__init__(self, parent)
            self.setLayout(QVBoxLayout())
            btn = QPushButton("Send Notify", self)
            self.layout().addWidget(btn)

            self.notification = Notification()
            btn.clicked.connect(self.notify)


        def notify(self):
            self.counter += 1
            print(self.counter)
            self.notification.set_notify("Title{}".format(self.counter),
                                        "messageeeeeeeee{}".format(self.counter))

    
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())