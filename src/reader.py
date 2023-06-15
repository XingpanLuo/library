# import sys
# import time
import os
# import typing
# from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QGridLayout, QGroupBox, QToolButton,
                             QSplitter, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QAbstractItemView,
                             QLineEdit, QFileDialog, QMessageBox, QComboBox)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize
from src import database
# from src import reader_information
# from src import book_information
# import database
# import reader_information
# import book_information


class readerPage(QWidget):

    def __init__(self, info):
        super().__init__()
        self.info = info
        self.focus = 0
        self.initUI()

    def initUI(self):
        # 标题栏
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(1250, 50)
        self.setTitleBar()

        # 分割
        self.body = QSplitter()
        self.setLeftMunu()
        self.content = None
        self.setContent()

        self.bodyLayout = QGridLayout()
        self.bodyLayout.addWidget(self.titleBar, 0, 0, 1, 7)
        self.bodyLayout.addWidget(self.body, 1, 0, 7, 7)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.bodyLayout)
        self.setFixedSize(1280, 720)
        self.setMyStyle()

    # 设置标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('图书馆管理系统--读者页面')
        self.title.setFixedHeight(30)

        self.account = QToolButton()
        # self.account.setIcon(QIcon('icon/person.png'))
        self.account.setText(self.info['ID'])
        self.account.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.account.setFixedHeight(20)
        self.account.setEnabled(False)

        self.out = QToolButton()
        self.out.setText('退出')
        self.out.setFixedHeight(30)

        titleLayout = QHBoxLayout()
        titleLayout.addSpacing(100)
        titleLayout.addWidget(self.title)
        titleLayout.addWidget(self.account)
        titleLayout.addWidget(self.out)
        self.titleBar.setLayout(titleLayout)

    # 左侧菜单栏
    def setLeftMunu(self):
        # 书籍管理
        self.bookManage = QToolButton()
        self.bookManage.setText('书籍查询')
        self.bookManage.setFixedSize(160, 50)
        self.bookManage.setIcon(QIcon('icon/book.png'))
        self.bookManage.setIconSize(QSize(30, 30))
        self.bookManage.clicked.connect(
            lambda: self.switch(0, self.bookManage))
        self.bookManage.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 读者管理
        self.borrowManage = QToolButton()
        self.borrowManage.setText('借阅历史')
        self.borrowManage.setFixedSize(160, 50)
        self.borrowManage.setIcon(QIcon('icon/detial.png'))
        self.borrowManage.setIconSize(QSize(30, 30))
        self.borrowManage.clicked.connect(
            lambda: self.switch(1, self.borrowManage))
        self.borrowManage.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 借阅日志
        self.readerInfo = QToolButton()
        self.readerInfo.setText('个人信息')
        self.readerInfo.setFixedSize(160, 50)
        self.readerInfo.setIcon(QIcon('icon/history.png'))
        self.readerInfo.setIconSize(QSize(30, 30))
        self.readerInfo.clicked.connect(
            lambda: self.switch(2, self.readerInfo))
        self.readerInfo.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 借阅日志
        self.refreshInfo = QToolButton()
        self.refreshInfo.setText('刷新信息')
        self.refreshInfo.setFixedSize(160, 50)
        self.refreshInfo.setIcon(QIcon('icon/history.png'))
        self.refreshInfo.setIconSize(QSize(30, 30))
        self.refreshInfo.clicked.connect(
            lambda: self.switch(3, self.refreshInfo))
        self.refreshInfo.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.btnList = [
            self.bookManage, self.borrowManage, self.readerInfo,
            self.refreshInfo
        ]

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.bookManage)
        self.layout.addWidget(self.borrowManage)
        self.layout.addWidget(self.readerInfo)
        self.layout.addWidget(self.refreshInfo)
        self.layout.addStretch()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.menu = QGroupBox()
        self.menu.setFixedSize(160, 500)
        self.menu.setLayout(self.layout)
        self.menu.setContentsMargins(0, 0, 0, 0)
        self.body.addWidget(self.menu)

    def switch(self, index, btn):
        self.focus = index
        self.setContent()

    # 设置右侧信息页
    def setContent(self):
        pages = [
            BookSearch(self.info['ID']),
            ReaderBorrowHistory(self.info['ID']),
            SelfInfo(self.info['ID'])
        ]
        if self.content is not None:
            self.content.deleteLater()
        if self.focus == 0:
            self.content = pages[0]
        elif self.focus == 1:
            # pages[1].refresh()
            self.content = pages[1]
        elif self.focus == 2:
            # pages[2].refresh()
            self.content = pages[2]
        elif self.focus == 3:
            self.content = pages[0]
            pages[1].refresh()
            pages[2].refresh()
        self.body.addWidget(self.content)

    def setMyStyle(self):
        pass


