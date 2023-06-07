import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QHBoxLayout, QLabel, QLineEdit, QToolButton,
                             QPushButton)
from PyQt5.QtCore import Qt


class Login(QWidget):

    def __init__(self):
        super().__init__()
        self.bodyLayout = QGridLayout()

        # 欢迎登陆图书馆系统标题
        self.titleText = QLabel(self)
        self.titleText.setText('欢迎使用图书馆管理系统')
        self.titleText.setAlignment(Qt.AlignCenter)
        self.titleText.setFixedSize(480, 60)

        # 账号标题
        account = QLabel()
        account.setText('账号')

        # 密码标题
        password = QLabel()
        password.setText('密码')

        # 学号输入框
        self.accountInput = QLineEdit()
        self.accountInput.setFixedSize(400, 50)
        self.accountInput.setText('账号')
        self.accountInput.setTextMargins(5, 5, 5, 5)
        self.accountInput.mousePressEvent = lambda x: self.inputClick(
            self.accountInput)
        # 密码输入框
        self.passwordInput = QLineEdit()
        self.passwordInput.setFixedSize(400, 50)
        self.passwordInput.setText('******')
        self.passwordInput.setTextMargins(5, 5, 5, 5)
        self.passwordInput.mousePressEvent = lambda x: self.inputClick(
            self.passwordInput)
        self.passwordInput.setEchoMode(QLineEdit.Password)

        # 注册按钮
        self.signupButton = QPushButton()
        self.signupButton.setText('注 册')
        self.signupButton.setFixedSize(100, 60)

        # 登录按钮
        self.loginButton = QToolButton()
        self.loginButton.setText('登  录')
        self.loginButton.setFixedSize(100, 60)

        # 注册和登录按钮合并在一行(水平布局)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.signupButton)
        self.buttonLayout.addWidget(self.loginButton)

        self.buttonBox = QWidget()
        self.buttonBox.setObjectName('buttonBox')
        self.buttonBox.setContentsMargins(10, 10, 10, 10)
        self.buttonBox.setFixedSize(350, 90)
        self.buttonBox.setLayout(self.buttonLayout)

        # 把上面定义的元素加入大框
        self.inputBoxLayout = QVBoxLayout()
        self.inputBoxLayout.addWidget(account)
        self.inputBoxLayout.addWidget(self.accountInput)
        self.inputBoxLayout.addWidget(password)
        self.inputBoxLayout.addWidget(self.passwordInput)
        self.inputBoxLayout.addWidget(self.buttonBox)

        # 下面一个大框
        self.inputBox = QWidget()
        self.inputBox.setObjectName('inputBox')
        self.inputBox.setContentsMargins(30, 30, 30, 30)
        self.inputBox.setFixedSize(480, 350)
        self.inputBox.setLayout(self.inputBoxLayout)

        # 把大标题和下面输入框加入self
        self.bodyLayout.addWidget(self.titleText, 0, 0)
        self.bodyLayout.addWidget(self.inputBox, 1, 0)
        self.setLayout(self.bodyLayout)
        self.setFixedSize(500, 450)

    def inputClick(self, e):
        if e.text() == '账号' or e.text() == '******':
            e.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())
