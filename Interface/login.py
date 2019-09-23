# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testeqt.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 237)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 70, 58, 18))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 58, 18))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(150, 20, 141, 31))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(80, 70, 251, 21))
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit.setPlaceholderText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 110, 251, 21))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 170, 88, 34))
        self.pushButton.setCheckable(False)
        self.pushButton.setChecked(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.verifica_senha)                                                                    
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(0, 140, 401, 20))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.actionVerificaSenha = QtWidgets.QAction(Dialog)
        self.actionVerificaSenha.setObjectName("actionVerificaSenha")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    #aplica os textos nas labels
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login"))
        self.label.setText(_translate("Dialog", "Nome:"))
        self.label_2.setText(_translate("Dialog", "Senha:"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Dados do Usuário</span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Login"))
        self.actionVerificaSenha.setText(_translate("Dialog", "VerificaSenha"))
        
    #verifica senha tela 1
    def verifica_senha(self):  
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        if self.lineEdit.text() == "adm123" and self.lineEdit_2.text() == "adm123":
            self.label_4.setText(_translate("Dialog", "Entrou cornao"))
            Dialog.hide()
            import os 
            os.system("python3 main.py " + self.lineEdit.text())
            sys.exit(app.exec_())

        else:
            self.label_4.setText(_translate("Dialog", "Senha Incorreta!"))
            
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    
    
    sys.exit(app.exec_())
