# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sys
import os

firstarg=sys.argv[1]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        font = QtGui.QFont()
        font.setFamily("Nimbus Roman No9 L")
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalFrame = QtWidgets.QFrame(self.centralwidget)
        self.verticalFrame.setMinimumSize(QtCore.QSize(350, 0))
        self.verticalFrame.setMaximumSize(QtCore.QSize(350, 16777215))
        self.verticalFrame.setAutoFillBackground(False)
        self.verticalFrame.setStyleSheet("background-color: rgb(230, 230, 230)")
        self.verticalFrame.setObjectName("verticalFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Nimbus Roman No9 L")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.horizontalLayout.addWidget(self.verticalFrame)
        self.buttonFrame = QtWidgets.QFrame(self.centralwidget)
        self.buttonFrame.setAutoFillBackground(False)
        self.buttonFrame.setObjectName("buttonFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.buttonFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.liveButton = QtWidgets.QPushButton(self.buttonFrame)
        self.liveButton.setMinimumSize(QtCore.QSize(320, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.liveButton.setFont(font)
        self.liveButton.setObjectName("liveButton")
        #self.liveButton.clicked.connect(self.openLive) 
        self.verticalLayout.addWidget(self.liveButton, 0, QtCore.Qt.AlignHCenter)
        self.openButton = QtWidgets.QPushButton(self.buttonFrame)
        self.openButton.setMinimumSize(QtCore.QSize(320, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.openButton.setFont(font)
        self.openButton.setObjectName("openButton")
        self.openButton.clicked.connect(self.openFileNameDialog)    
        self.verticalLayout.addWidget(self.openButton, 0, QtCore.Qt.AlignHCenter)
        self.facesButton = QtWidgets.QPushButton(self.buttonFrame)
        self.facesButton.setMinimumSize(QtCore.QSize(320, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.facesButton.setFont(font)
        self.facesButton.setObjectName("facesButton")
        self.verticalLayout.addWidget(self.facesButton, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.logoutButton = QtWidgets.QPushButton(self.buttonFrame)
        self.logoutButton.setMinimumSize(QtCore.QSize(320, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.logoutButton.setFont(font)
        self.logoutButton.setObjectName("logoutButton")
        self.logoutButton.clicked.connect(self.logout)  
        self.verticalLayout.addWidget(self.logoutButton, 0, QtCore.Qt.AlignHCenter)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.buttonFrame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Nome de Usuário"))
        self.liveButton.setText(_translate("MainWindow", "Live"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.facesButton.setText(_translate("MainWindow", "Faces"))
        self.logoutButton.setText(_translate("MainWindow", "Logout"))
        self.label.setText(_translate("MainWindow", "Olá, "+firstarg))

    def openFileNameDialog(self):
        # abre pra escolher o arquivo
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
       	import os 
        MainWindow.hide()
        os.system("python3 interface_recog_file.py " + fileName)
        MainWindow.show()
        

    #def openLive(self):
    	#MainWindow.hide()
        #os.system("python3 video.py")
        #MainWindow.show()

    def logout(self):
        MainWindow.hide()
        import os 
        os.system("python3 login.py")
        sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

