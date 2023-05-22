import sys
from src import database
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QLabel, QLineEdit, QToolButton, QGroupBox)


class Signup(QGroupBox):
    def __init__(self):
        super().__init__()

        self.title = QLabel()
        self.title.setText('注册账号')

        account = QLabel()
        account.setText('学号')
        
        email=QLabel()
        email.setText('邮箱')

        name = QLabel()
        name.setText('姓名')

        password = QLabel()
        password.setText('密码')

        repPassword = QLabel()
        repPassword.setText('重复密码')

        # 学号输入框
        self.accountInput = QLineEdit()
        self.accountInput.setFixedSize(400, 40)
        self.accountInput.setText('输入学号')
        self.accountInput.initText = '输入学号'
        self.accountInput.setTextMargins(5, 5, 5, 5)
        self.accountInput.mousePressEvent = lambda x: self.inputClick(self.accountInput)

        # 邮箱输入框
        self.emailInput=QLineEdit()
        self.emailInput.setFixedSize(400,40)
        self.emailInput.setText('输入邮箱')
        self.emailInput.initText='输入邮箱'
        self.emailInput.setTextMargins(5,5,5,5)
        self.emailInput.mousePressEvent = lambda x: self.inputClick(self.emailInput)

        # 姓名输入框
        self.nameInput = QLineEdit()
        self.nameInput.setFixedSize(400, 40)
        self.nameInput.setText('输入姓名')
        self.nameInput.initText = '输入姓名'
        self.nameInput.setTextMargins(5, 5, 5, 5)
        self.nameInput.mousePressEvent = lambda x: self.inputClick(self.nameInput)

        # 密码
        self.passwordInput = QLineEdit()
        self.passwordInput.setFixedSize(400, 40)
        self.passwordInput.setText('输入密码')
        self.passwordInput.initText = '输入密码'
        self.passwordInput.setTextMargins(5, 5, 5, 5)
        self.passwordInput.mousePressEvent = lambda x: self.inputClick(self.passwordInput)

        # 重复密码
        self.repPasswordInput = QLineEdit()
        self.repPasswordInput.setFixedSize(400, 40)
        self.repPasswordInput.setText('重复输入密码')
        self.repPasswordInput.initText = '重复输入密码'
        self.repPasswordInput.setTextMargins(5, 5, 5, 5)
        self.repPasswordInput.mousePressEvent = lambda x: self.inputClick(self.repPasswordInput)

        # 注册
        self.submit = QToolButton()
        self.submit.setText('注册')
        self.submit.setFixedSize(400, 40)

        # 返回
        self.back = QToolButton()
        self.back.setText('返回')
        self.back.setFixedSize(400, 40)

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.addWidget(self.title)
        self.bodyLayout.addWidget(self.accountInput)
        self.bodyLayout.addWidget(self.emailInput)
        self.bodyLayout.addWidget(self.nameInput)
        self.bodyLayout.addWidget(self.passwordInput)
        self.bodyLayout.addWidget(self.repPasswordInput)
        self.bodyLayout.addWidget(self.submit)
        self.bodyLayout.addWidget(self.back)

        self.setLayout(self.bodyLayout)
        self.initUI()

    def inputClick(self, e):
        for i in range(1, 6):
            item = self.bodyLayout.itemAt(i).widget()
            if item.text() == '':
                item.setText(item.initText)
                if item is self.passwordInput or item is self.repPasswordInput:
                    item.setEchoMode(QLineEdit.Normal)

        if e.text() == e.initText:
            e.setText('')
        if e is self.passwordInput or e is self.repPasswordInput:
            e.setEchoMode(QLineEdit.Password)

    def initUI(self):
        self.setFixedSize(422, 500)
        self.setWindowTitle('注册')

    def getInfo(self):
        for i in range(1, 6):
            item = self.bodyLayout.itemAt(i).widget()
            if item.text() == item.initText:
                item.setText('')

        info = {
            'SID': self.accountInput.text(),
            'PASSWORD': self.passwordInput.text(),
            'REPASSWORD': self.repPasswordInput.text(),
            'SNAME': self.nameInput.text(),
            'EMAIL': self.emailInput.text(),
            'PUNISHED': 0
        }
        return info

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Signup()
    ex.show()
    sys.exit(app.exec_())
