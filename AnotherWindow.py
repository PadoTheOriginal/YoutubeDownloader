# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnotherWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(QtWidgets.QWidget):
    def init(self):
        super(Ui_Form, self).__init__()
        self.setupUi(self)
        self.setObjectName("Form")
        self.resize(707, 430)
        self.setWindowTitle("Pesquisa")
        self.setStyleSheet("background-color: #181818;")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainWidget = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainWidget.sizePolicy().hasHeightForWidth())
        self.mainWidget.setSizePolicy(sizePolicy)
        self.mainWidget.setMinimumSize(QtCore.QSize(0, 220))
        self.mainWidget.setObjectName("mainWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.mainWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.image = QtWidgets.QWidget(self.mainWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setMinimumSize(QtCore.QSize(360, 202))
        self.image.setStyleSheet("background-image: url(:/image/hq720.jpg);\n"
"background-size: cover;")
        self.image.setObjectName("image")
        self.horizontalLayout_2.addWidget(self.image)
        self.video = QtWidgets.QWidget(self.mainWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video.sizePolicy().hasHeightForWidth())
        self.video.setSizePolicy(sizePolicy)
        self.video.setObjectName("video")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.video)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title = QtWidgets.QLabel(self.video)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setStyleSheet("color: white;")
        self.title.setText("Hopsin - Alone With Me")
        self.title.setObjectName("title")
        self.verticalLayout_2.addWidget(self.title)
        self.videoInfo = QtWidgets.QLabel(self.video)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.videoInfo.setFont(font)
        self.videoInfo.setStyleSheet("color: white;")
        self.videoInfo.setText("2.1M views - 4 days ago")
        self.videoInfo.setObjectName("videoInfo")
        self.verticalLayout_2.addWidget(self.videoInfo)
        self.channel = QtWidgets.QLabel(self.video)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.channel.setFont(font)
        self.channel.setStyleSheet("color: white;")
        self.channel.setText("Hopsintv")
        self.channel.setObjectName("channel")
        self.verticalLayout_2.addWidget(self.channel)
        self.description = QtWidgets.QLabel(self.video)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.description.setFont(font)
        self.description.setStyleSheet("color: white;")
        self.description.setText("Hopsin\'s new single ALONE WITH ME available everywhere:\n"
        "https://ffm.to/-alonewithme​\n"
        "")
        self.description.setObjectName("description")
        self.verticalLayout_2.addWidget(self.description)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.downloadBtn = QtWidgets.QPushButton(self.video)
        self.downloadBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.downloadBtn.setStyleSheet("QToolTip {\n"
        "color: white;\n"
        "}\n"
        " * {\n"
        "background-color: #202020;\n"
        "color: rgb(200, 200, 200);\n"
        "}\n"
        "")
        self.downloadBtn.setText("Baixar")
        self.downloadBtn.setObjectName("downloadBtn")
        self.verticalLayout_2.addWidget(self.downloadBtn)
        self.horizontalLayout_2.addWidget(self.video)
        self.verticalLayout.addWidget(self.mainWidget)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)

        QtCore.QMetaObject.connectSlotsByName(Form)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = Ui_Form()
    Form.show()
    sys.exit(app.exec_())