# 书籍查询
class BookSearch(QGroupBox):

    def __init__(self, SID: str):
        super().__init__()
        self.book_list = []
        self.body = QVBoxLayout()
        self.table = None
        self.SID = SID
        self.setSearchBar()
        self.searchFunction()

        self.setLayout(self.body)
        self.initUI()

    # 设置搜索框
    def setSearchBar(self):
        self.selectBox = QComboBox()
        self.selectBox.addItems(['书号', '作者', '书名'])
        self.selectBox.setFixedHeight(30)
        self.searchTitle = QLabel()
        self.searchTitle.setText('搜索书籍')
        self.searchInput = QLineEdit()
        self.searchInput.setText('')
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setFixedSize(400, 40)
        self.searchButton = QToolButton()
        self.searchButton.setFixedSize(100, 40)
        self.searchButton.setText('搜索')
        self.searchButton.clicked.connect(self.searchFunction)
        searchLayout = QHBoxLayout()
        searchLayout.addStretch()
        searchLayout.addWidget(self.selectBox)
        searchLayout.addWidget(self.searchTitle)
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addStretch()
        self.searchWidget = QWidget()
        self.searchWidget.setLayout(searchLayout)
        self.body.addWidget(self.searchWidget)

    # 搜索方法
    def searchFunction(self):
        convert = {'书号': 'ID', '作者': 'author', '书名': 'name', '': 'name'}
        self.book_list = database.search_book(
            self.searchInput.text(), convert[self.selectBox.currentText()])
        if self.book_list == []:
            print('未找到')
        if self.table is not None:
            self.table.deleteLater()
        self.setTable()

    # 设置表格
    def setTable(self):
        self.table = QTableWidget(1, 7)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(7, 85)

        self.table.setItem(0, 0, QTableWidgetItem('书号'))
        self.table.setItem(0, 1, QTableWidgetItem('书名'))
        self.table.setItem(0, 2, QTableWidgetItem('作者'))
        self.table.setItem(0, 3, QTableWidgetItem('价格'))
        self.table.setItem(0, 4, QTableWidgetItem('状态'))
        self.table.setItem(0, 5, QTableWidgetItem('借阅数'))
        self.table.setItem(0, 6, QTableWidgetItem('操作'))
        for i in range(7):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))

        # 显示借阅详情
        for i in self.book_list:
            self.insertRow(i)
        self.body.addWidget(self.table)

    # 插入行
    def insertRow(self, val: list):
        print(val)
        itemBID = QTableWidgetItem(val[0])
        itemBID.setTextAlignment(Qt.AlignCenter)

        itemNAME = QTableWidgetItem('《' + val[1] + '》')
        itemNAME.setTextAlignment(Qt.AlignCenter)

        itemAUTHOR = QTableWidgetItem(val[2])
        itemAUTHOR.setTextAlignment(Qt.AlignCenter)

        itemPRICE = QTableWidgetItem(str(val[3]))
        itemPRICE.setTextAlignment(Qt.AlignCenter)

        status_str = ""
        if val[4] == 0:
            status_str = "可借"
        elif val[4] == 1:
            status_str = "借出"
        elif val[4] == 2:
            status_str = "借出且被预约"
        elif val[4] == 3:
            status_str = "在馆且被预约"
        itemSTATUS = QTableWidgetItem(status_str)
        itemSTATUS.setTextAlignment(Qt.AlignCenter)

        itemSUM = QTableWidgetItem(str(val[5]))
        itemSUM.setTextAlignment(Qt.AlignCenter)

        itemBorrow = QToolButton(self.table)
        itemBorrow.setFixedSize(75, 25)
        if val[4] == 0:
            itemBorrow.setText('借阅')
            itemBorrow.clicked.connect(
                lambda: self.updateBorrowFunction(val[0]))
        else:
            itemBorrow.setText('预约')
            itemBorrow.clicked.connect(
                lambda: self.updateReserveFunction(val[0]))

        itemLayout = QHBoxLayout()
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemLayout.addWidget(itemBorrow)
        itemWidget = QWidget()
        itemWidget.setLayout(itemLayout)

        self.table.insertRow(1)
        self.table.setItem(1, 0, itemBID)
        self.table.setItem(1, 1, itemNAME)
        self.table.setItem(1, 2, itemAUTHOR)
        self.table.setItem(1, 3, itemPRICE)
        self.table.setItem(1, 4, itemSTATUS)
        self.table.setItem(1, 5, itemSUM)

        self.table.setCellWidget(1, 6, itemWidget)

    def updateBorrowFunction(self, BID: str):
        book_info = database.get_book_info(BID)
        if book_info is None:
            return
        database.borrow_book(book_info['ID'], self.SID)

    # 待完成
    def updateReserveFunction(self, BID: str):
        pass

    # def updateBook(self, book_info: dict):
    #     change = self.sum - book_info['SUM']
    #     # 书本减少的数量不能大于未借出的书本数
    #     if change > book_info['NUM']:
    #         book_info['SUM'] = self.sum - book_info['NUM']
    #         book_info['NUM'] = 0
    #     else:
    #         book_info['NUM'] -= change
    #     ans = database.update_book(book_info)
    #     if ans:
    #         self.searchFunction()

    def initUI(self):
        self.setFixedSize(1100, 600)


