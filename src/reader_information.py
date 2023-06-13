import sys
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QLabel, QLineEdit,
                             QToolButton, QGroupBox, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
try:
    from src import database
except:
    import database


class readerInfo(QGroupBox):
    after_close = pyqtSignal(dict)

    def __init__(self, stu_info: dict):
        super().__init__()
        self.stu_info = stu_info

        self.title = QLabel()
        self.title.setText('学生信息')

        self.rid = QLabel()
        self.rid.setText('学号')

        self.rname = QLabel()
        self.rname.setText('姓名')

        self.email = QLabel()
        self.email.setText('邮箱')

        self.pwd = QLabel()
        self.pwd.setText('密码')

        self.repwd = QLabel()
        self.repwd.setText('重复密码')
        # 学号输入框
        self.SIDInput = QLineEdit()
        self.SIDInput.setFixedSize(400, 40)
        self.SIDInput.setText(self.stu_info['ID'])
        self.SIDInput.initText = '请输入学号'
        self.SIDInput.setEnabled(False)

        # 姓名输入框
        self.nameInput = QLineEdit()
        self.nameInput.setFixedSize(400, 40)
        self.nameInput.setText(self.stu_info['NAME'])
        self.nameInput.initText = '请输入姓名'
        self.nameInput.setTextMargins(5, 5, 5, 5)
        self.nameInput.mousePressEvent = lambda x: self.inputClick(self.
                                                                   nameInput)
        # 邮箱
        self.emailInput = QLineEdit()
        self.emailInput.setFixedSize(400, 40)
        self.emailInput.setText(str(self.stu_info['EMAIL']))
        self.emailInput.initText = '请输入邮箱'
        self.emailInput.setTextMargins(5, 5, 5, 5)
        self.emailInput.mousePressEvent = lambda x: self.inputClick(self.
                                                                    emailInput)

        # 密码
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setFixedSize(400, 40)
        self.passwordInput.setText('请输入密码')
        self.passwordInput.initText = '请输入密码'
        self.passwordInput.setTextMargins(5, 5, 5, 5)
        self.passwordInput.mousePressEvent = lambda x: self.inputClick(
            self.passwordInput)

        # 重复密码
        self.repPasswordInput = QLineEdit()
        self.repPasswordInput.setEchoMode(QLineEdit.Password)
        self.repPasswordInput.setFixedSize(400, 40)
        self.repPasswordInput.setText('请重复输入密码')
        self.repPasswordInput.initText = '请重复输入密码'
        self.repPasswordInput.setTextMargins(5, 5, 5, 5)
        self.repPasswordInput.mousePressEvent = lambda x: self.inputClick(
            self.repPasswordInput)

        # 提交
        self.submit = QToolButton()
        self.submit.setText('提交')
        self.submit.setFixedSize(400, 40)
        self.submit.clicked.connect(self.submitFunction)

        # 退出
        self.back = QToolButton()
        self.back.setText('退出')
        self.back.setFixedSize(400, 40)
        self.back.clicked.connect(self.close)

        self.btnList = [
            self.SIDInput, self.nameInput, self.emailInput, self.passwordInput,
            self.repPasswordInput
        ]

        self.lableList = [
            self.rid, self.rname, self.email, self.pwd, self.repwd
        ]

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.addWidget(self.title)
        for i in range(0, len(self.btnList)):
            self.bodyLayout.addWidget(self.lableList[i])
            self.bodyLayout.addWidget(self.btnList[i])
        self.bodyLayout.addWidget(self.submit)
        self.bodyLayout.addWidget(self.back)

        self.setLayout(self.bodyLayout)
        self.initUI()

    def inputClick(self, e):
        for item in self.btnList:
            if item.text() == '':
                item.setText(item.initText)
        if e.text() == e.initText:
            e.setText('')

    def submitFunction(self):
        if self.passwordInput.text() != self.passwordInput.initText:
            if self.passwordInput.text() != self.repPasswordInput.text():
                msgBox = QMessageBox(QMessageBox.Warning, "错误!", '两次输入密码不一致!',
                                     QMessageBox.NoButton, self)
                msgBox.addButton("确认", QMessageBox.AcceptRole)
                msgBox.exec_()
                return
            self.stu_info['PWD'] = database.encrypt(self.passwordInput.text())
        self.stu_info['NAME'] = self.nameInput.text()
        self.stu_info['EMAIL'] = self.emailInput.text()
        self.close()
        self.after_close.emit(self.stu_info)

    def initUI(self):
        self.setFixedSize(422, 500)
        self.setWindowTitle('编辑学生信息')


if __name__ == '__main__':
    stu_msg = temp = {
        'ID': '201602',
        'NAME': '小王',
        'EMAIL': 'b@mail.ustc.edu.cn',
        'PWD': '123456'
    }
    app = QApplication(sys.argv)
    ex = readerInfo(stu_msg)
    ex.show()
    sys.exit(app.exec_())