class ReaderBorrowHistory(QWidget):

    def __init__(self, UID: str):
        super().__init__()
        self.UID = UID
        self.body = QVBoxLayout()
        self.table = None
        self.showHistory()
        self.setLayout(self.body)
        self.initUI()

    def refresh(self):
        self.showHistory()

    def showHistory(self):
        history = database.get_borrow_list(self.UID, False)
        print(history)
        self.table = QTableWidget(1, 5)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(7, 85)

        self.table.setItem(0, 0, QTableWidgetItem('书号'))
        self.table.setItem(0, 1, QTableWidgetItem('书名'))
        self.table.setItem(0, 2, QTableWidgetItem('借阅日期'))
        self.table.setItem(0, 3, QTableWidgetItem('归还日期'))
        self.table.setItem(0, 4, QTableWidgetItem('操作'))
        for i in range(5):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))

        # 显示借阅详情
        for i in history:
            i = i[2:]
            self.insertRow(i)
        self.body.addWidget(self.table)

    def insertRow(self, val: list):
        itemBID = QTableWidgetItem(val[0])
        itemBID.setTextAlignment(Qt.AlignCenter)
        itemNAME = QTableWidgetItem('《' + val[1] + '》')
        itemNAME.setTextAlignment(Qt.AlignCenter)
        itemBorrowDate = QTableWidgetItem(val[2].strftime('%Y-%m-%d'))
        itemBorrowDate.setTextAlignment(Qt.AlignCenter)
        itemReturnDate = QTableWidgetItem(
            val[3].strftime('%Y-%m-%d') if val[3] is not None else "未归还")
        itemReturnDate.setTextAlignment(Qt.AlignCenter)
        self.table.insertRow(1)
        self.table.setItem(1, 0, itemBID)
        self.table.setItem(1, 1, itemNAME)
        self.table.setItem(1, 2, itemBorrowDate)
        self.table.setItem(1, 3, itemReturnDate)
        if val[3] is None:
            itemBorrow = QToolButton(self.table)
            itemBorrow.setFixedSize(75, 25)
            itemBorrow.setText("归还")
            itemBorrow.clicked.connect(lambda: self.returnBook())
            itemLayout = QHBoxLayout()
            itemLayout.setContentsMargins(0, 0, 0, 0)
            itemLayout.addWidget(itemBorrow)
            itemWidget = QWidget()
            itemWidget.setLayout(itemLayout)
            self.table.setCellWidget(1, 4, itemWidget)

    # 待完成
    def returnBook(self):
        pass

    def initUI(self):
        self.setFixedSize(900, 600)


class SelfInfo(QWidget):

    def __init__(self, SID: str):
        super().__init__()
        self.SID = SID
        self.bodyLayout = QVBoxLayout()
        self.show_page()
        self.setLayout(self.bodyLayout)
        self.initUI()

    def refresh(self):
        self.show_page()

    def show_page(self):
        self.stu_info = database.get_reader_info(self.SID)
        self.title = QLabel()
        self.title.setText('学生信息')

        self.rid = QLabel()
        self.rid.setText('学号')

        self.rname = QLabel()
        self.rname.setText('姓名')

        self.email = QLabel()
        self.email.setText('邮箱')

        self.headname = QLabel()
        self.headname.setText('头像')

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

        # 头像
        self.headInput = QLineEdit()
        self.headInput.setFixedSize(400, 40)
        self.headInput.setText(str(self.stu_info['headshot']))
        self.headInput.initText = '请输入头像路径'
        self.headInput.setTextMargins(5, 5, 5, 5)
        self.headInput.mousePressEvent = lambda x: self.inputClick(self.
                                                                   headInput)

        # 头像
        self.headshot_ = QLabel(self)
        print(self.stu_info['headshot'])
        self.headshot = QPixmap(self.stu_info['headshot']).scaled(100, 100)
        self.headshot_.setPixmap(self.headshot)
        self.headshot_.resize(200, 200)

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

        self.btnList = [
            self.SIDInput, self.nameInput, self.emailInput, self.headInput,
            self.passwordInput, self.repPasswordInput
        ]

        self.lableList = [
            self.rid, self.rname, self.email, self.headname, self.pwd,
            self.repwd
        ]

        self.bodyLayout.addWidget(self.headshot_)
        self.bodyLayout.addWidget(self.title)
        for i in range(0, len(self.btnList)):
            self.bodyLayout.addWidget(self.lableList[i])
            self.bodyLayout.addWidget(self.btnList[i])
        self.bodyLayout.addWidget(self.submit)

    def inputClick(self, e):
        for item in self.btnList:
            if item.text() == '':
                item.setText(item.initText)
        if e.text() == e.initText:
            e.setText('')

    def submitFunction(self):
        submit_state = 0
        if os.path.exists(self.headInput.text()) is False:
            msgBox = QMessageBox(QMessageBox.Warning, "错误!", '头像文件不存在!',
                                 QMessageBox.NoButton, self)
            msgBox.addButton("确认", QMessageBox.AcceptRole)
            msgBox.exec_()
            return
        if self.passwordInput.text() != self.passwordInput.initText:
            submit_state = 1
            if self.passwordInput.text() != self.repPasswordInput.text():
                msgBox = QMessageBox(QMessageBox.Warning, "错误!", '两次输入密码不一致!',
                                     QMessageBox.NoButton, self)
                msgBox.addButton("确认", QMessageBox.AcceptRole)
                msgBox.exec_()
                return
            self.stu_info['PWD'] = database.encrypt(self.passwordInput.text())
        self.stu_info['NAME'] = self.nameInput.text()
        self.stu_info['EMAIL'] = self.emailInput.text()
        self.stu_info['headshot'] = self.headInput.text()

        if database.update_reader(self.stu_info, submit_state) is True:
            msgBox = QMessageBox(QMessageBox.Information, "成功", '更新信息成功',
                                 QMessageBox.NoButton, self)
            msgBox.addButton("确认", QMessageBox.AcceptRole)
            msgBox.exec_()
        else:
            msgBox = QMessageBox(QMessageBox.Warning, "错误", '更新信息失败',
                                 QMessageBox.NoButton, self)
            msgBox.addButton("确认", QMessageBox.AcceptRole)
            msgBox.exec_()

    def initUI(self):
        self.setFixedSize(900, 600)


class HistoryManage(QWidget):

    def __init__(self):
        super().__init__()
        self.body = QVBoxLayout()
        self.table = None
        self.setTitleBar()
        self.setSearchBar()
        self.searchFunction()
        self.body.addStretch()

        self.setLayout(self.body)
        self.initUI()

    # 标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('借阅记录管理')
        self.title.setFixedHeight(25)
        titleLayout = QHBoxLayout()
        titleLayout.addSpacing(50)
        titleLayout.addWidget(self.title)
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(900, 50)
        self.titleBar.setLayout(titleLayout)
        self.body.addWidget(self.titleBar)

    # 设置搜索框
    def setSearchBar(self):
        self.searchTitle = QLabel()
        self.searchTitle.setText('搜索读者')
        self.searchInput = QLineEdit()
        self.searchInput.setText('ID/姓名')
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setFixedSize(400, 40)
        self.searchreaderButton = QToolButton()
        self.searchreaderButton.setFixedSize(120, 40)
        self.searchreaderButton.setText('搜索学号')
        self.searchreaderButton.clicked.connect(
            lambda: self.searchFunction('SID'))

        self.searchBookButton = QToolButton()
        self.searchBookButton.setFixedSize(120, 40)
        self.searchBookButton.setText('搜索书号')
        self.searchBookButton.clicked.connect(lambda: self.searchFunction())

        self.outButton = QToolButton()
        self.outButton.setText('导出')
        self.outButton.clicked.connect(self.outFunction)
        self.outButton.setFixedSize(100, 40)

        searchLayout = QHBoxLayout()
        searchLayout.addStretch()
        searchLayout.addWidget(self.searchTitle)
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.searchreaderButton)
        searchLayout.addWidget(self.searchBookButton)
        searchLayout.addWidget(self.outButton)
        searchLayout.addStretch()

        self.searchWidget = QWidget()
        self.searchWidget.setFixedWidth(900)
        self.searchWidget.setLayout(searchLayout)
        self.body.addWidget(self.searchWidget)

    # 搜索方法
    def searchFunction(self, e: str = 'BID'):
        # 搜索书号
        if e == 'BID':
            self.log_list = database.get_log(self.searchInput.text(), True)
        else:
            # 搜索学号
            self.log_list = database.get_log(self.searchInput.text())
        if self.log_list == []:
            print('未找到')
        if self.table is not None:
            self.table.deleteLater()
        self.setTable()

    # 创建表格
    def setTable(self, val: dict = None):
        self.table = QTableWidget(1, 6)
        self.table.setFixedHeight(450)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 170)
        self.table.setColumnWidth(3, 175)
        self.table.setColumnWidth(4, 175)
        self.table.setColumnWidth(5, 100)
        self.table.setItem(0, 0, QTableWidgetItem('学号'))
        self.table.setItem(0, 1, QTableWidgetItem('书号'))
        self.table.setItem(0, 2, QTableWidgetItem('书名'))
        self.table.setItem(0, 3, QTableWidgetItem('借书日期'))
        self.table.setItem(0, 4, QTableWidgetItem('还书日期'))
        self.table.setItem(0, 5, QTableWidgetItem('罚金'))

        for i in range(6):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))

        for i in self.log_list:
            self.insertRow(i)
        self.body.addWidget(self.table)

    # 插入行
    def insertRow(self, val: list):
        itemSNAME = QTableWidgetItem(val[0])
        itemSNAME.setTextAlignment(Qt.AlignCenter)
        itemBID = QTableWidgetItem(val[1])
        itemBID.setTextAlignment(Qt.AlignCenter)
        itemNAME = QTableWidgetItem('《' + val[2] + '》')
        itemNAME.setTextAlignment(Qt.AlignCenter)
        itemBEGIN = QTableWidgetItem(val[3])
        itemBEGIN.setTextAlignment(Qt.AlignCenter)
        itemBACK = QTableWidgetItem(val[4])
        itemBACK.setTextAlignment(Qt.AlignCenter)
        itemPUNISHED = QLabel()
        itemPUNISHED.setText(str(val[5]))
        itemPUNISHED.setAlignment(Qt.AlignCenter)
        if val[5] == 0:
            itemPUNISHED.setStyleSheet('''
                *{
                    color: green;
                    font-size: 20px;
                }
            ''')
        else:
            itemPUNISHED.setStyleSheet('''
                *{
                    color: red;
                    font-size: 20px;
                }
            ''')
        self.table.insertRow(1)
        self.table.setItem(1, 0, itemSNAME)
        self.table.setItem(1, 1, itemBID)
        self.table.setItem(1, 2, itemNAME)
        self.table.setItem(1, 3, itemBEGIN)
        self.table.setItem(1, 4, itemBACK)
        self.table.setCellWidget(1, 5, itemPUNISHED)

    def outFunction(self):
        import csv
        dirName = QFileDialog.getExistingDirectory(self, '选择文件夹')
        title = ['SID', 'BID', 'BNAME', 'BORROW_DATE', 'BACK_DATE', 'PUNISHED']
        with open(os.path.join(dirName, 'log.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(title)
            for row in self.log_list:
                writer.writerow(row)

    def initUI(self):
        self.setFixedSize(1000, 600)
        self.setStyleSheet('''
        *{
            background-color: white;
            border:0px;
        }
        ''')
        self.titleBar.setStyleSheet('''
        QWidget {
            border:0;
            background-color: rgba(216, 216, 216, 1);
            border-radius: 20px;
            color: rgba(113, 118, 121, 1);
        }
        QLabel{
            font-size: 25px;
            font-family: 微软雅黑;
        }
        ''')
        self.table.setStyleSheet('''
            font-size:18px;
            color: black;
            background-color: white;
            font-family: 微软雅黑;
        ''')
        self.outButton.setStyleSheet('''
        QToolButton{
            border-radius: 10px;
            background-color:rgba(52, 118, 176, 1);
            color: white;
            font-size: 25px;
            font-family: 微软雅黑;
        }
        ''')
        self.searchWidget.setStyleSheet('''
            QToolButton{
                border-radius: 10px;
                background-color:rgba(52, 118, 176, 1);
                color: white;
                font-size: 25px;
                font-family: 微软雅黑;
            }
            QLineEdit{
                border: 1px solid rgba(201, 201, 201, 1);
                border-radius: 5px;
                color: rgba(120, 120, 120, 1)
            }
            QLabel{
                font-size:25px;
                color: black;
                font-family: 微软雅黑;
            }
        ''')


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     user_message = {'class': 'master', 'ID': 'master'}
#     ex = AdministratorPage(user_message)
#     ex.show()
#     sys.exit(app.exec_())
